import pandas as pd

def classify_fund_type(name):
    if "Direct" in str(name).lower():   
        return "Direct"
    else:
        return "Regular"

def classify_growth_type(name):
    name = str(name).lower()
    if any(x in name for x in ["idcw" , "dividend" , "income distribution cum capital withdrawal" , "payout"]):   
        return "Dividend"
    elif any(x in name for x in ["discipline advantage plan" , "dap", "principal units", "pu", "bonus units", "bu"]):
        return "uncatogerized"   
    else:
        return "growth"


df = pd.read_csv("AMCdata.csv" , encoding= "utf-8")

df['fund_type'] = df['Scheme NAV Name'].apply(classify_fund_type)
df['growth_type'] = df['Scheme NAV Name'].apply(classify_growth_type)

# df = df[["Scheme NAV Name" , "fund_type" ,"growth_type" , "ISIN Div Payout/ ISIN GrowthISIN Div Reinvestment", "Code"]]
df.rename(columns={"ISIN Div Payout/ ISIN GrowthISIN Div Reinvestment" : "ISIN"} , inplace=True) 
# df.rename(columns={"fund_type" : "Fund Type"} , inplace=True) 
# df.rename(columns={"growth_type" : "Growth Type"} , inplace=True) 

direct_growth_isin = df.loc[
    (df['fund_type'].str.lower() == "direct") & (df['growth_type'].str.lower() == "growth"),
    ["ISIN"]
].rename(columns={"ISIN": "Direct Growth ISIN"})

direct_growth_isin.to_excel("Modified.xlsx", index=False)
