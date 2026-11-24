"""
PART 2 - Task 7: Length-Based Text Splitter

Use CharacterTextSplitter. It splits on ONE separator (here a line break) and then
merges the pieces until chunk_size characters is reached.

  chunk_size    = 500  -> maximum characters in a chunk
  chunk_overlap = 50   -> characters repeated between consecutive chunks

Run:  python PART2_Text_Splitters/task7_character_splitter.py
"""

import os
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if ROOT not in sys.path:
    sys.path.insert(0, ROOT)

from config import CHUNK_OVERLAP, CHUNK_SIZE  # import first: sets user agent, hides warnings

from langchain_text_splitters import CharacterTextSplitter

from PART2_Text_Splitters.splitter_utils import (
    chunk_stats,
    load_sample_documents,
    overlap_between,
    short_source,
)


def build_character_splitter(chunk_size=CHUNK_SIZE, chunk_overlap=CHUNK_OVERLAP):
    return CharacterTextSplitter(
        separator="\n",
        chunk_size=chunk_size,
        chunk_overlap=chunk_overlap,
        length_function=len,
    )


def main():
    docs = load_sample_documents()
    splitter = build_character_splitter()
    chunks = splitter.split_documents(docs)

    print("=" * 70)
    print("TASK 7: LENGTH-BASED SPLITTER (CharacterTextSplitter)")
    print("=" * 70)
    print(f"Settings: separator='\\n', chunk_size={CHUNK_SIZE}, chunk_overlap={CHUNK_OVERLAP}")
    print("Input documents (notes.txt + 3 PDF pages):", len(docs))
    print("Number of chunks:", len(chunks))

    stats = chunk_stats(chunks, CHUNK_SIZE)
    print("Chunk length  min / avg / max :", stats["min_len"], "/", stats["avg_len"], "/", stats["max_len"])
    print("Chunks longer than chunk_size :", stats["over_limit"])

    print("\nChunks per source file:")
    for name in sorted({short_source(c) for c in chunks}):
        print(f"  {name}: {sum(1 for c in chunks if short_source(c) == name)}")

    print("\nSample chunk #1 (from", short_source(chunks[1]) + ", length", len(chunks[1].page_content), "):")
    print(chunks[1].page_content)

    # ---- show the overlap between two consecutive chunks of the same file ----
    for a, b in zip(chunks, chunks[1:]):
        shared = overlap_between(a.page_content, b.page_content, CHUNK_OVERLAP)
        if shared and short_source(a) == short_source(b):
            print(f"\nOverlap example - the end of one chunk is repeated at the start of the next:")
            print("  shared text:", repr(shared))
            break


if __name__ == "__main__":
    main()
