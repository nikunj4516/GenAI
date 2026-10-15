# Task 9: Bivariate Analysis

from pathlib import Path
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

# =====================================
# Load Cleaned Dataset
# =====================================

project_root = Path(__file__).resolve().parent.parent

clean_file = project_root / "titanic_clean.csv"

if not clean_file.exists():
    print("ERROR: titanic_clean.csv not found.")
    print("Run Task6_data_cleaning.py first.")
    exit()

df = pd.read_csv(clean_file)

target = "2urvived"

print("=" * 60)
print("TASK 9 - BIVARIATE ANALYSIS")
print("=" * 60)

# =====================================
# Scatter Plot
# =====================================

if "age" in df.columns and "fare" in df.columns:
    sns.scatterplot(
        x="age",
        y="fare",
        data=df
    )

    plt.title("Age vs Fare")
    plt.show()

# =====================================
# Survival vs Age
# =====================================

if target in df.columns and "age" in df.columns:
    sns.boxplot(
        x=target,
        y="age",
        data=df
    )

    plt.title("Survival vs Age")
    plt.show()

# =====================================
# Survival vs Fare
# =====================================

if target in df.columns and "fare" in df.columns:
    sns.boxplot(
        x=target,
        y="fare",
        data=df
    )

    plt.title("Survival vs Fare")
    plt.show()

# =====================================
# Sex vs Survival
# =====================================

if target in df.columns and "sex" in df.columns:
    sns.barplot(
        x="sex",
        y=target,
        data=df
    )

    plt.title("Sex vs Survival")
    plt.show()

# =====================================
# Pclass vs Survival
# =====================================

if target in df.columns and "pclass" in df.columns:
    sns.barplot(
        x="pclass",
        y=target,
        data=df
    )

    plt.title("Pclass vs Survival")
    plt.show()

# =====================================
# Correlation Heatmap
# =====================================

corr = df.corr(numeric_only=True)

plt.figure(figsize=(10, 8))

sns.heatmap(
    corr,
    annot=True,
    cmap="coolwarm"
)

plt.title("Correlation Heatmap")
plt.show()

# =====================================
# Pairplot
# =====================================

pair_cols = []

for col in ["age", "fare", "pclass", target]:
    if col in df.columns:
        pair_cols.append(col)

if len(pair_cols) > 1:
    sns.pairplot(df[pair_cols])
    plt.show()

print("\nTask 9 Completed Successfully")
