import pandas as pd
import nltk
import time

from gensim.models import Word2Vec

nltk.download('punkt')

df = pd.read_csv("dataset.csv")

sentences = [
    nltk.word_tokenize(str(text).lower())
    for text in df["clean_text"]
]

start = time.time()

skipgram_model = Word2Vec(
    sentences,
    vector_size=100,
    window=5,
    min_count=1,
    sg=1
)

end = time.time()

print("Training Time:")
print(end-start)

word = skipgram_model.wv.index_to_key[0]

print("\nMost Similar Words:")

print(
    skipgram_model.wv.most_similar(word, topn=5)
)