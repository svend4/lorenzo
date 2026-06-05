"""DocFeedbackRatings — combined feedback (rating + comment) tracking.

Stdlib only.  All mutations are guarded by a single ``threading.Lock``.
"""

from __future__ import annotations

import threading
from dataclasses import dataclass, field
from typing import Optional


@dataclass
class Feedback:
    """A single feedback entry combining rating and comment."""

    feedback_id: int
    doc_id: str
    user_id: str
    rating: int
    comment: str = ""
    created_at: float = 0.0


@dataclass
class RatingsSummary:
    """Summary statistics for a single document."""

    doc_id: str
    count: int
    avg_rating: float
    distribution: dict = field(default_factory=dict)


@dataclass
class FeedbackStats:
    """Aggregate statistics across the whole store."""

    total_feedback: int
    unique_docs: int
    unique_users: int
    global_avg_rating: float


class DocFeedbackRatings:
    """Thread-safe combined feedback + rating tracker.

    A single ``threading.Lock`` protects all internal state.  Indices keep
    look-ups by doc and user O(k) where k is the number of items for the
    given doc/user.
    """

    def __init__(self) -> None:
        self._lock = threading.Lock()
        self._feedback: dict[int, Feedback] = {}
        self._by_doc: dict[str, list[int]] = {}
        self._by_user: dict[str, list[int]] = {}
        self._next_id: int = 1

    # ------------------------------------------------------------------
    # Helpers
    # ------------------------------------------------------------------

    @staticmethod
    def _validate_rating(rating: int) -> None:
        if not isinstance(rating, int) or isinstance(rating, bool):
            raise ValueError(f"rating must be int, got {type(rating).__name__}")
        if rating < 1 or rating > 5:
            raise ValueError(f"rating must be in 1..5, got {rating}")

    # ------------------------------------------------------------------
    # Mutations
    # ------------------------------------------------------------------

    def submit(
        self,
        doc_id: str,
        user_id: str,
        rating: int,
        comment: str = "",
        now: Optional[float] = None,
    ) -> Feedback:
        """Submit new feedback.  Returns the stored :class:`Feedback`.

        Raises :class:`ValueError` if ``rating`` is not in 1..5.
        """
        self._validate_rating(rating)
        created_at = now if now is not None else 0.0
        with self._lock:
            fid = self._next_id
            self._next_id += 1
            fb = Feedback(
                feedback_id=fid,
                doc_id=doc_id,
                user_id=user_id,
                rating=rating,
                comment=comment,
                created_at=created_at,
            )
            self._feedback[fid] = fb
            self._by_doc.setdefault(doc_id, []).append(fid)
            self._by_user.setdefault(user_id, []).append(fid)
            return fb

    def update(
        self,
        feedback_id: int,
        rating: Optional[int] = None,
        comment: Optional[str] = None,
    ) -> Optional[Feedback]:
        """Partial update of an existing feedback item.

        Returns the updated :class:`Feedback`, or ``None`` if not found.
        Raises :class:`ValueError` if ``rating`` is provided and invalid.
        """
        if rating is not None:
            self._validate_rating(rating)
        with self._lock:
            fb = self._feedback.get(feedback_id)
            if fb is None:
                return None
            if rating is not None:
                fb.rating = rating
            if comment is not None:
                fb.comment = comment
            return fb

    def delete(self, feedback_id: int) -> bool:
        """Remove a feedback item.  Returns ``True`` if it existed."""
        with self._lock:
            fb = self._feedback.pop(feedback_id, None)
            if fb is None:
                return False
            doc_ids = self._by_doc.get(fb.doc_id)
            if doc_ids is not None:
                try:
                    doc_ids.remove(feedback_id)
                except ValueError:
                    pass
                if not doc_ids:
                    del self._by_doc[fb.doc_id]
            user_ids = self._by_user.get(fb.user_id)
            if user_ids is not None:
                try:
                    user_ids.remove(feedback_id)
                except ValueError:
                    pass
                if not user_ids:
                    del self._by_user[fb.user_id]
            return True

    def clear_doc(self, doc_id: str) -> int:
        """Remove all feedback for a document.  Returns count removed."""
        with self._lock:
            fids = self._by_doc.pop(doc_id, [])
            for fid in fids:
                fb = self._feedback.pop(fid, None)
                if fb is None:
                    continue
                user_ids = self._by_user.get(fb.user_id)
                if user_ids is not None:
                    try:
                        user_ids.remove(fid)
                    except ValueError:
                        pass
                    if not user_ids:
                        del self._by_user[fb.user_id]
            return len(fids)

    def clear_user(self, user_id: str) -> int:
        """Remove all feedback by a user.  Returns count removed."""
        with self._lock:
            fids = self._by_user.pop(user_id, [])
            for fid in fids:
                fb = self._feedback.pop(fid, None)
                if fb is None:
                    continue
                doc_ids = self._by_doc.get(fb.doc_id)
                if doc_ids is not None:
                    try:
                        doc_ids.remove(fid)
                    except ValueError:
                        pass
                    if not doc_ids:
                        del self._by_doc[fb.doc_id]
            return len(fids)

    # ------------------------------------------------------------------
    # Queries
    # ------------------------------------------------------------------

    def get(self, feedback_id: int) -> Optional[Feedback]:
        """Return feedback by id, or ``None``."""
        with self._lock:
            return self._feedback.get(feedback_id)

    def feedback_for_doc(
        self,
        doc_id: str,
        limit: Optional[int] = None,
    ) -> list[Feedback]:
        """Return feedback for a document, newest first."""
        with self._lock:
            fids = list(self._by_doc.get(doc_id, []))
            items = [self._feedback[fid] for fid in fids if fid in self._feedback]
        items.sort(key=lambda x: (x.created_at, x.feedback_id), reverse=True)
        if limit is not None:
            items = items[:limit]
        return items

    def feedback_by_user(
        self,
        user_id: str,
        limit: Optional[int] = None,
    ) -> list[Feedback]:
        """Return feedback from a user, newest first."""
        with self._lock:
            fids = list(self._by_user.get(user_id, []))
            items = [self._feedback[fid] for fid in fids if fid in self._feedback]
        items.sort(key=lambda x: (x.created_at, x.feedback_id), reverse=True)
        if limit is not None:
            items = items[:limit]
        return items

    def summary(self, doc_id: str) -> Optional[RatingsSummary]:
        """Return :class:`RatingsSummary` for the doc, or ``None`` if no feedback."""
        with self._lock:
            fids = self._by_doc.get(doc_id, [])
            if not fids:
                return None
            ratings: list[int] = []
            distribution: dict[int, int] = {1: 0, 2: 0, 3: 0, 4: 0, 5: 0}
            for fid in fids:
                fb = self._feedback.get(fid)
                if fb is None:
                    continue
                ratings.append(fb.rating)
                distribution[fb.rating] = distribution.get(fb.rating, 0) + 1
            if not ratings:
                return None
            avg = sum(ratings) / len(ratings)
            return RatingsSummary(
                doc_id=doc_id,
                count=len(ratings),
                avg_rating=avg,
                distribution=distribution,
            )

    def _ranked(
        self,
        descending: bool,
        limit: int,
        min_count: int,
    ) -> list[tuple[str, float]]:
        with self._lock:
            sums: dict[str, list[int]] = {}
            for fb in self._feedback.values():
                sums.setdefault(fb.doc_id, []).append(fb.rating)
        result: list[tuple[str, float]] = []
        for doc_id, rs in sums.items():
            if len(rs) < min_count:
                continue
            avg = sum(rs) / len(rs)
            result.append((doc_id, avg))
        # Primary key: avg (desc or asc); secondary: doc_id ascending
        if descending:
            result.sort(key=lambda kv: (-kv[1], kv[0]))
        else:
            result.sort(key=lambda kv: (kv[1], kv[0]))
        return result[:limit]

    def top_rated(
        self,
        limit: int = 10,
        min_count: int = 1,
    ) -> list[tuple[str, float]]:
        """Return ``[(doc_id, avg_rating)]`` sorted by avg desc, doc_id asc.

        Only documents with at least ``min_count`` ratings are considered.
        """
        return self._ranked(descending=True, limit=limit, min_count=min_count)

    def worst_rated(
        self,
        limit: int = 10,
        min_count: int = 1,
    ) -> list[tuple[str, float]]:
        """Return ``[(doc_id, avg_rating)]`` sorted by avg asc, doc_id asc.

        Only documents with at least ``min_count`` ratings are considered.
        """
        return self._ranked(descending=False, limit=limit, min_count=min_count)

    def count_for_doc(self, doc_id: str) -> int:
        """Return the number of feedback items for a doc."""
        with self._lock:
            return len(self._by_doc.get(doc_id, []))

    def count_by_user(self, user_id: str) -> int:
        """Return the number of feedback items by a user."""
        with self._lock:
            return len(self._by_user.get(user_id, []))

    def all_doc_ids(self) -> list[str]:
        """Return sorted list of doc ids with at least one feedback item."""
        with self._lock:
            return sorted(self._by_doc.keys())

    def stats(self) -> FeedbackStats:
        """Return :class:`FeedbackStats` for the entire store."""
        with self._lock:
            total = len(self._feedback)
            docs = len(self._by_doc)
            users = len(self._by_user)
            if total == 0:
                return FeedbackStats(
                    total_feedback=0,
                    unique_docs=0,
                    unique_users=0,
                    global_avg_rating=0.0,
                )
            total_rating = sum(fb.rating for fb in self._feedback.values())
            return FeedbackStats(
                total_feedback=total,
                unique_docs=docs,
                unique_users=users,
                global_avg_rating=total_rating / total,
            )
