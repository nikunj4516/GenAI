import pandas as pd


# Task 6: Filtering & Conditional Selection

students = {
    "Name": ["Amit", "Neha", "Rahul", "Sneha", "Pooja"],
    "Marks": [78, 85, 90, 66, 72],
    "Subject": ["Math", "Math", "Science", "Science", "Math"]
}

students_df = pd.DataFrame(students)

print("Students Scoring More Than 75:")
print(students_df[students_df["Marks"] > 75])

print("\nMath Students:")
print(students_df[students_df["Subject"] == "Math"])

average_marks = students_df["Marks"].mean()

print("\nStudents Above Average Marks:")
print(students_df[students_df["Marks"] > average_marks])

print("\nFailed Students:")
print(students_df[students_df["Marks"] < 70])