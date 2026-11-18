# Task 6: Combined Utility Function

def process_prices(prices):
    # Apply 10% discount to all prices
    discounted_prices = list(map(lambda p: p - (p * 0.10), prices))
    
    # Keep only discounted prices above 300
    filtered_prices = list(filter(lambda p: p > 300, discounted_prices))
    
    return discounted_prices, filtered_prices

# Test
discounted, filtered = process_prices([100, 500, 900, 50, 750])
print("Discounted Prices:", discounted)
print("Filtered Prices (>300):", filtered)
