"""
config.py - shared paths, model names and settings used by every task file.

API keys are read from a local ".env" file (copy ".env.example" to ".env").
"""

import os
import warnings

ROOT = os.path.dirname(os.path.abspath(__file__))


def _load_env_file(path):
    """Tiny .env reader: KEY=VALUE lines. Real environment variables win."""
    if not os.path.exists(path):
        return
    with open(path, encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith("#") or "=" not in line:
                continue
            key, value = line.split("=", 1)
            os.environ.setdefault(key.strip(), value.strip().strip('"').strip("'"))


_load_env_file(os.path.join(ROOT, ".env"))

# ------------------------------------------------------------------ data
DATA_DIR = os.path.join(ROOT, "data")
TXT_FILE = os.path.join(DATA_DIR, "notes.txt")
CSV_FILE = os.path.join(DATA_DIR, "Movie_recommendation.csv")
PDF_FILE = os.path.join(DATA_DIR, "company_handbook.pdf")
WEB_URL = "https://en.wikipedia.org/wiki/Natural_language_processing"

INCLUDE_WEB = True        # web page is skipped automatically when there is no internet
CSV_ROW_LIMIT = 100       # use the first 100 movies (set to None for all 4,803 rows)

# ------------------------------------------------------------------ splitting (same as Task 21)
CHUNK_SIZE = 500
CHUNK_OVERLAP = 50

# ------------------------------------------------------------------ embedding models
OPENAI_EMBEDDING_MODEL = os.getenv("OPENAI_EMBEDDING_MODEL", "text-embedding-3-small")
HF_EMBEDDING_MODEL = os.getenv("HF_EMBEDDING_MODEL", "sentence-transformers/all-MiniLM-L6-v2")
OLLAMA_EMBEDDING_MODEL = os.getenv("OLLAMA_EMBEDDING_MODEL", "nomic-embed-text")
OLLAMA_BASE_URL = os.getenv("OLLAMA_BASE_URL", "http://localhost:11434")

BACKENDS = ("openai", "huggingface", "ollama")
VECTOR_STORES = ("faiss", "chroma")
DEFAULT_BACKEND = "huggingface"     # free + local, so tasks 7, 8 and 10 run without an API key
DEFAULT_STORE = "faiss"

# ------------------------------------------------------------------ vector store locations
VECTORSTORE_DIR = os.path.join(ROOT, "vectorstores")

# Number of chunks embedded in Tasks 1, 2 and 6 (kept small: fast and cheap)
SAMPLE_CHUNKS = 20

# Queries used by the search tasks (one for each kind of document)
TEST_QUERIES = [
    "How many paid leave days does an employee get each year?",   # PDF
    "What is chunk overlap and why is it used?",                  # TXT
    "a movie about a space war on a distant moon",                # CSV
    "Which superhero fights criminals in Gotham city?",           # CSV
]

# ------------------------------------------------------------------ environment hygiene
os.environ.setdefault("USER_AGENT", "GenAI-Task22-Nikunj/1.0")
os.environ.setdefault("ANONYMIZED_TELEMETRY", "False")     # ChromaDB telemetry off
os.environ.setdefault("TOKENIZERS_PARALLELISM", "false")
warnings.filterwarnings("ignore", category=DeprecationWarning)
warnings.filterwarnings("ignore", category=FutureWarning)
