"""FAQ endpoint: returns the static Help-tab questions and answers."""
from __future__ import annotations

from fastapi import APIRouter

from app.knowledge.faqs import FAQS
from app.models.schemas import FAQResponse

router = APIRouter(prefix="/faq", tags=["faq"])


@router.get("", response_model=FAQResponse)
async def list_faqs() -> FAQResponse:
    """Return all FAQs."""
    return FAQResponse(items=FAQS)
