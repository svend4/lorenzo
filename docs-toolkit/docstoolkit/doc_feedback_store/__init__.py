"""E289 DocFeedbackStore — user feedback (ratings, comments, reactions) on documents.

Pure stdlib, thread-safe.

Public API
----------
:class:`FeedbackItem`  — individual feedback record
:class:`DocSummary`    — aggregated stats for one document
:class:`FeedbackStats` — global store statistics
:class:`DocFeedbackStore` — central feedback manager
"""

from docstoolkit.doc_feedback_store.store import (
    DocFeedbackStore,
    DocSummary,
    FeedbackItem,
    FeedbackStats,
)

__all__ = [
    "DocFeedbackStore",
    "DocSummary",
    "FeedbackItem",
    "FeedbackStats",
]
