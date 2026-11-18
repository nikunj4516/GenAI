import pandas as pd
from sklearn.feature_extraction.text import CountVectorizer

df = pd.read_csv("final_preprocessed_dataset.csv")

sentences = df["final_clean_text"].head(5)

vectorizer = CountVectorizer(binary=True)

encoded = vectorizer.fit_transform(sentences)

result = pd.DataFrame(
    encoded.toarray(),
    columns=vectorizer.get_feature_names_out()
)

print("Vocabulary:\n")
print(vectorizer.vocabulary_)

print("\nEncoded Matrix:\n")
print(result)