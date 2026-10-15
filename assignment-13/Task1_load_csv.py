# Task 1: Load Data from CSV

from pathlib import Path
import pandas as pd

# Get project root folder
project_root = Path(__file__).resolve().parent.parent

# Path to train.csv
csv_path = project_root / "train.csv"

# Load dataset
df = pd.read_csv(csv_path)

print("\n" + "=" * 50)
print("TASK 1 - LOAD DATA FROM CSV")
print("=" * 50)

print("\nDataset Shape:")
print(df.shape)

print("\nColumn Names:")
print(df.columns.tolist())

print("\nFirst 5 Rows:")
print(df.head())