import pandas as pd


# Task 5: Important DataFrame Functions

students = {
    "Name": ["Amit", "Neha", "Rahul", "Sneha", "Pooja"],
    "Marks": [78, 85, 90, 66, 72],
    "Subject": ["Math", "Math", "Science", "Science", "Math"]
}

students_df = pd.DataFrame(students)

print("Info:")
students_df.info()

print("\nDescribe:")
print(students_df.describe())

print("\nHead:")
print(students_df.head())

print("\nTail:")
print(students_df.tail())

sorted_students = students_df.sort_values(
    by="Marks",
    ascending=False
)

print("\nSorted DataFrame:")
print(sorted_students)

sorted_students = sorted_students.reset_index(drop=True)

print("\nReset Index:")
print(sorted_students)