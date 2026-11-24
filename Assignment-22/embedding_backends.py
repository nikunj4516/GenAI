"""
embedding_backends.py - one place that creates the three embedding models.

    get_embeddings("openai")       -> OpenAIEmbeddings        (cloud, needs OPENAI_API_KEY)
    get_embeddings("huggingface")  -> HuggingFaceEmbeddings   (local, free, downloads a model once)
    get_embeddings("ollama")       -> OllamaEmbeddings        (local, needs the Ollama app running)

If a backend cannot be used, BackendUnavailable is raised with a message that says how to fix it.
"""

import json
import os
import sys
import time
import urllib.request
from functools import lru_cache

ROOT = os.path.dirname(os.path.abspath(__file__))
if ROOT not in sys.path:
    sys.path.insert(0, ROOT)

import config  # import first: loads .env, hides warnings


class BackendUnavailable(Exception):
    """Raised when an embedding backend cannot be used (missing key, Ollama not running ...)."""


def choose_backend(default=config.DEFAULT_BACKEND):
    """Backend name from the command line (first argument) or the default."""
    name = sys.argv[1].lower() if len(sys.argv) > 1 else default
    if name not in config.BACKENDS:
        raise SystemExit(f"Unknown backend '{name}'. Choose one of: {', '.join(config.BACKENDS)}")
    return name


# ----------------------------------------------------------------------------- OpenAI
def _openai():
    if not os.getenv("OPENAI_API_KEY") or os.getenv("OPENAI_API_KEY") == "your-openai-api-key-here":
        raise BackendUnavailable(
            "OPENAI_API_KEY is not set.\n"
            "  -> Copy '.env.example' to '.env' and paste your key after OPENAI_API_KEY="
        )
    from langchain_openai import OpenAIEmbeddings

    # check_embedding_ctx_length=False sends plain text (our chunks are far below the token limit)
    return OpenAIEmbeddings(model=config.OPENAI_EMBEDDING_MODEL, check_embedding_ctx_length=False)


# ----------------------------------------------------------------------------- Hugging Face
def _huggingface():
    try:
        from langchain_huggingface import HuggingFaceEmbeddings

        return HuggingFaceEmbeddings(
            model_name=config.HF_EMBEDDING_MODEL,
            encode_kwargs={"normalize_embeddings": True},   # unit-length vectors -> cosine = dot product
        )
    except Exception as error:
        raise BackendUnavailable(
            f"Could not load the Hugging Face model '{config.HF_EMBEDDING_MODEL}' "
            f"({type(error).__name__}).\n"
            "  -> Run 'pip install sentence-transformers' and make sure you are online "
            "for the first download (about 90 MB)."
        )


# ----------------------------------------------------------------------------- Ollama
def ollama_models():
    """Names of the models installed in the local Ollama app (raises if Ollama is not running)."""
    with urllib.request.urlopen(f"{config.OLLAMA_BASE_URL}/api/tags", timeout=5) as response:
        data = json.loads(response.read().decode("utf-8"))
    return [m["name"] for m in data.get("models", [])]


def _ollama():
    try:
        installed = ollama_models()
    except Exception:
        raise BackendUnavailable(
            f"Ollama is not running at {config.OLLAMA_BASE_URL}.\n"
            "  -> Install Ollama from https://ollama.com, start it, then run:\n"
            f"     ollama pull {config.OLLAMA_EMBEDDING_MODEL}"
        )
    wanted = config.OLLAMA_EMBEDDING_MODEL
    if not any(name == wanted or name.split(":")[0] == wanted for name in installed):
        raise BackendUnavailable(
            f"Ollama is running but the model '{wanted}' is not installed.\n"
            f"  -> Run:  ollama pull {wanted}"
        )
    from langchain_ollama import OllamaEmbeddings

    return OllamaEmbeddings(model=wanted, base_url=config.OLLAMA_BASE_URL)


# ----------------------------------------------------------------------------- public API
_BUILDERS = {"openai": _openai, "huggingface": _huggingface, "ollama": _ollama}


@lru_cache(maxsize=None)
def get_embeddings(backend):
    """Return a LangChain Embeddings object for 'openai', 'huggingface' or 'ollama'."""
    if backend not in _BUILDERS:
        raise ValueError(f"Unknown backend '{backend}'. Choose one of: {', '.join(config.BACKENDS)}")
    return _BUILDERS[backend]()


def model_name(backend):
    return {
        "openai": config.OPENAI_EMBEDDING_MODEL,
        "huggingface": config.HF_EMBEDDING_MODEL,
        "ollama": config.OLLAMA_EMBEDDING_MODEL,
    }[backend]


def available_backends(verbose=False):
    """Backends that can be used right now."""
    usable = []
    for backend in config.BACKENDS:
        try:
            get_embeddings(backend)
            usable.append(backend)
        except BackendUnavailable as error:
            if verbose:
                print(f"  [{backend}] not available: {str(error).splitlines()[0]}")
    return usable


def embed_with_timing(embeddings, texts):
    """Return (vectors, seconds) for a list of texts."""
    start = time.perf_counter()
    vectors = embeddings.embed_documents(texts)
    return vectors, time.perf_counter() - start


def fail(message):
    """Print a clear message and stop the current task (run_all.py continues with the next one)."""
    print("\n" + message)
    sys.exit(1)
