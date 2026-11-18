import pandas as pd
import nltk

from nltk.tokenize import word_tokenize
from nltk.tokenize import sent_tokenize

nltk.download("punkt")

df = pd.read_csv("task5_output.csv")

print("TASK 6 : TOKENIZATION")

for i in range(3):

    text = str(df["normalized_text"].iloc[i])

    print("\n" + "=" * 50)
    print("SAMPLE", i + 1)

    print("\nOriginal Text:")
    print(text)

    print("\nWord Tokens:")
    print(word_tokenize(text))

    print("\nSentence Tokens:")
    print(sent_tokenize(text))