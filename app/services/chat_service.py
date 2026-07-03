"""Orchestrates a chat turn: builds the prompt, calls the LLM, tracks history."""
from __future__ import annotations

from collections.abc import AsyncIterator

from app.config import Settings, get_settings
from app.core.llm_client import LLMClient
from app.knowledge.platform import build_system_prompt
from app.services.session_store import SessionStore


class ChatService:
    def __init__(
        self,
        client: LLMClient,
        store: SessionStore,
        settings: Settings | None = None,
    ) -> None:
        self._client = client
        self._store = store
        self._settings = settings or get_settings()

    def _build_messages(self, session_id: str, user_message: str) -> list[dict[str, str]]:
        """System prompt + prior history + the new user message."""
        messages: list[dict[str, str]] = [
            {"role": "system", "content": build_system_prompt()}
        ]
        messages.extend(self._store.history(session_id))
        messages.append({"role": "user", "content": user_message})
        return messages

    async def reply(
        self,
        session_id: str,
        user_message: str,
        *,
        temperature: float | None = None,
        max_tokens: int | None = None,
    ) -> str:
        messages = self._build_messages(session_id, user_message)
        answer = await self._client.complete(
            messages, temperature=temperature, max_tokens=max_tokens
        )
        self._store.append(session_id, "user", user_message)
        self._store.append(session_id, "assistant", answer)
        return answer

    async def reply_stream(
        self,
        session_id: str,
        user_message: str,
        *,
        temperature: float | None = None,
        max_tokens: int | None = None,
    ) -> AsyncIterator[str]:
        """Stream the answer, persisting the full turn once complete."""
        messages = self._build_messages(session_id, user_message)
        chunks: list[str] = []
        async for token in self._client.stream(
            messages, temperature=temperature, max_tokens=max_tokens
        ):
            chunks.append(token)
            yield token
        self._store.append(session_id, "user", user_message)
        self._store.append(session_id, "assistant", "".join(chunks))
