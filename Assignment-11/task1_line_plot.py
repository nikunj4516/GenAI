import os
import pandas as pd
import matplotlib.pyplot as plt


# Task 1: Line Plot (Sales Trend)

# find sales_data.csv in the same folder as this file (works from any folder)
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
CSV_PATH = os.path.join(BASE_DIR, "sales_data.csv")

if not os.path.exists(CSV_PATH):
    raise SystemExit("sales_data.csv not found. Keep it in the same folder as this file.")

df = pd.read_csv(CSV_PATH, encoding="cp1252")

# sales column has commas in big values (e.g. "1,648"), so remove them first
df["sales"] = df["sales"].str.replace(",", "").astype(float)
df["order_date"] = pd.to_datetime(df["order_date"], format="%d-%m-%Y")

# total sales for every month
monthly_sales = df.groupby(df["order_date"].dt.to_period("M"))["sales"].sum()

print("Monthly Sales (first 5 months):")
print(monthly_sales.head())

months = monthly_sales.index.astype(str)

plt.figure(figsize=(12, 5))
plt.plot(months, monthly_sales.values, marker="o")
plt.xticks(range(0, len(months), 3), months[::3], rotation=45)
plt.title("Monthly Sales Trend (2011-2014)")
plt.xlabel("Month")
plt.ylabel("Total Sales")
plt.tight_layout()
plt.savefig(os.path.join(BASE_DIR, "task1_line_plot.png"))
plt.show()