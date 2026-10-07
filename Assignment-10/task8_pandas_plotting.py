import pandas as pd
import matplotlib.pyplot as plt


# Task 8: Pandas Plotting (Simple Graphs)

students = {
    "Name": ["Amit", "Neha", "Rahul", "Sneha", "Pooja"],
    "Marks": [78, 85, 90, 66, 72],
    "Subject": ["Math", "Math", "Science", "Science", "Math"]
}

students_df = pd.DataFrame(students)

students_df.plot(
    x="Name",
    y="Marks",
    kind="bar",
    title="Student Names vs Marks"
)

plt.show()

students_df["Marks"].plot(
    kind="line",
    title="Marks Line Graph"
)

plt.show()

students_df["Marks"].plot(
    kind="hist",
    title="Marks Histogram"
)

plt.show()
