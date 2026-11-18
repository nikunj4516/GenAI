# Task 5: Understanding the Data

from pathlib import Path
import pandas as pd

# =====================================
# Locate train.csv automatically
# =====================================

project_root = Path(__file__).resolve().parent.parent

csv_path = project_root / "train.csv"

if not csv_path.exists():
    print(f"ERROR: train.csv not found")
    print(f"Expected Location: {csv_path}")
    exit()

# =====================================
# Load Dataset
# =====================================

df = pd.read_csv(csv_path)

print("=" * 60)
print("TASK 5 - UNDERSTANDING THE DATA")
print("=" * 60)

# =====================================
# Dataset Shape
# =====================================

print("\n1. Dataset Shape")
print(df.shape)

# =====================================
# Data Types
# =====================================

print("\n2. Data Types")
print(df.dtypes)

# =====================================
# Numerical Columns
# =====================================

numerical_cols = df.select_dtypes(
    include=["int64", "float64"]
).columns.tolist()

print("\n3. Numerical Columns")
print(numerical_cols)

# =====================================
# Categorical Columns
# =====================================

categorical_cols = df.select_dtypes(
    include=["object"]
).columns.tolist()

print("\n4. Categorical Columns")
print(categorical_cols)

# =====================================
# Missing Values
# =====================================

print("\n5. Missing Values Count")
print(df.isnull().sum())

# =====================================
# Duplicate Rows
# =====================================

print("\n6. Duplicate Rows")
print(df.duplicated().sum())

# =====================================
# Descriptive Statistics
# =====================================

print("\n7. Statistical Summary")
print(df.describe())

# =====================================
# Dataset Information
# =====================================

print("\n8. Dataset Information")
print(df.info())

print("\nTask 5 Completed Successfully")