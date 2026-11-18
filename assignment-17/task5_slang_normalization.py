import pandas as pd
import re

df = pd.read_csv("task4_output.csv")

slang_dict = {
    "u": "you",
    "gr8": "great",
    "omg": "oh my god"
}

def normalize_text(text):

    text = re.sub(
        r'(.)\1{2,}',
        r'\1',
        text
    )

    words = text.split()

    words = [
        slang_dict.get(word, word)
        for word in words
    ]

    return " ".join(words)

df["normalized_text"] = df["text_no_stopwords"].apply(
    normalize_text
)

print(df[["text_no_stopwords",
          "normalized_text"]].head())

df.to_csv("task5_output.csv", index=False)