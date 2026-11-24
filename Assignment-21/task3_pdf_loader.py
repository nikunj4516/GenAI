"""
PART 1 - Task 3: PDF Loader

Use PyPDFLoader to load the PDF. It returns one Document per PAGE.
Prints the total number of pages and a sample page.

Run:  python PART1_Document_Loaders/task3_pdf_loader.py
"""

import os
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if ROOT not in sys.path:
    sys.path.insert(0, ROOT)

from config import PDF_FILE  # import first: sets user agent, hides warnings

from langchain_community.document_loaders import PyPDFLoader



def load_pdf():
    """Load company_handbook.pdf -> one Document per page."""
    loader = PyPDFLoader(PDF_FILE)
    return loader.load()


def main():
    pages = load_pdf()

    print("=" * 70)
    print("TASK 3: PDF LOADER (PyPDFLoader)")
    print("=" * 70)
    print("File        :", PDF_FILE)
    print("Total pages :", len(pages))

    print("\nSample page content (page 1, first 400 characters):")
    print(pages[0].page_content[:400])
    meta = pages[0].metadata
    print("\nMetadata of page 1:", {k: meta[k] for k in ("source", "page", "page_label", "total_pages") if k in meta})

    print("\nCharacters per page:")
    for p in pages:
        print(f"  page {p.metadata['page'] + 1}: {len(p.page_content)} characters")


if __name__ == "__main__":
    main()
