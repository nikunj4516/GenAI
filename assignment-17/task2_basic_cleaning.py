import pandas as pd
import re

df = pd.read_csv("product_reviews_dataset.csv")

def clean_text_basic(text):

    text = str(text).lower()

    text = re.sub(r'[^\w\s]', '', text)

    text = re.sub(r'\d+', '', text)

    text = re.sub(r'\s+', ' ', text).strip()

    return text

df["clean_text_basic"] = df["text"].apply(clean_text_basic)

print(df[["text", "clean_text_basic"]].head())

df.to_csv("task2_output.csv", index=False)