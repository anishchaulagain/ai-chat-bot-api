"""Pydantic request/response models for the chat API."""
from __future__ import annotations

from typing import Literal

from pydantic import BaseModel, Field

Role = Literal["system", "user", "assistant"]


class Message(BaseModel):
    role: Role
    content: str


class ChatRequest(BaseModel):
    """Incoming chat request from a client."""

    message: str = Field(..., min_length=1, description="The user's message.")
    session_id: str | None = Field(
        default=None,
        description="Conversation id. If omitted, a new session is created.",
    )
    temperature: float | None = Field(
        default=None, ge=0.0, le=2.0, description="Optional sampling override."
    )
    max_tokens: int | None = Field(
        default=None, gt=0, description="Optional max output tokens override."
    )


class ChatResponse(BaseModel):
    session_id: str
    reply: str
    model: str


class HealthResponse(BaseModel):
    status: str = "ok"
    model: str
