import pandas as pd
import nltk

from gensim.models import Word2Vec

nltk.download("punkt")

df = pd.read_csv("product_reviews_dataset.csv")

sentences = [
    nltk.word_tokenize(str(text).lower())
    for text in df["text"]
]

model = Word2Vec(
    sentences=sentences,
    vector_size=100,
    window=5,
    min_count=1,
    sg=0
)

print("=" * 50)

print("CBOW MODEL")

print("=" * 50)

print("Vocabulary Size:")

print(len(model.wv))

sample_word = "product"

if sample_word in model.wv:

    print("\nEmbedding Vector for:", sample_word)

    print(model.wv[sample_word])