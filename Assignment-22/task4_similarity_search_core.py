"""
PART 2 - Task 4: Similarity Search App (Core Logic)

  1. Convert the document chunks into embeddings with OpenAI
  2. Keep the embeddings in memory (a NumPy matrix)
  3. def search(query, top_k=3): returns the top_k most similar chunks
  4. Test with 4 different queries

How it works: the query is embedded too; the cosine similarity between the query vector
and every chunk vector is computed, and the highest scores are returned.

Needs:  OPENAI_API_KEY in the .env file
Run:    python PART2_Similarity_Search_OpenAI/task4_similarity_search_core.py
"""

import os
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if ROOT not in sys.path:
    sys.path.insert(0, ROOT)

import config  # import first: loads .env, hides warnings

import numpy as np

from embedding_backends import BackendUnavailable, fail, get_embeddings
from ingestion import docs_to_results, load_chunks, print_results

_INDEX = {}   # built once, reused by every search() call


def build_index(backend="openai"):
    """Chunks -> embeddings -> in-memory matrix."""
    embeddings = get_embeddings(backend)          # fails fast if there is no API key
    chunks = load_chunks()
    matrix = np.array(embeddings.embed_documents([c.page_content for c in chunks]), dtype=np.float32)
    matrix /= np.linalg.norm(matrix, axis=1, keepdims=True)      # unit length -> dot product = cosine
    _INDEX.update(chunks=chunks, matrix=matrix, embeddings=embeddings)
    return _INDEX


def search(query, top_k=3):
    """Return the top_k chunks most similar to the query (list of dictionaries)."""
    if not _INDEX:
        build_index()
    query_vector = np.array(_INDEX["embeddings"].embed_query(query), dtype=np.float32)
    query_vector /= np.linalg.norm(query_vector)

    scores = _INDEX["matrix"] @ query_vector                    # cosine similarity with every chunk
    best = np.argsort(scores)[::-1][:top_k]                     # indexes of the highest scores
    return docs_to_results([(_INDEX["chunks"][i], scores[i]) for i in best])


def main():
    print("=" * 70)
    print("TASK 4: SIMILARITY SEARCH APP (CORE LOGIC, OPENAI EMBEDDINGS)")
    print("=" * 70)

    try:
        build_index()
    except BackendUnavailable as error:
        fail(f"OpenAI embeddings are not available.\n{error}")
    except Exception as error:
        fail(f"The OpenAI request failed: {type(error).__name__}: {error}")

    print(f"Indexed {len(_INDEX['chunks'])} chunks, {_INDEX['matrix'].shape[1]} dimensions each (in memory)")

    try:
        for query in config.TEST_QUERIES:
            print_results(query, search(query, top_k=3))
    except Exception as error:
        fail(f"The OpenAI request failed: {type(error).__name__}: {error}")


if __name__ == "__main__":
    main()
