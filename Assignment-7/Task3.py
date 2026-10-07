# ==========================================
# Task 3: Inheritance (Single-Level)
# ==========================================

class Product:

    def __init__(self, name, price, category):
        self.name = name
        self.price = price
        self.category = category

    def get_info(self):
        return (
            f"Name: {self.name}\n"
            f"Price: {self.price}\n"
            f"Category: {self.category}"
        )


class ElectronicProduct(Product):

    def __init__(self, name, price, category, warranty_years):
        super().__init__(name, price, category)
        self.warranty_years = warranty_years

    def get_info(self):
        return (
            f"{super().get_info()}\n"
            f"Warranty: {self.warranty_years} Years"
        )


tv = ElectronicProduct(
    "Smart TV",
    40000,
    "Electronics",
    2
)

print("=" * 40)
print("           PRODUCT INFORMATION")
print("=" * 40)

print(tv.get_info())

print("=" * 40)