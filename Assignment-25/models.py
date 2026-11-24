"""
models.py - creates the chat model and the embedding model for every task.

    get_llm()         -> ChatOpenAI  or  ChatOllama       (chosen by LLM_PROVIDER in .env)
    get_embeddings()  -> OpenAIEmbeddings or OllamaEmbeddings (same provider)
    provider_label()  -> short text such as "openai / gpt-6-luna"

If the provider is not ready (no key, Ollama not running, model not pulled) ModelNotConfigured is raised
with a message that says how to fix it.
"""

import json
import os
import sys
import urllib.error
import urllib.request

ROOT = os.path.dirname(os.path.abspath(__file__))
if ROOT not in sys.path:
    sys.path.insert(0, ROOT)

import config  # import first: loads .env, hides warnings


class ModelNotConfigured(Exception):
    """The chosen LLM provider is not ready to be used."""


def provider_label():
    if config.LLM_PROVIDER == "ollama":
        return f"ollama / {config.OLLAMA_MODEL}"
    return f"openai / {config.OPENAI_CHAT_MODEL}"


def _ollama_get(path):
    with urllib.request.urlopen(f"{config.OLLAMA_BASE_URL}{path}", timeout=5) as response:
        return json.loads(response.read().decode("utf-8"))


def check_provider(need_embeddings=False):
    """Raise ModelNotConfigured (with instructions) when the provider cannot be used."""
    if config.LLM_PROVIDER == "openai":
        key = os.getenv("OPENAI_API_KEY", "")
        if not key or key == "your-openai-api-key-here":
            raise ModelNotConfigured(
                "OPENAI_API_KEY is not set.\n"
                "  -> Copy '.env.example' to '.env' and paste your key after OPENAI_API_KEY=\n"
                "     (or use the free local option: set LLM_PROVIDER=ollama in .env)"
            )
    elif config.LLM_PROVIDER == "ollama":
        try:
            installed = [m["name"] for m in _ollama_get("/api/tags").get("models", [])]
        except (urllib.error.URLError, OSError, ValueError):
            raise ModelNotConfigured(
                f"Cannot reach the Ollama server at {config.OLLAMA_BASE_URL}.\n"
                "  -> Install Ollama (https://ollama.com/download) and start it (the app, or `ollama serve`)."
            )
        wanted = [config.OLLAMA_MODEL] + ([config.OLLAMA_EMBEDDING_MODEL] if need_embeddings else [])
        for name in wanted:
            full = name if ":" in name else name + ":latest"
            if full not in installed:
                raise ModelNotConfigured(
                    f"The Ollama model '{name}' has not been pulled (you have: {', '.join(installed) or 'none'}).\n"
                    f"  -> Run:  ollama pull {name}"
                )
    else:
        raise ModelNotConfigured(f"LLM_PROVIDER must be 'openai' or 'ollama' (it is '{config.LLM_PROVIDER}').")


def get_llm(**overrides):
    """The chat model used by all chains."""
    check_provider()
    if config.LLM_PROVIDER == "ollama":
        from langchain_ollama import ChatOllama

        settings = {"model": config.OLLAMA_MODEL, "base_url": config.OLLAMA_BASE_URL,
                    "temperature": config.OLLAMA_TEMPERATURE, "client_kwargs": {"timeout": 300}}
        settings.update(overrides)
        return ChatOllama(**settings)

    from langchain_openai import ChatOpenAI

    settings = {"model": config.OPENAI_CHAT_MODEL, "timeout": 90, "max_retries": 2}
    if config.OPENAI_TEMPERATURE is not None:          # some newer models only accept their default temperature
        settings["temperature"] = float(config.OPENAI_TEMPERATURE)
    settings.update(overrides)
    return ChatOpenAI(**settings)


def get_embeddings():
    """The embedding model used for the vector store."""
    check_provider(need_embeddings=True)
    if config.LLM_PROVIDER == "ollama":
        from langchain_ollama import OllamaEmbeddings

        return OllamaEmbeddings(model=config.OLLAMA_EMBEDDING_MODEL, base_url=config.OLLAMA_BASE_URL)

    from langchain_openai import OpenAIEmbeddings

    return OpenAIEmbeddings(model=config.OPENAI_EMBEDDING_MODEL, check_embedding_ctx_length=False)


def embedding_name():
    return config.OLLAMA_EMBEDDING_MODEL if config.LLM_PROVIDER == "ollama" else config.OPENAI_EMBEDDING_MODEL


def explain_error(error):
    """Turn an exception into a short message that says what to check."""
    name, text = type(error).__name__, str(error)
    if name.endswith("AuthenticationError"):
        hint = "The API key was rejected. Check OPENAI_API_KEY in your .env file."
    elif name.endswith("NotFoundError"):
        hint = f"The model was not found for your account. Change OPENAI_CHAT_MODEL / OPENAI_EMBEDDING_MODEL in .env."
    elif name.endswith("RateLimitError"):
        hint = "Rate limit or no credit left. Check billing at https://platform.openai.com/."
    elif name.endswith("BadRequestError") and "temperature" in text.lower():
        hint = "This model does not accept a custom temperature. Leave OPENAI_TEMPERATURE empty in .env."
    elif name.endswith(("APIConnectionError", "APITimeoutError", "ConnectError", "ConnectionError")):
        hint = "Could not reach the model server. Check your internet connection (or that Ollama is running)."
    elif name == "ResponseError":
        hint = "Ollama rejected the request. Is the model pulled?  (ollama list)"
    else:
        hint = "See the error above."
    return f"The model request failed ({name}): {text[:300]}\n  -> {hint}"


def fail(message):
    """Print a clear message and stop the current task (run_all.py continues with the next one)."""
    print("\n" + message)
    sys.exit(1)


def fail_llm(error):
    fail(explain_error(error))
