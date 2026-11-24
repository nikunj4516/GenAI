"""
PART 4 - Task 8: Build Vector Store for YouTube Content

  1. Generate embeddings with OpenAI
  2. Store the embeddings in FAISS (saved on disk)
  3. Create a retriever

The store is saved in vectorstores/youtube_<video id>. Next time it is loaded from disk (no new
transcript download, no new embedding cost). It is rebuilt automatically when the video, the chunk
settings or the embedding model change, or when you use --rebuild.

Retriever: MMR (Task 4). The transcript chunks overlap, so plain similarity search would often return
neighbouring chunks that say almost the same thing; MMR picks more varied chunks.

Needs:  OPENAI_API_KEY in .env and internet for the first run
Run:    python PART4_YouTube_RAG_Chatbot/task8_youtube_vectorstore.py
"""

import argparse
import os
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if ROOT not in sys.path:
    sys.path.insert(0, ROOT)

import config  # import first: loads .env, hides warnings

from openai_models import OpenAINotConfigured, fail, fail_openai, get_embeddings
from PART4_YouTube_RAG_Chatbot.task7_load_youtube import (
    TranscriptUnavailable,
    load_youtube_chunks,
    video_id_from_url,
)
from store_utils import load_or_build_faiss


def youtube_folder(video_id):
    return os.path.join(config.VECTORSTORE_DIR, f"youtube_{video_id}")


def youtube_signature(video_id):
    fallback = config.YOUTUBE_FALLBACK_FILE
    return {
        "video_id": video_id,
        "segment_seconds": config.YOUTUBE_SEGMENT_SECONDS,
        "chunk_size": config.YOUTUBE_CHUNK_SIZE,
        "chunk_overlap": config.YOUTUBE_CHUNK_OVERLAP,
        "embedding_model": config.OPENAI_EMBEDDING_MODEL,
        "fallback_file_modified": os.path.getmtime(fallback) if os.path.exists(fallback) else None,
    }


def get_youtube_vectorstore(url=config.YOUTUBE_URL, rebuild=False, verbose=True):
    """FAISS store of the video transcript chunks (built once, then loaded from disk)."""
    video_id = video_id_from_url(url)
    store, _ = load_or_build_faiss(
        youtube_folder(video_id),
        youtube_signature(video_id),
        lambda: load_youtube_chunks(url, verbose),
        get_embeddings(),
        rebuild=rebuild,
        verbose=verbose,
    )
    return store


def get_youtube_retriever(store):
    """MMR retriever over the transcript chunks."""
    return store.as_retriever(
        search_type="mmr",
        search_kwargs={
            "k": config.YOUTUBE_RETRIEVER_K,
            "fetch_k": config.YOUTUBE_FETCH_K,
            "lambda_mult": config.YOUTUBE_LAMBDA,
        },
    )


def main():
    parser = argparse.ArgumentParser(description="Build the YouTube vector store")
    parser.add_argument("--url", default=config.YOUTUBE_URL, help="YouTube video URL")
    parser.add_argument("--rebuild", action="store_true", help="download and embed again")
    args = parser.parse_args()

    print("=" * 70)
    print("TASK 8: VECTOR STORE FOR YOUTUBE CONTENT (OpenAI embeddings + FAISS)")
    print("=" * 70)
    print(f"Video: {args.url}")

    try:
        get_embeddings()
    except OpenAINotConfigured as error:
        fail(f"OpenAI embeddings are not available.\n{error}")

    try:
        store = get_youtube_vectorstore(args.url, rebuild=args.rebuild)
    except TranscriptUnavailable as error:
        fail(str(error))
    except ValueError as error:
        fail(str(error))
    except Exception as error:
        fail_openai(error)

    print(f"\nVector store: {store.index.ntotal} chunks x {store.index.d} dimensions "
          f"({config.OPENAI_EMBEDDING_MODEL})")
    print("Saved in    :", youtube_folder(video_id_from_url(args.url)))

    retriever = get_youtube_retriever(store)
    print(f"\nRetriever   : {type(retriever).__name__}, search_type='mmr', k={config.YOUTUBE_RETRIEVER_K}, "
          f"fetch_k={config.YOUTUBE_FETCH_K}, lambda_mult={config.YOUTUBE_LAMBDA}")

    try:
        for query in ("What is a neuron?", "How does the network learn?"):
            docs = retriever.invoke(query)
            print(f"\nQuery: {query!r}  ->  {len(docs)} transcript chunks")
            for doc in docs:
                text = " ".join(doc.page_content.split())
                print(f"   [{doc.metadata.get('start_timestamp', '--:--:--')}] {text[:150]}...")
    except Exception as error:
        fail_openai(error)


if __name__ == "__main__":
    main()
