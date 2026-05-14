"""UserProfile — tracks user interactions for content recommendations."""
from __future__ import annotations

from dataclasses import dataclass, field


@dataclass
class UserProfile:
    """Stores a user's document interaction history and tag interests.

    Attributes:
        user_id: Unique identifier for the user.
        viewed_docs: Ordered list of viewed document IDs (most recent last).
        liked_docs: Set of document IDs the user liked.
        disliked_docs: Set of document IDs the user disliked.
        query_history: Ordered list of search queries (most recent last).
        tags: Mapping of tag → interest score (higher = more interested).
    """

    user_id: str
    viewed_docs: list[str] = field(default_factory=list)
    liked_docs: set[str] = field(default_factory=set)
    disliked_docs: set[str] = field(default_factory=set)
    query_history: list[str] = field(default_factory=list)
    tags: dict[str, float] = field(default_factory=dict)

    # ------------------------------------------------------------------
    # Interaction recording
    # ------------------------------------------------------------------

    def add_view(self, doc_id: str) -> None:
        """Record that the user viewed *doc_id*."""
        self.viewed_docs.append(doc_id)

    def add_like(self, doc_id: str) -> None:
        """Record a positive signal for *doc_id*."""
        self.liked_docs.add(doc_id)
        # Ensure it's not simultaneously disliked
        self.disliked_docs.discard(doc_id)

    def add_dislike(self, doc_id: str) -> None:
        """Record a negative signal for *doc_id*."""
        self.disliked_docs.add(doc_id)
        # Ensure it's not simultaneously liked
        self.liked_docs.discard(doc_id)

    # ------------------------------------------------------------------
    # Derived helpers
    # ------------------------------------------------------------------

    def interest_tags(self, n: int = 10) -> list[str]:
        """Return the top-*n* tags by interest score (descending)."""
        sorted_tags = sorted(self.tags.items(), key=lambda kv: kv[1], reverse=True)
        return [tag for tag, _ in sorted_tags[:n]]

    def seen_docs(self) -> set[str]:
        """Return the set of all documents the user has already seen.

        A document is considered "seen" if it appears in *viewed_docs*,
        *liked_docs*, or *disliked_docs*.
        """
        return set(self.viewed_docs) | self.liked_docs | self.disliked_docs
