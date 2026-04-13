import os
import pandas as pd

print("File still exists:", os.path.exists("sales.csv"))

df = pd.read_csv("sales.csv")
print(df)
print("Total profit:", df["profit"].sum())
