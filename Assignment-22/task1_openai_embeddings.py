"""
PART 1 - Task 1: OpenAI Embedding Model

  1. Use an OpenAI embedding model (text-embedding-3-small by default)
  2. Convert document chunks into embeddings
  3. Print the embedding vector length and sample embedding values

Needs:  OPENAI_API_KEY in the .env file (copy .env.example to .env)
Run:    python PART1_Embedding_Models/task1_openai_embeddings.py
"""

import os
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if ROOT not in sys.path:
    sys.path.insert(0, ROOT)

import config  # import first: loads .env, hides warnings

import numpy as np

from embedding_backends import BackendUnavailable, embed_with_timing, fail, get_embeddings, model_name
from ingestion import load_chunks, pick_sample


def main():
    print("=" * 70)
    print("TASK 1: OPENAI EMBEDDING MODEL")
    print("=" * 70)

    try:
        embeddings = get_embeddings("openai")
    except BackendUnavailable as error:
        fail(f"OpenAI embeddings are not available.\n{error}")

    chunks = pick_sample(load_chunks(verbose=False), config.SAMPLE_CHUNKS)
    texts = [c.page_content for c in chunks]
    print(f"Model            : {model_name('openai')}")
    print(f"Chunks embedded  : {len(texts)} (sample of the split documents)")

    try:
        vectors, seconds = embed_with_timing(embeddings, texts)
        query_vector = embeddings.embed_query("What is chunk overlap?")
    except Exception as error:   # wrong key, no internet, quota ...
        fail(f"The OpenAI request failed: {type(error).__name__}: {error}")

    matrix = np.array(vectors)
    print(f"\nEmbedding vector length : {matrix.shape[1]}")
    print(f"Matrix shape            : {matrix.shape}  (chunks x dimensions)")
    print(f"Time for {len(texts)} chunks       : {seconds:.2f} seconds")
    print(f"Vector length (norm)    : {np.linalg.norm(matrix[0]):.4f}  (OpenAI vectors are unit length)")

    print("\nSample chunk:", repr(" ".join(texts[0].split())[:120]))
    print("First 8 embedding values of that chunk:")
    print(" ", np.round(matrix[0][:8], 5).tolist())
    print("\nQuery embedding length  :", len(query_vector))


if __name__ == "__main__":
    main()
