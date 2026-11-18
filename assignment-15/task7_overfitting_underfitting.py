# task7_overfitting_underfitting.py

import pandas as pd

from pathlib import Path
from sklearn.tree import DecisionTreeClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score

project_root = Path(__file__).resolve().parent

df = pd.read_csv(project_root / "titanic_clean.csv")

TARGET_COLUMN = "survived"

X = df.drop(columns=[TARGET_COLUMN])
y = df[TARGET_COLUMN]

X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.2,
    random_state=42
)

print("=" * 50)
print("UNDERFITTING")
print("=" * 50)

simple_model = DecisionTreeClassifier(
    max_depth=1,
    random_state=42
)

simple_model.fit(X_train, y_train)

train_pred = simple_model.predict(X_train)
test_pred = simple_model.predict(X_test)

print("Training Accuracy:", accuracy_score(y_train, train_pred))
print("Testing Accuracy:", accuracy_score(y_test, test_pred))

print("\n")

print("=" * 50)
print("OVERFITTING")
print("=" * 50)

complex_model = DecisionTreeClassifier(
    max_depth=None,
    random_state=42
)

complex_model.fit(X_train, y_train)

train_pred = complex_model.predict(X_train)
test_pred = complex_model.predict(X_test)

print("Training Accuracy:", accuracy_score(y_train, train_pred))
print("Testing Accuracy:", accuracy_score(y_test, test_pred))

print("\nObservation:")
print("Underfitting -> Low training and testing accuracy.")
print("Overfitting -> High training accuracy but lower testing accuracy.")