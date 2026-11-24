"""
config.py - shared paths, model names, settings and test data used by every task file.

Values come from a local ".env" file (copy ".env.example" to ".env"). Real environment variables win.
The LLM provider is chosen with LLM_PROVIDER:  "openai" (default) or "ollama".
"""

import os
import warnings

ROOT = os.path.dirname(os.path.abspath(__file__))
warnings.filterwarnings("ignore")


def _load_env_file(path):
    """Tiny .env reader: KEY=VALUE lines."""
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

# ------------------------------------------------------------------ model provider
LLM_PROVIDER = os.getenv("LLM_PROVIDER", "openai").strip().lower()        # "openai" or "ollama"

OPENAI_CHAT_MODEL = os.getenv("OPENAI_CHAT_MODEL", "gpt-6-luna")
OPENAI_EMBEDDING_MODEL = os.getenv("OPENAI_EMBEDDING_MODEL", "text-embedding-3-small")
OPENAI_TEMPERATURE = os.getenv("OPENAI_TEMPERATURE", "").strip() or None   # not sent unless set

OLLAMA_MODEL = os.getenv("OLLAMA_MODEL", "llama3")
OLLAMA_EMBEDDING_MODEL = os.getenv("OLLAMA_EMBEDDING_MODEL", "nomic-embed-text")
OLLAMA_BASE_URL = os.getenv("OLLAMA_BASE_URL", "http://localhost:11434").rstrip("/")
OLLAMA_TEMPERATURE = 0.0                                                   # steady output for structured answers

# ------------------------------------------------------------------ documents (reused from Assignments 21-22)
DATA_DIR = os.path.join(ROOT, "data")
TXT_FILE = os.path.join(DATA_DIR, "notes.txt")
PDF_FILE = os.path.join(DATA_DIR, "company_handbook.pdf")
CSV_FILE = os.path.join(DATA_DIR, "Movie_recommendation.csv")
CSV_ROW_LIMIT = 200          # first 200 movies (set None for all 4,803 rows)

CHUNK_SIZE = 500
CHUNK_OVERLAP = 50
RETRIEVER_K = 4
VECTORSTORE_DIR = os.path.join(ROOT, "vectorstores")

# What the documents are about (used by the router of Task 6)
DOCUMENT_TOPICS = (
    "NovaTech Solutions company handbook (company overview, leave and work policy, IT and security rules), "
    "study notes about document loading, splitting and RAG, and a table of movies (plots, genres, taglines, keywords)"
)
NOT_FOUND_ANSWER = "I don't know based on the documents."

# ------------------------------------------------------------------ test data
PROMPT_INPUTS = [                       # Tasks 1, 2, 5, 8: general questions, no documents needed
    "What is a vector store?",
    "Why do we split documents into chunks?",
    "What does a retriever do in a RAG system?",
    "Explain overfitting to a beginner.",
    "What is the difference between an LLM and a chatbot?",
]

RAG_QUESTIONS = [                       # Tasks 3, 7, 9: answers are inside the documents (last one is not)
    "How many paid leave days does an employee get each year?",
    "What is chunk overlap and why is it used?",
    "How long must a password be and where must it be stored?",
    "Which movie is about a paraplegic Marine sent to the moon Pandora?",
    "Which superhero fights criminals in Gotham City?",
    "What is the capital of France?",   # NOT in the documents: the answer must say so
]

ROUTING_QUESTIONS = [                   # Task 6: (question, expected route)
    ("How many sick days do employees receive per year?", "factual"),
    ("What is chunk overlap and why is it used?", "factual"),
    ("Which movie is about a space war and a culture clash?", "factual"),
    ("Write a short motivational message for a team starting a new project.", "general"),
    ("Should I learn Python or JavaScript first?", "general"),
    ("Hello! How are you today?", "general"),
]

PARALLEL_QUESTION = "What are the rules for working from home?"
