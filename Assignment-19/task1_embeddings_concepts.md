# Task 1: Understanding Word Embeddings

## 1. What are Word Embeddings?

Word embeddings are dense numerical vector representations of words that capture semantic and contextual relationships between words. Similar words have similar vector representations.

Example:

Phone ≈ Mobile

Good ≈ Excellent

---

## 2. Why do One-Hot Encoding and BoW fail to capture semantics?

### One-Hot Encoding

- Produces sparse vectors.
- Every word is independent.
- Cannot capture relationships between words.

Example:

Phone = [1,0,0,0]

Mobile = [0,1,0,0]

Although phone and mobile mean similar things, vectors are unrelated.

### Bag of Words (BoW)

- Ignores context.
- Ignores word order.
- Cannot identify semantic similarity.

Example:

good product

excellent product

BoW treats good and excellent as different features.

---

## 3. How do Word Embeddings solve these problems?

Word embeddings:

- Capture semantic meaning.
- Learn contextual relationships.
- Reduce dimensionality.
- Place related words close together in vector space.

Examples:

phone ≈ mobile

good ≈ excellent

battery ≈ power