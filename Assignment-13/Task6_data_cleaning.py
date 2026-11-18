# Task 6: Data Cleaning

from pathlib import Path
import pandas as pd
import numpy as np

# =====================================
# Locate train.csv automatically
# =====================================

project_root = Path(__file__).resolve().parent.parent

csv_path = project_root / "train.csv"

if not csv_path.exists():
    print("ERROR: train.csv not found")
    print("Expected location:")
    print(csv_path)
    exit()

# =====================================
# Load Dataset
# =====================================

df = pd.read_csv(csv_path)

print("=" * 60)
print("TASK 6 - DATA CLEANING")
print("=" * 60)

# =====================================
# Remove duplicate column names
# =====================================

df = df.loc[:, ~df.columns.duplicated()]

# =====================================
# Remove unnecessary zero columns
# =====================================

zero_cols = [col for col in df.columns if col.lower() == "zero"]

if zero_cols:
    df.drop(columns=zero_cols, inplace=True)

print(f"\nRemoved {len(zero_cols)} zero columns")

# =====================================
# Rename columns
# =====================================

df.columns = (
    df.columns
    .str.lower()
    .str.strip()
    .str.replace(" ", "_")
)

# =====================================
# Handle Missing Values
# =====================================

for col in df.select_dtypes(include=["float64", "int64"]).columns:
    df[col] = df[col].fillna(df[col].median())

for col in df.select_dtypes(include=["object"]).columns:
    df[col] = df[col].fillna("Unknown")

# =====================================
# Remove Duplicate Rows
# =====================================

duplicates = df.duplicated().sum()

print(f"\nDuplicate Rows Found: {duplicates}")

df.drop_duplicates(inplace=True)

# =====================================
# Dataset Information
# =====================================

print("\nCleaned Dataset Shape:")
print(df.shape)

print("\nMissing Values After Cleaning:")
print(df.isnull().sum())

# =====================================
# Save Cleaned Dataset
# =====================================

output_file = project_root / "titanic_clean.csv"

df.to_csv(output_file, index=False)

print("\nCleaned dataset saved successfully:")
print(output_file)

print("\nTask 6 Completed Successfully")