# Task 2: Read File in Different Ways

with open("sales_data.txt", "r") as f:
    # Read entire file
    print("Using read():\n", f.read())

# Read first line
with open("sales_data.txt", "r") as f:
    print("Using readline():", f.readline().strip())

# Read all lines into list of integers
with open("sales_data.txt", "r") as f:
    lines = f.readlines()
    sales_list = [int(line.strip()) for line in lines]
    print("Using readlines() → List of Integers:", sales_list)
