# ====================================================
# Task 7: Mini Project - Simple Inventory System
# ====================================================


# Product Class

class Product:

    def __init__(self, name, price, category):
        self.name = name
        self.price = price
        self.category = category

    def get_info(self):
        return (
            f"Product Name: {self.name}\n"
            f"Price: {self.price}\n"
            f"Category: {self.category}"
        )

    def __add__(self, other):
        return self.price + other.price


# Inventory Class

class Inventory:

    def __init__(self):
        self.products = []

    def add_product(self, product):
        self.products.append(product)

    def remove_product(self, name):

        for product in self.products:

            if product.name.lower() == name.lower():
                self.products.remove(product)
                print(name, "removed successfully")
                return

        print("Product not found")

    def get_total_value(self):

        total = 0

        for product in self.products:
            total += product.price

        return total

    def show_all_products(self):

        sorted_products = sorted(
            self.products,
            key=lambda product: product.price
        )

        for index, product in enumerate(sorted_products, start=1):

            print("=" * 40)
            print(f"             PRODUCT {index}")
            print("=" * 40)
            print(product.get_info())


# Store Class

class Store:

    def __init__(self, store_name):
        self.store_name = store_name
        self.inventory = Inventory()

    def add_new_product(self):

        name = input("Enter product name: ")
        price = float(input("Enter price: "))
        category = input("Enter category: ")

        product = Product(
            name,
            price,
            category
        )

        self.inventory.add_product(product)

    def show_summary(self):

        print("=" * 40)
        print("             STORE")
        print("=" * 40)
        print("Store Name:", self.store_name)
        print("Total Items:", len(self.inventory.products))
        print(
            "Total Inventory Value:",
            self.inventory.get_total_value()
        )


# Step 1: Creating Store Object

store = Store("Tech World")


# Step 2: Adding 3 Products

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

product3 = Product(
    "Headphones",
    5000,
    "Accessories"
)

store.inventory.add_product(product1)
store.inventory.add_product(product2)
store.inventory.add_product(product3)


# Step 3: Showing Products

store.inventory.show_all_products()


# Step 4: Using + to combine prices

combined_price = product1 + product2 

print("=" * 40)
print("          COMBINED PRICE")
print("=" * 40)
print("Total Price:", combined_price)
print("=" * 40)