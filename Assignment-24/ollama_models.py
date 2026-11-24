"""
ollama_models.py - everything about the local Ollama server and the LangChain Ollama wrappers.

    check_server()          -> version string of the running Ollama server (or OllamaNotReady)
    list_models()           -> names of the models you have pulled
    model_is_pulled(name)   -> True / False
    pull_model(name)        -> downloads a model (same as `ollama pull <name>`), with progress
    get_llm()               -> OllamaLLM   (LangChain "LLM" wrapper: text in, text out)
    get_chat_model()        -> ChatOllama  (LangChain chat wrapper: messages in, message out)
"""

import json
import os
import sys
import urllib.error
import urllib.request

ROOT = os.path.dirname(os.path.abspath(__file__))
if ROOT not in sys.path:
    sys.path.insert(0, ROOT)

import config  # import first: loads .env


class OllamaNotReady(Exception):
    """Ollama is not installed / not running, or the model has not been pulled."""


INSTALL_HELP = (
    "  1. Install Ollama:  https://ollama.com/download   (Windows / macOS installer, or on Linux:\n"
    "     curl -fsSL https://ollama.com/install.sh | sh)\n"
    "  2. Start it:        the desktop app starts the server by itself; otherwise run  `ollama serve`\n"
    f"  3. Check it:        open {config.OLLAMA_BASE_URL} in a browser -> it says \"Ollama is running\""
)


def _client():
    from ollama import Client

    return Client(host=config.OLLAMA_BASE_URL, timeout=config.OLLAMA_TIMEOUT)


def check_server():
    """Return the Ollama server version, or raise OllamaNotReady with instructions."""
    try:
        with urllib.request.urlopen(f"{config.OLLAMA_BASE_URL}/api/version", timeout=5) as response:
            return json.loads(response.read().decode("utf-8")).get("version", "unknown")
    except (urllib.error.URLError, OSError, ValueError) as error:
        raise OllamaNotReady(
            f"Cannot reach the Ollama server at {config.OLLAMA_BASE_URL}  ({type(error).__name__}).\n"
            f"{INSTALL_HELP}"
        )


def list_models():
    try:
        return [m.model for m in _client().list().models]
    except Exception as error:
        raise OllamaNotReady(f"Could not list the Ollama models: {type(error).__name__}: {error}")


def _same_model(wanted, installed):
    """'llama3' matches 'llama3:latest'; 'llama3:8b' only matches 'llama3:8b'."""
    if ":" not in wanted:
        wanted += ":latest"
    return wanted == installed


def model_is_pulled(name=None):
    name = name or config.OLLAMA_MODEL
    return any(_same_model(name, installed) for installed in list_models())


def pull_model(name=None):
    """Download a model with a progress line (needs internet; llama3 is about 4.7 GB)."""
    name = name or config.OLLAMA_MODEL
    print(f"Pulling '{name}' (this can take several minutes the first time)...")
    last = None
    try:
        for part in _client().pull(name, stream=True):
            status = part.status or ""
            if part.total and part.completed is not None:
                line = f"  {status}: {part.completed * 100 // part.total}%"
            else:
                line = f"  {status}"
            if line != last:
                print(line)
                last = line
    except Exception as error:
        raise OllamaNotReady(
            f"Could not pull '{name}': {type(error).__name__}: {error}\n"
            "  -> Check the model name at https://ollama.com/library and your internet connection."
        )


def ensure_model(pull=False):
    """Make sure config.OLLAMA_MODEL is available; pull it when `pull` is True."""
    if model_is_pulled():
        return
    if pull:
        pull_model()
        if model_is_pulled():
            return
    pulled = ", ".join(list_models()) or "none"
    raise OllamaNotReady(
        f"The model '{config.OLLAMA_MODEL}' has not been pulled yet (models you have: {pulled}).\n"
        f"  -> Run:  ollama pull {config.OLLAMA_MODEL}\n"
        "     or run this task again with --pull to let the script do it."
    )


def get_llm(**overrides):
    """LangChain OllamaLLM - the 'Ollama LLM wrapper' of the assignment."""
    from langchain_ollama import OllamaLLM

    settings = {
        "model": config.OLLAMA_MODEL,
        "base_url": config.OLLAMA_BASE_URL,
        "temperature": config.OLLAMA_TEMPERATURE,
        "client_kwargs": {"timeout": config.OLLAMA_TIMEOUT},
    }
    settings.update(overrides)
    return OllamaLLM(**settings)


def get_chat_model(**overrides):
    """LangChain ChatOllama - same model, but with system/human messages."""
    from langchain_ollama import ChatOllama

    settings = {
        "model": config.OLLAMA_MODEL,
        "base_url": config.OLLAMA_BASE_URL,
        "temperature": config.OLLAMA_TEMPERATURE,
        "client_kwargs": {"timeout": config.OLLAMA_TIMEOUT},
    }
    settings.update(overrides)
    return ChatOllama(**settings)


def fail(message):
    """Print a clear message and stop the current task (run_all.py continues with the next one)."""
    print("\n" + message)
    sys.exit(1)
