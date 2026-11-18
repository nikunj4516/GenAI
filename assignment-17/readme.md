# Assignment 17: Text Cleaning, Preprocessing & NLP Pipeline

## Objective

This assignment demonstrates how raw text data is cleaned and preprocessed before being used in NLP and Generative AI applications.

The assignment covers:

- Basic Text Cleaning
- Advanced Text Cleaning
- Stopword Removal
- Tokenization
- Stemming
- Lemmatization
- End-to-End NLP Pipeline

---

## Dataset

Dataset Name:

Product Reviews Dataset (Custom Created)

Source:

Self-Created Dataset

Dataset File:

product_reviews_dataset.csv

Total Records:

25 Product Reviews

The dataset contains various types of noisy text including:

- Uppercase words
- Punctuation
- Numbers
- URLs
- Email Addresses
- Emojis
- Extra Whitespaces
- Slang Words
- Repeated Characters

---

## Tasks

### Task 1

Understanding Raw Text Data

- Load dataset using Pandas
- Display first 5 text samples
- Calculate text length
- Identify common text issues

---

### Task 2

Basic Text Cleaning

Applied:

- Lowercase Conversion
- Punctuation Removal
- Number Removal
- Extra Whitespace Removal

Output Column:

clean_text_basic

---

### Task 3

Advanced Text Cleaning

Applied:

- URL Removal
- Email Removal
- HTML Tag Removal
- Special Character Removal
- Emoji Removal

Output Column:

clean_text_advanced

---

### Task 4

Handling Stopwords

Applied NLTK Stopwords Removal

Output Column:

text_no_stopwords

---

### Task 5

Handling Repeated Characters & Slang

Applied:

- Repeated Character Normalization
- Slang Word Replacement

Examples:

- soooo → so
- superrrrr → super
- u → you
- gr8 → great

---

### Task 6

Tokenization

Implemented:

- Word Tokenization
- Sentence Tokenization

Displayed tokenization results for three review samples.

---

### Task 7

Stemming

Applied:

- Porter Stemmer

Compared:

- Original Words
- Stemmed Words

---

### Task 8

Lemmatization

Applied:

- WordNet Lemmatizer

Compared:

- Stemmed Words
- Lemmatized Words

---

### Task 9

Final NLP Pipeline

Created function:

```python
nlp_preprocess(text)
```

Pipeline includes:

- Lowercasing
- Noise Removal
- Stopword Removal
- Tokenization
- Lemmatization

Output Column:

final_clean_text

---

### Task 10

Observations & Insights

Implemented observations and analysis on:

- Difference between Basic and Advanced Cleaning
- Why Lemmatization is Preferred Over Stemming
- Importance of Preprocessing in NLP Models

File:

```text
task10_observations.py
```

---

## Libraries Used

- pandas
- nltk
- re

---

## Results

This assignment demonstrates:

- Text Cleaning
- Noise Removal
- Stopword Handling
- Tokenization
- Stemming
- Lemmatization
- NLP Preprocessing Pipeline Creation

---

## Observations

### 1. Difference Between Basic and Advanced Cleaning

Basic cleaning removes simple formatting issues such as punctuation, numbers, capital letters, and extra spaces.

Advanced cleaning removes more complex noise such as URLs, email addresses, HTML tags, emojis, and special characters.

Advanced cleaning provides cleaner and more meaningful text for NLP applications.

---

### 2. Why Lemmatization is Preferred Over Stemming

Stemming removes word endings using simple rules and may produce incomplete words.

Examples:

- running → run
- studies → studi

Lemmatization uses linguistic analysis and vocabulary to generate meaningful root words.

Examples:

- running → run
- studies → study

Lemmatization is generally preferred because it preserves the actual meaning of words.

---

### 3. Importance of Preprocessing in NLP Models

Text preprocessing is an essential step in NLP because it:

- Removes unnecessary noise
- Improves text consistency
- Reduces vocabulary size
- Improves model accuracy
- Increases training efficiency
- Helps models focus on meaningful information

Without preprocessing, NLP models may learn from irrelevant or noisy data and produce poor results.

---

## How To Run

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

## Conclusion

This assignment successfully demonstrates a complete NLP preprocessing workflow starting from raw text and ending with model-ready cleaned text. The project covers basic text cleaning, advanced noise removal, stopword handling, tokenization, stemming, lemmatization, and an end-to-end NLP pipeline using Python, Pandas, NLTK, and Regular Expressions. 