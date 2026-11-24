"""
PART 1 - Task 1: Text Loader

Use TextLoader to load the .txt file and print:
  - number of documents loaded
  - page content preview
  - metadata

Run:  python PART1_Document_Loaders/task1_text_loader.py
"""

import os
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if ROOT not in sys.path:
    sys.path.insert(0, ROOT)

from config import TXT_FILE  # import first: sets user agent, hides warnings

from langchain_community.document_loaders import TextLoader



def load_text():
    """Load notes.txt -> list of Document objects (one Document per file)."""
    loader = TextLoader(TXT_FILE, encoding="utf-8")
    return loader.load()


def main():
    docs = load_text()

    print("=" * 70)
    print("TASK 1: TEXT LOADER (TextLoader)")
    print("=" * 70)
    print("File                       :", TXT_FILE)
    print("Number of documents loaded :", len(docs))
    print("Total characters           :", len(docs[0].page_content))
    print("\nPage content preview (first 300 characters):")
    print(docs[0].page_content[:300])
    print("\nMetadata:", docs[0].metadata)


if __name__ == "__main__":
    main()
