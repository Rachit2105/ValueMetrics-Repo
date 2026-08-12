"""Data cleaning, classification, validation and Excel transformation."""
from pathlib import Path
from typing import Final

import pandas as pd

from logging_config import get_logger

logger = get_logger(__name__)

DIVIDEND_KEYWORDS: Final[tuple[str, ...]] = (
    "idcw",
    "dividend",
    "income distribution cum capital withdrawal",
    "payout",
)

REQUIRED_COLUMNS: Final[tuple[str, ...]] = (
    "Scheme Name",
    "Scheme NAV Name",
    "ISIN Div Payout/ ISIN GrowthISIN Div Reinvestment",
    "Code",
)


def normalize_text(value: object) -> str:
    """Return a normalized, lowercase representation of a value."""
    if pd.isna(value):
        return ""
    return " ".join(str(value).strip().lower().split())


def classify_plan(nav_name: object) -> str:
    """Classify a scheme as Direct/Regular + Growth/Dividend.

    Unknown plan modes/types are explicitly marked as Uncategorized rather
    than assuming every non-Direct scheme is Regular.
    """
    name = normalize_text(nav_name)

    if not name:
        return "Uncategorized Uncategorized"

    if "direct" in name:
        plan_mode = "Direct"
    elif "regular" in name:
        plan_mode = "Regular"
    else:
        plan_mode = "Uncategorized"

    if "growth" in name:
        plan_type = "Growth"
    elif any(keyword in name for keyword in DIVIDEND_KEYWORDS):
        plan_type = "Dividend"
    else:
        plan_type = "Uncategorized"

    return f"{plan_mode} {plan_type}"


def validate_input(df: pd.DataFrame) -> None:
    """Validate that the source contains all fields required by the pipeline."""
    missing = [column for column in REQUIRED_COLUMNS if column not in df.columns]
    if missing:
        raise ValueError(f"Missing required columns: {missing}")


def clean_and_classify(df: pd.DataFrame) -> pd.DataFrame:
    """Clean source data and add a plan classification."""
    validate_input(df)

    result = df.copy()
    result["Scheme Name"] = result["Scheme Name"].astype("string").str.strip()
    result["Scheme NAV Name"] = result["Scheme NAV Name"].astype("string").str.strip()
    result["Plan Type"] = result["Scheme NAV Name"].map(classify_plan)

    before = len(result)
    result = result.dropna(subset=["Scheme Name"])
    result = result[result["Plan Type"].isin(
        ["Direct Growth", "Direct Dividend", "Regular Growth", "Regular Dividend"]
    )]
    result = result.drop_duplicates()

    logger.info(
        "Prepared %d records from %d source records",
        len(result),
        before,
    )
    return result


def format_data(file_path: str, save_file_path: str) -> Path:
    """Run the complete CSV -> classified -> pivoted Excel transformation."""
    input_path = Path(file_path)
    output_path = Path(save_file_path)

    if not input_path.exists():
        raise FileNotFoundError(f"Input file not found: {input_path}")

    output_path.parent.mkdir(parents=True, exist_ok=True)

    df = pd.read_csv(input_path)
    processed = clean_and_classify(df)

    columns = [
        "Scheme Name",
        "Plan Type",
        "ISIN Div Payout/ ISIN GrowthISIN Div Reinvestment",
        "Code",
    ]
    subset = processed[columns]

    pivot = subset.pivot_table(
        index="Scheme Name",
        columns="Plan Type",
        values=[
            "ISIN Div Payout/ ISIN GrowthISIN Div Reinvestment",
            "Code",
        ],
        aggfunc="first",
    ).reset_index()

    expected = [
        "Scheme Name",
        "Direct Dividend Code",
        "Direct Growth Code",
        "Regular Dividend Code",
        "Regular Growth Code",
        "Direct Dividend ISIN",
        "Direct Growth ISIN",
        "Regular Dividend ISIN",
        "Regular Growth ISIN",
    ]

    # Pivot columns can vary with input data. Reindexing makes the output
    # schema stable and fills unavailable combinations with blank values.
    pivot.columns = [
        f"{value} {plan}".strip()
        if isinstance(value, tuple)
        else str(value)
        for value, plan in (
            [(c[0], c[1]) if isinstance(c, tuple) else (c, "") for c in pivot.columns]
        )
    ]

    # Rebuild the pivot with a predictable flat schema.
    final = subset.pivot_table(
        index="Scheme Name",
        columns="Plan Type",
        values=[
            "ISIN Div Payout/ ISIN GrowthISIN Div Reinvestment",
            "Code",
        ],
        aggfunc="first",
    )

    final.columns = [
        f"{plan} {field}".strip()
        for field, plan in final.columns
    ]
    final = final.reset_index()

    rename_map = {
        "Direct Dividend Code": "Direct Dividend Code",
        "Direct Growth Code": "Direct Growth Code",
        "Regular Dividend Code": "Regular Dividend Code",
        "Regular Growth Code": "Regular Growth Code",
        "Direct Dividend ISIN Div Payout/ ISIN GrowthISIN Div Reinvestment": "Direct Dividend ISIN",
        "Direct Growth ISIN Div Payout/ ISIN GrowthISIN Div Reinvestment": "Direct Growth ISIN",
        "Regular Dividend ISIN Div Payout/ ISIN GrowthISIN Div Reinvestment": "Regular Dividend ISIN",
        "Regular Growth ISIN Div Payout/ ISIN GrowthISIN Div Reinvestment": "Regular Growth ISIN",
    }
    final = final.rename(columns=rename_map)

    for column in expected:
        if column not in final.columns:
            final[column] = pd.NA

    final = final[expected]
    final.to_excel(output_path, index=False)

    logger.info("Saved %d formatted scheme records to %s", len(final), output_path)
    return output_path
