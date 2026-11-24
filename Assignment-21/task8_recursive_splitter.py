"""
PART 2 - Task 8: Text Structure-Based Splitter

Use RecursiveCharacterTextSplitter and compare it with the length-based
CharacterTextSplitter from Task 7 on the SAME documents.

How RecursiveCharacterTextSplitter respects text structure
----------------------------------------------------------
It tries a list of separators in order of importance:

    1. "\\n\\n"  paragraph break  -> try to keep whole paragraphs together
    2. "\\n"    line break
    3. " "      space             -> split between words (never inside a word)
    4. ""      single character  -> last resort

It first tries to cut at paragraph breaks. Only if a piece is still larger than
chunk_size does it go down to the next separator (lines, then words). Because it
always prefers the biggest natural boundary, chunks usually contain complete
paragraphs and complete sentences instead of being cut at an arbitrary position.

Run:  python PART2_Text_Splitters/task8_recursive_splitter.py
"""

import logging
import os
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if ROOT not in sys.path:
    sys.path.insert(0, ROOT)

from config import CHUNK_OVERLAP, CHUNK_SIZE  # import first: sets user agent, hides warnings

from langchain_text_splitters import RecursiveCharacterTextSplitter

from PART2_Text_Splitters.splitter_utils import (
    chunk_stats,
    load_sample_documents,
    short_source,
)
from PART2_Text_Splitters.task7_character_splitter import build_character_splitter


def build_recursive_splitter(chunk_size=CHUNK_SIZE, chunk_overlap=CHUNK_OVERLAP):
    return RecursiveCharacterTextSplitter(
        separators=["\n\n", "\n", " ", ""],
        chunk_size=chunk_size,
        chunk_overlap=chunk_overlap,
        length_function=len,
    )


def compare(docs, chunk_size, chunk_overlap):
    """Split the same documents with both splitters and print a comparison table."""
    length_chunks = build_character_splitter(chunk_size, chunk_overlap).split_documents(docs)
    recursive_chunks = build_recursive_splitter(chunk_size, chunk_overlap).split_documents(docs)

    a = chunk_stats(length_chunks, chunk_size)
    b = chunk_stats(recursive_chunks, chunk_size)

    print(f"\nCOMPARISON with chunk_size={chunk_size}, chunk_overlap={chunk_overlap}")
    print(f"{'Metric':<34}{'CharacterTextSplitter':>24}{'Recursive splitter':>22}")
    print("-" * 80)
    rows = [
        ("Number of chunks", "chunks"),
        ("Shortest chunk (chars)", "min_len"),
        ("Average chunk (chars)", "avg_len"),
        ("Longest chunk (chars)", "max_len"),
        ("Chunks over chunk_size", "over_limit"),
    ]
    for label, key in rows:
        print(f"{label:<34}{a[key]:>24}{b[key]:>22}")
    return length_chunks, recursive_chunks, a, b


def main():
    # Silence LangChain's "Created a chunk of size X, which is longer than ..." log lines;
    # the same information is printed in the table below ("Chunks over chunk_size").
    logging.getLogger("langchain_text_splitters.base").setLevel(logging.ERROR)

    docs = load_sample_documents()

    print("=" * 70)
    print("TASK 8: STRUCTURE-BASED SPLITTER (RecursiveCharacterTextSplitter)")
    print("=" * 70)
    print("Recursive separators: ['\\n\\n', '\\n', ' ', '']")
    print("Same input documents as Task 7:", len(docs), "(notes.txt + 3 PDF pages)")

    # 1) the project default size
    compare(docs, CHUNK_SIZE, CHUNK_OVERLAP)
    print(
        "\n-> At chunk_size=500 both give the same result, because every paragraph/line of\n"
        "   these small documents is already shorter than 500 characters."
    )

    # 2) a smaller size, where paragraphs no longer fit in one chunk
    small_size, small_overlap = 300, 30
    length_chunks, recursive_chunks, a, b = compare(docs, small_size, small_overlap)

    longest = max(length_chunks, key=lambda c: len(c.page_content))
    print(f"\nLongest chunk from CharacterTextSplitter ({len(longest.page_content)} chars, limit {small_size}):")
    print(longest.page_content)

    pieces = build_recursive_splitter(small_size, small_overlap).split_text(longest.page_content)
    print(f"\nThe recursive splitter cuts that same text into {len(pieces)} chunks:")
    for piece in pieces:
        print(f"  ({len(piece):>3} chars) {piece[:70]!r}...")

    print("\nOBSERVATION")
    print(
        f"  - CharacterTextSplitter splits on ONE separator only. When a paragraph is longer\n"
        f"    than chunk_size it cannot cut it, so {a['over_limit']} chunks passed the limit "
        f"(longest {a['max_len']} > {small_size}).\n"
        f"  - RecursiveCharacterTextSplitter falls back from paragraphs to lines to words, so\n"
        f"    {b['over_limit']} chunks passed the limit (longest {b['max_len']}) and words are never cut in half.\n"
        "  - It only cuts inside a paragraph when it has to, so it keeps paragraphs and\n"
        "    sentences together as much as the size limit allows. It is the recommended default."
    )


if __name__ == "__main__":
    main()
