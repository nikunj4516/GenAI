# Task 2: Process Multiple Orders (for loop)

# 1. Create a list of order amounts
orders = [1200, 2500, 800, 1750, 3000]

# 2. Create a variable to store total revenue
total_revenue = 0

# 3. Process each order using a for loop
for order_amount in orders:

    # Apply discount according to order amount
    if order_amount >= 2000:
        discount = 15
    elif order_amount >= 1500:
        discount = 10
    elif order_amount >= 1000:
        discount = 7
    else:
        discount = 0

    # Calculate final amount after discount
    discount_amount = order_amount * discount / 100
    final_amount = order_amount - discount_amount

    # Add final amount to total revenue
    total_revenue = total_revenue + final_amount

    # Print order summary
    print(order_amount, "->", discount, "% ->", final_amount)

# 4. Print total revenue after discounts
print("Total revenue:", total_revenue)