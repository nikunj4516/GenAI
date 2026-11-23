"""
PART 2 - Task 4: Similarity Computation

Computes cosine similarity between all movies and stores the matrix.

Why cosine similarity?
  - It measures the ANGLE between two TF-IDF vectors, not their length, so a short
    and a long description about the same topic are still judged similar.
  - Scores range from 0 (nothing in common) to 1 (identical), which is easy to rank.
  - It works well and runs fast on sparse, high-dimensional text vectors.

Run:  python PART2_Text_Vectorization/task4_cosine_similarity.py
"""

import os
import sys

ROOT = os.path.dirname(os.path.abspath(__file__))
if ROOT not in sys.path:
    sys.path.insert(0, ROOT)

import numpy as np
from sklearn.metrics.pairwise import cosine_similarity

from task1_load_dataset import load_data
from task2_text_preprocessing import preprocess
from task3_tfidf import build_tfidf


def build_similarity(matrix):
    """Cosine similarity between every pair of movies."""
    # float32 halves memory (~92 MB instead of ~184 MB) - helps on Render free tier
    return cosine_similarity(matrix, matrix).astype(np.float32)


def main():
    df = preprocess(load_data())
    _, matrix = build_tfidf(df)
    similarity = build_similarity(matrix)

    print("=" * 70)
    print("TASK 4: COSINE SIMILARITY")
    print("=" * 70)
    print("Similarity matrix shape:", similarity.shape)
    print("Diagonal (movie vs itself) is 1.0 ->", float(similarity[0, 0]))
    print("Avatar vs Pirates of the Caribbean score:", round(float(similarity[0, 1]), 4))
    print(
        "\nWhy cosine similarity?\n"
        "  - It measures the angle between two TF-IDF vectors, not their length.\n"
        "  - A short and a long description of the same topic still score as similar.\n"
        "  - Scores range 0 (nothing in common) to 1 (identical), easy to rank.\n"
        "  - It is fast and works well on sparse, high-dimensional text vectors."
    )


if __name__ == "__main__":
    main()
