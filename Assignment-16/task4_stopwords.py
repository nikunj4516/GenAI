import pandas as pd
import nltk
from nltk.corpus import stopwords

# Download stopwords
nltk.download('stopwords')

# Load data
df = pd.read_csv("task3_output.csv")

# Load English stopwords
stop_words = set(stopwords.words('english'))

def remove_stopwords(text):
    text = str(text)

    words = text.split()

    filtered_words = []

    for word in words:
        if word not in stop_words:
            filtered_words.append(word)

    return " ".join(filtered_words)

# Create new column
df["text_no_stopwords"] = df["clean_text_advanced"].apply(
    remove_stopwords
)

# Display result
print("\nStopwords Removal Output:\n")

print(
    df[
        [
            "clean_text_advanced",
            "text_no_stopwords"
        ]
    ].head()
)

# Save file
df.to_csv(
    "task4_output.csv",
    index=False
)

print("\nTask 4 Completed Successfully")