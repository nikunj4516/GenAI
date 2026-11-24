"""
PART 3 - Task 4: Maximal Marginal Relevance (MMR) Retriever

  1. search_type="mmr"
  2. Compare with normal similarity search
  3. Explain how MMR improves diversity (also in task4_mmr_explanation.md)

Plain similarity search returns the k chunks closest to the query. In our movie data this often means
several chunks of the SAME movie or of near-identical sequels. MMR first fetches fetch_k candidates
by similarity and then picks k of them one by one, each time choosing the candidate that is
relevant to the query but NOT similar to the chunks already chosen.

Quality numbers printed for every query (the ground truth comes from the data: a movie is
"relevant" when its text contains the keyword, e.g. "batman"):
  unique movies      : how many different movies are in the result (higher = more diverse)
  avg similarity     : mean cosine similarity between the returned chunks (lower = more diverse)
  precision          : share of returned chunks that belong to a relevant movie
  relevant movies    : how many different relevant movies were found

Needs:  OPENAI_API_KEY in .env
Run:    python PART3_Advanced_Retrieval/task4_mmr_retriever.py
"""

import os
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if ROOT not in sys.path:
    sys.path.insert(0, ROOT)

import config  # import first: loads .env, hides warnings

import numpy as np

from corpus import evaluate_docs, get_movie_vectorstore, metrics_line, print_docs, relevant_titles
from openai_models import OpenAINotConfigured, fail, fail_openai, get_embeddings


def avg_pairwise_similarity(embeddings, docs):
    """Mean cosine similarity between all pairs of returned chunks (lower = more diverse)."""
    if len(docs) < 2:
        return 0.0
    vectors = np.array(embeddings.embed_documents([d.page_content for d in docs]))
    vectors /= np.linalg.norm(vectors, axis=1, keepdims=True)
    sims = vectors @ vectors.T
    upper = sims[np.triu_indices(len(docs), k=1)]
    return round(float(upper.mean()), 3)


def build_retrievers(store, k=config.RETRIEVER_K, fetch_k=config.MMR_FETCH_K, lambda_mult=config.MMR_LAMBDA):
    similarity = store.as_retriever(search_type="similarity", search_kwargs={"k": k})
    mmr = store.as_retriever(
        search_type="mmr",
        search_kwargs={"k": k, "fetch_k": fetch_k, "lambda_mult": lambda_mult},
    )
    return similarity, mmr


def main():
    print("=" * 70)
    print("TASK 4: MAXIMAL MARGINAL RELEVANCE (MMR) RETRIEVER")
    print("=" * 70)

    try:
        embeddings = get_embeddings()
    except OpenAINotConfigured as error:
        fail(f"OpenAI embeddings are not available.\n{error}")

    try:
        store = get_movie_vectorstore()
        similarity, mmr = build_retrievers(store)
        print(f"\nSimilarity retriever : search_type='similarity', k={config.RETRIEVER_K}")
        print(f"MMR retriever        : search_type='mmr', k={config.RETRIEVER_K}, "
              f"fetch_k={config.MMR_FETCH_K}, lambda_mult={config.MMR_LAMBDA}")

        totals = {"similarity": [], "mmr": []}
        for case in config.LABELLED_QUERIES:
            query, relevant = case["query"], relevant_titles(case["keywords"])
            print("\n" + "-" * 70)
            print(f"Query: {query!r}")
            print(f"Ground truth: {len(relevant)} movies mention {case['keywords']}")

            for name, retriever in (("similarity", similarity), ("mmr", mmr)):
                docs = retriever.invoke(query)
                metrics = evaluate_docs(docs, relevant)
                metrics["avg_similarity"] = avg_pairwise_similarity(embeddings, docs)
                totals[name].append(metrics)
                print(f"\n  {name.upper()}  {metrics_line(metrics)}  avg similarity={metrics['avg_similarity']}")
                print_docs(docs, relevant)

        # ---------------------------------------------------------------- summary
        print("\n" + "=" * 70)
        print(f"SUMMARY over {len(config.LABELLED_QUERIES)} queries (average)")
        print("=" * 70)
        print(f"{'':<12}{'unique movies':>15}{'avg similarity':>17}{'precision':>12}{'relevant movies':>18}")
        for name, rows in totals.items():
            mean = lambda key: round(float(np.mean([r[key] for r in rows])), 2)
            print(f"{name:<12}{mean('unique_movies'):>15}{mean('avg_similarity'):>17}"
                  f"{mean('precision'):>12}{mean('relevant_movies_found'):>18}")

        # ---------------------------------------------------------------- lambda sweep
        query = config.LABELLED_QUERIES[0]["query"]
        print(f"\nEffect of lambda_mult (1.0 = same as similarity, 0.0 = maximum diversity)\nQuery: {query!r}")
        print(f"{'lambda_mult':<14}{'unique movies':>15}{'avg similarity':>17}")
        for lam in (1.0, 0.7, 0.5, 0.3, 0.0):
            _, retriever = build_retrievers(store, lambda_mult=lam)
            docs = retriever.invoke(query)
            print(f"{lam:<14}{len({d.metadata['title'] for d in docs}):>15}{avg_pairwise_similarity(embeddings, docs):>17}")
    except Exception as error:
        fail_openai(error)

    print(
        "\nHOW MMR IMPROVES DIVERSITY\n"
        "  - Similarity search ranks every chunk only by closeness to the query, so near-duplicates\n"
        "    (several chunks of one movie, or its sequels) fill all k places.\n"
        "  - MMR scores each candidate as:  lambda * relevance_to_query - (1 - lambda) * similarity_to_chosen_chunks.\n"
        "  - After every pick, candidates that look like the chunks already chosen are penalised, so the\n"
        "    result covers more different movies / ideas while staying relevant.\n"
        "  - Cost: a slightly lower raw relevance, and one extra step. lambda_mult controls the balance."
    )


if __name__ == "__main__":
    main()
