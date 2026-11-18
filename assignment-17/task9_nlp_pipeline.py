import pandas as pd
import re
import nltk

from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.stem import WordNetLemmatizer

nltk.download("stopwords")
nltk.download("punkt")
nltk.download("wordnet")

df = pd.read_csv("product_reviews_dataset.csv")

stop_words = set(stopwords.words("english"))

lemmatizer = WordNetLemmatizer()

def nlp_preprocess(text):

    text = str(text).lower()

    # Remove URLs
    text = re.sub(r'http\S+|www\S+', '', text)

    # Remove Emails
    text = re.sub(r'\S+@\S+', '', text)

    # Remove HTML
    text = re.sub(r'<.*?>', '', text)

    # Remove Emoji
    text = re.sub(r'[^\x00-\x7F]+', '', text)

    # Remove Special Characters
    text = re.sub(r'[^a-zA-Z\s]', '', text)

    # Remove Extra Spaces
    text = re.sub(r'\s+', ' ', text).strip()

    tokens = word_tokenize(text)

    tokens = [
        word
        for word in tokens
        if word not in stop_words
    ]

    tokens = [
        lemmatizer.lemmatize(word)
        for word in tokens
    ]

    return " ".join(tokens)

df["final_clean_text"] = df["text"].apply(
    nlp_preprocess
)

print(df[["text",
          "final_clean_text"]].head())

df.to_csv(
    "final_preprocessed_dataset.csv",
    index=False
)

print("\nPipeline Completed Successfully")