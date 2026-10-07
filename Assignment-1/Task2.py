# Task 2: Categories (Sets)

# Categories for each product
categories = [
    "Electronics",
    "Electronics",
    "Electronics",
    "Electronics",
    "Audio",
    "Electronics",
    "Electronics",
    "Audio",
    "AutoMobile"
]

# Create a set of unique categories
categories_set = set(categories)

print("Categories:", categories_set)

# Add a new category
categories_set.add("Accessories")
categories_set.add("Home Appliances")
print("After adding new category:", categories_set)

# Add the same category again
categories_set.add("Accessories")
print("After adding duplicate category:", categories_set)

# Check whether a category exists
print("Is Electronics available?", "Home Appliances" in categories_set)

# Extra: Count unique categories
print("Total unique categories:", len(categories_set))