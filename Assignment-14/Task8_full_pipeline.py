# Task 8: Full Pipeline

from pathlib import Path
import pandas as pd

from sklearn.pipeline import Pipeline
from sklearn.compose import ColumnTransformer

from sklearn.preprocessing import (
    StandardScaler,
    OneHotEncoder
)

from sklearn.linear_model import LogisticRegression

from sklearn.model_selection import (
    train_test_split
)

from sklearn.metrics import accuracy_score

project_root = Path(__file__).resolve().parent

# Task 8: Full Pipeline

from pathlib import Path
import pandas as pd

from sklearn.pipeline import Pipeline
from sklearn.compose import ColumnTransformer

from sklearn.preprocessing import (
    StandardScaler,
    OneHotEncoder
)

from sklearn.linear_model import LogisticRegression

from sklearn.model_selection import (
    train_test_split
)

from sklearn.metrics import accuracy_score

project_root = Path(__file__).resolve().parent

df = pd.read_csv(r"C:\GenAI\GenAI_Task(14)Nikunj\titanic_clean.csv")

X = df.drop("2urvived", axis=1)

y = df["2urvived"]

categorical_features = [
    "age",
 "fare",
 "sex",
 "sibsp",
 "parch",
 "pclass",
 "embarked"
]

numerical_features = [
    col for col in X.columns
    if col not in categorical_features
]

preprocessor = ColumnTransformer(
    transformers=[
        (
            "num",
            StandardScaler(),
            numerical_features
        ),
        (
            "cat",
            OneHotEncoder(
                handle_unknown="ignore"
            ),
            categorical_features
        )
    ]
)

pipeline = Pipeline(
    steps=[
        (
            "preprocessor",
            preprocessor
        ),
        (
            "model",
            LogisticRegression(
                max_iter=1000
            )
        )
    ]
)

X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.2,
    random_state=42
)

pipeline.fit(
    X_train,
    y_train
)

predictions = pipeline.predict(
    X_test
)

accuracy = accuracy_score(
    y_test,
    predictions
)

print("Accuracy:", accuracy)

X = df.drop("2urvived", axis=1)

y = df["2urvived"]

categorical_features = [
    "sex",
    "embarked"
]

numerical_features = [
    col for col in X.columns
    if col not in categorical_features
]

preprocessor = ColumnTransformer(
    transformers=[
        (
            "num",
            StandardScaler(),
            numerical_features
        ),
        (
            "cat",
            OneHotEncoder(
                handle_unknown="ignore"
            ),
            categorical_features
        )
    ]
)

pipeline = Pipeline(
    steps=[
        (
            "preprocessor",
            preprocessor
        ),
        (
            "model",
            LogisticRegression(
                max_iter=1000
            )
        )
    ]
)

X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.2,
    random_state=42
)

pipeline.fit(
    X_train,
    y_train
)

predictions = pipeline.predict(
    X_test
)

accuracy = accuracy_score(
    y_test,
    predictions
)

print("Accuracy:", accuracy)