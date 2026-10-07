import pandas as pd


# Task 7: Grouping & Basic Analysis

students = {
    "Name": ["Amit", "Neha", "Rahul", "Sneha", "Pooja"],
    "Marks": [78, 85, 90, 66, 72],
    "Subject": ["Math", "Math", "Science", "Science", "Math"]
}

students_df = pd.DataFrame(students)

print("Average Marks Per Subject:")
print(
    students_df.groupby("Subject")["Marks"].mean()
)

print("\nStudent Count Per Subject:")
print(
    students_df.groupby("Subject")["Name"].count()
)

print("\nMaximum Marks Per Subject:")
print(
    students_df.groupby("Subject")["Marks"].max()
)