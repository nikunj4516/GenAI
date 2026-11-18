# Task 6: MinMaxScaler

import pandas as pd

from sklearn.preprocessing import MinMaxScaler

# Task 6: MinMaxScaler

import pandas as pd

from sklearn.preprocessing import MinMaxScaler

df = pd.read_csv(r"C:\GenAI\GenAI_Task(14)Nikunj\titanic_clean.csv")

numerical_cols = [
    "age",
    "fare",
    "sibsp",
    "parch",
    "pclass"
]

scaler = MinMaxScaler()

scaled = scaler.fit_transform(
    df[numerical_cols]
)

scaled_df = pd.DataFrame(
    scaled,
    columns=numerical_cols
)

print(scaled_df.head())

print("\nMinimum Values:")
print(scaled_df.min())

print("\nMaximum Values:")
print(scaled_df.max())

numerical_cols = [
    "age",
    "fare",
    "sibsp",
    "parch",
    "pclass"
]

scaler = MinMaxScaler()

scaled = scaler.fit_transform(
    df[numerical_cols]
)

scaled_df = pd.DataFrame(
    scaled,
    columns=numerical_cols
)

print(scaled_df.head())

print("\nMinimum Values:")
print(scaled_df.min())

print("\nMaximum Values:")
print(scaled_df.max())