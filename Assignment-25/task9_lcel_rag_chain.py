"""
PART 4 - Task 9: LCEL-Based RAG Chain

  Build an LCEL pipeline:   Retriever | Prompt | LLM | Output Parser
  Test with multiple user queries.

    rag_chain = (
        {"context": retriever | format_docs, "question": RunnablePassthrough()}
        | RAG_PROMPT | llm | StrOutputParser()
    )

  * The dictionary at the start runs two things in parallel on the user's question:
      - retriever | format_docs      -> finds the chunks and turns them into the context text
      - RunnablePassthrough()        -> passes the question on unchanged
  * The prompt fills {context} and {question}, the LLM answers, the parser returns plain text.

The documents are the Text + PDF + CSV files stored in the FAISS vector store (ingestion.py).

Needs:  an LLM (OpenAI key or Ollama), see .env.example
Run:    python PART4_Runnables_LCEL/task9_lcel_rag_chain.py
        python PART4_Runnables_LCEL/task9_lcel_rag_chain.py --question "How many sick days are there?"
"""

import argparse
import os
import sys
import time

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if ROOT not in sys.path:
    sys.path.insert(0, ROOT)

import config  # import first: loads .env, hides warnings

from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnableParallel, RunnablePassthrough

import ingestion
import models
from prompts import RAG_PROMPT


def build_rag_chain(llm, retriever):
    """Retriever | Prompt | LLM | Output Parser."""
    return (
        {"context": retriever | ingestion.format_docs, "question": RunnablePassthrough()}
        | RAG_PROMPT
        | llm
        | StrOutputParser()
    )


def build_rag_chain_with_sources(llm, retriever):
    """The same chain, but the answer comes back together with the names of the retrieved sources."""
    return RunnableParallel(
        answer=build_rag_chain(llm, retriever),
        sources=retriever | ingestion.source_names,
    )


def main():
    parser = argparse.ArgumentParser(description="LCEL RAG chain")
    parser.add_argument("--question", help="ask one question and exit")
    args = parser.parse_args()

    print("=" * 70)
    print("TASK 9: LCEL-BASED RAG CHAIN  (Retriever | Prompt | LLM | Output Parser)")
    print("=" * 70)
    try:
        llm = models.get_llm()
        retriever = ingestion.get_retriever()
    except models.ModelNotConfigured as error:
        models.fail(f"No LLM available.\n{error}")
    except Exception as error:
        models.fail_llm(error)

    chain = build_rag_chain_with_sources(llm, retriever)
    print(f"\nLLM: {models.provider_label()}   |   retriever: FAISS similarity search, k={config.RETRIEVER_K}")
    questions = [args.question] if args.question else config.RAG_QUESTIONS

    try:
        for i, question in enumerate(questions, start=1):
            start = time.perf_counter()
            out = chain.invoke(question)
            print(f"\nQ{i}: {question}")
            print(f"    {'Answer':<20}: {out['answer'].strip()}")
            not_found = config.NOT_FOUND_ANSWER.lower().rstrip(".") in out["answer"].lower()
            label = "Retrieved (not used)" if not_found else "Sources"
            print(f"    {label:<20}: {', '.join(out['sources'])}   ({time.perf_counter() - start:.1f} s)")
            if not_found:
                print("    (the context did not contain the answer, so the chain said so instead of guessing)")

        if not args.question:
            print("\nStreaming the same chain (answer appears piece by piece):")
            print("    Q: " + config.RAG_QUESTIONS[0] + "\n    A: ", end="", flush=True)
            for piece in build_rag_chain(llm, retriever).stream(config.RAG_QUESTIONS[0]):
                print(piece, end="", flush=True)
            print()
    except Exception as error:
        models.fail_llm(error)


if __name__ == "__main__":
    main()
