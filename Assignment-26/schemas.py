"""Pydantic request/response models (Task 6: request validation)."""
from __future__ import annotations

from pydantic import BaseModel, ConfigDict, Field


class ChatRequest(BaseModel):
    # whitespace is stripped BEFORE length checks, so "   " is rejected as empty
    model_config = ConfigDict(
        str_strip_whitespace=True,
        json_schema_extra={"example": {"query": "What do customers say about battery life?"}},
    )

    query: str = Field(..., min_length=1, max_length=2000, description="Your question")


class ChatResponse(BaseModel):
    answer: str = Field(..., description="Model response")


class HealthResponse(BaseModel):
    status: str
    model: str
    mode: str
    rag_ready: bool
    groq_key_configured: bool
