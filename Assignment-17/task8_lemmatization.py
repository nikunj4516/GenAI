import pandas as pd
import nltk

from nltk.stem import PorterStemmer
from nltk.stem import WordNetLemmatizer

nltk.download("wordnet")

stemmer = PorterStemmer()
lemmatizer = WordNetLemmatizer()

df = pd.read_csv("task5_output.csv")

sample_text = df["normalized_text"].iloc[0]

words = sample_text.split()

print("Word Comparison\n")

for word in words:

    stemmed = stemmer.stem(word)

    lemmatized = lemmatizer.lemmatize(word)

    print(
        f"{word} -> "
        f"Stem: {stemmed} | "
        f"Lemma: {lemmatized}"
    )