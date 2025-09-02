import pandas as pd

def classify_fund(name):
    if "regular" in str(name).lower():   
        return "Regular"
    else:
        return "Direct"


df = pd.read_csv("AMCdata.csv" , encoding= "utf-8")

df['fund_type'] = df['Scheme NAV Name'].apply(classify_fund)

df = df[["ISIN Div Payout/ ISIN GrowthISIN Div Reinvestment", "Code", "fund_type"]]
df.rename(columns={"ISIN Div Payout/ ISIN GrowthISIN Div Reinvestment" : "ISIN"} , inplace=True) 
df.rename(columns={"fund_type" : "Fund Type"} , inplace=True) 


df.to_excel("Outfile.xlsx")