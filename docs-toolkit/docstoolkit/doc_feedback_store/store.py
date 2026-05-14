"""DocFeedbackStore — stores user feedback (ratings, comments, reactions) on documents.

Stdlib only — uses ``threading.Lock`` for thread safety.
"""

from __future__ import annotations

import threading
from dataclasses import dataclass, field
from typing import Any, Optional


@dataclass
class FeedbackItem:
    """A single feedback entry by a user on a document."""

    feedback_id: int
    doc_id: str
    user_id: str
    feedback_type: str      # "rating", "comment", "reaction"
    value: Any              # int for rating, str for comment/reaction
    timestamp: float


@dataclass
class DocSummary:
    """Aggregated feedback stats for one document."""

    doc_id: str
    total_feedback: int
    avg_rating: Optional[float]      # None if no ratings
    reaction_counts: dict             # reaction value -> count
    comment_count: int


@dataclass
class FeedbackStats:
    """Global store statistics."""

    total_items: int
    total_docs: int
    total_users: int
    type_counts: dict                 # feedback_type -> count


class DocFeedbackStore:
    """Central feedback manager.

    All mutations and reads are guarded by a single ``threading.Lock``, making
    this safe to use from multiple threads simultaneously.
    """

    def __init__(self) -> None:
        self._lock = threading.Lock()
        self._items: dict[int, FeedbackItem] = {}
        self._next_id: int = 1

    # ------------------------------------------------------------------
    # Mutations
    # ------------------------------------------------------------------

    def add(
        self,
        doc_id: str,
        user_id: str,
        feedback_type: str,
        value: Any,
        now: Optional[float] = None,
    ) -> FeedbackItem:
        """Add a feedback item.

        Auto-increments ``feedback_id``.  ``now`` defaults to ``0.0`` when
        not provided, allowing deterministic testing without importing time.
        """
        timestamp = now if now is not None else 0.0
        with self._lock:
            fid = self._next_id
            self._next_id += 1
            item = FeedbackItem(
                feedback_id=fid,
                doc_id=doc_id,
                user_id=user_id,
                feedback_type=feedback_type,
                value=value,
                timestamp=timestamp,
            )
            self._items[fid] = item
            return item

    def delete(self, feedback_id: int) -> bool:
        """Delete a feedback item by id.  Returns ``True`` if it existed."""
        with self._lock:
            if feedback_id in self._items:
                del self._items[feedback_id]
                return True
            return False

    def delete_doc_feedback(self, doc_id: str) -> int:
        """Delete all feedback for a document.  Returns the count removed."""
        with self._lock:
            to_remove = [
                fid for fid, item in self._items.items()
                if item.doc_id == doc_id
            ]
            for fid in to_remove:
                del self._items[fid]
            return len(to_remove)

    # ------------------------------------------------------------------
    # Queries
    # ------------------------------------------------------------------

    def get(self, feedback_id: int) -> Optional[FeedbackItem]:
        """Return the feedback item with the given id, or ``None``."""
        with self._lock:
            return self._items.get(feedback_id)

    def feedback_for_doc(
        self,
        doc_id: str,
        feedback_type: Optional[str] = None,
        limit: Optional[int] = None,
    ) -> list[FeedbackItem]:
        """Return feedback for a document, optionally filtered by type.

        Results are ordered newest-first (by timestamp, then by feedback_id
        descending for ties).
        """
        with self._lock:
            items = [
                item for item in self._items.values()
                if item.doc_id == doc_id
                and (feedback_type is None or item.feedback_type == feedback_type)
            ]
        items.sort(key=lambda x: (x.timestamp, x.feedback_id), reverse=True)
        if limit is not None:
            items = items[:limit]
        return items

    def feedback_by_user(
        self,
        user_id: str,
        doc_id: Optional[str] = None,
    ) -> list[FeedbackItem]:
        """Return all feedback from a user, optionally filtered by doc_id."""
        with self._lock:
            return [
                item for item in self._items.values()
                if item.user_id == user_id
                and (doc_id is None or item.doc_id == doc_id)
            ]

    def doc_summary(self, doc_id: str) -> DocSummary:
        """Return aggregated stats for a document.

        - ``avg_rating``: mean of all "rating" feedback values (or ``None``).
        - ``reaction_counts``: per-value counts for "reaction" type items.
        - ``comment_count``: number of "comment" type items.
        """
        with self._lock:
            ratings: list[float] = []
            reaction_counts: dict[str, int] = {}
            comment_count = 0
            total = 0

            for item in self._items.values():
                if item.doc_id != doc_id:
                    continue
                total += 1
                if item.feedback_type == "rating":
                    try:
                        ratings.append(float(item.value))
                    except (TypeError, ValueError):
                        pass
                elif item.feedback_type == "reaction":
                    key = str(item.value)
                    reaction_counts[key] = reaction_counts.get(key, 0) + 1
                elif item.feedback_type == "comment":
                    comment_count += 1

        avg_rating: Optional[float] = (
            sum(ratings) / len(ratings) if ratings else None
        )
        return DocSummary(
            doc_id=doc_id,
            total_feedback=total,
            avg_rating=avg_rating,
            reaction_counts=reaction_counts,
            comment_count=comment_count,
        )

    def top_rated_docs(self, limit: int = 10) -> list[tuple[str, float]]:
        """Return ``[(doc_id, avg_rating)]`` sorted by avg_rating descending.

        Only documents that have at least one "rating" feedback item are
        included.
        """
        with self._lock:
            rating_map: dict[str, list[float]] = {}
            for item in self._items.values():
                if item.feedback_type != "rating":
                    continue
                try:
                    v = float(item.value)
                except (TypeError, ValueError):
                    continue
                rating_map.setdefault(item.doc_id, []).append(v)

        result = [
            (doc_id, sum(vs) / len(vs))
            for doc_id, vs in rating_map.items()
        ]
        result.sort(key=lambda kv: (-kv[1], kv[0]))
        return result[:limit]

    def stats(self) -> FeedbackStats:
        """Return global store statistics."""
        with self._lock:
            type_counts: dict[str, int] = {}
            docs: set[str] = set()
            users: set[str] = set()
            for item in self._items.values():
                type_counts[item.feedback_type] = (
                    type_counts.get(item.feedback_type, 0) + 1
                )
                docs.add(item.doc_id)
                users.add(item.user_id)
            return FeedbackStats(
                total_items=len(self._items),
                total_docs=len(docs),
                total_users=len(users),
                type_counts=type_counts,
            )

    # ------------------------------------------------------------------
    # Properties
    # ------------------------------------------------------------------

    @property
    def total_items(self) -> int:
        """Total number of feedback items currently stored."""
        with self._lock:
            return len(self._items)
