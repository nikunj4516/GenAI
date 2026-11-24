"""
ingestion.py - documents -> chunks (reuses the Assignment 21 loaders and splitter).

  load_chunks()        : txt + pdf + csv + web -> split chunks (list of Documents)
  pick_sample()        : a small, mixed sample of chunks (used by Tasks 1, 2, 6)
  comparison_corpus()  : a small offline corpus used to compare embedding models
  print_results()      : nicely prints search results
"""

import os
import re
import sys

ROOT = os.path.dirname(os.path.abspath(__file__))
if ROOT not in sys.path:
    sys.path.insert(0, ROOT)

import config  # import first: loads .env, sets user agent, hides warnings

import bs4
from langchain_community.document_loaders import CSVLoader, PyPDFLoader, TextLoader, WebBaseLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter

# Only the useful columns of the movie CSV become text (the other columns are numbers/ids).
# The title is added separately (see load_documents / load_chunks) so it appears exactly once.
CSV_CONTENT_COLUMNS = ["tagline", "overview", "genres", "keywords"]
TYPE_ORDER = ["txt", "pdf", "csv", "web"]


def _tag(docs, kind):
    for doc in docs:
        doc.metadata["type"] = kind
    return docs


def _json_names_to_text(text):
    """'[{"id": 28, "name": "Action"}, ...]' -> 'Action, ...' (genres / keywords columns)."""
    return re.sub(
        r"\[\{.*?\}\]",
        lambda m: ", ".join(re.findall(r'"name": "([^"]+)"', m.group(0))),
        text,
    )


def load_documents(include_web=config.INCLUDE_WEB, verbose=True):
    """Load text, PDF, CSV and (optionally) web documents with LangChain loaders."""
    docs = []
    docs += _tag(TextLoader(config.TXT_FILE, encoding="utf-8").load(), "txt")
    docs += _tag(PyPDFLoader(config.PDF_FILE).load(), "pdf")

    csv_docs = CSVLoader(
        config.CSV_FILE,
        content_columns=CSV_CONTENT_COLUMNS,
        metadata_columns=["title"],
        encoding="utf-8",
    ).load()
    if config.CSV_ROW_LIMIT:
        csv_docs = csv_docs[: config.CSV_ROW_LIMIT]
    for doc in csv_docs:
        # the title is a metadata column, so add it to the text as well (helps title searches)
        doc.page_content = f"title: {doc.metadata['title']}\n" + _json_names_to_text(doc.page_content)
    docs += _tag(csv_docs, "csv")

    web_status = "skipped"
    if include_web:
        try:
            web_docs = WebBaseLoader(
                web_paths=[config.WEB_URL],
                bs_kwargs={"parse_only": bs4.SoupStrainer(["h1", "h2", "h3", "p"])},
                bs_get_text_kwargs={"separator": " ", "strip": True},
            ).load()
            docs += _tag(web_docs, "web")
            web_status = "loaded"
        except Exception as error:
            web_status = f"not available ({type(error).__name__}) - continuing without web content"

    if verbose:
        print(f"Loaded documents: txt=1, pdf=3 pages, csv={len(csv_docs)} rows, web={web_status}")
    return docs


def _label(chunk):
    """Short readable name of where a chunk came from."""
    kind = chunk.metadata.get("type")
    if kind == "csv":
        return chunk.metadata.get("title", "csv row")
    source = str(chunk.metadata.get("source", ""))
    if kind == "pdf":
        return f"{os.path.basename(source)} (page {chunk.metadata.get('page', 0) + 1})"
    return os.path.basename(source) if kind == "txt" else source


def split_documents(docs, chunk_size=config.CHUNK_SIZE, chunk_overlap=config.CHUNK_OVERLAP):
    splitter = RecursiveCharacterTextSplitter(chunk_size=chunk_size, chunk_overlap=chunk_overlap)
    return splitter.split_documents(docs)


def load_chunks(include_web=config.INCLUDE_WEB, verbose=True):
    """Documents -> Splitter -> chunks. Every chunk gets a 'chunk_id' and a 'label'."""
    chunks = split_documents(load_documents(include_web, verbose))
    for i, chunk in enumerate(chunks):
        chunk.metadata["chunk_id"] = f"chunk-{i:05d}"
        chunk.metadata["label"] = _label(chunk)
        # a movie split into 2 chunks: the 2nd chunk must also say which movie it is about
        if chunk.metadata["type"] == "csv" and not chunk.page_content.startswith("title:"):
            chunk.page_content = f"title: {chunk.metadata['title']}\n" + chunk.page_content
    if verbose:
        counts = {k: sum(1 for c in chunks if c.metadata["type"] == k) for k in TYPE_ORDER}
        print(f"Split into {len(chunks)} chunks (size {config.CHUNK_SIZE}, overlap {config.CHUNK_OVERLAP}): "
              + ", ".join(f"{k}={v}" for k, v in counts.items() if v))
    return chunks


def pick_sample(chunks, n=config.SAMPLE_CHUNKS):
    """Take n chunks, mixing the document types (round-robin) so every type is represented."""
    groups = [[c for c in chunks if c.metadata["type"] == k] for k in TYPE_ORDER]
    groups = [g for g in groups if g]
    sample, i = [], 0
    while len(sample) < min(n, len(chunks)):
        for group in groups:
            if i < len(group) and len(sample) < n:
                sample.append(group[i])
        i += 1
    return sample


def comparison_corpus(chunks, csv_chunks=40):
    """Offline corpus (no web): all txt + pdf chunks and the first csv chunks."""
    base = [c for c in chunks if c.metadata["type"] in ("txt", "pdf")]
    movies = [c for c in chunks if c.metadata["type"] == "csv"][:csv_chunks]
    return base + movies


def docs_to_results(pairs):
    """[(Document, similarity), ...] -> list of plain dictionaries."""
    results = []
    for rank, (doc, score) in enumerate(pairs, start=1):
        results.append(
            {
                "rank": rank,
                "score": round(float(score), 4),
                "label": doc.metadata.get("label", "?"),
                "type": doc.metadata.get("type", "?"),
                "content": doc.page_content,
            }
        )
    return results


def print_results(query, results, preview=170):
    print(f"\nQuery: {query!r}")
    for r in results:
        text = " ".join(r["content"].split())
        print(f"  {r['rank']}. [{r['type']}] {r['label']}  (cosine similarity {r['score']})")
        print(f"     {text[:preview]}{'...' if len(text) > preview else ''}")
