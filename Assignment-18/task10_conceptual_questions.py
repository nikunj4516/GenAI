print("TASK 10 : CONCEPTUAL QUESTIONS\n")

print("1. Difference between One-Hot Encoding and Bag of Words")
print("-" * 60)

print("""
One-Hot Encoding:
- Indicates whether a word exists or not.
- Uses binary values (0 or 1).
- Does not consider frequency.

Bag of Words:
- Counts word occurrences.
- Captures frequency information.
- Produces richer text representation.
""")

print("\n2. Why N-Grams Increase Dimensionality")
print("-" * 60)

print("""
N-Grams create combinations of words.

Example:
Unigram:
good, product

Bigram:
good product

Trigram:
very good product

As combinations increase, vocabulary size grows rapidly,
which increases dimensionality.
""")

print("\n3. When to Prefer TF-IDF Over BoW")
print("-" * 60)

print("""
TF-IDF is preferred when we want important words
to receive higher weights while reducing the importance
of frequently occurring words.

It helps highlight keywords that are more meaningful
within documents.
""")

print("\n4. Limitations of Count-Based Vectorization")
print("-" * 60)

print("""
1. Ignores word meaning.
2. Ignores word order.
3. Produces sparse matrices.
4. High dimensionality.
5. Cannot capture semantic relationships between words.
""")