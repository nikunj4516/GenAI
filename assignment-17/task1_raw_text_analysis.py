import pandas as pd

# Load dataset
df = pd.read_csv("product_reviews_dataset.csv")

print("First 5 Text Samples:\n")
print(df["text"].head())

# Text Length
df["text_length"] = df["text"].astype(str).apply(len)

print("\nText Lengths:\n")
print(df[["id", "text_length"]])

print("\nCommon Issues Found:")
print("- Uppercase / Lowercase mismatch")
print("- Punctuation")
print("- Numbers")
print("- URLs")
print("- Emails")
print("- Emojis")
print("- Extra Whitespaces")
print("- Slang words")
print("- Repeated characters")