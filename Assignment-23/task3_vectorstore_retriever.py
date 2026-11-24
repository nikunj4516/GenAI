"""
PART 2 - Task 3: Vector Store Retriever

  1. Load documents: custom text = the movie descriptions in data/Movie_recommendation.csv
  2. Create embeddings with OpenAI (text-embedding-3-small)
  3. Store the embeddings in a vector store (FAISS) and save it to disk
  4. Perform similarity search using a retriever: vectorstore.as_retriever()

The saved store (vectorstores/movies_faiss) is reused by Tasks 4, 5 and 6.

Needs:  OPENAI_API_KEY in .env
Run:    python PART2_Retriever_Based_RAG/task3_vectorstore_retriever.py
"""

import os
import sys
import time

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if ROOT not in sys.path:
    sys.path.insert(0, ROOT)

import config  # import first: loads .env, hides warnings

from langchain_community.vectorstores import FAISS

from corpus import load_movie_chunks, movie_folder, movie_signature, print_docs
from openai_models import OpenAINotConfigured, fail, fail_openai, get_embeddings
from store_utils import save_faiss


def main():
    print("=" * 70)
    print("TASK 3: VECTOR STORE RETRIEVER (OpenAI embeddings + FAISS)")
    print("=" * 70)

    try:
        embeddings = get_embeddings()
    except OpenAINotConfigured as error:
        fail(f"OpenAI embeddings are not available.\n{error}")

    # ---- 1) load documents (and split them) ----
    chunks = load_movie_chunks()

    # ---- 2) + 3) embeddings -> FAISS vector store ----
    try:
        start = time.perf_counter()
        vectorstore = FAISS.from_documents(chunks, embeddings)
        print(f"\nEmbedded and stored {vectorstore.index.ntotal} chunks "
              f"({vectorstore.index.d} dimensions) in {time.perf_counter() - start:.1f} s")
        save_faiss(vectorstore, movie_folder(), movie_signature())
        print("Saved to:", movie_folder())

        # ---- 4) retriever ----
        retriever = vectorstore.as_retriever(search_type="similarity", search_kwargs={"k": config.RETRIEVER_K})
        print(f"\nRetriever created: {type(retriever).__name__}, search_type='similarity', k={config.RETRIEVER_K}")

        queries = [
            "a movie about a space war on a distant moon",
            "a toy that comes to life",
            "a heist crew plans an impossible robbery",
        ]
        for query in queries:
            docs = retriever.invoke(query)               # the retriever is a LangChain Runnable
            print(f"\nQuery: {query!r}  ->  {len(docs)} chunks")
            print_docs(docs)

        # the vector store can also return the similarity score
        query = queries[0]
        print(f"\nsimilarity_search_with_score({query!r}, k=3):")
        for doc, distance in vectorstore.similarity_search_with_score(query, k=3):
            print(f"   distance {distance:.4f} (lower = more similar) | {doc.metadata['title']}")
    except Exception as error:
        fail_openai(error)


if __name__ == "__main__":
    main()
