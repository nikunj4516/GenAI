# Assignment 6 - Task 2
# Bill Calculator with Error Handling

prices = [120, 350, 'abc', 500, -200, 800]

total = 0

# Loop through each item
for price in prices:

    try:
        # Check if value is numeric
        if not isinstance(price, (int, float)):
            raise TypeError("Not a number")

        # Check for negative price
        if price < 0:
            raise ValueError("Negative price not allowed")

        # Add valid price
        total += price

        print("Running Total:", total)

    except TypeError:
        print(price, "is not a valid number.")

    except ValueError as e:
        print(e)

print("Final Total:", total)