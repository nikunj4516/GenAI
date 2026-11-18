# Task 3: Types of Word2Vec Techniques

## 1. CBOW (Continuous Bag of Words)

Predicts target word from context words.

Example:

This phone is _____

Context Words:

this phone is

Prediction:

good

Advantages:

- Faster training
- Efficient on large datasets
- Good for common words

### When to Use CBOW

Use CBOW when:

- Dataset is large
- Faster training is required
- Frequent words are important

---

## 2. Skip-Gram

Predicts context words from target word.

Example:

Target:

good

Predict:

phone
quality
battery

Advantages:

- Better embeddings
- Works well on small datasets
- Better for rare words

### When to Use Skip-Gram

Use Skip-Gram when:

- Dataset is small
- Rare words are important
- Better semantic quality is needed

---

## Comparison

CBOW = Faster

Skip-Gram = More accurate