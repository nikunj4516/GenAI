# Task 1: Discount Rules (if / elif / else)

# 1. Take order amount from the user
order_amount = int(input("Enter order amount: "))

# 2. Apply discount according to order amount
if order_amount >= 2000:
    discount = 15
elif order_amount >= 1500:
    discount = 10
elif order_amount >= 1000:
    discount = 7
else:
    discount = 0

# 3. Calculate discount amount
discount_amount = order_amount * discount / 100

# 4. Calculate final amount after discount
final_amount = order_amount - discount_amount

# 5. Print order details
print("Order Amount:", order_amount)
print("Discount:", discount, "%")
print("Discount Amount:", discount_amount)
print("Final Amount:", final_amount)