"""
PART 5 - Task 10: End-to-End Similarity Search Pipeline

    Documents -> Splitter -> Embeddings -> Vector Store -> Similarity Search

Switchable embedding backend : openai | huggingface | ollama
Switchable vector store      : faiss  | chroma

Usage
-----
  python PART5_Mini_Project/task10_end_to_end_pipeline.py
        demo: runs every embedding backend that is available with both vector stores

  python PART5_Mini_Project/task10_end_to_end_pipeline.py --embeddings huggingface --store chroma
  python PART5_Mini_Project/task10_end_to_end_pipeline.py --embeddings openai --store faiss --query "How do I report a lost laptop?"
  python PART5_Mini_Project/task10_end_to_end_pipeline.py --interactive      (type your own questions)
  python PART5_Mini_Project/task10_end_to_end_pipeline.py --rebuild          (ignore saved stores)

The first run builds the store and saves it in vectorstores/; later runs load the saved store
(no re-embedding), which is why a vector store is useful.
"""

import argparse
import os
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if ROOT not in sys.path:
    sys.path.insert(0, ROOT)

import config  # import first: loads .env, hides warnings

from embedding_backends import BackendUnavailable, available_backends, fail, get_embeddings, model_name
from ingestion import load_chunks, print_results
from PART4_Vector_Stores.task7_faiss_store import (
    build_faiss_store,
    faiss_folder,
    faiss_search,
    load_faiss_store,
)
from PART4_Vector_Stores.task8_chroma_store import (
    build_chroma_store,
    chroma_folder,
    chroma_search,
    open_chroma_store,
)


class KnowledgeSearchEngine:
    """Documents -> Splitter -> Embeddings -> Vector Store -> Similarity Search."""

    def __init__(self, embedding_backend=config.DEFAULT_BACKEND, vector_store=config.DEFAULT_STORE,
                 rebuild=False, chunks=None, verbose=True):
        if embedding_backend not in config.BACKENDS:
            raise ValueError(f"embedding_backend must be one of {config.BACKENDS}")
        if vector_store not in config.VECTOR_STORES:
            raise ValueError(f"vector_store must be one of {config.VECTOR_STORES}")

        self.backend = embedding_backend
        self.store_name = vector_store
        self.verbose = verbose
        self.embeddings = get_embeddings(embedding_backend)          # may raise BackendUnavailable
        self.store = self._prepare_store(rebuild, chunks)

    # ------------------------------------------------------------------ helpers
    def _log(self, text):
        if self.verbose:
            print(text)

    def _saved_store_exists(self):
        if self.store_name == "faiss":
            return os.path.exists(os.path.join(faiss_folder(self.backend), "index.faiss"))
        folder = chroma_folder(self.backend)
        if not os.path.isdir(folder) or not os.listdir(folder):
            return False
        try:
            return open_chroma_store(folder, self.backend, self.embeddings)._collection.count() > 0
        except Exception:
            return False

    def _prepare_store(self, rebuild, chunks):
        self._log(f"\n=== Pipeline: embeddings = {self.backend} ({model_name(self.backend)}), "
                  f"vector store = {self.store_name} ===")

        if self._saved_store_exists() and not rebuild:
            self._log("[1-3/5] Documents, Splitter, Embeddings: skipped (a saved store already holds the vectors)")
            self._log("[4/5] Vector store: loading the saved store from disk")
            if self.store_name == "faiss":
                store = load_faiss_store(faiss_folder(self.backend), self.embeddings)
            else:
                store = open_chroma_store(chroma_folder(self.backend), self.backend, self.embeddings)
        else:
            if chunks is None:
                self._log("[1/5] Documents: loading txt / pdf / csv / web")
                self._log("[2/5] Splitter: RecursiveCharacterTextSplitter")
                chunks = load_chunks(verbose=self.verbose)
            else:
                self._log("[1-2/5] Documents + Splitter: using the chunks that were already loaded and split")
            self._log(f"[3/5] Embeddings: {self.backend} / {model_name(self.backend)} for {len(chunks)} chunks")
            self._log(f"[4/5] Vector store: building {self.store_name} and saving it to disk")
            if self.store_name == "faiss":
                store = build_faiss_store(chunks, self.embeddings, faiss_folder(self.backend))
            else:
                store = build_chroma_store(chunks, self.embeddings, chroma_folder(self.backend), self.backend)
        self._log("[5/5] Similarity search: ready")
        return store

    # ------------------------------------------------------------------ search
    def search(self, query, top_k=3):
        """Return the top_k most similar chunks as a list of dictionaries."""
        if self.store_name == "faiss":
            return faiss_search(self.store, query, top_k)
        return chroma_search(self.store, query, top_k)


def run_demo(rebuild=False):
    """Run every available embedding backend with both vector stores and compare the top results."""
    print("Checking which embedding backends are available:")
    backends = available_backends(verbose=True)
    if not backends:
        fail("No embedding backend is available. Install sentence-transformers, add an OpenAI key, or start Ollama.")
    print("Available:", ", ".join(backends))

    chunks = load_chunks()
    queries = config.TEST_QUERIES
    top_results = {}                                   # (backend, store) -> [top-1 label per query]

    for backend in backends:
        for store_name in config.VECTOR_STORES:
            try:
                engine = KnowledgeSearchEngine(backend, store_name, rebuild=rebuild, chunks=chunks)
                results = [engine.search(q, top_k=3) for q in queries]
            except Exception as error:
                print(f"  -> {backend} + {store_name} failed: {type(error).__name__}: {error}")
                continue
            top_results[(backend, store_name)] = [r[0]["label"] for r in results]
            print_results(queries[0], results[0])

    print("\n" + "=" * 70)
    print("SUMMARY - best match (top-1) for each query")
    print("=" * 70)
    for i, query in enumerate(queries):
        print(f"\n{query!r}")
        for (backend, store_name), labels in top_results.items():
            print(f"   {backend + ' + ' + store_name:<22} -> {labels[i]}")


def interactive(engine):
    print("\nType a question and press Enter (empty line to quit).")
    while True:
        try:
            query = input("\nsearch> ").strip()
        except EOFError:
            break
        if not query:
            break
        print_results(query, engine.search(query, top_k=3))


def parse_args():
    parser = argparse.ArgumentParser(description="End-to-end similarity search pipeline")
    parser.add_argument("--embeddings", choices=config.BACKENDS, help="embedding backend")
    parser.add_argument("--store", choices=config.VECTOR_STORES, help="vector store")
    parser.add_argument("--query", help="one question to search for")
    parser.add_argument("--top-k", type=int, default=3, help="number of results (default 3)")
    parser.add_argument("--interactive", action="store_true", help="ask your own questions")
    parser.add_argument("--rebuild", action="store_true", help="re-embed and overwrite the saved store")
    return parser.parse_args()


def main():
    args = parse_args()
    print("=" * 70)
    print("TASK 10: END-TO-END SIMILARITY SEARCH PIPELINE")
    print("Documents -> Splitter -> Embeddings -> Vector Store -> Similarity Search")
    print("=" * 70)

    single_run = args.embeddings or args.store or args.query or args.interactive
    if not single_run:
        run_demo(rebuild=args.rebuild)
        return

    backend = args.embeddings or config.DEFAULT_BACKEND
    store_name = args.store or config.DEFAULT_STORE
    try:
        engine = KnowledgeSearchEngine(backend, store_name, rebuild=args.rebuild)
    except BackendUnavailable as error:
        fail(f"The '{backend}' embeddings are not available.\n{error}")
    except Exception as error:
        fail(f"Could not build the pipeline: {type(error).__name__}: {error}")

    try:
        queries = [args.query] if args.query else config.TEST_QUERIES
        for query in queries:
            print_results(query, engine.search(query, top_k=args.top_k))
        if args.interactive:
            interactive(engine)
    except Exception as error:
        fail(f"The search failed: {type(error).__name__}: {error}")


if __name__ == "__main__":
    main()
