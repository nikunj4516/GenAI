"""
PART 1 - Task 4: Directory Loader

Use DirectoryLoader to load all files inside data/.
A suitable loader class is applied to each file type:
    *.txt -> TextLoader
    *.csv -> CSVLoader
    *.pdf -> PyPDFLoader

Then we VERIFY that every document type was loaded correctly by comparing the
DirectoryLoader result with loading each file directly.

Run:  python PART1_Document_Loaders/task4_directory_loader.py
"""

import os
import sys
from collections import Counter

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if ROOT not in sys.path:
    sys.path.insert(0, ROOT)

from config import CSV_FILE, DATA_DIR, PDF_FILE, TXT_FILE  # import first: sets user agent, hides warnings

from langchain_community.document_loaders import (
    CSVLoader,
    DirectoryLoader,
    PyPDFLoader,
    TextLoader,
)


# glob pattern -> (loader class, loader keyword arguments)
LOADER_MAPPING = {
    "**/*.txt": (TextLoader, {"encoding": "utf-8"}),
    "**/*.csv": (CSVLoader, {"encoding": "utf-8", "source_column": "title"}),
    "**/*.pdf": (PyPDFLoader, {}),
}


def load_directory(directory=DATA_DIR):
    """Load every supported file in a directory using the matching loader class."""
    documents = []
    for pattern, (loader_cls, loader_kwargs) in LOADER_MAPPING.items():
        loader = DirectoryLoader(
            directory,
            glob=pattern,
            loader_cls=loader_cls,
            loader_kwargs=loader_kwargs,
        )
        documents.extend(loader.load())
    return documents


def file_type_of(doc):
    """Detect the file type of a document from its metadata."""
    source = str(doc.metadata.get("source", ""))
    if "page" in doc.metadata:          # only PDF documents have a page number
        return "pdf"
    if "row" in doc.metadata:           # only CSV documents have a row number
        return "csv"
    return os.path.splitext(source)[1].lstrip(".") or "unknown"


def main():
    print("=" * 70)
    print("TASK 4: DIRECTORY LOADER (DirectoryLoader)")
    print("=" * 70)
    print("Directory:", DATA_DIR)
    print("Files inside:", sorted(os.listdir(DATA_DIR)))

    documents = load_directory()
    counts = Counter(file_type_of(d) for d in documents)

    print("\nTotal documents loaded:", len(documents))
    print("Documents per file type:", dict(counts))

    # ---- Verification: compare with loading each file directly ----
    expected = {
        "txt": len(TextLoader(TXT_FILE, encoding="utf-8").load()),
        "csv": len(CSVLoader(CSV_FILE, source_column="title", encoding="utf-8").load()),
        "pdf": len(PyPDFLoader(PDF_FILE).load()),
    }
    print("\nVerification (DirectoryLoader vs direct loading):")
    all_ok = True
    for kind, expected_count in expected.items():
        got = counts.get(kind, 0)
        ok = got == expected_count
        all_ok = all_ok and ok
        print(f"  {kind}: expected {expected_count}, got {got} -> {'OK' if ok else 'MISMATCH'}")

    print("\nOne sample document from each type:")
    shown = set()
    for d in documents:
        kind = file_type_of(d)
        if kind not in shown:
            shown.add(kind)
            print(f"\n[{kind}] metadata: {d.metadata}")
            print("      content :", d.page_content[:150].replace("\n", " "))

    print("\nRESULT:", "all document types loaded correctly" if all_ok else "CHECK FAILED")


if __name__ == "__main__":
    main()
