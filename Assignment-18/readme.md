# Assignment 18: Text Vectorization Techniques

## Objective

This assignment demonstrates how text data is converted into numerical representations using fundamental NLP feature extraction techniques. These vectorization methods are essential for transforming text into a format that machine learning algorithms can understand.

The assignment covers:

- One-Hot Encoding
- Bag of Words (BoW)
- N-Grams
- TF-IDF Vectorization
- Vectorizer Parameter Exploration

⚠️ No machine learning models are used in this assignment. The focus is entirely on text feature extraction and representation.

---

## Dataset

Dataset Name:

Product Reviews Dataset (Custom Created)

Source:

Self-Created Dataset from Assignment 17

Dataset File:

product_reviews_dataset.csv

Total Records:

25 Product Reviews

Text Used:

The cleaned text generated from Assignment 17 using:

```python
final_clean_text
```

column.

---

## Requirements Fulfilled

- Dataset contains more than 20 text samples.
- Uses cleaned text from previous assignment.
- Uses only:
  - pandas
  - numpy
  - scikit-learn
- No ML classifiers used.
- Focused entirely on feature extraction techniques.

---

## Tasks

### Task 1

Manual One-Hot Encoding

- Selected 5 sentences from dataset
- Built a vocabulary manually
- Created one-hot vectors using Python dictionaries and lists
- Displayed vocabulary and vectors

---

### Task 2

One-Hot Encoding using Scikit-learn

Used:

```python
CountVectorizer(binary=True)
```

Displayed:

- Vocabulary
- Encoded Matrix

---

### Task 3

Bag of Words (BoW)

Used:

```python
CountVectorizer()
```

Applied on complete dataset.

Displayed:

- Vocabulary Size
- Sample Feature Vectors

---

### Task 4

Word Frequency Analysis

Calculated:

- Total frequency of each word

Displayed:

- Top 10 most frequent words
- Least frequent words

Also explained how BoW captures word frequency information.

---

### Task 5

Unigrams, Bigrams & Trigrams

Implemented:

```python
ngram_range=(1,1)
ngram_range=(2,2)
ngram_range=(3,3)
```

Compared:

- Vocabulary Size
- Feature Vectors

---

### Task 6

Combined N-Grams

Implemented:

```python
ngram_range=(1,2)
```

Observed context improvement compared to unigram representation.

---

### Task 7

TF-IDF Vectorization

Used:

```python
TfidfVectorizer()
```

Displayed:

- Vocabulary
- TF-IDF Matrix Shape

---

### Task 8

BoW vs TF-IDF Comparison

Compared:

- Common Word Weights
- High TF-IDF Terms
- Low TF-IDF Terms

Observed how TF-IDF reduces the impact of frequently occurring words.

---

### Task 9

Vectorizer Parameter Exploration

Experimented with:

```python
max_features
min_df
max_df
```

Observed changes in vocabulary size.

---

### Task 10

Conceptual Questions

Answered:

1. Difference between One-Hot Encoding and BoW
2. Why N-Grams increase dimensionality
3. When TF-IDF is preferred over BoW
4. Limitations of Count-Based Vectorization

---

## Libraries Used

- pandas
- numpy
- scikit-learn

---

## Results

This assignment demonstrates:

- Text Feature Extraction
- One-Hot Encoding
- Bag of Words Representation
- Frequency Analysis
- N-Gram Modeling
- TF-IDF Vectorization
- Vocabulary Control Techniques

---

## How To Run

```bash
python task1_manual_one_hot.py

python task2_sklearn_one_hot.py

python task3_bag_of_words.py

python task4_word_frequency.py

python task5_ngrams.py

python task6_combined_ngrams.py

python task7_tfidf.py

python task8_bow_vs_tfidf.py

python task9_vectorizer_parameters.py

python task10_conceptual_questions.py
```

---

## Conclusion

This assignment successfully demonstrates the core text vectorization techniques used in Natural Language Processing. Through One-Hot Encoding, Bag of Words, N-Grams, and TF-IDF, raw text is transformed into numerical features that can be used by machine learning and deep learning models in later stages of NLP pipelines.