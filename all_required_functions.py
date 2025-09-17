import pandas as pd

dividend_list = ["idcw", "dividend", "income distribution cum capital withdrawal", "payout"]

def classify_plan(nav_name):
    nav_name = str(nav_name).lower()

    if "growth" in nav_name:
        plan_type = "Growth"
    elif any(word in nav_name for word in dividend_list):
        plan_type = "Dividend"
    else:
        plan_type = "Uncategorized"


    if "direct" in nav_name:
        plan_mode = "Direct"
    else:
        plan_mode = "Regular"
    return f"{plan_mode} {plan_type}"

    pass


def format_data(file_path: str, save_file_path: str):
    df = pd.read_csv(file_path)

    df['Plan Type'] = df['Scheme NAV Name'].apply(classify_plan)

    df_filtered = df[df['Plan Type'] != "Regular Uncategorized"]
    df_filtered = df_filtered[df_filtered['Plan Type'] != "Direct Uncategorized"]

    df_subset = df_filtered[['Scheme Name', 'Plan Type', 'ISIN Div Payout/ ISIN GrowthISIN Div Reinvestment', 'Code']]

    df_pivot = df_subset.pivot_table(
        index='Scheme Name',
        columns='Plan Type',
        values=['ISIN Div Payout/ ISIN GrowthISIN Div Reinvestment' , 'Code'],
        aggfunc='first'
    ).reset_index()

    df_pivot.columns = ['Scheme Name', 
                            'Direct Dividend Code', 'Direct Growth Code', 
                            'Regular Dividend Code', 'Regular Growth Code',
                            'Direct Dividend ISIN', 'Direct Growth ISIN',
                            'Regular Dividend ISIN', 'Regular Growth ISIN']
    
    df_pivot.to_excel(save_file_path)

