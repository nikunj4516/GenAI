"""
PART 1 - Task 1: Load & Understand Dataset

Dataset : TMDB 5000 Movie Dataset (Kaggle)
Link    : https://www.kaggle.com/datasets/tmdb/tmdb-movie-metadata
File    : Movie_recommendation.csv

Run:  python PART1_Data_Preprocessing/task1_load_dataset.py
"""

import os
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if ROOT not in sys.path:
    sys.path.insert(0, ROOT)

import pandas as pd

CSV_CANDIDATES = ["Movie_recommendation.csv", "Movie recommendation.csv"]


def find_csv():
    """Return the dataset path (works with either file name)."""
    for name in CSV_CANDIDATES:
        path = os.path.join(ROOT, name)
        if os.path.exists(path):
            return path
    raise FileNotFoundError(
        "Dataset not found. Put 'Movie_recommendation.csv' in the project root folder."
    )


def load_data():
    """Load the dataset with Pandas."""
    return pd.read_csv(find_csv())


def main():
    pd.set_option("display.max_columns", None)
    pd.set_option("display.width", 200)
    pd.set_option("display.max_colwidth", 50)

    df = load_data()

    print("=" * 70)
    print("TASK 1: LOAD & UNDERSTAND DATASET")
    print("=" * 70)
    print("Dataset shape :", df.shape)
    print("\nColumn names  :", list(df.columns))
    print("\nFirst 5 rows:\n", df.head())
    print("\nData types:\n", df.dtypes)
    print("\nMissing values per column:\n", df.isnull().sum())
    print("\nDuplicate titles:", df["title"].duplicated().sum())
    print("\nSummary statistics:\n", df.describe().round(2))

    print("\nItem identifier column               : title")
    print("Text columns used for recommendations: overview, tagline, genres, keywords")


if __name__ == "__main__":
    main()
