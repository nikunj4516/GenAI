import pandas as pd

from nltk.stem import PorterStemmer

stemmer = PorterStemmer()

df = pd.read_csv("task5_output.csv")

text = str(df["normalized_text"].iloc[0])

words = text.split()

stemmed_words = []

for word in words:
    stemmed_words.append(
        stemmer.stem(word)
    )

comparison = pd.DataFrame({
    "Original": words,
    "Stemmed": stemmed_words
})

print("TASK 7 : STEMMING\n")

print(comparison)