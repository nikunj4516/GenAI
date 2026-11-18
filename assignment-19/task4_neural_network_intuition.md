# Task 4: Neural Network Intuition Behind Word2Vec

## 1. Input Layer

Input word is converted into one-hot encoding.

Example:

phone

[0 1 0 0 0]

---

## 2. Hidden Layer (Embedding Layer)

Transforms high-dimensional one-hot vectors into dense vectors.

Example:

100-dimensional embedding

[0.12, 0.56, -0.23, ...]

---

## 3. Output Layer

Predicts:

- Target word (CBOW)
- Context words (Skip-Gram)

---

## 4. How Weights Become Embeddings

During training:

- Weights are continuously updated.
- Similar words get similar representations.

Final weight matrix becomes the word embedding matrix.

Each row corresponds to one word vector.