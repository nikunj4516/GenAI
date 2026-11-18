# Task 3: Product Pricing (Dictionaries)

price_dict = {
    "Laptop": 49000,
    "Mouse": 249,
    "Keyboard": 1500,
    "Monitor": 11999,
    "Headphones": 2499,
    "Webcam": 2999
}

# Add a new product
price_dict["Printer"] = 7999
print("After adding Printer:", price_dict)

# Update the price of an existing product
price_dict["Laptop"] = 9999
print("After updating Laptop:", price_dict)

# Remove a product
if "Mouse" in price_dict:
    del price_dict["Mouse"]
else:
    print("Product not found")

print("After removing Mouse:", price_dict)

# Average price
average_price = sum(price_dict.values()) / len(price_dict)
print("Average price:", average_price)

# Extra: Maximum and minimum prices
max_product = max(price_dict, key=price_dict.get)
min_product = min(price_dict, key=price_dict.get)

print("Most expensive product:", max_product)
print("Cheapest product:", min_product)