# Assignment 6 - Task 5
# Safe Shopping Cart

cart = []

while True:

    value = input("Enter price (q to quit): ")

    # Exit condition
    if value.lower() == "q":
        break

    try:
        # Convert input to float
        price = float(value)

        # Negative price not allowed
        if price < 0:
            raise ValueError("Negative price is not allowed")

        # Add valid price to cart
        cart.append(price)

    except ValueError as e:
        print("Error:", e)

# Display summary
print("\nShopping Summary")
print("Total Items:", len(cart))
print("Total Bill:", sum(cart))