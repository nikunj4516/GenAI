import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt


# Task 4: Multiple Bar Plot (Sales of Different Years)

# find sales_data.csv in the same folder as this file (works from any folder)
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
CSV_PATH = os.path.join(BASE_DIR, "sales_data.csv")

if not os.path.exists(CSV_PATH):
    raise SystemExit("sales_data.csv not found. Keep it in the same folder as this file.")

df = pd.read_csv(CSV_PATH, encoding="cp1252")

df["sales"] = df["sales"].str.replace(",", "").astype(float)

# rows = category, columns = year
yearly_sales = df.groupby(["category", "year"])["sales"].sum().unstack()

print("Sales Per Category For Each Year:")
print(yearly_sales)

categories = yearly_sales.index
years = yearly_sales.columns

x = np.arange(len(categories))
width = 0.2  # 4 bars in each group (4 x 0.2 = 0.8)

plt.figure(figsize=(9, 5))

for i, year in enumerate(years):
    # shift each year's bar so the group is centered on the category
    position = x + (i - 1.5) * width
    plt.bar(position, yearly_sales[year], width, label=str(year))

plt.xticks(x, categories)
plt.title("Sales by Category for Different Years")
plt.xlabel("Category")
plt.ylabel("Total Sales")
plt.legend(title="Year")
plt.tight_layout()
plt.savefig(os.path.join(BASE_DIR, "task4_multiple_bar.png"))
plt.show()