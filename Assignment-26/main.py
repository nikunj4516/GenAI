"""Task 5 & 6: FastAPI application serving the Groq chatbot / RAG backend.

Run:  uvicorn main:app --reload
Docs: http://127.0.0.1:8000/docs
"""
from __future__ import annotations

import time
from contextlib import asynccontextmanager

from fastapi import FastAPI, HTTPException, Request
from fastapi.concurrency import run_in_threadpool

from app import config
from app.chat_service import generate_answer, rag_ready, warm_up
from app.groq_service import GroqServiceError
from app.logger import get_logger
from app.rag_service import RAGError
from app.schemas import ChatRequest, ChatResponse, HealthResponse

logger = get_logger("api")


@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("Starting API | mode=%s | model=%s", config.CHAT_MODE, config.GROQ_MODEL)
    try:
        await run_in_threadpool(warm_up)
    except Exception as exc:  # the API must still start; /chat reports the problem
        logger.error("Warm-up failed (will retry on first request): %s", exc)
    yield
    logger.info("Shutting down API")


app = FastAPI(
    title="Groq Chatbot & RAG API",
    description="Low-latency LLM backend powered by the Groq API.",
    version="1.0.0",
    lifespan=lifespan,
)


@app.middleware("http")
async def log_requests(request: Request, call_next):
    started = time.perf_counter()
    response = await call_next(request)
    elapsed_ms = (time.perf_counter() - started) * 1000
    response.headers["X-Process-Time-ms"] = f"{elapsed_ms:.1f}"
    logger.info("%s %s -> %s (%.1f ms)", request.method, request.url.path, response.status_code, elapsed_ms)
    return response


@app.get("/", include_in_schema=False)
def root() -> dict:
    return {"message": "Groq Chatbot & RAG API is running.", "docs": "/docs", "health": "/health"}


@app.get("/health", response_model=HealthResponse, tags=["System"])
def health() -> HealthResponse:
    """Health check endpoint."""
    return HealthResponse(
        status="ok",
        model=config.GROQ_MODEL,
        mode=config.CHAT_MODE,
        rag_ready=rag_ready(),
        groq_key_configured=bool(config.GROQ_API_KEY),
    )


@app.post("/chat", response_model=ChatResponse, tags=["Chat"])
def chat(request: ChatRequest) -> ChatResponse:
    """Answer a question using the Groq-powered RAG (or plain chat) pipeline."""
    logger.info("POST /chat | query=%r", request.query[:120])
    try:
        answer = generate_answer(request.query)
    except GroqServiceError as exc:
        logger.error("Groq error (HTTP %s): %s", exc.status_code, exc.message)
        raise HTTPException(status_code=exc.status_code, detail=exc.message) from exc
    except RAGError as exc:
        logger.error("RAG error: %s", exc)
        raise HTTPException(status_code=503, detail=f"Knowledge base unavailable: {exc}") from exc
    except Exception as exc:
        logger.exception("Unexpected error while handling /chat")
        raise HTTPException(status_code=500, detail="Internal server error. Please try again later.") from exc
    return ChatResponse(answer=answer)


if __name__ == "__main__":
    import uvicorn

    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)
