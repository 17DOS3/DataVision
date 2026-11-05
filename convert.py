import pandas as pd

df = pd.read_csv("datasetpractice.csv")

df.to_excel("datasetpractice.xlsx", index=False)

print("Excel file created successfully!")