# Assignment 19 - Word2Vec Text Embeddings

## Objective

The objective of this assignment is to understand Word Embeddings and Word2Vec models used in Natural Language Processing (NLP).

Traditional vectorization methods such as Bag of Words (BoW) and TF-IDF represent words as independent features and fail to capture semantic meaning. Word2Vec overcomes this limitation by learning dense vector representations of words.

This assignment covers:

- Word Embeddings
- Word2Vec Overview
- CBOW Technique
- Skip-Gram Technique
- Neural Network Intuition
- Training Word2Vec on Custom Data
- Word Similarity Analysis
- Vector Arithmetic
- Embedding Visualization
- Observations and Limitations

---

## Technologies Used

- Python
- Pandas
- NumPy
- NLTK
- Gensim
- Scikit-Learn
- Matplotlib

---

## Dataset Used

Dataset: `product_reviews_dataset.csv`

The dataset contains customer product reviews related to:

- Mobile Phones
- Laptops
- Headphones
- Product Quality
- Battery Performance
- Customer Service
- Delivery Experience

The dataset is preprocessed before training the Word2Vec model.

---

## Project Structure

```text
Assignment19_Word2Vec/

│
├── product_reviews_dataset.csv
├── task1_embeddings_concepts.md
├── task2_word2vec_overview.md
├── task3_cbow_skipgram.md
├── task4_neural_network_intuition.md
├── task5_prepare_text.py
├── task6_train_cbow.py
├── task7_train_skipgram.py
├── task8_similarity_operations.py
├── task9_visualization.py
├── task10_observations.md
│
└── README.md
```

---

## Installation

Install required libraries:

```bash
pip install pandas numpy nltk gensim matplotlib scikit-learn
```

Download NLTK resources:

```python
import nltk

nltk.download("punkt")
nltk.download("stopwords")
```

---

## Tasks Performed

### Task 1

Understanding Word Embeddings

- Definition of Word Embeddings
- Issues with One-Hot Encoding
- Issues with Bag of Words
- Advantages of Semantic Representations

### Task 2

Word2Vec Overview

- Word2Vec Introduction
- Predictive Learning Approach
- Vocabulary
- Context Window
- Embedding Dimension

### Task 3

Word2Vec Techniques

- CBOW
- Skip-Gram
- Practical Use Cases
- Technique Comparison

### Task 4

Neural Network Intuition

- Input Layer
- Hidden Layer
- Output Layer
- Embedding Matrix Learning

### Task 5

Text Preparation

- Text Cleaning
- Tokenization
- Creating List of Lists
- Preparing Corpus for Word2Vec

### Task 6

CBOW Model Training

Parameters:

```python
vector_size=100
window=5
min_count=1
sg=0
```

Outputs:

- Vocabulary Size
- Sample Embedding Vector

### Task 7

Skip-Gram Model Training

Parameters:

```python
vector_size=100
window=5
min_count=1
sg=1
```

Comparison:

- Training Time
- Similar Words Output

### Task 8

Word Similarity & Vector Operations

Performed:

- Most Similar Words
- Cosine Similarity
- Embedding Exploration
- Vector Arithmetic

Example:

```python
good + quality - worst
```

### Task 9

Word Embedding Visualization

Techniques Used:

- PCA
- 2D Visualization
- Cluster Inspection

Outputs:

- Scatter Plot
- Nearby Word Clusters

### Task 10

Observations & Limitations

Covered:

- Difference between CBOW and Skip-Gram
- Advantages of Word2Vec over TF-IDF
- Limitations of Word2Vec
- Importance of Context in Modern NLP
- Introduction to Contextual Embeddings (BERT, GPT)

---

## How To Run

### Task 5

```bash
python task5_prepare_text.py
```

### Task 6

```bash
python task6_train_cbow.py
```

### Task 7

```bash
python task7_train_skipgram.py
```

### Task 8

```bash
python task8_similarity_operations.py
```

### Task 9

```bash
python task9_visualization.py
```

---

## Key Findings

### CBOW

- Faster training
- Suitable for larger datasets
- Works well for frequent words

### Skip-Gram

- Better semantic understanding
- Better for rare words
- More accurate on smaller datasets

### Word2Vec Advantages

- Dense vector representation
- Captures semantic meaning
- Learns relationships among words
- Enables similarity calculations

### Word2Vec Limitations

- Static embeddings
- One vector per word
- Cannot fully capture context
- Limited handling of unseen words

### Modern NLP Perspective

Word2Vec assigns a single embedding to a word regardless of context.

Modern Transformer models such as:

- BERT
- GPT
- RoBERTa

generate context-aware embeddings and provide better language understanding.

---

## Conclusion

Word2Vec is one of the most important breakthroughs in NLP. It transforms words into meaningful dense vectors and captures semantic relationships between words. Through CBOW and Skip-Gram architectures, Word2Vec learns contextual information from text data and forms the foundation for many modern language representation techniques.