# ==========================================
# Task 6: Magic Methods & Operator Overloading
# ==========================================

class Product:

    def __init__(self, name, price, category):
        self.name = name
        self.price = price
        self.category = category

    def __str__(self):
        return (
            f"Product Name: {self.name}\n"
            f"Price: {self.price}\n"
            f"Category: {self.category}"
        )

    def __add__(self, other):
        return self.price + other.price


product1 = Product(
    "Laptop",
    50000,
    "Electronics"
)

product2 = Product(
    "Mobile",
    30000,
    "Electronics"
)


print("=" * 40)
print("             PRODUCT 1")
print("=" * 40)
print(product1)

print("=" * 40)
print("             PRODUCT 2")
print("=" * 40)
print(product2)

total_price = product1 + product2

print("=" * 40)
print("          COMBINED PRICE")
print("=" * 40)
print("Total Price:", total_price)
print("=" * 40)