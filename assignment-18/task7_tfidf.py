import pandas as pd

from sklearn.feature_extraction.text import TfidfVectorizer

df = pd.read_csv(
    "final_preprocessed_dataset.csv"
)

text = df["final_clean_text"]

vectorizer = TfidfVectorizer()

tfidf_matrix = vectorizer.fit_transform(text)

print("Vocabulary:\n")
print(vectorizer.get_feature_names_out())

print("\nTF-IDF Matrix Shape:")
print(tfidf_matrix.shape)