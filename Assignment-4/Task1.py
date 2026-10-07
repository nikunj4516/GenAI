# Task 1: Write Sales Records to a File

sales = [1200, 450, 980, 1500, 3000]

# Write each sale on a new line
with open("sales_data.txt", "w") as f:
    for s in sales:
        f.write(str(s) + "\n")

# Reopen and print contents
with open("sales_data.txt", "r") as f:
    print("File Contents:\n", f.read())
