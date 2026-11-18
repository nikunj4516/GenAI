# Task 1: Creating New Features

import pandas as pd

df = pd.read_csv(
    "C:/GenAI/GenAI_Task(14)Nikunj/titanic_clean.csv"
)

df["family_size"] = df["sibsp"] + df["parch"]

df["fare_per_person"] = df["fare"] / (df["family_size"] + 1)

print(df.head())
print("\nNew Features Added:")
print("family_size")
print("fare_per_person")