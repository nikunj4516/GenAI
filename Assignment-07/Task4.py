# ==========================================
# Task 4: Polymorphism
# ==========================================

class Product:

    def __init__(self, name, price):
        self.name = name
        self.price = price

    def get_info(self):
        pass


class Laptop(Product):

    def get_info(self):
        print("=" * 40)
        print("       LAPTOP INFORMATION")
        print("=" * 40)
        print(f"Laptop Name: {self.name}")
        print(f"Price: {self.price}")
        print("=" * 40)


class Mobile(Product):

    def get_info(self):
        print("=" * 40)
        print("       MOBILE INFORMATION")
        print("=" * 40)
        print(f"Mobile Name: {self.name}")
        print(f"Price: {self.price}")
        print("=" * 40)


laptop = Laptop("Dell", 55000)
mobile = Mobile("iPhone", 70000)

products = [laptop, mobile]

for product in products:
    product.get_info()