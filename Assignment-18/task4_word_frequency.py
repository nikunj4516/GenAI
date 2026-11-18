import pandas as pd
from sklearn.feature_extraction.text import CountVectorizer

df = pd.read_csv("final_preprocessed_dataset.csv")

text = df["final_clean_text"]

vectorizer = CountVectorizer()

bow = vectorizer.fit_transform(text)

frequencies = bow.sum(axis=0).A1

words = vectorizer.get_feature_names_out()

freq_df = pd.DataFrame({
    "Word": words,
    "Frequency": frequencies
})

freq_df = freq_df.sort_values(
    by="Frequency",
    ascending=False
)

print("Top 10 Most Frequent Words\n")
print(freq_df.head(10))

print("\nLeast Frequent Words\n")
print(freq_df.tail(10))

print("\nObservation:")
print("Bag of Words captures how many times a word occurs in documents.")