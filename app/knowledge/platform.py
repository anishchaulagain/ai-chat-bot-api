"""Loads the platform knowledge base and builds the chatbot system prompt.

The markdown file referenced by ``settings.knowledge_file`` holds everything
the assistant should know about the platform. It is read once and combined
with the base persona to form the system prompt sent on every request.
"""
from __future__ import annotations

from functools import lru_cache
from pathlib import Path

from app.config import get_settings

# Persona / behavioural rules wrapped around the platform knowledge.
_BASE_PERSONA = """\
You are a helpful, friendly support assistant for the platform described in \
the KNOWLEDGE BASE below.

Rules:
- Answer strictly using the information in the KNOWLEDGE BASE.
- If the answer is not covered by the knowledge base, say you don't have that \
information and, when appropriate, suggest contacting support — do not invent \
facts, prices, or features.
- Be concise, clear, and polite. Use plain language.
- Keep responses focused on the platform; politely decline unrelated requests.
"""


def _load_knowledge_text() -> str:
    settings = get_settings()
    path = Path(settings.knowledge_file)
    if not path.is_absolute():
        # Resolve relative to the project root (two levels up from this file).
        path = Path(__file__).resolve().parents[2] / settings.knowledge_file
    if not path.exists():
        return "(No platform knowledge has been provided yet.)"
    return path.read_text(encoding="utf-8").strip()


@lru_cache
def build_system_prompt() -> str:
    """Return the full system prompt (persona + platform knowledge)."""
    knowledge = _load_knowledge_text()
    return f"{_BASE_PERSONA}\n\n=== KNOWLEDGE BASE ===\n{knowledge}\n=== END KNOWLEDGE BASE ==="
