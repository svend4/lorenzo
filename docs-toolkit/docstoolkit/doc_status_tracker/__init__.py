"""Document lifecycle status tracker (E294).

Tracks document status (draft/review/published/archived) with a full
transition history.  Pure stdlib, thread-safe.
"""

from docstoolkit.doc_status_tracker.tracker import (
    DocStatus,
    DocStatusTracker,
    StatusStats,
    StatusTransition,
)

__all__ = [
    "DocStatus",
    "DocStatusTracker",
    "StatusStats",
    "StatusTransition",
]
