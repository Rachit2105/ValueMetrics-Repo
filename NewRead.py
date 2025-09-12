import pandas as pd
from AllRequiredFunctions import classify_plan

df = pd.read_csv("AMCdata.csv")

try:

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

    df_pivot.to_excel("AMCdata_formatted.xlsx")

    print("✅ AMC data formatted and saved without Uncategorized rows")


except Exception as e:
    print(e)
