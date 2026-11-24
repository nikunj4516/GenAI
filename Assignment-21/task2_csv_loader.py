"""
PART 1 - Task 2: CSV Loader

Use CSVLoader to load the .csv file. Every row of the CSV becomes one Document.
We use source_column="title" so the metadata 'source' shows the movie title.

Run:  python PART1_Document_Loaders/task2_csv_loader.py
"""

import os
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if ROOT not in sys.path:
    sys.path.insert(0, ROOT)

from config import CSV_FILE  # import first: sets user agent, hides warnings

from langchain_community.document_loaders import CSVLoader



def load_csv():
    """Load Movie_recommendation.csv -> one Document per row."""
    loader = CSVLoader(file_path=CSV_FILE, source_column="title", encoding="utf-8")
    return loader.load()


def main():
    docs = load_csv()

    print("=" * 70)
    print("TASK 2: CSV LOADER (CSVLoader)")
    print("=" * 70)
    print("File                       :", CSV_FILE)
    print("Rows converted to documents:", len(docs))

    print("\nSample document #0 (first 600 characters):")
    print(docs[0].page_content[:600])
    print("\nMetadata of document #0:", docs[0].metadata)

    print("\nSample sources (movie titles) of the first 5 documents:")
    for d in docs[:5]:
        print("  -", d.metadata["source"], "| row", d.metadata["row"])


if __name__ == "__main__":
    main()
