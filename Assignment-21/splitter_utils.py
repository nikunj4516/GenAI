"""
splitter_utils.py - small helpers shared by the splitter tasks (Tasks 7, 8, 9, 10).

  load_sample_documents() : loads the SAME documents for every splitter
                            (notes.txt + every page of company_handbook.pdf)
  chunk_stats()           : numbers used to compare splitters
  overlap_between()       : shows the text shared by two consecutive chunks
"""

import os
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if ROOT not in sys.path:
    sys.path.insert(0, ROOT)

import config  # noqa: F401  (import first: sets user agent, hides warnings)

from PART1_Document_Loaders.task1_text_loader import load_text
from PART1_Document_Loaders.task3_pdf_loader import load_pdf


def load_sample_documents():
    """Return notes.txt (1 document) + company_handbook.pdf (3 page documents)."""
    return load_text() + load_pdf()


def short_source(doc):
    """File name of a document, e.g. 'notes.txt'."""
    return os.path.basename(str(doc.metadata.get("source", "unknown")))


def chunk_stats(chunks, chunk_size):
    """Return a dictionary of simple statistics about a list of chunks."""
    lengths = [len(c.page_content) for c in chunks]
    ends_cleanly = sum(
        1 for c in chunks if c.page_content.rstrip().endswith((".", "!", "?", ":"))
    )
    return {
        "chunks": len(chunks),
        "min_len": min(lengths),
        "avg_len": round(sum(lengths) / len(lengths), 1),
        "max_len": max(lengths),
        "over_limit": sum(1 for n in lengths if n > chunk_size),
        "end_at_sentence": ends_cleanly,
        "end_mid_sentence": len(chunks) - ends_cleanly,
    }


def overlap_between(first, second, max_len):
    """Longest text (<= max_len) that ends the first chunk and starts the second."""
    for size in range(min(len(first), len(second), max_len), 0, -1):
        if first.endswith(second[:size]):
            return second[:size]
    return ""
