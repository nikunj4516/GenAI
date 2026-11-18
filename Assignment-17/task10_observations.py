print("TASK 10: OBSERVATIONS & INSIGHTS\n")

print("1. Difference Between Basic and Advanced Cleaning")
print("-" * 40)

print("""
Basic Cleaning:
- Converts text to lowercase.
- Removes punctuation.
- Removes numbers.
- Removes extra white spaces.

Advanced Cleaning:
- Removes URLs.
- Removes email addresses.
- Removes HTML tags.
- Removes special characters.
- Removes emojis and other text noise.

Conclusion:
Advanced cleaning provides cleaner and more meaningful text
for NLP applications than basic cleaning alone.
""")

print("\n2. Why Lemmatization is Preferred Over Stemming")
print("-" * 40)

print("""
Stemming:
- Removes word endings using heuristic rules.
- Sometimes produces incomplete or invalid words.

Examples:
running -> run
studies -> studi

Lemmatization:
- Uses vocabulary and linguistic rules.
- Produces meaningful dictionary words.

Examples:
running -> run
studies -> study

Conclusion:
Lemmatization preserves the actual meaning of words and
is usually preferred in modern NLP pipelines.
""")

print("\n3. Importance of Preprocessing in NLP Models")
print("-" * 40)

print("""
Text preprocessing is a critical step in NLP because:

1. Removes unnecessary noise.
2. Improves text consistency.
3. Reduces vocabulary size.
4. Enhances model accuracy.
5. Improves training efficiency.
6. Helps models understand meaningful patterns.

Without preprocessing, NLP models may learn from
irrelevant information and produce poor results.
""")