"""
config.py - shared settings used by every task file.

Values come from a local ".env" file (copy ".env.example" to ".env"). Real environment variables win.
Ollama runs on your own computer, so it needs no API key. LangSmith (tracking) needs a free API key.
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

# ------------------------------------------------------------------ Ollama
OLLAMA_BASE_URL = os.getenv("OLLAMA_BASE_URL", "http://localhost:11434").rstrip("/")
OLLAMA_MODEL = os.getenv("OLLAMA_MODEL", "llama3")          # the assignment suggests llama3 or mistral
OLLAMA_TEMPERATURE = float(os.getenv("OLLAMA_TEMPERATURE", "0.7"))
OLLAMA_TIMEOUT = 300       # seconds: the first answer is slow because the model is loaded into memory

# ------------------------------------------------------------------ LangSmith
LANGSMITH_PLACEHOLDER = "your-langsmith-api-key-here"
LANGSMITH_PROJECT = os.getenv("LANGSMITH_PROJECT", "genai-assignment-24-ollama-chatbot")
os.environ["LANGSMITH_PROJECT"] = LANGSMITH_PROJECT

_key = os.getenv("LANGSMITH_API_KEY", "").strip()
if not _key or _key == LANGSMITH_PLACEHOLDER:
    os.environ.pop("LANGSMITH_API_KEY", None)               # no usable key -> tracing stays off
    os.environ["LANGSMITH_TRACING"] = "false"
else:
    # a real key is present: turn tracing on unless the user switched it off explicitly
    os.environ.setdefault("LANGSMITH_TRACING", "true")

# ------------------------------------------------------------------ task data
BASIC_PROMPT = "Explain what a large language model is in two simple sentences."
SYSTEM_PROMPT = "You are a friendly teacher. Answer in one short sentence for a beginner."
SYSTEM_QUESTION = "What is Ollama?"
TRACE_TAGS = ["assignment-24", "task-1", "ollama"]
