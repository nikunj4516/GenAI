import pandas as pd

df = pd.read_csv("product_reviews_dataset.csv")

print("FIRST 5 TEXT SAMPLES\n")
print(df["text"].head())

df["text_length"] = df["text"].astype(str).apply(len)

print("\nTEXT LENGTHS\n")
print(df[["id", "text_length"]])

print("\nCOMMON ISSUES IDENTIFIED")
print("- Uppercase and lowercase mismatch")
print("- Punctuation")
print("- Numbers")
print("- URLs")
print("- Email addresses")
print("- Emojis")
print("- Extra whitespaces")
print("- Slang words")
print("- Repeated characters")