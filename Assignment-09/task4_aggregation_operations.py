# Task 4: Aggregation Operations

import numpy as np

data = np.array([
    [10, 20, 30],
    [40, 50, 60],
    [70, 80, 90]
])

print("Row-wise Sum:")
print(np.sum(data, axis=1))

print("\nColumn-wise Sum:")
print(np.sum(data, axis=0))

print("\nMinimum Value:")
print(np.min(data))

print("\nMaximum Value:")
print(np.max(data))

print("\nOverall Mean:")
print(np.mean(data))