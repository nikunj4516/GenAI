# Task 2: Word2Vec Overview

## 1. What is Word2Vec?

Word2Vec is a shallow neural-network-based technique that learns vector representations of words from text data.

It learns embeddings by predicting words using their surrounding context.

---

## 2. Predicting Words from Context

Example:

I love this _____

Expected word:

product

Word2Vec repeatedly performs such tasks to learn semantic meaning.

---

## 3. Definitions

### Vocabulary

The set of unique words present in the corpus.

Example:

good
product
battery
phone

---

### Context Window

Number of neighboring words considered around a target word.

Window = 5 means five words left and five words right.

---

### Embedding Dimension

Length of numerical vector representing a word.

Example:

vector_size = 100

Each word is represented using a vector of 100 values.