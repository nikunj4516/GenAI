import pandas as pd
import nltk

from nltk.stem import PorterStemmer
from nltk.stem import WordNetLemmatizer

nltk.download("wordnet")

stemmer = PorterStemmer()
lemmatizer = WordNetLemmatizer()

df = pd.read_csv("task5_output.csv")

text = str(df["normalized_text"].iloc[0])

words = text.split()

stemmed_words = []
lemmatized_words = []

for word in words:

    stemmed_words.append(
        stemmer.stem(word)
    )

    lemmatized_words.append(
        lemmatizer.lemmatize(word)
    )

comparison = pd.DataFrame({
    "Original": words,
    "Stemmed": stemmed_words,
    "Lemmatized": lemmatized_words
})

print("TASK 8 : LEMMATIZATION\n")

print(comparison)