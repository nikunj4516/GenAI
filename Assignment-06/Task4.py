# Assignment 6 - Task 4
# File Reader with Exception Handling

filename = input("Enter filename: ")

try:
    # Open file
    file = open(filename, "r")

    # Print first 3 lines
    for i in range(3):
        print(file.readline().strip())

except FileNotFoundError:
    print("File not found.")

except PermissionError:
    print("Permission denied.")

finally:
    print("File operation attempted.")