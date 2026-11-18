import pandas as pd
import nltk

nltk.download("punkt")

df = pd.read_csv("product_reviews_dataset.csv")

sentences = []

for review in df["text"]:

    words = nltk.word_tokenize(str(review).lower())

    sentences.append(words)

print("First 5 Sentences:\n")

for sentence in sentences[:5]:

    print(sentence)

print("\nTotal Sentences:", len(sentences))