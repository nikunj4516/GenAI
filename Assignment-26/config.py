"""Central configuration.

Every secret and tunable comes from environment variables (optionally loaded
from a local `.env` file). Nothing sensitive is hard-coded.
"""
from __future__ import annotations

import os
from pathlib import Path

from dotenv import load_dotenv

PROJECT_ROOT = Path(__file__).resolve().parents[1]
load_dotenv(PROJECT_ROOT / ".env")

# --------------------------------------------------------------------------- #
# Groq / LLM
# --------------------------------------------------------------------------- #
GROQ_API_KEY: str = os.getenv("GROQ_API_KEY", "").strip()
# NOTE: llama-3.3-70b-versatile and llama-3.1-8b-instant were retired on
# 16 Aug 2026. openai/gpt-oss-120b is Groq's recommended replacement.
GROQ_MODEL: str = os.getenv("GROQ_MODEL", "openai/gpt-oss-120b").strip()
GROQ_TIMEOUT_SECONDS: float = float(os.getenv("GROQ_TIMEOUT_SECONDS", "30"))
GROQ_MAX_RETRIES: int = int(os.getenv("GROQ_MAX_RETRIES", "2"))
LLM_TEMPERATURE: float = float(os.getenv("LLM_TEMPERATURE", "0.2"))
# Reasoning models (gpt-oss) spend part of this budget on hidden reasoning,
# so keep it generous to avoid empty answers.
LLM_MAX_TOKENS: int = int(os.getenv("LLM_MAX_TOKENS", "1024"))
# Only sent for openai/gpt-oss-* models. Allowed: low | medium | high
GROQ_REASONING_EFFORT: str = os.getenv("GROQ_REASONING_EFFORT", "low").strip().lower()

# --------------------------------------------------------------------------- #
# Application behaviour
# --------------------------------------------------------------------------- #
CHAT_MODE: str = os.getenv("CHAT_MODE", "rag").strip().lower()  # "rag" | "chat"
if CHAT_MODE not in {"rag", "chat"}:
    raise ValueError(f"CHAT_MODE must be 'rag' or 'chat', got {CHAT_MODE!r}")

LOG_LEVEL: str = os.getenv("LOG_LEVEL", "INFO").strip().upper()
LOG_DIR: Path = PROJECT_ROOT / "logs"

# --------------------------------------------------------------------------- #
# RAG
# --------------------------------------------------------------------------- #
DATASET_FILENAME = "product_reviews_dataset.csv"
EMBEDDING_MODEL: str = os.getenv("EMBEDDING_MODEL", "sentence-transformers/all-MiniLM-L6-v2")
CHUNK_SIZE: int = int(os.getenv("CHUNK_SIZE", "500"))
CHUNK_OVERLAP: int = int(os.getenv("CHUNK_OVERLAP", "50"))
TOP_K: int = int(os.getenv("TOP_K", "5"))
VECTORSTORE_DIR: Path = PROJECT_ROOT / "vectorstore"


def find_dataset_path() -> Path:
    """Locate product_reviews_dataset.csv.

    Search order: $DATASET_PATH -> project folder -> parent folder (the GenAI
    root, where the dataset lives in the course layout) -> current directory.
    """
    candidates: list[Path] = []
    env_path = os.getenv("DATASET_PATH", "").strip()
    if env_path:
        candidates.append(Path(env_path).expanduser())
    candidates += [
        PROJECT_ROOT / DATASET_FILENAME,
        PROJECT_ROOT.parent / DATASET_FILENAME,
        Path.cwd() / DATASET_FILENAME,
    ]
    for path in candidates:
        if path.is_file():
            return path
    searched = "\n  - ".join(str(p) for p in candidates)
    raise FileNotFoundError(
        f"Could not find '{DATASET_FILENAME}'. Searched:\n  - {searched}\n"
        "Place the CSV in the project folder or set DATASET_PATH in .env."
    )
