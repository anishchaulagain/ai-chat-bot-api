"""Chat endpoints: full reply, streaming reply, and session reset."""
from __future__ import annotations

from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import StreamingResponse
from groq import GroqError

from app.api.deps import get_chat_service, get_session_store
from app.config import get_settings
from app.models.schemas import ChatRequest, ChatResponse
from app.services.chat_service import ChatService
from app.services.session_store import SessionStore

router = APIRouter(prefix="/chat", tags=["chat"])


@router.post("", response_model=ChatResponse)
async def chat(
    payload: ChatRequest,
    service: ChatService = Depends(get_chat_service),
    store: SessionStore = Depends(get_session_store),
) -> ChatResponse:
    """Send a message and get the assistant's full reply."""
    session_id = payload.session_id or store.new_session()
    try:
        reply = await service.reply(
            session_id,
            payload.message,
            temperature=payload.temperature,
            max_tokens=payload.max_tokens,
        )
    except GroqError as exc:  # upstream LLM failure
        raise HTTPException(status_code=502, detail=f"LLM error: {exc}") from exc

    return ChatResponse(
        session_id=session_id, reply=reply, model=get_settings().groq_model
    )


@router.post("/stream")
async def chat_stream(
    payload: ChatRequest,
    service: ChatService = Depends(get_chat_service),
    store: SessionStore = Depends(get_session_store),
) -> StreamingResponse:
    """Stream the assistant's reply as plain-text chunks (text/event-stream)."""
    session_id = payload.session_id or store.new_session()

    async def event_generator():
        # Surface the session id first so clients can persist it.
        yield f"data: [session:{session_id}]\n\n"
        try:
            async for token in service.reply_stream(
                session_id,
                payload.message,
                temperature=payload.temperature,
                max_tokens=payload.max_tokens,
            ):
                yield f"data: {token}\n\n"
        except GroqError as exc:
            yield f"data: [error] {exc}\n\n"
        yield "data: [done]\n\n"

    return StreamingResponse(event_generator(), media_type="text/event-stream")


@router.delete("/{session_id}", status_code=204)
async def reset_session(
    session_id: str,
    store: SessionStore = Depends(get_session_store),
) -> None:
    """Clear a conversation's history."""
    store.clear(session_id)
