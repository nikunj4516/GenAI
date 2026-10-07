# ==========================================
# Task 1: Basic Class & Object Creation
# ==========================================

class Product:

    def __init__(self, name, price, category):
        self.name = name
        self.price = price
        self.category = category

    def get_info(self):
        print("Name:", self.name)
        print("Price:", self.price)
        print("Category:", self.category)


product1 = Product("Laptop", 50000, "Electronics")
product2 = Product("Mobile", 30000, "Electronics")

print("="*40)

product1.get_info()
print()
print("="*40)


product2.get_info()
print()

print("="*40)