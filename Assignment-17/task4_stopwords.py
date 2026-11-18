import pandas as pd
import nltk

from nltk.corpus import stopwords

nltk.download("stopwords")

df = pd.read_csv("task3_output.csv")

stop_words = set(stopwords.words("english"))

def remove_stopwords(text):

    words = text.split()

    filtered = [
        word
        for word in words
        if word not in stop_words
    ]

    return " ".join(filtered)

df["text_no_stopwords"] = df["clean_text_advanced"].apply(remove_stopwords)

print(df[["clean_text_advanced",
          "text_no_stopwords"]].head())

df.to_csv("task4_output.csv", index=False)