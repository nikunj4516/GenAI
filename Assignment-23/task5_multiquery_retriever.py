"""
PART 3 - Task 5: Multi-Query Retriever

  1. MultiQueryRetriever
  2. The LLM generates several reformulated versions of the user question
  3. Documents are retrieved for ALL the queries (the results are merged, duplicates removed)
  4. Compare the retrieval quality with a normal similarity search

Why: a single query is one point in the embedding space. If the user words the question
differently from the documents, relevant chunks can be missed. Several reformulations
look at the same question from different angles.

The comparison has THREE rows so it is fair:
  similarity (k=4)          : a normal retriever
  multi-query               : up to 3 queries x 4 chunks, merged
  similarity (same budget)  : a normal retriever asked for as many chunks as multi-query returned

Needs:  OPENAI_API_KEY in .env
Run:    python PART3_Advanced_Retrieval/task5_multiquery_retriever.py
"""

import logging
import os
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if ROOT not in sys.path:
    sys.path.insert(0, ROOT)

import config  # import first: loads .env, hides warnings

import numpy as np

from corpus import evaluate_docs, get_movie_vectorstore, metrics_line, print_docs, relevant_titles
from lc_compat import MultiQueryRetriever
from openai_models import OpenAINotConfigured, fail, fail_openai, get_llm


class QueryCapture(logging.Handler):
    """Collects the 'Generated queries' message that MultiQueryRetriever logs."""

    def __init__(self):
        super().__init__(level=logging.INFO)
        self.messages = []

    def emit(self, record):
        self.messages.append(record.getMessage())


def build_multi_query_retriever(store, llm, k=config.RETRIEVER_K):
    base = store.as_retriever(search_type="similarity", search_kwargs={"k": k})
    return MultiQueryRetriever.from_llm(retriever=base, llm=llm), base


def main():
    print("=" * 70)
    print("TASK 5: MULTI-QUERY RETRIEVER")
    print("=" * 70)

    try:
        llm = get_llm()
    except OpenAINotConfigured as error:
        fail(f"OpenAI is not available.\n{error}")

    capture = QueryCapture()
    logger = logging.getLogger(MultiQueryRetriever.__module__)
    logger.addHandler(capture)
    logger.setLevel(logging.INFO)

    try:
        store = get_movie_vectorstore()
        multi_query, base = build_multi_query_retriever(store, llm)
        print(f"\nBase retriever: similarity, k={config.RETRIEVER_K}")
        print("MultiQueryRetriever: the LLM writes 3 reformulated queries; each one retrieves "
              f"k={config.RETRIEVER_K} chunks; results are merged.")

        rows = {"similarity (k=4)": [], "multi-query": [], "similarity (same budget)": []}
        for case in config.LABELLED_QUERIES:
            query, relevant = case["query"], relevant_titles(case["keywords"])
            print("\n" + "-" * 70)
            print(f"Original query: {query!r}")
            print(f"Ground truth  : {len(relevant)} movies mention {case['keywords']}")

            capture.messages.clear()
            mq_docs = multi_query.invoke(query)
            for message in capture.messages:
                print(f"  LLM reformulations -> {message}")

            base_docs = base.invoke(query)
            budget_docs = store.similarity_search(query, k=len(mq_docs))

            for name, docs in (("similarity (k=4)", base_docs), ("multi-query", mq_docs),
                               ("similarity (same budget)", budget_docs)):
                metrics = evaluate_docs(docs, relevant)
                rows[name].append(metrics)
                print(f"\n  {name.upper()}  {metrics_line(metrics)}")
                if name != "similarity (same budget)":
                    print_docs(docs, relevant)

        print("\n" + "=" * 70)
        print(f"SUMMARY over {len(config.LABELLED_QUERIES)} queries (average)")
        print("=" * 70)
        print(f"{'':<28}{'chunks':>8}{'unique movies':>15}{'precision':>12}{'relevant movies':>18}")
        for name, metrics_list in rows.items():
            mean = lambda key: round(float(np.mean([m[key] for m in metrics_list])), 2)
            print(f"{name:<28}{mean('chunks'):>8}{mean('unique_movies'):>15}"
                  f"{mean('precision'):>12}{mean('relevant_movies_found'):>18}")
    except Exception as error:
        fail_openai(error)
    finally:
        logger.removeHandler(capture)

    print(
        "\nHOW TO READ THE RESULT\n"
        "  - 'relevant movies' is the number of different movies that really match the question: this is\n"
        "    the recall-like number that multi-query tries to increase.\n"
        "  - Compare multi-query with 'similarity (same budget)': both return the same number of chunks,\n"
        "    so any difference comes from the reformulated queries, not from simply getting more results.\n"
        "  - Cost: one extra LLM call per question and 3 vector searches instead of 1."
    )


if __name__ == "__main__":
    main()
