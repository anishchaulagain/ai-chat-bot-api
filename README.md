# AI Chatbot API

A FastAPI backend for an AI chatbot powered by **Groq**. The bot answers from a
configurable **platform knowledge base** that is injected into the system
prompt, so you can point it at any platform by editing one markdown file.

## Features

- `POST /chat` — send a message, get a full reply (with conversation memory).
- `POST /chat/stream` — same, streamed token-by-token over SSE.
- `DELETE /chat/{session_id}` — clear a conversation.
- `GET /health` — liveness + active model.
- Per-session rolling conversation history (in-memory, swappable).
- Knowledge base driven persona — edit `app/knowledge/platform_info.md`.

## Project layout

```
app/
├── main.py                  # FastAPI app factory + middleware
├── config.py                # pydantic-settings (reads .env)
├── api/
│   ├── deps.py              # singleton dependency wiring
│   └── routes/
│       ├── chat.py          # chat / stream / reset endpoints
│       └── health.py
├── core/groq_client.py      # async Groq SDK wrapper (sync + streaming)
├── models/schemas.py        # request/response models
├── services/
│   ├── chat_service.py      # prompt assembly + Groq call + history
│   └── session_store.py     # in-memory conversation store
└── knowledge/
    ├── platform.py          # builds system prompt from the knowledge file
    └── platform_info.md     # <-- PUT YOUR PLATFORM INFO HERE
```

## Setup

1. Configure environment — copy `.env.example` to `.env` and set your
   `GROQ_API_KEY` (already present in this project).

2. Install dependencies:

   ```powershell
   venv\Scripts\python.exe -m pip install -r requirements.txt
   ```

3. Add your platform information by editing
   [app/knowledge/platform_info.md](app/knowledge/platform_info.md). This text
   becomes the assistant's source of truth.

4. Run the server:

   ```powershell
   venv\Scripts\python.exe -m uvicorn app.main:app --reload
   ```

   Interactive docs: http://127.0.0.1:8000/docs

## Example

```bash
# First message — omit session_id to start a new conversation
curl -X POST http://127.0.0.1:8000/chat \
  -H "Content-Type: application/json" \
  -d '{"message":"What can you help me with?"}'

# Follow-up — reuse the returned session_id to keep context
curl -X POST http://127.0.0.1:8000/chat \
  -H "Content-Type: application/json" \
  -d '{"message":"Tell me more","session_id":"<id-from-previous-response>"}'
```

## Configuration

All settings come from `.env` (see `.env.example`):

| Variable | Default | Purpose |
| --- | --- | --- |
| `GROQ_API_KEY` | — | Groq API key (required) |
| `GROQ_MODEL` | `llama-3.3-70b-versatile` | Model id |
| `GROQ_TEMPERATURE` | `0.6` | Sampling temperature |
| `GROQ_MAX_TOKENS` | `1024` | Max output tokens |
| `MAX_HISTORY_MESSAGES` | `20` | Messages kept per session |
| `CORS_ORIGINS` | `*` | Allowed origins (comma-separated) |
| `KNOWLEDGE_FILE` | `app/knowledge/platform_info.md` | Knowledge source |

## Notes

- Conversation history is **in-memory** and resets on restart. Swap
  `SessionStore` for Redis/DB for production without changing call sites.
- The knowledge file is cached at startup; restart the server after editing it.
