# Assignment 6 - Task 1
# Safe Division Utility

try:
    # Take input from user
    numerator = float(input("Enter numerator: "))
    denominator = float(input("Enter denominator: "))

    # Perform division
    result = numerator / denominator

except ValueError:
    print("Error: Please enter numeric values only.")

except ZeroDivisionError:
    print("Error: Division by zero is not allowed.")

else:
    print("Result =", result)

finally:
    print("Program finished.")