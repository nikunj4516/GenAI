import pandas as pd
from sklearn.feature_extraction.text import CountVectorizer

df = pd.read_csv("final_preprocessed_dataset.csv")

text = df["final_clean_text"]

configs = {
    "Unigram": (1, 1),
    "Bigram": (2, 2),
    "Trigram": (3, 3)
}

for name, gram in configs.items():

    print(f"\n{name}")
    print("-" * 40)

    vectorizer = CountVectorizer(
        ngram_range=gram
    )

    matrix = vectorizer.fit_transform(text)

    print("Vocabulary Size:",
          len(vectorizer.vocabulary_))

    print("Matrix Shape:",
          matrix.shape)