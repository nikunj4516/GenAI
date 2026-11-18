import pandas as pd
import re

# Load previous output file
df = pd.read_csv("task4_output.csv")

# Slang dictionary
slang_dict = {
    "u": "you",
    "gr8": "great",
    "omg": "oh my god"
}


def normalize_text(text):

    text = str(text).lower()

    # Normalize repeated characters
    # soooo -> so
    # superrrrr -> super

    text = re.sub(r"(.)\1{2,}", r"\1", text)

    words = text.split()

    normalized_words = []

    for word in words:

        if word in slang_dict:
            normalized_words.append(
                slang_dict[word]
            )
        else:
            normalized_words.append(word)

    return " ".join(normalized_words)


# Apply normalization
df["normalized_text"] = df[
    "text_no_stopwords"
].apply(normalize_text)

# Display results
print("\nSLANG NORMALIZATION OUTPUT\n")

print(
    df[
        [
            "text_no_stopwords",
            "normalized_text"
        ]
    ].head(10)
)

# Save output
df.to_csv(
    "task5_output.csv",
    index=False
)

print("\nTask 5 Completed Successfully")