"""
schemas.py - the Pydantic models that describe the structured output of the LLM.

    Answer         chatbot answer: answer + confidence + source   (Tasks 3, 4, 6)
    RouteDecision  factual / general decision                       (Task 6)
    FollowUps      suggested follow-up questions                    (Task 7)

Pydantic checks every field. If the LLM returns something that does not fit (wrong type, confidence
outside 0-1, missing field) the parser raises an error, which Task 4 handles.
"""

from typing import Literal

from pydantic import BaseModel, Field, field_validator


class Answer(BaseModel):
    """The response of the chatbot."""

    answer: str = Field(min_length=1, description="The answer to the question, in one to three sentences.")
    confidence: float = Field(
        ge=0.0, le=1.0,
        description="How sure the answer is, from 0.0 (not sure, or not in the context) to 1.0 (stated clearly in the context).",
    )
    source: str = Field(
        description="Where the answer comes from: the source label of the context excerpt that was used, or 'none'.",
    )

    @field_validator("answer", "source")
    @classmethod
    def _not_blank(cls, value):
        value = value.strip()
        if not value:
            raise ValueError("must not be blank")
        return value


class RouteDecision(BaseModel):
    """Decision of the router in the conditional chain."""

    route: Literal["factual", "general"] = Field(
        description="'factual' = asks for specific information that is stored in the documents; 'general' = anything else.",
    )
    reason: str = Field(description="One short sentence that explains the decision.")


class FollowUps(BaseModel):
    """Follow-up questions a user could ask next."""

    questions: list[str] = Field(min_length=2, max_length=5, description="Two to five short follow-up questions.")
