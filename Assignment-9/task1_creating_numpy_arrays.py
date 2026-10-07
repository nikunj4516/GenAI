# Task 1: Creating NumPy Arrays

import numpy as np

array_1d = np.arange(1, 11)
array_2d = np.arange(1, 10).reshape(3, 3)
array_list = np.array([10, 20, 30, 40, 50])

print("1D Array:")
print(array_1d)

print("\n2D Array:")
print(array_2d)

print("\nArray From List:")
print(array_list)

print("\nShape of 1D Array:", array_1d.shape)
print("Shape of 2D Array:", array_2d.shape)
print("Shape of List Array:", array_list.shape)

print("\nData Type of 1D Array:", array_1d.dtype)
print("Data Type of 2D Array:", array_2d.dtype)
print("Data Type of List Array:", array_list.dtype)