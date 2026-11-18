# task5_knn.py

import pandas as pd
import matplotlib.pyplot as plt

from pathlib import Path
from sklearn.model_selection import train_test_split
from sklearn.neighbors import KNeighborsClassifier
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

k_values = [3, 5, 7]

accuracies = []

for k in k_values:

    model = KNeighborsClassifier(n_neighbors=k)

    model.fit(X_train, y_train)

    predictions = model.predict(X_test)

    accuracy = accuracy_score(y_test, predictions)

    accuracies.append(accuracy)

    print(f"K = {k} Accuracy = {accuracy:.4f}")

best_k = k_values[accuracies.index(max(accuracies))]

print("\nBest K =", best_k)

plt.plot(k_values, accuracies, marker="o")

plt.xlabel("K Value")
plt.ylabel("Accuracy")
plt.title("KNN Accuracy Comparison")

plt.savefig(project_root / "knn_accuracy_vs_k.png")

plt.show()