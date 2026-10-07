import pandas as pd
import matplotlib.pyplot as plt


# Task 9: Mini Use Case: Sales Data Analysis

sales = {
    "Day": ["Mon", "Tue", "Wed", "Thu", "Fri"],
    "Revenue": [1200, 1500, 900, 2000, 1800]
}

sales_df = pd.DataFrame(sales)

total_revenue = sales_df["Revenue"].sum()

average_revenue = sales_df["Revenue"].mean()

highest_revenue_day = sales_df.loc[
    sales_df["Revenue"].idxmax(),
    "Day"
]

above_average_revenue = sales_df[
    sales_df["Revenue"] > average_revenue
]

print("Total Revenue:")
print(total_revenue)

print("\nAverage Daily Revenue:")
print(average_revenue)

print("\nDay with Highest Revenue:")
print(highest_revenue_day)

print("\nDays Where Revenue is Above Average:")
print(above_average_revenue)

sales_df.plot(
    x="Day",
    y="Revenue",
    kind="line",
    title="Revenue vs Day"
)

plt.show()