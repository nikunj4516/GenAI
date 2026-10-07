# Task 2: Recursive Function - Factorial

def factorial(n):
    if n == 0 or n == 1:
        return 1
    else:
        return n * factorial(n - 1)

# Test cases
print("Factorial of 5:", factorial(5))   # 120
print("Factorial of 0:", factorial(0))   # 1
