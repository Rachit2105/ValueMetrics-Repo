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