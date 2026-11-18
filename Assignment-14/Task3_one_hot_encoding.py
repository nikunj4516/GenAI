# Task 3: One Hot Encoding

import pandas as pd

df = pd.read_csv(r"C:\GenAI\GenAI_Task(14)Nikunj\titanic_clean.csv")

df = df[
    [
        "age",
        "fare",
        "sex",
        "sibsp",
        "parch",
        "pclass",
        "embarked",
        "2urvived"
    ]
]

categorical_cols = [
    "sex",
    "embarked"
]

encoded_df = pd.get_dummies(
    df,
    columns=categorical_cols,
    drop_first=True
)

print(encoded_df.head())

print("\nEncoded Shape:")
print(encoded_df.shape)