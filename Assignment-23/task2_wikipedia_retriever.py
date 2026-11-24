"""
PART 2 - Task 2: Wikipedia Retriever

  1. LangChain's WikipediaRetriever
  2. Retrieve documents for a user query
  3. Print the retrieved content

Bonus (only when an OpenAI key is available): the retrieved pages are given to the LLM, which
answers using ONLY that text - the smallest possible RAG system.

Needs internet. Run:  python PART2_Retriever_Based_RAG/task2_wikipedia_retriever.py
"""

import os
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if ROOT not in sys.path:
    sys.path.insert(0, ROOT)

import config  # import first: loads .env, hides warnings

from langchain_community.retrievers import WikipediaRetriever
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate

from openai_models import OpenAINotConfigured, fail, get_llm


def build_wikipedia_retriever():
    return WikipediaRetriever(
        lang="en",
        top_k_results=config.WIKI_TOP_K,
        doc_content_chars_max=config.WIKI_MAX_CHARS,
    )


def print_documents(docs):
    for i, doc in enumerate(docs, start=1):
        print(f"\n  [{i}] {doc.metadata.get('title')}")
        print(f"      source : {doc.metadata.get('source')}")
        summary = " ".join(str(doc.metadata.get("summary", "")).split())
        print(f"      summary: {summary[:220]}{'...' if len(summary) > 220 else ''}")
        content = " ".join(doc.page_content.split())
        print(f"      content ({len(doc.page_content)} chars): {content[:350]}...")


def answer_from_documents(question, docs):
    """Bonus: let the LLM answer using only the retrieved Wikipedia text."""
    context = "\n\n".join(f"[{d.metadata.get('title')}]\n{d.page_content}" for d in docs)
    prompt = ChatPromptTemplate.from_messages(
        [
            ("system", "Answer the question using ONLY the Wikipedia text below. "
                       "If the text does not contain the answer, say you do not know. Keep it short.\n\n{context}"),
            ("human", "{question}"),
        ]
    )
    chain = prompt | get_llm() | StrOutputParser()
    return chain.invoke({"context": context, "question": question})


def main():
    print("=" * 70)
    print("TASK 2: WIKIPEDIA RETRIEVER (WikipediaRetriever)")
    print("=" * 70)
    retriever = build_wikipedia_retriever()
    print(f"Settings: lang=en, top_k_results={config.WIKI_TOP_K}, doc_content_chars_max={config.WIKI_MAX_CHARS}")

    answers_possible = True
    try:
        get_llm()
    except OpenAINotConfigured:
        answers_possible = False

    for query in config.WIKI_QUERIES:
        print(f"\nQuery: {query!r}")
        try:
            docs = retriever.invoke(query)
        except Exception as error:   # no internet, Wikipedia blocked ...
            fail(f"Could not reach Wikipedia ({type(error).__name__}: {str(error)[:150]}).\n"
                 "  -> Check your internet connection and run the task again.")
        print(f"Retrieved {len(docs)} Wikipedia pages")
        print_documents(docs)

        if docs and answers_possible:
            try:
                print(f"\n  Bonus - LLM answer from these pages:\n  {answer_from_documents(query, docs)}")
            except Exception as error:
                print(f"\n  (Bonus answer skipped: {type(error).__name__})")

    if not answers_possible:
        print("\n(Bonus LLM answers were skipped because OPENAI_API_KEY is not set; the retriever itself needs no key.)")


if __name__ == "__main__":
    main()
