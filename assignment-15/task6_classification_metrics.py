# task6_classification_metrics.py

import pandas as pd
import matplotlib.pyplot as plt

from pathlib import Path

from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.naive_bayes import GaussianNB
from sklearn.neighbors import KNeighborsClassifier

from sklearn.metrics import (
    classification_report,
    confusion_matrix,
    ConfusionMatrixDisplay
)

project_root = Path(__file__).resolve().parent

df = pd.read_csv(project_root / "titanic_clean.csv")

# CHANGE IF YOUR TARGET COLUMN IS DIFFERENT
TARGET_COLUMN = "survived"

X = df.drop(columns=[TARGET_COLUMN])
y = df[TARGET_COLUMN]

X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.2,
    random_state=42
)

models = {
    "Logistic Regression": LogisticRegression(max_iter=1000),
    "Naive Bayes": GaussianNB(),
    "KNN": KNeighborsClassifier(n_neighbors=5)
}

for model_name, model in models.items():

    model.fit(X_train, y_train)

    predictions = model.predict(X_test)

    print("\n" + "="*40)
    print(model_name)
    print("="*40)

    print(classification_report(y_test, predictions))

    cm = confusion_matrix(y_test, predictions)

    fig, ax = plt.subplots(figsize=(6, 5))

    ConfusionMatrixDisplay(
        confusion_matrix=cm
    ).plot(ax=ax)

    plt.title(f"{model_name} Confusion Matrix")

    if model_name == "Logistic Regression":

        plt.savefig(
            project_root / "logistic_confusion_matrix.png"
        )

    elif model_name == "Naive Bayes":

        plt.savefig(
            project_root / "nb_confusion_matrix.png"
        )

    elif model_name == "KNN":

        plt.savefig(
            project_root / "knn_confusion_matrix.png"
        )

    plt.close()

print("\nAll confusion matrices saved successfully.")