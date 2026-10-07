# ==========================================
# Task 2: Constructor & Encapsulation
# ==========================================

class Product:

    def __init__(self, name, price, category):
        self.name = name
        self.__price = price
        self.category = category

    def get_price(self):
        return self.__price

    def set_price(self, new_price):

        if new_price > 0:
            self.__price = new_price

    def get_info(self):
        print("Name:", self.name)
        print("Price:", self.__price)
        print("Category:", self.category)


product = Product("Laptop", 50000, "Electronics")

print("Old Price:", product.get_price())

product.set_price(55000)

print("New Price:", product.get_price())

print("="*40)

product.get_info()

print("="*40)
