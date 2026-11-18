import os
import pandas as pd
import matplotlib.pyplot as plt


# Task 3: Bar Plot (Total Sales by Market)

# find sales_data.csv in the same folder as this file (works from any folder)
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
CSV_PATH = os.path.join(BASE_DIR, "sales_data.csv")

if not os.path.exists(CSV_PATH):
    raise SystemExit("sales_data.csv not found. Keep it in the same folder as this file.")

df = pd.read_csv(CSV_PATH, encoding="cp1252")

df["sales"] = df["sales"].str.replace(",", "").astype(float)

market_sales = df.groupby("market")["sales"].sum()

print("Total Sales Per Market:")
print(market_sales)

# 1. Vertical bar chart
plt.figure(figsize=(8, 5))
plt.bar(market_sales.index, market_sales.values)
plt.title("Total Sales by Market (Vertical)")
plt.xlabel("Market")
plt.ylabel("Total Sales")
plt.tight_layout()
plt.savefig(os.path.join(BASE_DIR, "task3_bar_vertical.png"))
plt.show()

# 2. Horizontal bar chart (same data)
plt.figure(figsize=(8, 5))
plt.barh(market_sales.index, market_sales.values)
plt.title("Total Sales by Market (Horizontal)")
plt.xlabel("Total Sales")
plt.ylabel("Market")
plt.tight_layout()
plt.savefig(os.path.join(BASE_DIR, "task3_bar_horizontal.png"))
plt.show()