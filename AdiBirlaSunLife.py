import pandas as pd
from AllRequiredFunctions import select_schemeNAV_name
from AllRequiredFunctions import select_scheme_name




df = pd.read_csv('AMCdata.csv')

unique_schemes = select_scheme_name('Aditya Birla Sun Life', 'AMCdata.csv')

filtered_df = pd.DataFrame(unique_schemes, columns=['Scheme Name'])

filtered_df.to_excel('Modified.xlsx')