"""Feedback loop: thumbs-up/down + quality tracking.

Использование:
    from docstoolkit.feedback import FeedbackStore, Feedback

    store = FeedbackStore()
    store.record(Feedback(
        request_id="req_123", request="что такое X",
        response_text="ответ", thumbs="up",
        skill="rag", retriever="hybrid",
    ))

    # Aggregations
    stats = store.aggregate_per_skill()
    quality = store.quality_score(skill="rag")
"""
from docstoolkit.feedback.store import FeedbackStore, Feedback

__all__ = ["FeedbackStore", "Feedback"]
