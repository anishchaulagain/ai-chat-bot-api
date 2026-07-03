"""Thin wrapper around the OpenAI SDK, pointed at OpenRouter, for chat
completions (sync + streaming)."""
from __future__ import annotations

from collections.abc import AsyncIterator

from openai import AsyncOpenAI

from app.config import Settings, get_settings


class LLMClient:
    """Encapsulates chat-completion calls so the rest of the app stays
    independent of the SDK/provider details."""

    def __init__(self, settings: Settings | None = None) -> None:
        self._settings = settings or get_settings()
        self._client = AsyncOpenAI(
            api_key=self._settings.openrouter_api_key,
            base_url=self._settings.openrouter_base_url,
        )

    async def complete(
        self,
        messages: list[dict[str, str]],
        *,
        temperature: float | None = None,
        max_tokens: int | None = None,
    ) -> str:
        """Return a full chat completion as a single string."""
        response = await self._client.chat.completions.create(
            model=self._settings.llm_model,
            messages=messages,
            temperature=self._resolve_temperature(temperature),
            max_tokens=max_tokens or self._settings.llm_max_tokens,
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
            model=self._settings.llm_model,
            messages=messages,
            temperature=self._resolve_temperature(temperature),
            max_tokens=max_tokens or self._settings.llm_max_tokens,
            stream=True,
        )
        async for chunk in stream:
            delta = chunk.choices[0].delta.content
            if delta:
                yield delta

    def _resolve_temperature(self, override: float | None) -> float:
        return override if override is not None else self._settings.llm_temperature
