import pandas as pd

DataFile = pd.read_csv("AMCdata.csv" , encoding= "utf-8")

print(DataFile.head(10))

