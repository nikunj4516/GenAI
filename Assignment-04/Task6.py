# Task 6: Read File Safely

import os

filename = input("Enter filename to open: ")

if os.path.exists(filename):
    with open(filename, "r") as f:
        print("File Contents:\n", f.read())
else:
    print("File not found. Please check the filename.")
