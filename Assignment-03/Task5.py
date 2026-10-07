# Task 5: Filter Expensive Products

prices = [100, 250, 400, 1200, 50, 2000, 850]

# Prices greater than 500
expensive = list(filter(lambda p: p > 500, prices))

# Prices less than or equal to 500
affordable = list(filter(lambda p: p <= 500, prices))

print("Expensive Products (>500):", expensive)
print("Affordable Products (<=500):", affordable)
