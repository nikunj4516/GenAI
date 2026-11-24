"""Groq LLM access (Tasks 1, 2 and 6): client, chat function and error mapping."""
from __future__ import annotations

import time

import groq
from groq import Groq

from app import config
from app.logger import get_logger
from app.prompts import DEFAULT_SYSTEM_PROMPT

logger = get_logger(__name__)


class GroqServiceError(Exception):
    """Raised for any Groq failure. `status_code` is the HTTP status the API should return."""

    def __init__(self, message: str, status_code: int = 502) -> None:
        super().__init__(message)
        self.message = message
        self.status_code = status_code


class GroqConfigError(GroqServiceError):
    """Raised when the service is not configured (e.g. missing API key)."""

    def __init__(self, message: str) -> None:
        super().__init__(message, status_code=503)


_client: Groq | None = None


def get_client() -> Groq:
    """Create the Groq client lazily so the app can start (and /health work) without a key."""
    global _client
    if not config.GROQ_API_KEY:
        raise GroqConfigError(
            "GROQ_API_KEY is not set. Add it to your .env file or environment variables."
        )
    if _client is None:
        _client = Groq(
            api_key=config.GROQ_API_KEY,
            timeout=config.GROQ_TIMEOUT_SECONDS,
            max_retries=config.GROQ_MAX_RETRIES,
        )
    return _client


def groq_chat_messages(
    messages: list[dict[str, str]],
    *,
    temperature: float | None = None,
    max_tokens: int | None = None,
) -> str:
    """Send a full message list to Groq and return the text reply."""
    client = get_client()
    model = config.GROQ_MODEL

    kwargs: dict = {
        "model": model,
        "messages": messages,
        "temperature": config.LLM_TEMPERATURE if temperature is None else temperature,
        "max_completion_tokens": max_tokens or config.LLM_MAX_TOKENS,
    }
    if model.startswith("openai/gpt-oss") and config.GROQ_REASONING_EFFORT in {"low", "medium", "high"}:
        kwargs["extra_body"] = {"reasoning_effort": config.GROQ_REASONING_EFFORT}

    started = time.perf_counter()
    try:
        completion = client.chat.completions.create(**kwargs)
    except groq.AuthenticationError as exc:
        logger.error("Groq authentication failed: %s", exc)
        raise GroqServiceError("Groq rejected the API key. Check GROQ_API_KEY.", 503) from exc
    except groq.RateLimitError as exc:
        logger.warning("Groq rate limit hit: %s", exc)
        raise GroqServiceError("Groq rate limit reached. Please retry shortly.", 429) from exc
    except groq.APITimeoutError as exc:
        logger.error("Groq request timed out: %s", exc)
        raise GroqServiceError("The request to Groq timed out. Please retry.", 504) from exc
    except groq.APIConnectionError as exc:
        logger.error("Could not reach Groq: %s", exc)
        raise GroqServiceError("Could not connect to Groq. Check your network.", 503) from exc
    except groq.APIStatusError as exc:
        logger.error("Groq API error %s: %s", exc.status_code, exc)
        raise GroqServiceError(
            f"Groq returned an error (HTTP {exc.status_code}). "
            "If this persists, check that GROQ_MODEL is still available.",
            502,
        ) from exc
    except groq.GroqError as exc:
        logger.error("Groq SDK error: %s", exc)
        raise GroqServiceError("Unexpected Groq SDK error.", 502) from exc

    elapsed = time.perf_counter() - started
    content = (completion.choices[0].message.content or "").strip() if completion.choices else ""
    usage = getattr(completion, "usage", None)
    logger.info(
        "Groq call ok | model=%s | latency=%.2fs | total_tokens=%s",
        model,
        elapsed,
        getattr(usage, "total_tokens", "n/a"),
    )
    if not content:
        logger.error("Groq returned an empty message (finish_reason=%s)", completion.choices[0].finish_reason if completion.choices else "n/a")
        raise GroqServiceError(
            "Groq returned an empty response. Try increasing LLM_MAX_TOKENS.", 502
        )
    return content


def groq_chat(prompt: str, system_prompt: str | None = None) -> str:
    """Task 2 core function: system + user message in, model response out."""
    if not isinstance(prompt, str) or not prompt.strip():
        raise ValueError("prompt must be a non-empty string")
    messages = [
        {"role": "system", "content": system_prompt or DEFAULT_SYSTEM_PROMPT},
        {"role": "user", "content": prompt.strip()},
    ]
    return groq_chat_messages(messages)
