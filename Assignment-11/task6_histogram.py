import os
import pandas as pd
import matplotlib.pyplot as plt


# Task 6: Histogram (Sales Distribution)

# find sales_data.csv in the same folder as this file (works from any folder)
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
CSV_PATH = os.path.join(BASE_DIR, "sales_data.csv")

if not os.path.exists(CSV_PATH):
    raise SystemExit("sales_data.csv not found. Keep it in the same folder as this file.")

df = pd.read_csv(CSV_PATH, encoding="cp1252")

df["sales"] = df["sales"].str.replace(",", "").astype(float)

print("Sales Summary:")
print(df["sales"].describe())

# most orders are small (median is 85), so the plot shows orders up to 1000
# with 40 bins (each bin is 25 wide)
plt.figure(figsize=(8, 5))
plt.hist(df["sales"], bins=40, range=(0, 1000), edgecolor="black")
plt.title("Distribution of Order Sales (0 - 1000)")
plt.xlabel("Sales")
plt.ylabel("Number of Orders")
plt.tight_layout()
plt.savefig(os.path.join(BASE_DIR, "task6_histogram.png"))
plt.show()