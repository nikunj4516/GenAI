"""
PART 3 - Task 6: Ollama Embedding Model

  1. Ollama must be installed and running (see task6_ollama_setup.md)
  2. Embedding model: nomic-embed-text
  3. Generate embeddings for document chunks
  4. Compare with OpenAI embeddings (and Hugging Face when available)

The comparison has two parts:
  A) vector size and speed on the same sample chunks
  B) retrieval: do the models return the same top-3 chunks for the same queries?

Run:  python PART3_Ollama_Embeddings/task6_ollama_embeddings.py
"""

import os
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if ROOT not in sys.path:
    sys.path.insert(0, ROOT)

import config  # import first: loads .env, hides warnings

import numpy as np

from embedding_backends import (
    BackendUnavailable,
    embed_with_timing,
    fail,
    get_embeddings,
    model_name,
)
from ingestion import comparison_corpus, load_chunks, pick_sample


def top_k_labels(embeddings, corpus_vectors, corpus, query, k=3):
    """Indexes of the k chunks most similar to the query."""
    q = np.array(embeddings.embed_query(query))
    q /= np.linalg.norm(q)
    scores = corpus_vectors @ q
    return list(np.argsort(scores)[::-1][:k])


def main():
    print("=" * 70)
    print("TASK 6: OLLAMA EMBEDDING MODEL")
    print("=" * 70)

    try:
        ollama = get_embeddings("ollama")
    except BackendUnavailable as error:
        fail(f"Ollama embeddings are not available.\n{error}\n\nFull setup steps: PART3_Ollama_Embeddings/task6_ollama_setup.md")

    all_chunks = load_chunks()
    sample = pick_sample(all_chunks, config.SAMPLE_CHUNKS)
    texts = [c.page_content for c in sample]

    # ---------------------------------------------------------------- Ollama on the sample
    try:
        vectors, seconds = embed_with_timing(ollama, texts)
    except Exception as error:
        fail(f"The Ollama request failed: {type(error).__name__}: {error}")
    matrix = np.array(vectors)

    print(f"\nModel                   : {model_name('ollama')}")
    print(f"Chunks embedded         : {len(texts)}")
    print(f"Embedding vector length : {matrix.shape[1]}")
    print(f"Time for {len(texts)} chunks       : {seconds:.2f} seconds")
    print("First 8 values          :", np.round(matrix[0][:8], 5).tolist())

    # ---------------------------------------------------------------- A) size and speed
    models = {"ollama": ollama}
    timings = {"ollama": (matrix.shape[1], seconds)}
    for name in ("openai", "huggingface"):
        try:
            other = get_embeddings(name)
            other_vectors, other_seconds = embed_with_timing(other, texts)
            models[name] = other
            timings[name] = (len(other_vectors[0]), other_seconds)
        except BackendUnavailable as error:
            print(f"\n[{name}] skipped: {str(error).splitlines()[0]}")
        except Exception as error:
            print(f"\n[{name}] skipped: request failed ({type(error).__name__})")

    print("\n" + "-" * 70)
    print(f"A) VECTOR SIZE AND SPEED ({len(texts)} chunks)")
    print("-" * 70)
    print(f"{'Backend':<14}{'Model':<40}{'Dimensions':<12}{'Time (s)'}")
    for name, (dim, secs) in timings.items():
        print(f"{name:<14}{model_name(name):<40}{dim:<12}{secs:.2f}")
    if "openai" not in models:
        print("(OpenAI was not measured - add OPENAI_API_KEY to .env to include it.)")

    # ---------------------------------------------------------------- B) retrieval agreement
    corpus = comparison_corpus(all_chunks)
    corpus_texts = [c.page_content for c in corpus]
    print("\n" + "-" * 70)
    print(f"B) RETRIEVAL COMPARISON (top-3 chunks, corpus of {len(corpus)} chunks)")
    print("-" * 70)

    corpus_vectors, tops = {}, {}
    for name, embeddings in models.items():
        vectors = np.array(embeddings.embed_documents(corpus_texts))
        corpus_vectors[name] = vectors / np.linalg.norm(vectors, axis=1, keepdims=True)

    for query in config.TEST_QUERIES:
        print(f"\nQuery: {query!r}")
        tops[query] = {}
        for name, embeddings in models.items():
            best = top_k_labels(embeddings, corpus_vectors[name], corpus, query)
            tops[query][name] = set(best)
            print(f"  {name:<12} -> " + " | ".join(corpus[i].metadata["label"][:28] for i in best))

    if len(models) > 1:
        print("\nTop-3 overlap with Ollama (how many of the 3 chunks are the same):")
        for name in models:
            if name == "ollama":
                continue
            shared = [len(tops[q]["ollama"] & tops[q][name]) for q in config.TEST_QUERIES]
            print(f"  Ollama vs {name:<12}: {shared} out of 3 for each query")

    print(
        "\nSUMMARY\n"
        "  - Ollama: local, free, private, 768 dimensions; needs the Ollama app running.\n"
        "  - OpenAI: cloud, paid per token, 1536 dimensions; no local setup.\n"
        "  - Compare the top-3 lists in part B to see how much the models agree on this data."
    )


if __name__ == "__main__":
    main()
