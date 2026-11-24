"""
PART 2 - Task 9: Document Structure-Based Splitting

Splitters for structured documents. The structure (headers, sections, pages) is kept
in the chunk METADATA so every chunk can be traced back to where it came from.

  A) Markdown  -> MarkdownHeaderTextSplitter  (keeps Header 1 / 2 / 3 in metadata)
  B) PDF       -> PyPDFLoader pages + RecursiveCharacterTextSplitter
                  (every chunk keeps its page number)
  C) Markdown  -> RecursiveCharacterTextSplitter.from_language(Language.MARKDOWN)

Run:  python PART2_Text_Splitters/task9_structure_based_splitter.py
"""

import os
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if ROOT not in sys.path:
    sys.path.insert(0, ROOT)

from config import CHUNK_OVERLAP, CHUNK_SIZE, MD_FILE  # import first: sets user agent

from langchain_text_splitters import (
    Language,
    MarkdownHeaderTextSplitter,
    RecursiveCharacterTextSplitter,
)

from PART1_Document_Loaders.task3_pdf_loader import load_pdf

HEADERS_TO_SPLIT_ON = [
    ("#", "Header 1"),
    ("##", "Header 2"),
    ("###", "Header 3"),
]


def split_markdown_by_headers(markdown_text):
    """Split markdown at its headers; header names are stored in metadata."""
    splitter = MarkdownHeaderTextSplitter(
        headers_to_split_on=HEADERS_TO_SPLIT_ON,
        strip_headers=False,   # keep the header line inside the chunk text as well
    )
    return splitter.split_text(markdown_text)


def split_pdf_by_pages(chunk_size=CHUNK_SIZE, chunk_overlap=CHUNK_OVERLAP):
    """Split the PDF page by page. Chunks never cross a page and keep the page number."""
    pages = load_pdf()
    splitter = RecursiveCharacterTextSplitter(chunk_size=chunk_size, chunk_overlap=chunk_overlap)
    return pages, splitter.split_documents(pages)


def main():
    print("=" * 70)
    print("TASK 9: DOCUMENT STRUCTURE-BASED SPLITTING")
    print("=" * 70)

    # ------------------------------------------------------------------ A
    print("\n--- A) Markdown: MarkdownHeaderTextSplitter ---")
    with open(MD_FILE, encoding="utf-8") as f:
        markdown_text = f.read()

    md_chunks = split_markdown_by_headers(markdown_text)
    print("Markdown file:", MD_FILE)
    print("Number of chunks (one per section):", len(md_chunks))
    for i, chunk in enumerate(md_chunks[:4]):
        print(f"\nChunk {i}")
        print("  metadata:", chunk.metadata)
        print("  content :", chunk.page_content[:110].replace("\n", " | "))

    all_have_headers = all("Header 1" in c.metadata for c in md_chunks)
    print("\nEvery chunk keeps its header(s) in metadata:", all_have_headers)

    # Second pass: make sure no section is bigger than chunk_size
    size_limiter = RecursiveCharacterTextSplitter(chunk_size=CHUNK_SIZE, chunk_overlap=CHUNK_OVERLAP)
    final_md_chunks = size_limiter.split_documents(md_chunks)
    print(f"After size limit pass (chunk_size={CHUNK_SIZE}): {len(final_md_chunks)} chunks, metadata kept:",
          all("Header 1" in c.metadata for c in final_md_chunks))

    # ------------------------------------------------------------------ B
    print("\n--- B) PDF: page-aware splitting ---")
    pages, pdf_chunks = split_pdf_by_pages()
    print("PDF pages:", len(pages), "| chunks:", len(pdf_chunks))
    for i, chunk in enumerate(pdf_chunks):
        print(f"  chunk {i}: page {chunk.metadata['page'] + 1}, {len(chunk.page_content):>3} chars | "
              f"{chunk.page_content[:60]!r}")

    pages_kept = all("page" in c.metadata for c in pdf_chunks)
    section_heads = [c for c in pdf_chunks if c.page_content[:2] in ("1.", "2.", "3.")]
    print("\nEvery chunk keeps its page number:", pages_kept)
    print("Section headings found at the start of chunks:", [c.page_content.split("\n")[0] for c in section_heads])

    print("\nSample PDF chunk with metadata:")
    sample = pdf_chunks[1]
    print("  page   :", sample.metadata["page"] + 1)
    print("  source :", os.path.basename(sample.metadata["source"]))
    print("  content:", sample.page_content)

    # ------------------------------------------------------------------ C
    print("\n--- C) Markdown: RecursiveCharacterTextSplitter.from_language(MARKDOWN) ---")
    md_splitter = RecursiveCharacterTextSplitter.from_language(
        language=Language.MARKDOWN, chunk_size=250, chunk_overlap=0
    )
    lang_chunks = md_splitter.create_documents([markdown_text])
    print("Number of chunks (chunk_size=250):", len(lang_chunks))
    for i, chunk in enumerate(lang_chunks[:3]):
        print(f"  chunk {i}: {chunk.page_content[:90]!r}")
    print("(It prefers to cut before '## ' and '### ' headers, so sections stay together.)")


if __name__ == "__main__":
    main()
