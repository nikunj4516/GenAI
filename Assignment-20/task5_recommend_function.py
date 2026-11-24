"""
PART 3 - Task 5: Build Recommendation Function

def recommend(itemname, top_n=5): returns the top N similar movies.

Steps inside the function:
  1. Find the index of the selected movie
  2. Compute (look up) similarity scores
  3. Sort and return the top recommendations

Run:  python PART3_Recommendation_Logic/task5_recommend_function.py
"""

import os
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if ROOT not in sys.path:
    sys.path.insert(0, ROOT)

import pandas as pd

from PART1_Data_Preprocessing.task1_load_dataset import load_data
from PART1_Data_Preprocessing.task2_text_preprocessing import preprocess
from PART2_Text_Vectorization.task3_tfidf import build_tfidf
from PART2_Text_Vectorization.task4_cosine_similarity import build_similarity

_MODEL = {}  # built once, reused on every call (keeps the app fast)


def get_model():
    """Build (or return the cached) dataframe, similarity matrix and title index."""
    if not _MODEL:
        df = preprocess(load_data())
        _, matrix = build_tfidf(df)
        _MODEL["df"] = df
        _MODEL["similarity"] = build_similarity(matrix)
        _MODEL["index"] = pd.Series(df.index, index=df["title"].str.lower())
    return _MODEL


def get_titles():
    """All movie titles, sorted (used by the dropdown)."""
    return sorted(get_model()["df"]["title"].tolist())


def recommend(itemname, top_n=5):
    """Return a DataFrame with the top_n movies most similar to itemname."""
    model = get_model()
    df, similarity, index_map = model["df"], model["similarity"], model["index"]

    key = str(itemname).strip().lower()
    if key not in index_map:
        raise ValueError(f"Movie '{itemname}' not found in the dataset.")

    idx = int(index_map[key])                                   # 1. find index
    scores = list(enumerate(similarity[idx]))                   # 2. similarity scores
    scores = sorted(scores, key=lambda x: x[1], reverse=True)   # 3. sort
    scores = [s for s in scores if s[0] != idx][:top_n]         # skip the movie itself

    rows = [i for i, _ in scores]
    result = df.loc[rows, ["title", "genres_display", "vote_average", "overview"]].copy()
    result["similarity"] = [round(float(s), 4) for _, s in scores]
    result = result.rename(columns={"genres_display": "genres"})
    return result.reset_index(drop=True)


def main():
    print("=" * 70)
    print("TASK 5: RECOMMENDATION FUNCTION")
    print("=" * 70)
    for movie in ["Avatar", "The Dark Knight", "Toy Story", "The Godfather"]:
        print(f"\nTop 5 recommendations for '{movie}':")
        print(recommend(movie, 5)[["title", "genres", "similarity"]].to_string(index=False))

    print("\nError handling test:")
    try:
        recommend("This Movie Does Not Exist")
    except ValueError as e:
        print("  ", e)


if __name__ == "__main__":
    main()
