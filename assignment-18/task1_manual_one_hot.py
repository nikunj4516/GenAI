import pandas as pd

df = pd.read_csv("final_preprocessed_dataset.csv")

sentences = df["final_clean_text"].head(5).tolist()

# Vocabulary
vocabulary = sorted(set(
    word
    for sentence in sentences
    for word in sentence.split()
))

print("Vocabulary:\n")
print(vocabulary)

print("\nOne Hot Vectors:\n")

for sentence in sentences:

    vector = [
        1 if word in sentence.split() else 0
        for word in vocabulary
    ]

    print(f"Sentence: {sentence}")
    print(vector)
    print()