"""Thin wrapper around the Groq SDK for chat completions (sync + streaming)."""
from __future__ import annotations

from collections.abc import AsyncIterator

from groq import AsyncGroq

from app.config import Settings, get_settings


class GroqClient:
    """Encapsulates Groq chat-completion calls so the rest of the app stays
    independent of the SDK details."""

    def __init__(self, settings: Settings | None = None) -> None:
        self._settings = settings or get_settings()
        self._client = AsyncGroq(api_key=self._settings.groq_api_key)

    async def complete(
        self,
        messages: list[dict[str, str]],
        *,
        temperature: float | None = None,
        max_tokens: int | None = None,
    ) -> str:
        """Return a full chat completion as a single string."""
        response = await self._client.chat.completions.create(
            model=self._settings.groq_model,
            messages=messages,
            temperature=self._resolve_temperature(temperature),
            max_tokens=max_tokens or self._settings.groq_max_tokens,
            stream=False,
        )
        return response.choices[0].message.content or ""

    async def stream(
        self,
        messages: list[dict[str, str]],
        *,
        temperature: float | None = None,
        max_tokens: int | None = None,
    ) -> AsyncIterator[str]:
        """Yield chat-completion content token-by-token as it arrives."""
        stream = await self._client.chat.completions.create(
            model=self._settings.groq_model,
            messages=messages,
            temperature=self._resolve_temperature(temperature),
            max_tokens=max_tokens or self._settings.groq_max_tokens,
            stream=True,
        )
        async for chunk in stream:
            delta = chunk.choices[0].delta.content
            if delta:
                yield delta

    def _resolve_temperature(self, override: float | None) -> float:
        return override if override is not None else self._settings.groq_temperature
