import os
import pandas as pd
import matplotlib.pyplot as plt


# Task 7: Pie Chart (Category Share of Sales)

# find sales_data.csv in the same folder as this file (works from any folder)
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
CSV_PATH = os.path.join(BASE_DIR, "sales_data.csv")

if not os.path.exists(CSV_PATH):
    raise SystemExit("sales_data.csv not found. Keep it in the same folder as this file.")

df = pd.read_csv(CSV_PATH, encoding="cp1252")

df["sales"] = df["sales"].str.replace(",", "").astype(float)

category_sales = df.groupby("category")["sales"].sum()

print("Total Sales Per Category:")
print(category_sales)

plt.figure(figsize=(7, 7))
plt.pie(category_sales.values, labels=category_sales.index, autopct="%1.1f%%")
plt.title("Category Share of Total Sales")
plt.tight_layout()
plt.savefig(os.path.join(BASE_DIR, "task7_pie_chart.png"))
plt.show()