"""
PART 1 - Task 2: Hugging Face Embedding Model

  1. Use sentence-transformers/all-MiniLM-L6-v2 through LangChain's HuggingFaceEmbeddings
  2. Generate embeddings for the SAME document chunks as Task 1
  3. Compare vector dimensions and performance (speed, ease of use)

The model runs locally and needs no API key (about 90 MB is downloaded the first time).
If OPENAI_API_KEY is set, the OpenAI numbers are measured too and shown side by side.

Run:  python PART1_Embedding_Models/task2_huggingface_embeddings.py
"""

import os
import sys
import time

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if ROOT not in sys.path:
    sys.path.insert(0, ROOT)

import config  # import first: loads .env, hides warnings

import numpy as np

from embedding_backends import BackendUnavailable, embed_with_timing, fail, get_embeddings, model_name
from ingestion import load_chunks, pick_sample


def main():
    print("=" * 70)
    print("TASK 2: HUGGING FACE EMBEDDING MODEL")
    print("=" * 70)

    chunks = pick_sample(load_chunks(verbose=False), config.SAMPLE_CHUNKS)
    texts = [c.page_content for c in chunks]
    print(f"Model           : {model_name('huggingface')}")
    print(f"Chunks embedded : {len(texts)} (same sample as Task 1)")

    # ---- load the model (this is the "setup cost" of a local model) ----
    start = time.perf_counter()
    try:
        embeddings = get_embeddings("huggingface")
    except BackendUnavailable as error:
        fail(f"Hugging Face embeddings are not available.\n{error}")
    load_seconds = time.perf_counter() - start

    vectors, seconds = embed_with_timing(embeddings, texts)
    matrix = np.array(vectors)

    print(f"\nEmbedding vector length : {matrix.shape[1]}")
    print(f"Matrix shape            : {matrix.shape}  (chunks x dimensions)")
    print(f"Model load time         : {load_seconds:.2f} seconds (one time)")
    print(f"Time for {len(texts)} chunks       : {seconds:.2f} seconds ({len(texts) / seconds:.1f} chunks/second)")
    print(f"Vector length (norm)    : {np.linalg.norm(matrix[0]):.4f}  (normalized to unit length)")
    print("\nFirst 8 embedding values of the first chunk:")
    print(" ", np.round(matrix[0][:8], 5).tolist())

    # ---- sanity check: related texts should be closer than unrelated texts ----
    a, b, c = embeddings.embed_documents(
        ["The cat sat on the sofa.", "A kitten is resting on the couch.", "Stock markets fell sharply today."]
    )
    print("\nMeaning check (cosine similarity):")
    print(f"  cat/sofa  vs kitten/couch : {float(np.dot(a, b)):.3f}  (similar meaning)")
    print(f"  cat/sofa  vs stock market : {float(np.dot(a, c)):.3f}  (different meaning)")

    # ---- comparison with OpenAI (only if a key is available) ----
    print("\n" + "-" * 70)
    print("COMPARISON: Hugging Face vs OpenAI")
    print("-" * 70)
    openai_dim, openai_time = "not measured (no key)", "not measured (no key)"
    try:
        openai_embeddings = get_embeddings("openai")
        openai_vectors, openai_seconds = embed_with_timing(openai_embeddings, texts)
        openai_dim = len(openai_vectors[0])
        openai_time = f"{openai_seconds:.2f} s (includes network time)"
    except BackendUnavailable:
        pass
    except Exception as error:
        openai_time = f"request failed ({type(error).__name__})"

    rows = [
        ("Model", model_name("huggingface"), model_name("openai")),
        ("Vector dimensions", matrix.shape[1], openai_dim),
        (f"Time for {len(texts)} chunks", f"{seconds:.2f} s (local CPU)", openai_time),
        ("Setup", "pip install + 90 MB download", "API key only"),
        ("Runs offline / data stays local", "yes", "no (text is sent to OpenAI)"),
        ("Cost", "free (your own hardware)", "$0.02 per 1M tokens"),
    ]
    print(f"{'':<34}{'Hugging Face':<42}{'OpenAI'}")
    for label, hf_value, oa_value in rows:
        print(f"{label:<34}{str(hf_value):<42}{oa_value}")


if __name__ == "__main__":
    main()
