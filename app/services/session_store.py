"""In-memory conversation store.

Keeps a rolling window of messages per session id. This is intentionally
simple (process-local, non-persistent); swap the implementation for Redis or a
database without changing the public method signatures.
"""
from __future__ import annotations

import uuid
from collections import defaultdict, deque
from threading import Lock


class SessionStore:
    def __init__(self, max_messages: int) -> None:
        # Two slots per turn (user + assistant); store a bit of headroom.
        self._max_messages = max_messages
        self._sessions: dict[str, deque[dict[str, str]]] = defaultdict(
            lambda: deque(maxlen=max_messages)
        )
        self._lock = Lock()

    def new_session(self) -> str:
        return uuid.uuid4().hex

    def history(self, session_id: str) -> list[dict[str, str]]:
        with self._lock:
            return list(self._sessions[session_id])

    def append(self, session_id: str, role: str, content: str) -> None:
        with self._lock:
            self._sessions[session_id].append({"role": role, "content": content})

    def clear(self, session_id: str) -> None:
        with self._lock:
            self._sessions.pop(session_id, None)
