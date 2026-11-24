"""
PART 4 - Task 8: ChromaDB Vector Store

  1. Create a ChromaDB collection
  2. Store the document embeddings (with their metadata) in it
  3. Persist the database to disk
  4. Perform similarity search (also after reopening the database from disk)

Embedding backend: Hugging Face by default (free). Choose another one with an argument:
    python PART4_Vector_Stores/task8_chroma_store.py            (huggingface)
    python PART4_Vector_Stores/task8_chroma_store.py openai
    python PART4_Vector_Stores/task8_chroma_store.py ollama

The collection uses cosine distance, so cosine similarity = 1 - distance.
"""

import os
import sys
import time

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if ROOT not in sys.path:
    sys.path.insert(0, ROOT)

import config  # import first: loads .env, hides warnings

import chromadb
from langchain_chroma import Chroma
from langchain_community.vectorstores.utils import filter_complex_metadata

from embedding_backends import BackendUnavailable, choose_backend, fail, get_embeddings, model_name
from ingestion import docs_to_results, load_chunks, print_results


def chroma_folder(backend):
    return os.path.join(config.VECTORSTORE_DIR, f"chroma_{backend}")


def collection_name(backend):
    return f"knowledge_{backend}"


def open_chroma_store(folder, backend, embeddings):
    """Open (or create) the persistent collection."""
    return Chroma(
        collection_name=collection_name(backend),
        embedding_function=embeddings,
        persist_directory=folder,
        collection_metadata={"hnsw:space": "cosine"},
    )


def build_chroma_store(chunks, embeddings, folder, backend):
    """Create the collection, embed the chunks and store them. Data is written to 'folder'."""
    os.makedirs(folder, exist_ok=True)

    # start from an empty collection so running the task twice never creates duplicates
    try:
        open_chroma_store(folder, backend, embeddings).delete_collection()
    except Exception:
        pass

    store = open_chroma_store(folder, backend, embeddings)
    clean_chunks = filter_complex_metadata(chunks)          # Chroma accepts only str/int/float/bool
    store.add_documents(clean_chunks, ids=[c.metadata["chunk_id"] for c in clean_chunks])
    return store


def chroma_search(store, query, k=3):
    """Similarity search -> list of result dictionaries with cosine similarity."""
    pairs = store.similarity_search_with_score(query, k=k)
    return docs_to_results([(doc, 1 - distance) for doc, distance in pairs])


def main():
    backend = choose_backend()
    print("=" * 70)
    print("TASK 8: CHROMADB VECTOR STORE")
    print("=" * 70)

    try:
        embeddings = get_embeddings(backend)
    except BackendUnavailable as error:
        fail(f"The '{backend}' embeddings are not available.\n{error}")

    chunks = load_chunks()
    folder = chroma_folder(backend)
    print(f"Embedding model : {backend} / {model_name(backend)}")

    # ---- 1) + 2) create the collection and store the embeddings ----
    try:
        start = time.perf_counter()
        store = build_chroma_store(chunks, embeddings, folder, backend)
        count = store._collection.count()
        print(f"\nCollection '{collection_name(backend)}' created in {time.perf_counter() - start:.2f} s "
              f"with {count} documents")
    except Exception as error:
        fail(f"Building the collection failed: {type(error).__name__}: {error}")

    # ---- 3) persisted to disk ----
    print("Persisted to    :", folder)
    for name in sorted(os.listdir(folder)):
        print("   ", name)

    # ---- 4) similarity search ----
    print("\n--- Similarity search ---")
    before = {}
    for query in config.TEST_QUERIES:
        before[query] = chroma_search(store, query)
        print_results(query, before[query])

    # ---- prove the data really lives on disk: open it again with the plain chromadb client ----
    print("\n--- Reopen the database from disk ---")
    client = chromadb.PersistentClient(path=folder)
    for col in client.list_collections():
        print(f"chromadb client sees collection '{col.name}' with {col.count()} documents")

    reopened = open_chroma_store(folder, backend, embeddings)
    all_same = True
    for query in config.TEST_QUERIES:
        after = chroma_search(reopened, query)
        same = [r["content"] for r in before[query]] == [r["content"] for r in after]
        all_same = all_same and same
        print(f"  {'same results' if same else 'DIFFERENT results'} -> {query!r}")
    print("\nVERIFICATION:", "PASSED - the persisted database returns identical results" if all_same else "FAILED")


if __name__ == "__main__":
    main()
