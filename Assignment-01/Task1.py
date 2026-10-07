# Task 1: Product Collections (Lists & Tuples)

# 1. Create a list of products
products = ["Wi-Fi", "Earbuds", "Fan", "Clock", "Monitor", "PC"]

# 2. Create a tuple for one sample product
sample_product = ("Bike", 70000, "vehicle")

# 3. Print the 2nd and last product
print("Second product:", products[1])
print("Last product:", products[-2])

# 4. Add two new products
products.append("Printer")
products.append("Speaker")

print("Updated products list:", products)


# Extra: Convert tuple into a list, change price, and convert it back
sample_product = list(sample_product)
sample_product[0]="Mountain Bike"
sample_product[1] = 65000
sample_product = tuple(sample_product)

print("Updated sample product:", sample_product)
