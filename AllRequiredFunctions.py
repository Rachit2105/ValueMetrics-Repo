import pandas as pd

def select_schemeNAV_name(name:str , filePath: str):
    df = pd.read_csv(filePath)
    new_df = df['Scheme NAV Name'].str.contains(name, case = False, na = False)
    return new_df
    pass


def select_scheme_name(name:str , filePath: str):
    df = pd.read_csv(filePath)
    new_df = df[['Scheme Name']]
    filtered_df = new_df[new_df['Scheme Name'].str.contains(name, case=False, na=False)]
    unique_df = filtered_df[['Scheme Name']].drop_duplicates()

    return unique_df
    pass
