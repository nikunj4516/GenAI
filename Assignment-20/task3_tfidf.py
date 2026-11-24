"""
PART 2 - Task 3: Vectorization using TF-IDF

Parameters:
  max_features = 5000   -> keep the 5000 most important terms
  ngram_range  = (1, 2) -> single words and two-word phrases
  min_df       = 2      -> ignore terms that appear in only one movie

Run:  python PART2_Text_Vectorization/task3_tfidf.py
"""

import os
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if ROOT not in sys.path:
    sys.path.insert(0, ROOT)

from sklearn.feature_extraction.text import TfidfVectorizer

from PART1_Data_Preprocessing.task1_load_dataset import load_data
from PART1_Data_Preprocessing.task2_text_preprocessing import preprocess


def build_tfidf(df, max_features=5000, ngram_range=(1, 2)):
    """Convert the 'cleantext' column into a TF-IDF matrix."""
    tfidf = TfidfVectorizer(
        max_features=max_features,
        ngram_range=ngram_range,
        min_df=2,
    )
    matrix = tfidf.fit_transform(df["cleantext"])
    return tfidf, matrix


def main():
    df = preprocess(load_data())
    tfidf, matrix = build_tfidf(df)

    print("=" * 70)
    print("TASK 3: TF-IDF VECTORIZATION")
    print("=" * 70)
    print("Parameters: max_features=5000, ngram_range=(1, 2), min_df=2")
    print("TF-IDF matrix shape:", matrix.shape)
    print("Sample features    :", list(tfidf.get_feature_names_out()[:15]))


if __name__ == "__main__":
    main()
