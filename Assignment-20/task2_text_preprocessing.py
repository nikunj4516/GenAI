"""
PART 1 - Task 2: Text Preprocessing for Recommendation

Steps applied to the text columns:
  1. Convert text to lowercase
  2. Remove punctuation and special characters
  3. Remove stopwords
  4. Handle missing values (replace with empty string)
Cleaned text is stored in a new column: cleantext

Run:  python PART1_Data_Preprocessing/task2_text_preprocessing.py
"""

import json
import os
import re
import string
import sys

ROOT = os.path.dirname(os.path.abspath(__file__))
if ROOT not in sys.path:
    sys.path.insert(0, ROOT)

from sklearn.feature_extraction.text import ENGLISH_STOP_WORDS

from task1_load_dataset import load_data

STOPWORDS = set(ENGLISH_STOP_WORDS)
PUNCT_TABLE = str.maketrans("", "", string.punctuation)


def extract_names(value, join_words=True):
    """Turn a JSON string like '[{"id": 28, "name": "Action"}]' into ['Action'].

    join_words=True  -> 'ScienceFiction' (one token per genre/keyword, for TF-IDF)
    join_words=False -> 'Science Fiction' (readable names)
    """
    try:
        items = json.loads(value)
        names = [i["name"] for i in items]
    except (TypeError, ValueError, KeyError):
        return []
    return [n.replace(" ", "") if join_words else n for n in names]


def clean_text(text):
    """Lowercase -> remove punctuation/special characters -> remove stopwords."""
    if not isinstance(text, str):
        return ""
    text = text.lower()                                          # 1. lowercase
    text = re.sub(r"[‘’“”]", "", text)      # curly quotes
    text = text.translate(PUNCT_TABLE)                           # 2. punctuation
    text = re.sub(r"[^a-z0-9\s]", " ", text)                     # 2. special characters
    text = re.sub(r"\s+", " ", text).strip()
    return " ".join(w for w in text.split() if w not in STOPWORDS)  # 3. stopwords


def preprocess(df):
    """Build the 'cleantext' column and return a cleaned copy of the dataframe."""
    df = df.copy()

    # Keep every movie title unique
    df = df.drop_duplicates(subset="title").reset_index(drop=True)

    # 4. Handle missing values -> empty string
    for col in ["overview", "tagline", "genres", "keywords"]:
        df[col] = df[col].fillna("")

    # genres / keywords are JSON strings -> plain words
    df["genres_text"] = df["genres"].apply(lambda v: " ".join(extract_names(v)))
    df["keywords_text"] = df["keywords"].apply(lambda v: " ".join(extract_names(v)))
    df["genres_display"] = df["genres"].apply(
        lambda v: ", ".join(extract_names(v, join_words=False))
    )

    # Combine all text features, then clean
    combined = (
        df["overview"] + " " + df["tagline"] + " "
        + df["genres_text"] + " " + df["keywords_text"]
    )
    df["cleantext"] = combined.apply(clean_text)
    return df


def main():
    raw = load_data()
    print("=" * 70)
    print("TASK 2: TEXT PREPROCESSING")
    print("=" * 70)
    print("Missing values before cleaning:")
    print(raw[["overview", "tagline", "genres", "keywords"]].isnull().sum())

    df = preprocess(raw)
    print("\nShape after removing duplicate titles:", df.shape)

    print("\nBefore vs after cleaning (first 3 rows):")
    for i in range(3):
        print(f"\n[{df.loc[i, 'title']}]")
        print("  overview  :", df.loc[i, "overview"][:120])
        print("  cleantext :", df.loc[i, "cleantext"][:120])

    print("\nMissing values in 'cleantext':", df["cleantext"].isnull().sum())
    print("Empty cleantext rows         :", (df["cleantext"] == "").sum())


if __name__ == "__main__":
    main()
