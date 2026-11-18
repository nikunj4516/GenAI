import pandas as pd
import re

df = pd.read_csv("product_reviews_dataset.csv")

def clean_text_advanced(text):

    text = str(text)

    # URLs
    text = re.sub(r'http\S+|www\S+', '', text)

    # Emails
    text = re.sub(r'\S+@\S+', '', text)

    # HTML Tags
    text = re.sub(r'<.*?>', '', text)

    # Emojis / Non ASCII
    text = re.sub(r'[^\x00-\x7F]+', '', text)

    # Special Characters
    text = re.sub(r'[^a-zA-Z\s]', '', text)

    text = text.lower()

    text = re.sub(r'\s+', ' ', text).strip()

    return text

df["clean_text_advanced"] = df["text"].apply(clean_text_advanced)

print(df[["text", "clean_text_advanced"]].head())

df.to_csv("task3_output.csv", index=False)