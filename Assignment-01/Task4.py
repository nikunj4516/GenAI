# Task 4: Combined Operations
#1. Create a catalog of products with their prices and categories using a list of tuples.
catalog = [
    ("Laptop", 45000, "Electronics"),
    ("Keyboard", 1500, "Electronics"),
    ("Monitor", 12000, "Electronics"),
    ("Headphones", 2500, "Audio"),
    ("Webcam", 3000, "Accessories"),
    ("Printer", 9000, "Electronics"),
    ("Mic", 2500, "Audio"),
    ("Boult Air Bass", 1499, "Audio"),
    ("Amplifer", 24999, "Audio"),
    ("Speaker", 24345, "Audio")
]

#2. Create a dictionary mapping categories to lists of products.
category_to_products = {}

for product_name, price, category in catalog:
    if category not in category_to_products:
        category_to_products[category] = []

    category_to_products[category].append(product_name)

print("Category to products:")
print(category_to_products)

#3. Find the category with the maximum number of products.
max_category = max(
    category_to_products,
    key=lambda category: len(category_to_products[category])
)

print("Category with maximum products:", max_category)
print("Products in this category:", category_to_products[max_category])