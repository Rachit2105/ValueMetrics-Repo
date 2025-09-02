
import pandas as pd

Data = {
    "Name" : ["Rachit", "Swadhin", "Yaduveer"],
    "Age" : ["20", "21" ,"19"],
    "Job" : ["Intern", "Jobless", "Busiest"] 
}

df = pd.DataFrame(Data)
print(df)

df.to_excel("output.xlsx", index=False)
