import pandas as pd
from fastapi import FastAPI

app = FastAPI()

df = pd.read_excel("Outfile.xlsx")

@app.get("/get-data")
def get_data():
    df = pd.read_excel("Outfile.xlsx")
    clean_df = df.fillna("").astype(str)
    return clean_df.to_dict(orient="records")

@app.get("/get-data/{name}")
def get_data(name : str):
    df = pd.read_excel("Outfile.xlsx")
    
    filtered_df = df[df['Scheme NAV Name'].str.contains(name, case=False, na=False)]
    clean_df = filtered_df.fillna("").astype(str)
    return clean_df.to_dict(orient="records")
