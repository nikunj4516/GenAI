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

stop_words = set(
    stopwords.words("english")
)

lemmatizer = WordNetLemmatizer()

def nlp_preprocess(text):

    text = str(text).lower()

    # Remove URLs
    text = re.sub(r"http\S+|www\S+", "", text)

    # Remove Emails
    text = re.sub(r"\S+@\S+", "", text)

    # Remove HTML
    text = re.sub(r"<.*?>", "", text)

    # Remove Emojis
    text = re.sub(r"[^\x00-\x7F]+", "", text)

    # Remove Special Characters
    text = re.sub(r"[^a-zA-Z\s]", "", text)

    # Remove Extra Spaces
    text = re.sub(r"\s+", " ", text)

    text = text.strip()

    tokens = word_tokenize(text)

    filtered_tokens = []

    for word in tokens:

        if word not in stop_words:

            filtered_tokens.append(
                lemmatizer.lemmatize(word)
            )

    return " ".join(filtered_tokens)

df["final_clean_text"] = df["text"].apply(
    nlp_preprocess
)

print("TASK 9 : NLP PIPELINE\n")

print(
    df[
        [
            "text",
            "final_clean_text"
        ]
    ].head()
)

df.to_csv(
    "final_preprocessed_dataset.csv",
    index=False
)

print("\nFinal dataset saved successfully.")