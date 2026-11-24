"""
openai_models.py - creates the OpenAI chat model and embedding model for every task.

    get_llm()         -> ChatOpenAI          (answers, query rewriting, extraction)
    get_embeddings()  -> OpenAIEmbeddings    (text -> vectors)

If the API key is missing, OpenAINotConfigured is raised with a message that says how to fix it.
"""

import os
import sys

ROOT = os.path.dirname(os.path.abspath(__file__))
if ROOT not in sys.path:
    sys.path.insert(0, ROOT)

import config  # import first: loads .env, hides warnings


class OpenAINotConfigured(Exception):
    """Raised when OPENAI_API_KEY is missing."""


def require_api_key():
    key = os.getenv("OPENAI_API_KEY", "")
    if not key or key == "your-openai-api-key-here":
        raise OpenAINotConfigured(
            "OPENAI_API_KEY is not set.\n"
            "  -> Copy '.env.example' to '.env' and paste your key after OPENAI_API_KEY=\n"
            "     (create a key at https://platform.openai.com/api-keys)"
        )
    return key


def get_llm(**overrides):
    """ChatOpenAI with the model from config.OPENAI_CHAT_MODEL."""
    require_api_key()
    from langchain_openai import ChatOpenAI

    settings = {"model": config.OPENAI_CHAT_MODEL, "timeout": 90, "max_retries": 2}
    if config.OPENAI_TEMPERATURE is not None:
        settings["temperature"] = float(config.OPENAI_TEMPERATURE)
    settings.update(overrides)
    return ChatOpenAI(**settings)


def get_embeddings():
    """OpenAIEmbeddings with the model from config.OPENAI_EMBEDDING_MODEL."""
    require_api_key()
    from langchain_openai import OpenAIEmbeddings

    # check_embedding_ctx_length=False sends plain text (all our chunks are far below the limit)
    return OpenAIEmbeddings(model=config.OPENAI_EMBEDDING_MODEL, check_embedding_ctx_length=False)


def fail(message):
    """Print a clear message and stop the current task (run_all.py continues with the next one)."""
    print("\n" + message)
    sys.exit(1)


def explain_error(error):
    """Turn an exception into a short message that says what to check."""
    name = type(error).__name__
    text = str(error)
    if name == "AuthenticationError":
        hint = "The API key was rejected. Check OPENAI_API_KEY in your .env file."
    elif name == "NotFoundError":
        hint = (f"The model was not found for your account. Set OPENAI_CHAT_MODEL / "
                f"OPENAI_EMBEDDING_MODEL in .env (now: {config.OPENAI_CHAT_MODEL} / {config.OPENAI_EMBEDDING_MODEL}).")
    elif name == "RateLimitError":
        hint = "Rate limit or no credit left. Check billing at https://platform.openai.com/."
    elif name in ("APIConnectionError", "APITimeoutError", "ConnectError"):
        hint = "Could not reach OpenAI. Check your internet connection."
    elif name == "BadRequestError" and "temperature" in text.lower():
        hint = "This model does not accept a custom temperature. Leave OPENAI_TEMPERATURE empty in .env."
    else:
        hint = "See the error above."
    return f"The OpenAI request failed ({name}): {text[:300]}\n  -> {hint}"


def fail_openai(error):
    fail(explain_error(error))
