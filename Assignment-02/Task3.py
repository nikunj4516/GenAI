# Task 3: User Menu (while loop + break / continue)

# 1. Create an empty list to store order amounts
orders = []

# 2. Keep showing the menu until the user quits
while True:

    # Show menu options
    print("\n1 - Add order amount")
    print("2 - Show all orders")
    print("q - Quit")

    choice = input("Enter your choice: ")

    # 3. Add order amount to the list
    if choice == "1":
        order_amount = int(input("Enter order amount: "))
        orders.append(order_amount)
        print("Order added successfully.")

    # 4. Show all orders after applying discounts
    elif choice == "2":

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

            # Calculate final amount
            discount_amount = order_amount * discount / 100
            final_amount = order_amount - discount_amount

            print(order_amount, "->", discount, "% ->", final_amount)

    # 5. Exit the loop when user enters q
    elif choice == "q":
        print("Program ended.")
        break

    # 6. Show menu again for invalid input
    else:
        print("Invalid choice. Please try again.")
        continue