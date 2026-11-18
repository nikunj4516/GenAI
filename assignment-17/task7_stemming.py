import pandas as pd
import nltk

from nltk.stem import PorterStemmer

nltk.download("punkt")

stemmer = PorterStemmer()

df = pd.read_csv("task5_output.csv")

sample_text = df["normalized_text"].iloc[0]

words = sample_text.split()

stemmed_words = [
    stemmer.stem(word)
    for word in words
]

print("Original Words:")
print(words)

print("\nStemmed Words:")
print(stemmed_words)