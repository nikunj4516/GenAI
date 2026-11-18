# Task 5: Create Product Info File

products = []
for i in range(3):
    name = input("Enter product name: ")
    price = input("Enter product price: ")
    products.append(f"{name} | {price}")

# Write to file
with open("products.txt", "w") as f:
    for p in products:
        f.write(p + "\n")
# Read and print
with open("products.txt", "r") as f:
    print("Product Info:")
    for line in f:
        print(line.strip())