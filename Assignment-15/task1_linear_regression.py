# task1_linear_regression.py

import pandas as pd
import matplotlib.pyplot as plt

from pathlib import Path
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression

project_root = Path(__file__).resolve().parent

df = pd.read_csv(project_root / "titanic_clean.csv")

TARGET_COLUMN = "fare"

feature_columns = [
    "pclass",
    "age",
    "sibsp",
    "parch",
    "sex"
]

X = df[feature_columns]
y = df[TARGET_COLUMN]

X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.2,
    random_state=42
)

model = LinearRegression()

model.fit(X_train, y_train)

predictions = model.predict(X_test)

plt.figure(figsize=(8, 6))
plt.scatter(y_test, predictions)

plt.xlabel("Actual Fare")
plt.ylabel("Predicted Fare")
plt.title("Actual vs Predicted Fare")

plt.savefig(project_root / "actual_vs_predicted.png")

plt.show()

print("Linear Regression Model Trained Successfully")