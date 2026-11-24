"""
PART 3 - Task 6: Contextual Compression Retriever

  1. ContextualCompressionRetriever
  2. A base retriever + a document compressor
  3. Reduce irrelevant content in the retrieved chunks
  4. Show BEFORE vs AFTER compression

A retrieved chunk is often only partly useful: a movie chunk contains genres, keywords, plot and tagline,
but the question may only need the plot. The compressor reads every retrieved chunk together with the
question and keeps only the parts that help to answer it (chunks with nothing useful are dropped).

Two compressors are shown:
  A) LLMChainExtractor                       : the LLM extracts the relevant sentences of each chunk
  B) EmbeddingsFilter -> LLMChainExtractor   : a cheap embedding filter first drops weak chunks,
                                               so the LLM has fewer chunks to read (fewer LLM calls)

Needs:  OPENAI_API_KEY in .env
Run:    python PART3_Advanced_Retrieval/task6_contextual_compression.py
"""

import os
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if ROOT not in sys.path:
    sys.path.insert(0, ROOT)

import config  # import first: loads .env, hides warnings

from corpus import get_movie_vectorstore
from lc_compat import (
    ContextualCompressionRetriever,
    DocumentCompressorPipeline,
    EmbeddingsFilter,
    LLMChainExtractor,
)
from openai_models import OpenAINotConfigured, fail, fail_openai, get_embeddings, get_llm

QUERIES = [
    "What is the plot of the movie Avatar?",
    "What happens in the Dark Knight Rises?",
]


def total_chars(docs):
    return sum(len(d.page_content) for d in docs)


def clean(text):
    return " ".join(text.split())


def show_before_after(before, after):
    """Print every chunk before compression and what is left after it."""
    after_by_id = {d.metadata.get("chunk_id"): d for d in after}
    for i, doc in enumerate(before, start=1):
        kept = after_by_id.get(doc.metadata.get("chunk_id"))
        print(f"\n   Chunk {i} - {doc.metadata['title']}  ({len(doc.page_content)} chars)")
        print(f"     BEFORE: {clean(doc.page_content)[:230]}...")
        if kept is None:
            print("     AFTER : (dropped - nothing relevant to the question)")
        else:
            print(f"     AFTER : {clean(kept.page_content)[:230]}  ({len(kept.page_content)} chars)")


def main():
    print("=" * 70)
    print("TASK 6: CONTEXTUAL COMPRESSION RETRIEVER")
    print("=" * 70)

    try:
        llm = get_llm()
        embeddings = get_embeddings()
    except OpenAINotConfigured as error:
        fail(f"OpenAI is not available.\n{error}")

    try:
        store = get_movie_vectorstore()
        base = store.as_retriever(search_type="similarity", search_kwargs={"k": config.RETRIEVER_K})

        extractor = LLMChainExtractor.from_llm(llm)
        compression_retriever = ContextualCompressionRetriever(base_compressor=extractor, base_retriever=base)

        pipeline = DocumentCompressorPipeline(
            transformers=[EmbeddingsFilter(embeddings=embeddings, k=2), LLMChainExtractor.from_llm(llm)]
        )
        pipeline_retriever = ContextualCompressionRetriever(base_compressor=pipeline, base_retriever=base)

        print(f"\nBase retriever        : similarity, k={config.RETRIEVER_K}")
        print("A) Compression        : LLMChainExtractor (1 LLM call per retrieved chunk)")
        print("B) Compression        : EmbeddingsFilter(k=2) -> LLMChainExtractor")

        summary = []
        for query in QUERIES:
            print("\n" + "-" * 70)
            print(f"Query: {query!r}")

            before = base.invoke(query)
            after = compression_retriever.invoke(query)
            show_before_after(before, after)

            before_chars, after_chars = total_chars(before), total_chars(after)
            saved = round(100 * (1 - after_chars / before_chars), 1) if before_chars else 0.0
            print(f"\n   A) chunks {len(before)} -> {len(after)} | characters {before_chars} -> {after_chars} "
                  f"({saved}% less text for the LLM)")

            piped = pipeline_retriever.invoke(query)
            piped_chars = total_chars(piped)
            saved_b = round(100 * (1 - piped_chars / before_chars), 1) if before_chars else 0.0
            print(f"   B) chunks {len(before)} -> {len(piped)} | characters {before_chars} -> {piped_chars} "
                  f"({saved_b}% less text, LLM read only {min(2, len(before))} chunks instead of {len(before)})")
            summary.append((query, before_chars, after_chars, piped_chars))

        print("\n" + "=" * 70)
        print("SUMMARY - characters sent to the LLM as context")
        print("=" * 70)
        print(f"{'Query':<46}{'before':>8}{'A) after':>10}{'B) after':>10}")
        for query, b, a, p in summary:
            print(f"{query[:44]:<46}{b:>8}{a:>10}{p:>10}")
    except Exception as error:
        fail_openai(error)

    print(
        "\nWHY COMPRESSION HELPS\n"
        "  - The final prompt only contains text that answers the question: lower token cost, less noise.\n"
        "  - A smaller, cleaner context lets the LLM focus, which usually improves answer quality.\n"
        "  - Trade-off: the extractor needs one extra LLM call per chunk (adds cost and latency), and it\n"
        "    could drop a useful sentence. The embeddings filter in B) reduces that cost."
    )


if __name__ == "__main__":
    main()
