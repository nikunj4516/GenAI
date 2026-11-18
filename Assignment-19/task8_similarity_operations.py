import pandas as pd
import nltk

from gensim.models import Word2Vec

nltk.download('punkt')

df = pd.read_csv("dataset.csv")

sentences = [
    nltk.word_tokenize(str(text).lower())
    for text in df["clean_text"]
]

model = Word2Vec(
    sentences,
    vector_size=100,
    window=5,
    min_count=1,
    sg=1
)

word = model.wv.index_to_key[0]

print("Similar Words:\n")

print(
    model.wv.most_similar(word)
)

try:

    result = model.wv.most_similar(
        positive=["good", "movie"],
        negative=["bad"],
        topn=5
    )

    print("\nVector Arithmetic Result:")

    print(result)

except:
    print("Required words not found in vocabulary.")