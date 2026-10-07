# Task 3: Lambda, Map, and Filter

# Sample list of prices
prices = [100, 250, 400, 50, 1200, 75]

# Lambda with map: Apply 10% discount to all prices
discounted_prices = list(map(lambda p: p - (p * 0.10), prices))
print("Discounted Prices:", discounted_prices)

# Lambda with filter: Keep only prices greater than 200
filtered_prices = list(filter(lambda p: p > 200, prices))
print("Filtered Prices (greater than 200):", filtered_prices)

# Lambda with map + filter combined: Apply discount only to prices > 200
discounted_filtered = list(map(lambda p: p - (p * 0.10), filter(lambda p: p > 200, prices)))
print("Discounted & Filtered Prices:", discounted_filtered)
