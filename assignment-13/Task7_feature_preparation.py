# Task 7: Feature Preparation

from pathlib import Path
import pandas as pd

# =====================================
# Locate titanic_clean.csv
# =====================================

project_root = Path(__file__).resolve().parent.parent

clean_file = project_root / "titanic_clean.csv"

if not clean_file.exists():
    print("ERROR: titanic_clean.csv not found.")
    print("Run Task6_data_cleaning.py first.")
    exit()

# =====================================
# Load Cleaned Data
# =====================================

df = pd.read_csv(clean_file)

print("=" * 60)
print("TASK 7 - FEATURE PREPARATION")
print("=" * 60)

# =====================================
# Target Column
# =====================================

if "2urvived" in df.columns:
    target = "2urvived"
elif "survived" in df.columns:
    target = "survived"
else:
    print("Target column not found.")
    print("Available Columns:")
    print(df.columns.tolist())
    exit()

# =====================================
# Features and Target
# =====================================

X = df.drop(columns=[target])
y = df[target]

print("\nTarget Column:")
print(target)

print("\nFeature Matrix Shape:")
print(X.shape)

print("\nTarget Shape:")
print(y.shape)

print("\nFirst 5 Rows of Features:")
print(X.head())

print("\nFirst 5 Values of Target:")
print(y.head())

# =====================================
# Save Output Files
# =====================================

X_file = project_root / "titanic_features_X.csv"
y_file = project_root / "titanic_target_y.csv"

X.to_csv(X_file, index=False)
y.to_csv(y_file, index=False)

print("\nFiles Created Successfully")

print("\nFeature File:")
print(X_file)

print("\nTarget File:")
print(y_file)

print("\nTask 7 Completed Successfully")