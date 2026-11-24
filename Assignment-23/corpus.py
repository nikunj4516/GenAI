"""
corpus.py - the movie knowledge base used by Tasks 3-6 (custom text from Movie_recommendation.csv)
and the helpers that measure retrieval quality.

  load_movie_chunks()      : CSV -> documents -> split chunks
  get_movie_vectorstore()  : OpenAI embeddings + FAISS (saved on disk and reused)
  relevant_titles()        : objective ground truth: movies whose text contains the keywords
  evaluate_docs()          : precision / unique movies of a retrieval result
"""

import os
import re
import sys

ROOT = os.path.dirname(os.path.abspath(__file__))
if ROOT not in sys.path:
    sys.path.insert(0, ROOT)

import config  # import first: loads .env, hides warnings

from langchain_community.document_loaders import CSVLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter

from openai_models import get_embeddings
from store_utils import load_or_build_faiss

# Only the text columns of the movie CSV are used (the other columns are numbers / ids).
# The title is added separately so it appears exactly once at the start of every chunk.
CSV_CONTENT_COLUMNS = ["tagline", "overview", "genres", "keywords"]


def movie_folder():
    return os.path.join(config.VECTORSTORE_DIR, "movies_faiss")


def movie_signature():
    return {
        "source": "Movie_recommendation.csv",
        "rows": config.CSV_ROW_LIMIT,
        "chunk_size": config.CHUNK_SIZE,
        "chunk_overlap": config.CHUNK_OVERLAP,
        "embedding_model": config.OPENAI_EMBEDDING_MODEL,
    }


def _json_names_to_text(text):
    """'[{"id": 28, "name": "Action"}, ...]' -> 'Action, ...' (genres / keywords columns)."""
    return re.sub(
        r"\[\{.*?\}\]",
        lambda m: ", ".join(re.findall(r'"name": "([^"]+)"', m.group(0))),
        text,
    )


def load_movie_documents():
    """CSVLoader: one Document per movie (the first CSV_ROW_LIMIT rows)."""
    docs = CSVLoader(
        config.CSV_FILE,
        content_columns=CSV_CONTENT_COLUMNS,
        metadata_columns=["title"],
        encoding="utf-8",
    ).load()
    if config.CSV_ROW_LIMIT:
        docs = docs[: config.CSV_ROW_LIMIT]
    for doc in docs:
        doc.page_content = f"title: {doc.metadata['title']}\n" + _json_names_to_text(doc.page_content)
    return docs


def load_movie_chunks(verbose=True):
    """Documents -> RecursiveCharacterTextSplitter -> chunks (every chunk knows its movie title)."""
    docs = load_movie_documents()
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=config.CHUNK_SIZE, chunk_overlap=config.CHUNK_OVERLAP
    )
    chunks = splitter.split_documents(docs)
    for i, chunk in enumerate(chunks):
        chunk.metadata["chunk_id"] = f"chunk-{i:05d}"
        # a movie split into several chunks: every chunk must say which movie it is about
        if not chunk.page_content.startswith("title:"):
            chunk.page_content = f"title: {chunk.metadata['title']}\n" + chunk.page_content
    if verbose:
        print(f"Loaded {len(docs)} movies from the CSV -> {len(chunks)} chunks "
              f"(size {config.CHUNK_SIZE}, overlap {config.CHUNK_OVERLAP})")
    return chunks


def get_movie_vectorstore(rebuild=False, verbose=True):
    """FAISS store of the movie chunks. Built once, then loaded from disk."""
    store, _ = load_or_build_faiss(
        movie_folder(),
        movie_signature(),
        lambda: load_movie_chunks(verbose),
        get_embeddings(),
        rebuild=rebuild,
        verbose=verbose,
    )
    return store


# --------------------------------------------------------------------------- retrieval quality
def relevant_titles(keywords):
    """Ground truth: titles of the movies whose full text contains one of the keywords."""
    wanted = [k.lower() for k in keywords]
    return {
        doc.metadata["title"]
        for doc in load_movie_documents()
        if any(k in doc.page_content.lower() for k in wanted)
    }


def evaluate_docs(docs, relevant):
    """Quality numbers for one retrieval result (a list of chunks)."""
    titles = [d.metadata.get("title", "?") for d in docs]
    hits = [t for t in titles if t in relevant]
    return {
        "chunks": len(docs),
        "unique_movies": len(set(titles)),
        "relevant_chunks": len(hits),
        "precision": round(len(hits) / len(docs), 2) if docs else 0.0,
        "relevant_movies_found": len(set(hits)),
    }


def print_docs(docs, relevant=None, preview=110):
    """Print retrieved chunks, marking the relevant ones with a check mark."""
    for i, doc in enumerate(docs, start=1):
        mark = ""
        if relevant is not None:
            mark = " [relevant]" if doc.metadata.get("title") in relevant else " [not relevant]"
        text = " ".join(doc.page_content.split())
        print(f"   {i}. {doc.metadata.get('title', '?')}{mark}")
        print(f"      {text[:preview]}{'...' if len(text) > preview else ''}")


def metrics_line(metrics):
    return (f"chunks={metrics['chunks']}  unique movies={metrics['unique_movies']}  "
            f"precision={metrics['precision']}  relevant movies found={metrics['relevant_movies_found']}")
