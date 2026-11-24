"""
PART 4 - Task 7: Load YouTube Content

  1. YoutubeLoader loads the transcript (captions) of a YouTube video
  2. The transcript is split with a text splitter

The transcript is loaded in 60-second documents (TranscriptFormat.CHUNKS) so that every piece
keeps its start time. The splitter then cuts them into chunks of at most 1000 characters with
200 characters of overlap; every chunk keeps the timestamp, so answers can point to the exact
moment in the video.

Default video: 3Blue1Brown - "But what is a neural network? | Deep learning chapter 1"
Needs internet. If YouTube blocks the download, see data/youtube_transcript.txt (fallback).

Run:  python PART4_YouTube_RAG_Chatbot/task7_load_youtube.py
      python PART4_YouTube_RAG_Chatbot/task7_load_youtube.py --url https://www.youtube.com/watch?v=VIDEO_ID
"""

import argparse
import os
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if ROOT not in sys.path:
    sys.path.insert(0, ROOT)

import config  # import first: loads .env, hides warnings

from langchain_community.document_loaders import YoutubeLoader
from langchain_community.document_loaders.youtube import TranscriptFormat
from langchain_core.documents import Document
from langchain_text_splitters import RecursiveCharacterTextSplitter

from openai_models import fail


class TranscriptUnavailable(Exception):
    """The transcript could not be loaded (blocked, disabled, no internet ...)."""


def video_id_from_url(url):
    return YoutubeLoader.extract_video_id(url)


def _read_fallback_file(url):
    """Optional: a transcript pasted by the user into data/youtube_transcript.txt."""
    path = config.YOUTUBE_FALLBACK_FILE
    if not os.path.exists(path):
        return []
    with open(path, encoding="utf-8") as f:
        text = f.read().strip()
    if not text:
        return []
    return [Document(page_content=text, metadata={"source": url})]


def load_transcript_documents(url):
    """Return (documents, origin). origin is 'youtube' or 'fallback file'."""
    problem = None
    try:
        loader = YoutubeLoader.from_youtube_url(
            url,
            add_video_info=False,                     # video info needs the extra (unreliable) pytube package
            language=config.YOUTUBE_LANGUAGES,
            transcript_format=TranscriptFormat.CHUNKS,
            chunk_size_seconds=config.YOUTUBE_SEGMENT_SECONDS,
        )
        docs = loader.load()
        if docs:
            return docs, "youtube"
        problem = "the video has no transcript (captions are disabled)"
    except Exception as error:
        name = type(error).__name__
        if name in ("RequestBlocked", "IpBlocked"):
            problem = ("YouTube is blocking transcript requests from this network "
                       "(common on cloud servers, VPNs and some shared networks)")
        else:
            problem = f"{name}: {str(error).splitlines()[0][:160] if str(error) else 'no details'}"

    docs = _read_fallback_file(url)
    if docs:
        return docs, "fallback file"

    raise TranscriptUnavailable(
        f"Could not load the transcript: {problem}.\n"
        "  What you can do:\n"
        "   1. Run the task on your own computer / home network (YouTube often blocks cloud servers).\n"
        "   2. Check that the video has captions and that the URL is correct.\n"
        f"   3. Open the video on YouTube -> '...more' -> 'Show transcript', copy the text and save it in\n"
        f"      {config.YOUTUBE_FALLBACK_FILE}  (then run this task again)."
    )


def split_transcript(docs):
    """Split the transcript documents into overlapping chunks (timestamps are kept)."""
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=config.YOUTUBE_CHUNK_SIZE,
        chunk_overlap=config.YOUTUBE_CHUNK_OVERLAP,
    )
    chunks = splitter.split_documents(docs)
    for i, chunk in enumerate(chunks):
        chunk.metadata["chunk_id"] = f"yt-{i:04d}"
    return chunks


def load_youtube_chunks(url=config.YOUTUBE_URL, verbose=True):
    """Video URL -> transcript documents -> chunks."""
    docs, origin = load_transcript_documents(url)
    chunks = split_transcript(docs)
    if verbose:
        print(f"Transcript loaded from {origin}: {len(docs)} segments -> {len(chunks)} chunks "
              f"(size {config.YOUTUBE_CHUNK_SIZE}, overlap {config.YOUTUBE_CHUNK_OVERLAP})")
    return chunks


def main():
    parser = argparse.ArgumentParser(description="Load and split a YouTube transcript")
    parser.add_argument("--url", default=config.YOUTUBE_URL, help="YouTube video URL")
    args = parser.parse_args()

    print("=" * 70)
    print("TASK 7: LOAD YOUTUBE CONTENT (YoutubeLoader + text splitter)")
    print("=" * 70)

    try:
        video_id = video_id_from_url(args.url)
    except ValueError as error:
        fail(str(error))
    print(f"Video URL : {args.url}")
    print(f"Video ID  : {video_id}")
    print(f"Language  : {config.YOUTUBE_LANGUAGES}")

    try:
        docs, origin = load_transcript_documents(args.url)
    except TranscriptUnavailable as error:
        fail(str(error))

    total_chars = sum(len(d.page_content) for d in docs)
    print(f"\nTranscript source        : {origin}")
    print(f"Transcript segments      : {len(docs)}  ({config.YOUTUBE_SEGMENT_SECONDS}-second documents)")
    print(f"Total transcript length  : {total_chars} characters (about {total_chars // 5} words)")
    last = docs[-1].metadata.get("start_timestamp")
    if last:
        print(f"Last segment starts at   : {last}")

    print("\nSample segment (before splitting):")
    print("  metadata:", {k: v for k, v in docs[0].metadata.items() if k in ("source", "start_timestamp", "start_seconds")})
    print("  text    :", " ".join(docs[0].page_content.split())[:300], "...")

    chunks = split_transcript(docs)
    lengths = [len(c.page_content) for c in chunks]
    print(f"\nAfter RecursiveCharacterTextSplitter(chunk_size={config.YOUTUBE_CHUNK_SIZE}, "
          f"chunk_overlap={config.YOUTUBE_CHUNK_OVERLAP}):")
    print(f"  chunks: {len(chunks)} | length min/avg/max: {min(lengths)} / {round(sum(lengths) / len(lengths))} / {max(lengths)}")

    for i in sorted({0, len(chunks) // 2}):
        chunk = chunks[i]
        print(f"\nSample chunk #{i}:")
        print("  metadata:", {k: v for k, v in chunk.metadata.items() if k in ("chunk_id", "start_timestamp", "source")})
        print("  text    :", " ".join(chunk.page_content.split())[:350], "...")


if __name__ == "__main__":
    main()
