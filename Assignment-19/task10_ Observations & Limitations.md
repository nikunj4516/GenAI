---

# Task 10: Observations & Limitations

## 1. Difference Between CBOW and Skip-Gram

| CBOW | Skip-Gram |
|--------|------------|
| Predicts target word from context words | Predicts context words from target word |
| Faster training | Slower training |
| Better for frequent words | Better for rare words |
| Suitable for large datasets | Suitable for small datasets |

### Observation

In our product review dataset, CBOW trained faster while Skip-Gram generated slightly better semantic relationships between product-related words.

---

## 2. Advantages of Word2Vec over TF-IDF

- Captures semantic meaning of words.
- Generates dense vector representations.
- Similar words receive similar embeddings.
- Supports similarity calculations.
- Enables vector arithmetic operations.

### Example

```text
good ≈ excellent
phone ≈ mobile
fast ≈ powerful