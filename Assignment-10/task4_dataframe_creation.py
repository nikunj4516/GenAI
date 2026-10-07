import pandas as pd


# Task 4: Create a DataFrame

students = {
    "Name": ["Amit", "Neha", "Rahul", "Sneha", "Pooja"],
    "Marks": [78, 85, 90, 66, 72],
    "Subject": ["Math", "Math", "Science", "Science", "Math"]
}

students_df = pd.DataFrame(students)

print("First 3 Rows:")
print(students_df.head(3))

print("\nLast 2 Rows:")
print(students_df.tail(2))

print("\nShape:")
print(students_df.shape)

print("\nColumns:")
print(students_df.columns.tolist())