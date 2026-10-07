import pandas as pd


# Task 1: Pandas Series Basics

marks = [78, 85, 90, 66, 72]

marks_series = pd.Series(marks)

print("Series Values:")
print(marks_series)

print("\nIndex:")
print(marks_series.index)

print("\nData Type:")
print(marks_series.dtype)

print("\nFirst Element:")
print(marks_series.iloc[0])

print("\nLast Two Elements:")
print(marks_series.iloc[-2:])