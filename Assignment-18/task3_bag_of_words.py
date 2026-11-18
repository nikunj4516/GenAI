import pandas as pd
from sklearn.feature_extraction.text import CountVectorizer

df = pd.read_csv("final_preprocessed_dataset.csv")

text = df["final_clean_text"]

vectorizer = CountVectorizer()

bow_matrix = vectorizer.fit_transform(text)

print("Vocabulary Size:")
print(len(vectorizer.vocabulary_))

print("\nBoW Matrix Shape:")
print(bow_matrix.shape)

print("\nSample Feature Vectors:\n")
print(bow_matrix.toarray()[:5])