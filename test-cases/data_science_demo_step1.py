import pandas as pd

df = pd.DataFrame({
    "country": ["India", "USA", "Japan", "Germany"],
    "sales": [5000, 7200, 6100, 4800],
    "profit": [1200, 2100, 1600, 900],
})

df.to_csv("global_sales.csv", index=False)
print("Dataset saved successfully.")
