# Task 1: Discount Rules

order_input = input("Enter your order amount: ")

# Validate numeric input
if not order_input.isdigit():
    print("Error: Please enter a valid numeric amount.")
else:
    order_amount = int(order_input)

    # Apply discount rules
    if order_amount >= 2000:
        discount_rate = 0.15
    elif order_amount >= 1500:
        discount_rate = 0.10
    elif order_amount >= 1000:
        discount_rate = 0.07
    else:
        discount_rate = 0.0

    discount = order_amount * discount_rate
    subtotal = order_amount - discount

    # Optional: Add tax (5%)
    tax_rate = 0.05
    tax = subtotal * tax_rate
    final_total = subtotal + tax

    # Print results
    print("Original Amount:", order_amount)
    print("Discount Applied:", discount)
    print("Subtotal after Discount:", subtotal)
    print("Tax (5%):", tax)
    print("Final Total:", final_total)
