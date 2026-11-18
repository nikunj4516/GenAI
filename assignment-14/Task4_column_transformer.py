# Task 4: ColumnTransformer

import pandas as pd

from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import OneHotEncoder

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

X = df.drop("2urvived", axis=1)

categorical_features = [
    "sex",
    "embarked"
]

numerical_features = [
    "age",
    "fare",
    "sibsp",
    "parch",
    "pclass"
]

transformer = ColumnTransformer(
    transformers=[
        (
            "cat",
            OneHotEncoder(handle_unknown="ignore"),
            categorical_features
        )
    ],
    remainder="passthrough"
)

X_transformed = transformer.fit_transform(X)

print("Transformed Shape:")
print(X_transformed.shape)