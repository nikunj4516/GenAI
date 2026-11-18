# task2_regression_metrics.py

import pandas as pd
import numpy as np

from pathlib import Path
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_absolute_error
from sklearn.metrics import mean_squared_error

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

mae = mean_absolute_error(y_test, predictions)
mse = mean_squared_error(y_test, predictions)
rmse = np.sqrt(mse)

print("MAE :", mae)
print("MSE :", mse)
print("RMSE :", rmse)

print("\nInterpretation")
print("MAE -> Average prediction error")
print("MSE -> Larger errors get larger penalties")
print("RMSE -> Error in actual Fare units")