import pandas as pd

def classify_fund(name):
    if "regular" in str(name).lower():   
        return "Regular"
    else:
        return "Direct"


df = pd.read_csv("AMCdata.csv" , encoding= "utf-8")

df['fund_type'] = df['Scheme NAV Name'].apply(classify_fund)


Direct_Funds = df[df['fund_type'] == "Direct"][["ISIN Div Payout/ ISIN GrowthISIN Div Reinvestment" , "Code"]]
Regular_Funds = df[df['fund_type'] == "Regular"][["ISIN Div Payout/ ISIN GrowthISIN Div Reinvestment" , "Code"]]

Direct_Funds.columns = ["Direct ISIN" , "Direct Code"]
Regular_Funds.columns = ["Regular ISIN" , "Regular Code"]

Combined = pd.concat([Direct_Funds, Regular_Funds], axis=1)

Combined.to_excel("Outfile.xlsx" , index= False)