"""
ingestion.py - documents -> chunks -> vector store -> retriever (reused from Assignments 21 and 22).

    load_documents()     Text + PDF + CSV loaders
    split_documents()    RecursiveCharacterTextSplitter (size 500, overlap 50)
    get_vectorstore()    FAISS store, saved in vectorstores/ and rebuilt automatically when settings change
    get_retriever()      the store as a LangChain retriever (top-k similarity search)
    format_docs()        retrieved chunks -> one text block for the prompt
    source_names()       the readable names of the retrieved chunks
"""

import json
import os
import re
import sys

ROOT = os.path.dirname(os.path.abspath(__file__))
if ROOT not in sys.path:
    sys.path.insert(0, ROOT)

import config  # import first: loads .env, hides warnings

from langchain_community.document_loaders import CSVLoader, PyPDFLoader, TextLoader
from langchain_community.vectorstores import FAISS
from langchain_text_splitters import RecursiveCharacterTextSplitter

import models

# Only the useful columns of the movie CSV become text (the other columns are numbers / ids).
CSV_CONTENT_COLUMNS = ["tagline", "overview", "genres", "keywords"]


def _tag(docs, kind):
    for doc in docs:
        doc.metadata["type"] = kind
    return docs


def _json_names_to_text(text):
    """'[{"id": 28, "name": "Action"}, ...]' -> 'Action, ...' (genres / keywords columns)."""
    return re.sub(r"\[\{.*?\}\]", lambda m: ", ".join(re.findall(r'"name": "([^"]+)"', m.group(0))), text)


def _label(chunk):
    """Short readable name of where a chunk came from (used as 'source' in answers)."""
    kind = chunk.metadata.get("type")
    if kind == "csv":
        return f"movie: {chunk.metadata.get('title', 'unknown')}"
    name = os.path.basename(str(chunk.metadata.get("source", "")))
    if kind == "pdf":
        return f"{name} (page {chunk.metadata.get('page', 0) + 1})"
    return name


def load_documents(verbose=True):
    """Load the text file, the PDF and the movie CSV with LangChain loaders."""
    docs = []
    docs += _tag(TextLoader(config.TXT_FILE, encoding="utf-8").load(), "txt")
    docs += _tag(PyPDFLoader(config.PDF_FILE).load(), "pdf")
    csv_docs = CSVLoader(config.CSV_FILE, content_columns=CSV_CONTENT_COLUMNS,
                         metadata_columns=["title"], encoding="utf-8").load()
    if config.CSV_ROW_LIMIT:
        csv_docs = csv_docs[: config.CSV_ROW_LIMIT]
    for doc in csv_docs:
        doc.page_content = f"title: {doc.metadata['title']}\n" + _json_names_to_text(doc.page_content)
    docs += _tag(csv_docs, "csv")
    if verbose:
        pdf_pages = sum(1 for d in docs if d.metadata["type"] == "pdf")
        print(f"Loaded documents : txt=1, pdf={pdf_pages} pages, csv={len(csv_docs)} movies")
    return docs


def split_documents(docs, verbose=True):
    splitter = RecursiveCharacterTextSplitter(chunk_size=config.CHUNK_SIZE, chunk_overlap=config.CHUNK_OVERLAP)
    chunks = splitter.split_documents(docs)
    for i, chunk in enumerate(chunks):
        chunk.metadata["chunk_id"] = f"chunk-{i:05d}"
        chunk.metadata["label"] = _label(chunk)
        if chunk.metadata["type"] == "csv" and not chunk.page_content.startswith("title:"):
            chunk.page_content = f"title: {chunk.metadata['title']}\n" + chunk.page_content   # 2nd chunk keeps its movie
    if verbose:
        counts = {k: sum(1 for c in chunks if c.metadata["type"] == k) for k in ("txt", "pdf", "csv")}
        print(f"Split into chunks: {len(chunks)} (size {config.CHUNK_SIZE}, overlap {config.CHUNK_OVERLAP}): "
              + ", ".join(f"{k}={v}" for k, v in counts.items()))
    return chunks


# ------------------------------------------------------------------ vector store
def _signature():
    """Everything that changes the content of the store. If it changes, the store is rebuilt."""
    files = {os.path.basename(p): os.path.getsize(p) for p in (config.TXT_FILE, config.PDF_FILE, config.CSV_FILE)}
    return {"provider": config.LLM_PROVIDER, "embedding_model": models.embedding_name(),
            "chunk_size": config.CHUNK_SIZE, "chunk_overlap": config.CHUNK_OVERLAP,
            "csv_rows": config.CSV_ROW_LIMIT, "files": files}


def _store_folder():
    return os.path.join(config.VECTORSTORE_DIR, f"faiss_{config.LLM_PROVIDER}")


def get_vectorstore(rebuild=False, verbose=True):
    """Return the FAISS store: loaded from disk when it is up to date, otherwise built and saved."""
    embeddings = models.get_embeddings()
    folder, info_file = _store_folder(), os.path.join(_store_folder(), "build_info.json")
    signature = _signature()

    if not rebuild and os.path.exists(info_file):
        try:
            with open(info_file, encoding="utf-8") as f:
                if json.load(f) == signature:
                    store = FAISS.load_local(folder, embeddings, allow_dangerous_deserialization=True)
                    if verbose:
                        print(f"Vector store     : loaded from disk ({store.index.ntotal} chunks, {models.embedding_name()})")
                    return store
        except Exception:
            pass                                                  # damaged or old store: rebuild below

    chunks = split_documents(load_documents(verbose), verbose)
    if verbose:
        print(f"Embedding {len(chunks)} chunks with {models.embedding_name()} ...")
    store = FAISS.from_documents(chunks, embeddings)
    os.makedirs(folder, exist_ok=True)
    store.save_local(folder)
    with open(info_file, "w", encoding="utf-8") as f:
        json.dump(signature, f, indent=2)
    if verbose:
        print(f"Vector store     : built and saved ({store.index.ntotal} chunks) -> {os.path.relpath(folder, config.ROOT)}")
    return store


def get_retriever(k=config.RETRIEVER_K, rebuild=False, verbose=True):
    """The FAISS store as a retriever: a Runnable that turns a question into the top-k chunks."""
    return get_vectorstore(rebuild, verbose).as_retriever(search_type="similarity", search_kwargs={"k": k})


# ------------------------------------------------------------------ helpers for prompts
def format_docs(docs):
    """Retrieved chunks -> one text block, every chunk starts with its source label."""
    return "\n\n".join(f"[source: {d.metadata.get('label', '?')}]\n{d.page_content}" for d in docs)


def source_names(docs):
    """Unique source labels, in retrieval order."""
    seen, names = set(), []
    for d in docs:
        label = d.metadata.get("label", "?")
        if label not in seen:
            seen.add(label)
            names.append(label)
    return names
