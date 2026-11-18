# Task 7: Menu Using Functions

# Function to add a price to the list
def add_price(prices_list, price):
    prices_list.append(price)

# Function to calculate average price
def get_average_price(prices_list):
    if len(prices_list) == 0:
        return 0
    return sum(prices_list) / len(prices_list)

# Function to get maximum price
def get_max_price(prices_list):
    if len(prices_list) == 0:
        return 0
    return max(prices_list)

# Main program with menu
prices = []

while True:
    print("\nMenu:")
    print("1 → Add price")
    print("2 → Show average price")
    print("3 → Show highest price")
    print("q → Quit")

    choice = input("Enter your choice: ")

    if choice == "1":
        value = input("Enter price: ")
        if value.isdigit():
            add_price(prices, int(value))
            print("Price added successfully.")
        else:
            print("Invalid input. Please enter a number.")
    elif choice == "2":
        avg = get_average_price(prices)
        print("Average Price:", avg)
    elif choice == "3":
        highest = get_max_price(prices)
        print("Highest Price:", highest)
    elif choice.lower() == "q":
        print("Exiting program. Goodbye!")
        break
    else:
        print("Invalid choice. Try again.")
