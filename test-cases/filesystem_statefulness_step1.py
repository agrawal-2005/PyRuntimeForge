import os
import pandas as pd

df = pd.DataFrame({
    "product": ["A", "B", "C"],
    "profit": [1200, 3400, 5600],
})

df.to_csv("sales.csv", index=False)

print("File created:", os.path.exists("sales.csv"))
print("Current files:", os.listdir("."))
