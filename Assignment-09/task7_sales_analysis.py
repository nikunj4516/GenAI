# Task 7: Mini Use Case - Sales Analysis

import numpy as np

sales = np.array([1200, 1500, 900, 2000, 1800, 1700, 1600])

days = np.array([
    "Day 1",
    "Day 2",
    "Day 3",
    "Day 4",
    "Day 5",
    "Day 6",
    "Day 7"
])

total_sales = np.sum(sales)
average_sales = np.mean(sales)

highest_day = days[np.argmax(sales)]
lowest_day = days[np.argmin(sales)]

sales_std = np.std(sales)

above_average_days = days[sales > average_sales]

print("Total Weekly Sales:")
print(total_sales)

print("\nAverage Daily Sales:")
print(average_sales)

print("\nHighest Sales Day:")
print(highest_day)

print("\nLowest Sales Day:")
print(lowest_day)

print("\nStandard Deviation:")
print(sales_std)

print("\nDays With Above Average Sales:")
print(above_average_days)