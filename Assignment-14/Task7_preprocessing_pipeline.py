# Task 7: Preprocessing Pipeline

from pathlib import Path
import pandas as pd

from sklearn.pipeline import Pipeline
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import (
    StandardScaler,
    OneHotEncoder
)

project_root = Path(__file__).resolve().parent

df = pd.read_csv(r"C:\GenAI\GenAI_Task(14)Nikunj\titanic_clean.csv")

X = df.drop("2urvived", axis=1)

categorical_features = [
    "sex",
    "embarked"
]

numerical_features = [
    col for col in X.columns
    if col not in categorical_features
]

numeric_pipeline = Pipeline(
    steps=[
        ("scaler", StandardScaler())
    ]
)

categorical_pipeline = Pipeline(
    steps=[
        (
            "encoder",
            OneHotEncoder(
                handle_unknown="ignore"
            )
        )
    ]
)

preprocessor = ColumnTransformer(
    [
        ("num", numeric_pipeline,
         numerical_features),

        ("cat", categorical_pipeline,
         categorical_features)
    ]
)

processed = preprocessor.fit_transform(X)

print(processed.shape)