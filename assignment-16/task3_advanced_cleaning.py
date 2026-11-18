import pandas as pd
import re

df = pd.read_csv("task2_output.csv")

def clean_text_advanced(text):

    text = str(text)

    # Remove URLs
    text = re.sub(r"http\S+|www\S+", "", text)

    # Remove Emails
    text = re.sub(r"\S+@\S+", "", text)

    # Remove HTML Tags
    text = re.sub(r"<.*?>", "", text)

    # Remove Emojis / Non ASCII Characters
    text = re.sub(r"[^\x00-\x7F]+", "", text)

    # Remove Special Characters
    text = re.sub(r"[^a-zA-Z\s]", "", text)

    text = text.lower()

    text = re.sub(r"\s+", " ", text).strip()

    return text

df["clean_text_advanced"] = df["text"].apply(
    clean_text_advanced
)

print(df[["text", "clean_text_advanced"]].head())

df.to_csv("task3_output.csv", index=False)

print("\nAdvanced cleaning completed successfully.")