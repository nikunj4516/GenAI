# Task 4: Calculate Total Order Amounts

# 1. Create a list of order amounts
orders = [1200, 2500, 800, 1750, 3000]

# 2. Create a variable to store total amount
total_amount = 0

# 3. Process each order using a for loop
for order_amount in orders:

    # Add order amount to total
    total_amount = total_amount + order_amount

    # Print the running total
    print("Running total:", total_amount)

# 4. Print the final total
print("Total order amount:", total_amount)