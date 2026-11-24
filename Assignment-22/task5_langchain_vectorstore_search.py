"""
PART 2 - Task 5: Similarity Search with LangChain Abstraction

  1. LangChain embedding class  : OpenAIEmbeddings
  2. LangChain vector store     : FAISS  (FAISS.from_documents does embedding + storing in one call)
  3. vectorstore.similarity_search(query)  -> retrieved Documents
  4. Print the retrieved documents

Compare with Task 4: the manual NumPy code is replaced by two lines of LangChain.

Needs:  OPENAI_API_KEY in the .env file
Run:    python PART2_Similarity_Search_OpenAI/task5_langchain_vectorstore_search.py
"""

import os
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if ROOT not in sys.path:
    sys.path.insert(0, ROOT)

import config  # import first: loads .env, hides warnings

from langchain_community.vectorstores import FAISS

from embedding_backends import BackendUnavailable, fail, get_embeddings
from ingestion import load_chunks


def main():
    print("=" * 70)
    print("TASK 5: SIMILARITY SEARCH WITH LANGCHAIN ABSTRACTION")
    print("=" * 70)

    try:
        embeddings = get_embeddings("openai")
    except BackendUnavailable as error:
        fail(f"OpenAI embeddings are not available.\n{error}")

    chunks = load_chunks()

    try:
        # LangChain embeds every chunk and stores the vectors in FAISS
        vectorstore = FAISS.from_documents(chunks, embeddings, normalize_L2=True)
        print(f"Vector store created with {vectorstore.index.ntotal} vectors "
              f"of {vectorstore.index.d} dimensions")

        for query in config.TEST_QUERIES:
            documents = vectorstore.similarity_search(query)          # default k = 4
            print(f"\nQuery: {query!r}  ->  {len(documents)} documents retrieved")
            for i, doc in enumerate(documents, start=1):
                text = " ".join(doc.page_content.split())
                print(f"  {i}. [{doc.metadata['type']}] {doc.metadata['label']}")
                print(f"     {text[:160]}{'...' if len(text) > 160 else ''}")

        # Same search, but also returning the score
        query = config.TEST_QUERIES[0]
        print(f"\nsimilarity_search_with_score({query!r}, k=2):")
        for doc, distance in vectorstore.similarity_search_with_score(query, k=2):
            print(f"  distance {distance:.4f} (lower = more similar) | {doc.metadata['label']}")
    except Exception as error:
        fail(f"The OpenAI request failed: {type(error).__name__}: {error}")


if __name__ == "__main__":
    main()
