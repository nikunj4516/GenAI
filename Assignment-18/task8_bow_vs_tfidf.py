import pandas as pd

from sklearn.feature_extraction.text import (
    CountVectorizer,
    TfidfVectorizer
)

df = pd.read_csv(
    "final_preprocessed_dataset.csv"
)

text = df["final_clean_text"]

# BoW
bow = CountVectorizer()

bow_matrix = bow.fit_transform(text)

# TF-IDF
tfidf = TfidfVectorizer()

tfidf_matrix = tfidf.fit_transform(text)

tfidf_scores = tfidf_matrix.sum(axis=0).A1

words = tfidf.get_feature_names_out()

result = pd.DataFrame({
    "Word": words,
    "TFIDF": tfidf_scores
})

print("\nTop TF-IDF Words\n")

print(
    result.sort_values(
        by="TFIDF",
        ascending=False
    ).head(10)
)

print("\nLow TF-IDF Words\n")

print(
    result.sort_values(
        by="TFIDF"
    ).head(10)
)

print("\nObservation:")
print("TF-IDF down-weights very common words.")