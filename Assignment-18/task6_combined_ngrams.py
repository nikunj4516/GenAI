import pandas as pd

from sklearn.feature_extraction.text import CountVectorizer

df = pd.read_csv(
    "final_preprocessed_dataset.csv"
)

text = df["final_clean_text"]

vectorizer = CountVectorizer(
    ngram_range=(1, 2)
)

matrix = vectorizer.fit_transform(text)

print("Vocabulary Size:")
print(len(vectorizer.vocabulary_))

print("\nSample Features:\n")
print(
    vectorizer.get_feature_names_out()[:30]
)

print("\nObservation:")
print("Combined N-grams capture individual words and word pairs.")