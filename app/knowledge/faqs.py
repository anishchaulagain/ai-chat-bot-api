"""Static Help-tab FAQs served by the /faq endpoint."""
from __future__ import annotations

FAQS: list[dict[str, str]] = [
    {
        "question": "How do I list a business for sale?",
        "answer": (
            'Open the dashboard, click "Create listing", and follow the guided '
            "steps. You can save a draft at any point and publish once your "
            "details and financials are ready."
        ),
    },
    {
        "question": "What is an NDA request?",
        "answer": (
            "Before a buyer can view confidential details, they request to sign "
            "a non-disclosure agreement. You review the request and, once "
            "approved, the buyer gains access to the protected information."
        ),
    },
    {
        "question": "How does buyer verification work?",
        "answer": (
            "Buyers confirm their identity and proof of funds before engaging "
            "with sellers. Verified buyers get a badge, which helps sellers "
            "prioritise serious, qualified inquiries."
        ),
    },
    {
        "question": "Are my financial details kept private?",
        "answer": (
            "Yes. Sensitive financials stay hidden until a buyer signs an NDA "
            "you've approved. You stay in control of who sees what, and when."
        ),
    },
    {
        "question": "How do I contact a seller or buyer?",
        "answer": (
            "Use the Messages section to start a secure conversation. All "
            "communication stays on-platform so you have a clear record of "
            "every exchange."
        ),
    },
]
