import pandas as pd


# Task 2: Mathematical Operations on Series

marks = [78, 85, 90, 66, 72]

marks_series = pd.Series(marks)

print("Add 5 Grace Marks:")
print(marks_series + 5)

print("\nSubtract 2 Marks:")
print(marks_series - 2)

print("\nMultiply Marks by 1.05:")
print(marks_series * 1.05)

print("\nDivide Marks by 2:")
print(marks_series / 2)