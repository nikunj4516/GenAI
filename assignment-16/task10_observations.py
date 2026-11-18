print("TASK 10 : OBSERVATIONS & INSIGHTS\n")

print("1. Difference Between Basic and Advanced Cleaning")
print("-" * 60)

print("""
Basic Cleaning:
- Converts text to lowercase.
- Removes punctuation.
- Removes numbers.
- Removes extra spaces.

Advanced Cleaning:
- Removes URLs.
- Removes email addresses.
- Removes HTML tags.
- Removes emojis.
- Removes special characters.

Conclusion:
Advanced cleaning removes more noise and makes text
better suited for NLP tasks.
""")

print("\n2. Why Lemmatization is Preferred Over Stemming")
print("-" * 60)

print("""
Stemming:
- Applies simple rules.
- May generate incomplete words.

Examples:
running -> run
studies -> studies

Lemmatization:
- Uses vocabulary and linguistic rules.
- Produces meaningful words.

Examples:
running -> run
studies -> study

Conclusion:
Lemmatization preserves actual word meaning and
is generally preferred in NLP applications.
""")

print("\n3. Importance of Preprocessing in NLP Models")
print("-" * 60)

print("""
Text preprocessing helps:

1. Remove unnecessary noise.
2. Improve text consistency.
3. Reduce vocabulary size.
4. Improve model accuracy.
5. Improve training efficiency.
6. Focus on meaningful information.

Conclusion:
Proper preprocessing is one of the most important
steps in any NLP pipeline.
""")

print("\nEnd of Task 10")