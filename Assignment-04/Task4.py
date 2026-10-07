# Task 4: Generate Summary Report

with open("sales_data.txt", "r") as f:
    sales = [int(line.strip()) for line in f.readlines()]

print("Total Sales:", sum(sales))
print("Highest Sale:", max(sales))
print("Lowest Sale:", min(sales))
print("Average Sale:", sum(sales) / len(sales))
