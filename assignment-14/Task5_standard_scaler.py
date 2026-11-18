# Task 5: StandardScaler

import pandas as pd

from sklearn.preprocessing import StandardScaler

# Task 5: StandardScaler

import pandas as pd

from sklearn.preprocessing import StandardScaler

# Task 5: StandardScaler

import pandas as pd

from sklearn.preprocessing import StandardScaler

df = pd.read_csv(r"C:\GenAI\GenAI_Task(14)Nikunj\titanic_clean.csv")


numerical_cols = [
    "age",
    "fare",
    "sibsp",
    "parch",
    "pclass"
]

scaler = StandardScaler()

scaled = scaler.fit_transform(
    df[numerical_cols]
)

scaled_df = pd.DataFrame(
    scaled,
    columns=numerical_cols
)

print(scaled_df.head())

print("\nMean:")
print(scaled_df.mean())

print("\nStandard Deviation:")
print(scaled_df.std())

numerical_cols = [
    "age",
    "fare",
    "sibsp",
    "parch",
    "pclass"
]

scaler = StandardScaler()

scaled = scaler.fit_transform(
    df[numerical_cols]
)

scaled_df = pd.DataFrame(
    scaled,
    columns=numerical_cols
)

print(scaled_df.head())

print("\nMean:")
print(scaled_df.mean())

print("\nStandard Deviation:")
print(scaled_df.std())

numerical_cols = [
    "age",
    "fare",
    "sibsp",
    "parch",
    "pclass"
]

scaler = StandardScaler()

scaled = scaler.fit_transform(
    df[numerical_cols]
)

scaled_df = pd.DataFrame(
    scaled,
    columns=numerical_cols
)

print(scaled_df.head())

print("\nMean:")
print(scaled_df.mean())

print("\nStandard Deviation:")
print(scaled_df.std())