"""Single entry point used by the API: routes a question to RAG or plain chat."""
from __future__ import annotations

from app import config
from app.groq_service import groq_chat
from app.rag_service import get_rag_pipeline


def generate_answer(query: str) -> str:
    if config.CHAT_MODE == "rag":
        return get_rag_pipeline().answer(query)["answer"]
    return groq_chat(query)


def warm_up() -> None:
    """Build/load the vector store at startup so the first request is fast."""
    if config.CHAT_MODE == "rag":
        get_rag_pipeline().build_or_load()


def rag_ready() -> bool:
    return config.CHAT_MODE == "rag" and get_rag_pipeline().ready
