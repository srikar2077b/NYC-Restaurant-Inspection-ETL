import pandas as pd
from pandasgui import show

# Load the cleaned CSV file
df = pd.read_csv("nyc_data_project/output/DOHMH_New_York_City_Restaurant_Inspection_T.csv")


show(df)