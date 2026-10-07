import pandas as pd


# Task 3: Python Functionalities on Series

marks = [78, 85, 90, 66, 72]

marks_series = pd.Series(marks)

print("Maximum Marks:")
print(marks_series.max())

print("\nMinimum Marks:")
print(marks_series.min())

print("\nSum of Marks:")
print(marks_series.sum())

print("\nMean Marks:")
print(marks_series.mean())

pass_status = marks_series.apply(lambda x: x >= 70)

print("\nPass Status:")
print(pass_status)

print("\nStudents Passed:")
print(pass_status.sum())