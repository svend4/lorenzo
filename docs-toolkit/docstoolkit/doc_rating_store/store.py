"""DocRatingStore implementation — E318."""

from __future__ import annotations

import threading
import time
from dataclasses import dataclass, field
from typing import Optional


@dataclass
class Rating:
    """A single user rating for a document."""

    doc_id: str
    user_id: str
    score: float
    rated_at: float = 0.0
    review: str = ""


@dataclass
class RatingSummary:
    """Aggregate rating summary for a document."""

    doc_id: str
    count: int
    avg_score: float
    min_score: float
    max_score: float
    score_distribution: dict = field(default_factory=dict)


@dataclass
class RatingStats:
    """Global statistics across all ratings."""

    total_ratings: int
    unique_docs: int
    unique_users: int
    global_avg: float


class DocRatingStore:
    """Thread-safe store for document ratings.

    One rating per (doc_id, user_id) pair; rating a document a second time
    replaces the previous rating.
    """

    def __init__(self) -> None:
        self._lock = threading.Lock()
        # (doc_id, user_id) → Rating
        self._ratings: dict[tuple, Rating] = {}
        # doc_id → set of user_ids
        self._by_doc: dict[str, set[str]] = {}

    # ------------------------------------------------------------------
    # Write operations
    # ------------------------------------------------------------------

    def rate(
        self,
        doc_id: str,
        user_id: str,
        score: float,
        review: str = "",
        now: Optional[float] = None,
    ) -> Rating:
        """Create or replace a rating.

        Parameters
        ----------
        doc_id:  Document identifier.
        user_id: User identifier.
        score:   Numeric score (caller's responsibility to keep in range).
        review:  Optional free-text review.
        now:     Timestamp override; defaults to ``time.time()``.

        Returns
        -------
        The stored :class:`Rating` instance.
        """
        timestamp = now if now is not None else time.time()
        rating = Rating(
            doc_id=doc_id,
            user_id=user_id,
            score=score,
            rated_at=timestamp,
            review=review,
        )
        key = (doc_id, user_id)
        with self._lock:
            self._ratings[key] = rating
            self._by_doc.setdefault(doc_id, set()).add(user_id)
        return rating

    def delete_rating(self, doc_id: str, user_id: str) -> bool:
        """Delete a rating.

        Returns
        -------
        ``True`` if the rating existed and was removed, ``False`` otherwise.
        """
        key = (doc_id, user_id)
        with self._lock:
            if key not in self._ratings:
                return False
            del self._ratings[key]
            self._by_doc[doc_id].discard(user_id)
            if not self._by_doc[doc_id]:
                del self._by_doc[doc_id]
            return True

    # ------------------------------------------------------------------
    # Read operations
    # ------------------------------------------------------------------

    def get_rating(self, doc_id: str, user_id: str) -> Optional[Rating]:
        """Return the rating for *doc_id* by *user_id*, or ``None``."""
        with self._lock:
            return self._ratings.get((doc_id, user_id))

    def has_rated(self, user_id: str, doc_id: str) -> bool:
        """Return ``True`` if *user_id* has rated *doc_id*."""
        with self._lock:
            return (doc_id, user_id) in self._ratings

    def ratings_for_doc(self, doc_id: str) -> list[Rating]:
        """Return all ratings for *doc_id*, sorted by ``rated_at`` ascending."""
        with self._lock:
            user_ids = self._by_doc.get(doc_id, set())
            ratings = [self._ratings[(doc_id, uid)] for uid in user_ids]
        return sorted(ratings, key=lambda r: r.rated_at)

    def ratings_by_user(self, user_id: str) -> list[Rating]:
        """Return all ratings submitted by *user_id*, sorted by ``rated_at``."""
        with self._lock:
            ratings = [
                r for (did, uid), r in self._ratings.items() if uid == user_id
            ]
        return sorted(ratings, key=lambda r: r.rated_at)

    def summary(self, doc_id: str) -> Optional[RatingSummary]:
        """Return an aggregate :class:`RatingSummary` for *doc_id*.

        Returns ``None`` if no ratings exist for the document.
        """
        with self._lock:
            user_ids = self._by_doc.get(doc_id, set())
            if not user_ids:
                return None
            ratings = [self._ratings[(doc_id, uid)] for uid in user_ids]

        scores = [r.score for r in ratings]
        count = len(scores)
        avg_score = sum(scores) / count
        min_score = min(scores)
        max_score = max(scores)

        distribution: dict = {}
        for s in scores:
            key = round(s, 1)
            distribution[key] = distribution.get(key, 0) + 1

        return RatingSummary(
            doc_id=doc_id,
            count=count,
            avg_score=avg_score,
            min_score=min_score,
            max_score=max_score,
            score_distribution=distribution,
        )

    def top_rated_docs(self, limit: int = 10) -> list[tuple]:
        """Return *(doc_id, avg_score)* pairs for the top-rated documents.

        Results are sorted by *avg_score* descending, then *doc_id* ascending.
        Only documents with at least one rating are included.

        Parameters
        ----------
        limit: Maximum number of entries to return.
        """
        with self._lock:
            doc_ids = list(self._by_doc.keys())

        results: list[tuple] = []
        for doc_id in doc_ids:
            summ = self.summary(doc_id)
            if summ is not None:
                results.append((doc_id, summ.avg_score))

        results.sort(key=lambda t: (-t[1], t[0]))
        return results[:limit]

    def all_doc_ids(self) -> list[str]:
        """Return a sorted list of all document IDs that have ratings."""
        with self._lock:
            return sorted(self._by_doc.keys())

    def stats(self) -> RatingStats:
        """Return global :class:`RatingStats` across all stored ratings."""
        with self._lock:
            total = len(self._ratings)
            unique_docs = len(self._by_doc)
            unique_users = len({uid for (_, uid) in self._ratings})
            scores = [r.score for r in self._ratings.values()]

        global_avg = sum(scores) / len(scores) if scores else 0.0
        return RatingStats(
            total_ratings=total,
            unique_docs=unique_docs,
            unique_users=unique_users,
            global_avg=global_avg,
        )
