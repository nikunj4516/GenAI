# Assignment 6 - Task 3
# Age Validator

def check_age(age):

    # Validate age range
    if age < 1 or age > 120:
        raise ValueError("Age must be between 1 and 120")

    print("Valid Age")


try:
    age = int(input("Enter age: "))

    check_age(age)

except ValueError as e:
    print("Error:", e)