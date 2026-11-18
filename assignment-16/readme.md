# Assignment 16: NLP Text Cleaning, Preprocessing & Pipeline

## Objective

This assignment demonstrates the complete Natural Language Processing (NLP) preprocessing workflow required before building NLP or Generative AI models.

The objective is to convert raw text data into clean and structured text by applying various preprocessing techniques such as cleaning, stopword removal, tokenization, stemming, lemmatization, and a complete NLP pipeline.

---

# Dataset Information

## Dataset Name

Product Reviews Dataset (Custom Created)

## Source

Self-Created Dataset

## Dataset File

product_reviews_dataset.csv

## Number of Records

25 Product Reviews

The dataset contains different types of noisy text including:

- Uppercase and lowercase text
- Punctuation marks
- Numbers
- URLs
- Email addresses
- HTML tags
- Emojis
- Extra whitespaces
- Slang words
- Repeated characters

---

# Libraries Used

- pandas
- nltk
- re

---

# Task 1: Understanding Raw Text Data

### Objectives

- Load dataset using Pandas
- Display the first five text samples
- Calculate text lengths
- Identify common text issues

### Common Issues Identified

- Uppercase/Lowercase inconsistency
- Punctuation marks
- Numbers
- Extra spaces
- URLs
- Email addresses
- Emojis
- Slang words
- Repeated characters

---

# Task 2: Basic Text Cleaning

Created:

```python
clean_text_basic
```

Applied the following preprocessing steps:

- Convert text to lowercase
- Remove punctuation
- Remove numbers
- Remove extra whitespaces

### Output Column

```python
clean_text_basic
```

---

# Task 3: Advanced Text Cleaning

Created:

```python
clean_text_advanced
```

Applied:

- URL removal
- Email removal
- HTML tag removal
- Special character removal
- Emoji removal

### Output Column

```python
clean_text_advanced
```

---

# Task 4: Stopword Removal

Used NLTK stopwords and removed common English stopwords from cleaned text.

### Output Column

```python
text_no_stopwords
```

---

# Task 5: Repeated Character Handling & Slang Normalization

Applied the following normalizations:

### Repeated Characters

Examples:

```text
soooo → so
superrrrr → super
```

### Slang Words

Examples:

```text
u     → you
gr8   → great
omg   → oh my god
```

---

# Task 6: Tokenization

Implemented:

### Word Tokenization

Splits text into individual words.

### Sentence Tokenization

Splits text into individual sentences.

Tokenization results were displayed for at least three samples.

---

# Task 7: Stemming

Used:

```python
PorterStemmer
```

Comparison displayed:

| Original Word | Stemmed Word |
|--------------|-------------|
| running | run |
| studies | studi |

---

# Task 8: Lemmatization

Used:

```python
WordNetLemmatizer
```

Comparison displayed:

| Original | Stemmed | Lemmatized |
|----------|----------|------------|
| running | run | run |
| studies | studi | study |

---

# Task 9: NLP Pipeline Creation

Created a complete NLP preprocessing function:

```python
def nlp_preprocess(text):
```

The function performs:

1. Lowercasing
2. Noise Removal
3. Stopword Removal
4. Tokenization
5. Lemmatization

### Output Column

```python
final_clean_text
```

The preprocessing pipeline was applied to the full dataset.

---

# Task 10: Observations & Insights

Implemented observations regarding:

### 1. Difference Between Basic and Advanced Cleaning

Basic cleaning focuses on punctuation, numbers, and casing.

Advanced cleaning removes URLs, emails, HTML tags, emojis, and other noise.

Advanced cleaning produces cleaner and more meaningful text for NLP applications.

### 2. Why Lemmatization is Preferred Over Stemming

Stemming often generates incomplete root words.

Example:

```text
studies → studi
```

Lemmatization generates meaningful dictionary words.

Example:

```text
studies → study
```

Therefore, lemmatization preserves semantic meaning better than stemming.

### 3. Importance of Preprocessing in NLP

Text preprocessing:

- Removes unwanted noise
- Improves consistency
- Reduces vocabulary size
- Improves model performance
- Improves training efficiency
- Helps models focus on meaningful information

---

# Results

This assignment successfully demonstrates:

- Basic Text Cleaning
- Advanced Text Cleaning
- Noise Removal
- Stopword Removal
- Tokenization
- Stemming
- Lemmatization
- Slang Normalization
- NLP Pipeline Creation

---

# How To Run

```bash
python task1_raw_text_analysis.py

python task2_basic_cleaning.py

python task3_advanced_cleaning.py

python task4_stopwords.py

python task5_slang_normalization.py

python task6_tokenization.py

python task7_stemming.py

python task8_lemmatization.py

python task9_nlp_pipeline.py

python task10_observations.py
```

---

# Conclusion

This assignment demonstrates a complete NLP preprocessing workflow. Raw text was cleaned, normalized, tokenized, stemmed, lemmatized, and processed through a reusable NLP pipeline to generate model-ready text. These preprocessing techniques are essential before performing feature extraction, machine learning, deep learning, or Generative AI tasks.