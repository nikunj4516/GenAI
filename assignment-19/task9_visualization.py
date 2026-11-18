import pandas as pd
import nltk

from gensim.models import Word2Vec

from sklearn.decomposition import PCA

import matplotlib.pyplot as plt

nltk.download('punkt')

df = pd.read_csv("dataset.csv")

sentences = [
    nltk.word_tokenize(str(text).lower())
    for text in df["clean_text"]
]

model = Word2Vec(
    sentences,
    vector_size=100,
    min_count=1
)

words = model.wv.index_to_key[:20]

vectors = [model.wv[word] for word in words]

pca = PCA(n_components=2)

result = pca.fit_transform(vectors)

plt.figure(figsize=(10,6))

for i, word in enumerate(words):

    plt.scatter(
        result[i,0],
        result[i,1]
    )

    plt.annotate(
        word,
        (result[i,0], result[i,1])
    )

plt.title("Word2Vec Embeddings PCA")

plt.show()