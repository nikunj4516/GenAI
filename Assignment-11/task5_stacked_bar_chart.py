import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt


# Task 5: Stacked Bar Chart (Yearly Sales Stacked by Category)

# find sales_data.csv in the same folder as this file (works from any folder)
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
CSV_PATH = os.path.join(BASE_DIR, "sales_data.csv")

if not os.path.exists(CSV_PATH):
    raise SystemExit("sales_data.csv not found. Keep it in the same folder as this file.")

df = pd.read_csv(CSV_PATH, encoding="cp1252")

df["sales"] = df["sales"].str.replace(",", "").astype(float)

# rows = year, columns = category
category_sales = df.groupby(["year", "category"])["sales"].sum().unstack()

print("Sales Per Year For Each Category:")
print(category_sales)

years = category_sales.index.astype(str)
bottom = np.zeros(len(years))

plt.figure(figsize=(8, 5))

for category in category_sales.columns:
    plt.bar(years, category_sales[category], bottom=bottom, label=category)
    bottom = bottom + category_sales[category].values

plt.title("Yearly Sales Stacked by Category")
plt.xlabel("Year")
plt.ylabel("Total Sales")
plt.legend(title="Category")
plt.tight_layout()
plt.savefig(os.path.join(BASE_DIR, "task5_stacked_bar.png"))
plt.show()