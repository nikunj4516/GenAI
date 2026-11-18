# Task 8: Univariate Analysis

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

print("=" * 60)
print("TASK 8 - UNIVARIATE ANALYSIS")
print("=" * 60)

# ==============================
# Histogram + KDE (Age)
# ==============================

if "age" in df.columns:
    sns.histplot(df["age"], kde=True)
    plt.title("Age Distribution")
    plt.show()

# ==============================
# Histogram + KDE (Fare)
# ==============================

if "fare" in df.columns:
    sns.histplot(df["fare"], kde=True)
    plt.title("Fare Distribution")
    plt.show()

# ==============================
# Count Plot (Sex)
# ==============================

if "sex" in df.columns:
    sns.countplot(x="sex", data=df)
    plt.title("Sex Count Plot")
    plt.show()

# ==============================
# Count Plot (Pclass)
# ==============================

if "pclass" in df.columns:
    sns.countplot(x="pclass", data=df)
    plt.title("Passenger Class Count")
    plt.show()

# ==============================
# Box Plot (Age)
# ==============================

if "age" in df.columns:
    sns.boxplot(y=df["age"])
    plt.title("Age Boxplot")
    plt.show()

# ==============================
# Box Plot (Fare)
# ==============================

if "fare" in df.columns:
    sns.boxplot(y=df["fare"])
    plt.title("Fare Boxplot")
    plt.show()

# ==============================
# Violin Plot
# ==============================

if "age" in df.columns:
    sns.violinplot(y=df["age"])
    plt.title("Age Violin Plot")
    plt.show()

# ==============================
# Pie Chart (Target)
# ==============================

target = "2urvived"

if target in df.columns:
    df[target].value_counts().plot(
        kind="pie",
        autopct="%1.1f%%"
    )

    plt.title("Survival Distribution")
    plt.ylabel("")
    plt.show()

print("\nTask 8 Completed Successfully")