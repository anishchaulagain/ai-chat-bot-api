"""Health / readiness endpoint."""
from __future__ import annotations

from fastapi import APIRouter

from app.config import get_settings
from app.models.schemas import HealthResponse

router = APIRouter(tags=["health"])


@router.get("/health", response_model=HealthResponse)
async def health() -> HealthResponse:
    return HealthResponse(status="ok", model=get_settings().llm_model)
