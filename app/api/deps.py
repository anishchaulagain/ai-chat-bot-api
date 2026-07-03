"""FastAPI dependency wiring.

Singletons are created on first use and shared across requests. The LLMClient
and SessionStore hold no per-request state, so sharing them is safe and avoids
re-creating an HTTP client on every call.
"""
from __future__ import annotations

from functools import lru_cache

from app.config import get_settings
from app.core.llm_client import LLMClient
from app.services.chat_service import ChatService
from app.services.session_store import SessionStore


@lru_cache
def get_llm_client() -> LLMClient:
    return LLMClient()


@lru_cache
def get_session_store() -> SessionStore:
    return SessionStore(max_messages=get_settings().max_history_messages)


@lru_cache
def get_chat_service() -> ChatService:
    return ChatService(client=get_llm_client(), store=get_session_store())
