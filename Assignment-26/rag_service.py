"""RAG pipeline (Task 3): load CSV -> chunk -> embed -> FAISS -> retrieve -> Groq answer."""
from __future__ import annotations

import json
import threading
from pathlib import Path

import faiss
import numpy as np
import pandas as pd

from app import config
from app.groq_service import groq_chat_messages
from app.logger import get_logger
from app.prompts import NO_ANSWER_MESSAGE, build_rag_messages

logger = get_logger(__name__)

INDEX_FILE = "index.faiss"
CHUNKS_FILE = "chunks.json"
META_FILE = "meta.json"


class RAGError(Exception):
    """Raised when the knowledge base cannot be built or loaded."""


# --------------------------------------------------------------------------- #
# Loading + chunking
# --------------------------------------------------------------------------- #
def load_documents(csv_path: Path) -> list[dict]:
    """Load the CSV; every row becomes one document made of 'column: value' pairs.

    This is schema-agnostic: whatever columns the reviews file has (product,
    rating, review text, ...) all end up in the searchable text.
    """
    try:
        df = pd.read_csv(csv_path)
    except UnicodeDecodeError:
        df = pd.read_csv(csv_path, encoding="latin-1")
    except Exception as exc:  # malformed CSV, empty file, ...
        raise RAGError(f"Could not read dataset '{csv_path}': {exc}") from exc

    df.columns = [str(c).strip() for c in df.columns]
    documents: list[dict] = []
    for row_number, (_, row) in enumerate(df.iterrows(), start=1):
        parts = [
            f"{col}: {str(value).strip()}"
            for col, value in row.items()
            if pd.notna(value) and str(value).strip()
        ]
        if parts:
            documents.append({"doc_id": row_number, "text": " | ".join(parts)})
    return documents


def split_text(text: str, chunk_size: int = 500, overlap: int = 50) -> list[str]:
    """Split text into overlapping chunks without cutting words in half."""
    if chunk_size <= 0:
        raise ValueError("chunk_size must be positive")
    if overlap < 0 or overlap >= chunk_size:
        raise ValueError("overlap must be >= 0 and smaller than chunk_size")

    text = " ".join(text.split())
    if not text:
        return []
    if len(text) <= chunk_size:
        return [text]

    chunks: list[str] = []
    start = 0
    while start < len(text):
        end = min(start + chunk_size, len(text))
        if end < len(text):
            space = text.rfind(" ", start + chunk_size // 2, end)
            if space != -1:
                end = space
        chunk = text[start:end].strip()
        if chunk:
            chunks.append(chunk)
        if end >= len(text):
            break
        new_start = max(end - overlap, start + 1)
        if text[new_start - 1] != " ":  # landed mid-word: move to the next word start
            nxt = text.find(" ", new_start)
            if nxt != -1 and nxt < end:
                new_start = nxt + 1
        start = new_start
    return chunks


def chunk_documents(documents: list[dict], chunk_size: int, overlap: int) -> list[dict]:
    chunks: list[dict] = []
    for doc in documents:
        for piece in split_text(doc["text"], chunk_size, overlap):
            chunks.append({"chunk_id": len(chunks), "doc_id": doc["doc_id"], "text": piece})
    return chunks


# --------------------------------------------------------------------------- #
# Pipeline
# --------------------------------------------------------------------------- #
class RAGPipeline:
    def __init__(self, csv_path: Path | str | None = None) -> None:
        self._csv_path = Path(csv_path) if csv_path else None
        self._embedder = None
        self._index: faiss.Index | None = None
        self._chunks: list[dict] = []
        self._meta: dict = {}
        self._lock = threading.Lock()
        self._ready = False

    # -- helpers ----------------------------------------------------------- #
    @property
    def ready(self) -> bool:
        return self._ready

    def stats(self) -> dict:
        return {
            "documents": self._meta.get("num_documents", 0),
            "chunks": self._meta.get("num_chunks", 0),
            "embedding_model": config.EMBEDDING_MODEL,
            "dataset": self._meta.get("fingerprint", {}).get("csv_name", ""),
        }

    def _get_embedder(self):
        if self._embedder is None:
            logger.info("Loading embedding model: %s", config.EMBEDDING_MODEL)
            try:
                from sentence_transformers import SentenceTransformer

                self._embedder = SentenceTransformer(config.EMBEDDING_MODEL)
            except Exception as exc:  # missing package, no internet on first download, bad name
                raise RAGError(
                    f"Could not load embedding model '{config.EMBEDDING_MODEL}': {exc}"
                ) from exc
        return self._embedder

    def _embed(self, texts: list[str]) -> np.ndarray:
        vectors = self._get_embedder().encode(
            texts,
            batch_size=64,
            convert_to_numpy=True,
            normalize_embeddings=True,  # cosine similarity == inner product
            show_progress_bar=len(texts) > 1000,
        )
        return np.ascontiguousarray(vectors, dtype="float32")

    @staticmethod
    def _fingerprint(csv_path: Path) -> dict:
        stat = csv_path.stat()
        return {
            "csv_name": csv_path.name,
            "csv_size": stat.st_size,
            "csv_mtime_ns": stat.st_mtime_ns,
            "embedding_model": config.EMBEDDING_MODEL,
            "chunk_size": config.CHUNK_SIZE,
            "chunk_overlap": config.CHUNK_OVERLAP,
        }

    # -- persistence ------------------------------------------------------- #
    def _try_load(self, fingerprint: dict) -> bool:
        store = config.VECTORSTORE_DIR
        files = [store / INDEX_FILE, store / CHUNKS_FILE, store / META_FILE]
        if not all(f.is_file() for f in files):
            return False
        try:
            meta = json.loads(files[2].read_text(encoding="utf-8"))
            if meta.get("fingerprint") != fingerprint:
                logger.info("Vector store is stale (dataset or settings changed); rebuilding.")
                return False
            # bytes round-trip avoids FAISS path-encoding problems on Windows
            index = faiss.deserialize_index(np.frombuffer(files[0].read_bytes(), dtype="uint8"))
            chunks = json.loads(files[1].read_text(encoding="utf-8"))
            if index.ntotal != len(chunks):
                return False
        except Exception as exc:
            logger.warning("Could not load saved vector store (%s); rebuilding.", exc)
            return False
        self._index, self._chunks, self._meta = index, chunks, meta
        logger.info("Loaded vector store from disk: %d chunks", len(chunks))
        return True

    def _save(self) -> None:
        store = config.VECTORSTORE_DIR
        try:
            store.mkdir(parents=True, exist_ok=True)
            (store / INDEX_FILE).write_bytes(faiss.serialize_index(self._index).tobytes())
            (store / CHUNKS_FILE).write_text(json.dumps(self._chunks, ensure_ascii=False), encoding="utf-8")
            (store / META_FILE).write_text(json.dumps(self._meta, indent=2), encoding="utf-8")
        except OSError as exc:
            logger.warning("Could not save vector store (continuing in memory): %s", exc)

    def _build(self, csv_path: Path, fingerprint: dict) -> None:
        logger.info("Building vector store from %s", csv_path)
        documents = load_documents(csv_path)
        if not documents:
            raise RAGError(f"Dataset '{csv_path.name}' contains no usable rows.")
        chunks = chunk_documents(documents, config.CHUNK_SIZE, config.CHUNK_OVERLAP)
        embeddings = self._embed([c["text"] for c in chunks])
        index = faiss.IndexFlatIP(embeddings.shape[1])
        index.add(embeddings)
        self._index, self._chunks = index, chunks
        self._meta = {
            "fingerprint": fingerprint,
            "num_documents": len(documents),
            "num_chunks": len(chunks),
        }
        self._save()
        logger.info("Vector store ready: %d documents -> %d chunks", len(documents), len(chunks))

    def build_or_load(self) -> None:
        """Load the saved FAISS index if it matches the dataset, otherwise build it."""
        with self._lock:
            if self._ready:
                return
            try:
                csv_path = self._csv_path or config.find_dataset_path()
            except FileNotFoundError as exc:
                raise RAGError(str(exc)) from exc
            fingerprint = self._fingerprint(csv_path)
            if not self._try_load(fingerprint):
                self._build(csv_path, fingerprint)
            self._ready = True

    # -- retrieval + generation ------------------------------------------- #
    def retrieve(self, query: str, k: int | None = None) -> list[dict]:
        self.build_or_load()
        k = min(k or config.TOP_K, self._index.ntotal)
        scores, ids = self._index.search(self._embed([query]), k)
        results = []
        for score, idx in zip(scores[0], ids[0]):
            if idx < 0:
                continue
            chunk = self._chunks[int(idx)]
            results.append({**chunk, "score": float(score)})
        return results

    def answer(self, query: str) -> dict:
        """Retrieve context, build the grounded prompt, call Groq, return answer + sources."""
        sources = self.retrieve(query)
        if not sources:
            return {"answer": NO_ANSWER_MESSAGE, "sources": []}
        messages = build_rag_messages([s["text"] for s in sources], query)
        answer = groq_chat_messages(messages, temperature=0.1)
        return {"answer": answer, "sources": sources}


_pipeline: RAGPipeline | None = None
_pipeline_lock = threading.Lock()


def get_rag_pipeline() -> RAGPipeline:
    """Process-wide singleton so the index is built/loaded once."""
    global _pipeline
    with _pipeline_lock:
        if _pipeline is None:
            _pipeline = RAGPipeline()
        return _pipeline
