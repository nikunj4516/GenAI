"""
store_utils.py - save / load FAISS vector stores safely.

A saved store is only reused when its "signature" (embedding model, chunk settings, source)
matches the current settings. If you change the model or the chunking, the store is rebuilt
automatically, so you never search vectors made with different settings.
"""

import json
import os
import sys

ROOT = os.path.dirname(os.path.abspath(__file__))
if ROOT not in sys.path:
    sys.path.insert(0, ROOT)

import config  # import first: loads .env, hides warnings

from langchain_community.vectorstores import FAISS

INFO_FILE = "build_info.json"


def save_faiss(store, folder, signature):
    """Save the FAISS index and remember the settings it was built with."""
    os.makedirs(folder, exist_ok=True)
    store.save_local(folder)
    with open(os.path.join(folder, INFO_FILE), "w", encoding="utf-8") as f:
        json.dump(signature, f, indent=2, sort_keys=True)


def saved_store_matches(folder, signature):
    info_path = os.path.join(folder, INFO_FILE)
    if not (os.path.exists(os.path.join(folder, "index.faiss")) and os.path.exists(info_path)):
        return False
    try:
        with open(info_path, encoding="utf-8") as f:
            return json.load(f) == json.loads(json.dumps(signature))
    except (OSError, ValueError):
        return False


def load_faiss(folder, embeddings):
    """Reload a saved index. (The pickle file is our own, so loading it is safe.)"""
    return FAISS.load_local(folder, embeddings, allow_dangerous_deserialization=True)


def load_or_build_faiss(folder, signature, make_chunks, embeddings, rebuild=False, verbose=True):
    """Return (store, 'loaded' | 'built'). make_chunks is only called when a build is needed."""
    if not rebuild and saved_store_matches(folder, signature):
        if verbose:
            print(f"Loaded the saved vector store: {folder}")
        return load_faiss(folder, embeddings), "loaded"

    chunks = make_chunks()
    if verbose:
        print(f"Embedding {len(chunks)} chunks with {config.OPENAI_EMBEDDING_MODEL} ...")
    store = FAISS.from_documents(chunks, embeddings)
    save_faiss(store, folder, signature)
    if verbose:
        print(f"Built and saved the vector store: {folder}")
    return store, "built"
