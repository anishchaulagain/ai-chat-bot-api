"""Application configuration loaded from environment / .env file."""
from __future__ import annotations

from functools import lru_cache

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Strongly-typed settings sourced from environment variables."""

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )

    # --- Groq / LLM ---
    groq_api_key: str
    groq_model: str = "llama-3.3-70b-versatile"
    groq_temperature: float = 0.6
    groq_max_tokens: int = 300

    # --- Conversation memory ---
    # Max number of prior messages (user + assistant) kept per session.
    max_history_messages: int = 20

    # --- API ---
    app_name: str = "AI Chatbot API"
    cors_origins: str = "*"

    # --- Knowledge base ---
    # Markdown file holding platform information injected into the system prompt.
    knowledge_file: str = "app/knowledge/platform_info.md"

    @property
    def cors_origin_list(self) -> list[str]:
        if self.cors_origins.strip() == "*":
            return ["*"]
        return [o.strip() for o in self.cors_origins.split(",") if o.strip()]


@lru_cache
def get_settings() -> Settings:
    """Return a cached Settings instance (read once per process)."""
    return Settings()
