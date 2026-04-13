import pandas as pd

df = pd.read_csv("global_sales.csv")
print(df)
print("Total Sales:", df["sales"].sum())
print("Total Profit:", df["profit"].sum())
