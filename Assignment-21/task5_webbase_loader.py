"""
PART 1 - Task 5: WebBase Loader

Use WebBaseLoader to load the text of a public webpage (documentation, blog, help page).
Only headings and paragraphs are kept, so menus and scripts are not included.
The first 500 characters of the extracted text are printed.

NOTE: this task needs an internet connection.

Run:  python PART1_Document_Loaders/task5_webbase_loader.py
      python PART1_Document_Loaders/task5_webbase_loader.py https://your-page-url
"""

import os
import re
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if ROOT not in sys.path:
    sys.path.insert(0, ROOT)

from config import WEB_URL  # import first: sets user agent, hides warnings

import bs4
from langchain_community.document_loaders import WebBaseLoader



def load_webpage(url=WEB_URL):
    """Load a webpage and keep only its headings and paragraphs."""
    loader = WebBaseLoader(
        web_paths=[url],
        bs_kwargs={"parse_only": bs4.SoupStrainer(["h1", "h2", "h3", "p"])},
        bs_get_text_kwargs={"separator": " ", "strip": True},
    )
    return loader.load()


def main():
    url = sys.argv[1] if len(sys.argv) > 1 else WEB_URL

    print("=" * 70)
    print("TASK 5: WEBBASE LOADER (WebBaseLoader)")
    print("=" * 70)
    print("URL:", url)

    try:
        docs = load_webpage(url)
    except Exception as error:  # no internet, blocked site, wrong URL ...
        print("\nCould not load the page:", type(error).__name__)
        print("Check your internet connection or try another public URL.")
        sys.exit(1)

    text = re.sub(r"\s+", " ", docs[0].page_content).strip()
    print("\nNumber of documents loaded :", len(docs))
    print("Total characters extracted :", len(text))
    print("\nFirst 500 characters:")
    print(text[:500])
    print("\nMetadata:", docs[0].metadata)


if __name__ == "__main__":
    main()
