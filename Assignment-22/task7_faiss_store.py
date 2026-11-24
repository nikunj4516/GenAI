"""
PART 4 - Task 7: FAISS Vector Store

  1. Store the embeddings in FAISS
  2. Perform similarity search
  3. Save the FAISS index locally
  4. Reload the index and verify that search still works (same results)

Embedding backend: Hugging Face by default (free). Choose another one with an argument:
    python PART4_Vector_Stores/task7_faiss_store.py            (huggingface)
    python PART4_Vector_Stores/task7_faiss_store.py openai
    python PART4_Vector_Stores/task7_faiss_store.py ollama

Vectors are normalized (normalize_L2=True). FAISS then returns a squared L2 distance d and
the cosine similarity is 1 - d / 2 (printed below, so all vector stores can be compared).
"""

import os
import sys
import time

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if ROOT not in sys.path:
    sys.path.insert(0, ROOT)

import config  # import first: loads .env, hides warnings

from langchain_community.vectorstores import FAISS

from embedding_backends import BackendUnavailable, choose_backend, fail, get_embeddings, model_name
from ingestion import docs_to_results, load_chunks, print_results


def faiss_folder(backend):
    return os.path.join(config.VECTORSTORE_DIR, f"faiss_{backend}")


def build_faiss_store(chunks, embeddings, folder):
    """Embed the chunks, store the vectors in FAISS and save the index to disk."""
    store = FAISS.from_documents(chunks, embeddings, normalize_L2=True)
    os.makedirs(folder, exist_ok=True)
    store.save_local(folder)
    return store


def load_faiss_store(folder, embeddings):
    """Reload a saved FAISS index. (The pickle file is our own, so loading it is safe.)"""
    return FAISS.load_local(
        folder, embeddings, allow_dangerous_deserialization=True, normalize_L2=True
    )


def faiss_search(store, query, k=3):
    """Similarity search -> list of result dictionaries with cosine similarity."""
    pairs = store.similarity_search_with_score(query, k=k)
    return docs_to_results([(doc, 1 - distance / 2) for doc, distance in pairs])


def main():
    backend = choose_backend()
    print("=" * 70)
    print("TASK 7: FAISS VECTOR STORE")
    print("=" * 70)

    try:
        embeddings = get_embeddings(backend)
    except BackendUnavailable as error:
        fail(f"The '{backend}' embeddings are not available.\n{error}")

    chunks = load_chunks()
    folder = faiss_folder(backend)
    print(f"Embedding model : {backend} / {model_name(backend)}")

    # ---- 1) store embeddings in FAISS (and 3) save the index) ----
    try:
        start = time.perf_counter()
        store = build_faiss_store(chunks, embeddings, folder)
        print(f"\nFAISS index built in {time.perf_counter() - start:.2f} s: "
              f"{store.index.ntotal} vectors x {store.index.d} dimensions")
    except Exception as error:
        fail(f"Building the index failed: {type(error).__name__}: {error}")

    print("Saved to        :", folder)
    for name in sorted(os.listdir(folder)):
        print(f"   {name:<14}{os.path.getsize(os.path.join(folder, name)) / 1024:>10.1f} KB")

    # ---- 2) similarity search ----
    print("\n--- Similarity search (index in memory) ---")
    before = {}
    for query in config.TEST_QUERIES:
        before[query] = faiss_search(store, query)
        print_results(query, before[query])

    # ---- 4) reload from disk and verify ----
    print("\n--- Reload the saved index and verify ---")
    reloaded = load_faiss_store(folder, embeddings)
    print(f"Reloaded index: {reloaded.index.ntotal} vectors x {reloaded.index.d} dimensions")

    all_same = True
    for query in config.TEST_QUERIES:
        after = faiss_search(reloaded, query)
        same = [r["content"] for r in before[query]] == [r["content"] for r in after]
        all_same = all_same and same
        print(f"  {'same results' if same else 'DIFFERENT results'} -> {query!r}")

    print("\nVERIFICATION:", "PASSED - the reloaded index returns identical results" if all_same else "FAILED")


if __name__ == "__main__":
    main()
