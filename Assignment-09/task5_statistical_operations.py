# Task 5: Statistical Operations

import numpy as np

marks = np.array([78, 85, 90, 66, 72, 88, 95, 60])

print("Mean:")
print(np.mean(marks))

print("\nMedian:")
print(np.median(marks))

print("\nVariance:")
print(np.var(marks))

print("\nStandard Deviation:")
print(np.std(marks))

print("\nMinimum:")
print(np.min(marks))

print("\nMaximum:")
print(np.max(marks))

print("\nRange:")
print(np.max(marks) - np.min(marks))