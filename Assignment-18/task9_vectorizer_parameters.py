import pandas as pd

from sklearn.feature_extraction.text import CountVectorizer

df = pd.read_csv(
    "final_preprocessed_dataset.csv"
)

text = df["final_clean_text"]

settings = [

    {"max_features":10},

    {"max_features":20},

    {"min_df":2},

    {"max_df":0.8}

]

for params in settings:

    vectorizer = CountVectorizer(
        **params
    )

    vectorizer.fit(text)

    print("\nParameters:")
    print(params)

    print("Vocabulary Size:")
    print(
        len(
            vectorizer.vocabulary_
        )
    )