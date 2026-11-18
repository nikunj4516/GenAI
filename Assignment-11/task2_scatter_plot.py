import os
import pandas as pd
import matplotlib.pyplot as plt


# Task 2: Scatter Plot (Sales vs Profit)

# find sales_data.csv in the same folder as this file (works from any folder)
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
CSV_PATH = os.path.join(BASE_DIR, "sales_data.csv")

if not os.path.exists(CSV_PATH):
    raise SystemExit("sales_data.csv not found. Keep it in the same folder as this file.")

df = pd.read_csv(CSV_PATH, encoding="cp1252")

df["sales"] = df["sales"].str.replace(",", "").astype(float)

print("Sales and Profit (first 5 rows):")
print(df[["sales", "profit"]].head())

plt.figure(figsize=(8, 6))
plt.scatter(df["sales"], df["profit"], s=6, alpha=0.3)
plt.title("Relationship between Sales and Profit")
plt.xlabel("Sales")
plt.ylabel("Profit")
plt.tight_layout()
plt.savefig(os.path.join(BASE_DIR, "task2_scatter_plot.png"))
plt.show()