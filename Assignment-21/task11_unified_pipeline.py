"""
PART 3 - Task 11: Unified Preprocessing Pipeline

    def load_and_split_documents(path_or_url):
        # loads documents   -> the right loader is chosen automatically
        # splits them       -> RecursiveCharacterTextSplitter
        # returns chunks

Works for:
  - a local directory   (every .txt / .md / .csv / .pdf file inside it)
  - a single local file (.txt / .md / .csv / .pdf)
  - a web URL           (http:// or https://)

Run:  python PART3_Mini_Integration/task11_unified_pipeline.py
      python PART3_Mini_Integration/task11_unified_pipeline.py <folder-or-url> [<folder-or-url> ...]
"""

import os
import sys
from collections import Counter

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if ROOT not in sys.path:
    sys.path.insert(0, ROOT)

from config import CHUNK_OVERLAP, CHUNK_SIZE, DATA_DIR, WEB_URL  # import first: sets user agent

import bs4
from langchain_community.document_loaders import (
    CSVLoader,
    DirectoryLoader,
    PyPDFLoader,
    TextLoader,
    WebBaseLoader,
)
from langchain_text_splitters import RecursiveCharacterTextSplitter

# file extension -> (loader class, loader keyword arguments)
LOADER_BY_EXTENSION = {
    ".txt": (TextLoader, {"encoding": "utf-8"}),
    ".md": (TextLoader, {"encoding": "utf-8"}),
    ".csv": (CSVLoader, {"encoding": "utf-8"}),
    ".pdf": (PyPDFLoader, {}),
}


def is_url(value):
    return str(value).lower().startswith(("http://", "https://"))


def load_documents(path_or_url):
    """Load documents from a URL, a directory or a single file."""
    # ---- web page ----
    if is_url(path_or_url):
        loader = WebBaseLoader(
            web_paths=[path_or_url],
            bs_kwargs={"parse_only": bs4.SoupStrainer(["h1", "h2", "h3", "p"])},
            bs_get_text_kwargs={"separator": " ", "strip": True},
        )
        return loader.load()

    # ---- local directory ----
    if os.path.isdir(path_or_url):
        documents = []
        for extension, (loader_cls, loader_kwargs) in LOADER_BY_EXTENSION.items():
            loader = DirectoryLoader(
                path_or_url,
                glob=f"**/*{extension}",
                loader_cls=loader_cls,
                loader_kwargs=loader_kwargs,
            )
            documents.extend(loader.load())
        return documents

    # ---- single local file ----
    if os.path.isfile(path_or_url):
        extension = os.path.splitext(path_or_url)[1].lower()
        if extension not in LOADER_BY_EXTENSION:
            raise ValueError(
                f"Unsupported file type '{extension}'. Supported: {sorted(LOADER_BY_EXTENSION)}"
            )
        loader_cls, loader_kwargs = LOADER_BY_EXTENSION[extension]
        return loader_cls(path_or_url, **loader_kwargs).load()

    raise FileNotFoundError(f"'{path_or_url}' is not an existing folder, file or http(s) URL.")


def load_and_split_documents(path_or_url, chunk_size=CHUNK_SIZE, chunk_overlap=CHUNK_OVERLAP):
    """Load documents from a folder, file or URL, split them and return the chunks."""
    documents = load_documents(path_or_url)                 # 1. load
    splitter = RecursiveCharacterTextSplitter(              # 2. split
        chunk_size=chunk_size,
        chunk_overlap=chunk_overlap,
    )
    return splitter.split_documents(documents)              # 3. return chunks


def source_type(chunk):
    """Detect where a chunk came from (pdf / csv / txt / md / web)."""
    if "page" in chunk.metadata:
        return "pdf"
    if "row" in chunk.metadata:
        return "csv"
    source = str(chunk.metadata.get("source", ""))
    if is_url(source):
        return "web"
    return os.path.splitext(source)[1].lstrip(".") or "unknown"


def report(label, target):
    """Run the pipeline on one target and print a summary."""
    print("\n" + "-" * 70)
    print(f"{label}: {target}")
    print("-" * 70)
    try:
        chunks = load_and_split_documents(target)
    except Exception as error:   # no internet, wrong path, unsupported file ...
        print(f"Could not process this target -> {type(error).__name__}: {error}")
        return None

    lengths = [len(c.page_content) for c in chunks]
    print("Number of chunks      :", len(chunks))
    if chunks:
        print("Chunk length min/avg/max:", min(lengths), "/", round(sum(lengths) / len(lengths), 1), "/", max(lengths))
        print("Chunks per source type:", dict(Counter(source_type(c) for c in chunks)))
        sample = next((c for c in chunks if source_type(c) != "csv"), chunks[0])
        print("\nSample chunk (metadata):", {k: v for k, v in sample.metadata.items() if k in ("source", "page", "row")})
        print("Sample chunk (content) :", sample.page_content[:300].replace("\n", " "))
    return chunks


def main():
    print("=" * 70)
    print("TASK 11: UNIFIED PREPROCESSING PIPELINE")
    print("=" * 70)
    print(f"load_and_split_documents(path_or_url)  [chunk_size={CHUNK_SIZE}, chunk_overlap={CHUNK_OVERLAP}]")

    targets = sys.argv[1:]
    if targets:
        for target in targets:
            report("Target", target)
        return

    report("1) Local directory", DATA_DIR)
    report("2) Web URL", WEB_URL)

    # Extra checks of the error handling
    print("\n" + "-" * 70)
    print("3) Error handling")
    print("-" * 70)
    for bad in (os.path.join(DATA_DIR, "missing_folder"), os.path.join(ROOT, "config.py")):
        try:
            load_and_split_documents(bad)
        except (FileNotFoundError, ValueError) as error:
            print(f"{type(error).__name__}: {error}")


if __name__ == "__main__":
    main()
