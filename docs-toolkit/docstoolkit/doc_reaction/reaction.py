"""Reactions on documents (emoji/like/etc.) with user tracking and aggregation.

Stdlib only — uses ``threading.Lock`` for thread safety.
"""

from __future__ import annotations

import threading
from dataclasses import dataclass, field
from enum import Enum
from typing import Optional


class ReactionType(Enum):
    """Supported reaction kinds."""

    THUMBS_UP = "thumbs_up"
    THUMBS_DOWN = "thumbs_down"
    HEART = "heart"
    LAUGH = "laugh"
    WOW = "wow"
    SAD = "sad"
    ANGRY = "angry"
    INSIGHTFUL = "insightful"
    FIRE = "fire"
    EYES = "eyes"


@dataclass
class Reaction:
    """A single reaction by a user on a document."""

    doc_id: str
    user_id: str
    reaction_type: ReactionType
    created_at: float = 0.0


@dataclass
class ReactionSummary:
    """Aggregated reaction counts for one document."""

    doc_id: str
    counts: dict = field(default_factory=dict)
    total: int = 0
    top_reaction: Optional[ReactionType] = None
    unique_reactors: int = 0


@dataclass
class UserActivity:
    """Aggregated reaction stats for one user."""

    user_id: str
    total_reactions: int = 0
    by_type: dict = field(default_factory=dict)
    last_at: float = 0.0


class DocReaction:
    """Central reaction manager.

    Parameters
    ----------
    unique_per_user:
        When ``True`` (default), at most one reaction per user per doc is
        retained. Adding a new reaction replaces the existing one. When
        ``False``, multiple reactions of different types from the same
        user are allowed (still at most one of each type per user per doc).
    """

    def __init__(self, unique_per_user: bool = True) -> None:
        self._unique_per_user = bool(unique_per_user)
        self._lock = threading.Lock()
        # All reactions as a list keeps history ordering simple.
        self._reactions: list[Reaction] = []

    # ------------------------------------------------------------------
    # Helpers (internal; assume lock is held)
    # ------------------------------------------------------------------
    def _find_indexes_for_doc_user(
        self, doc_id: str, user_id: str
    ) -> list[int]:
        return [
            i
            for i, r in enumerate(self._reactions)
            if r.doc_id == doc_id and r.user_id == user_id
        ]

    def _find_index(
        self, doc_id: str, user_id: str, reaction_type: ReactionType
    ) -> Optional[int]:
        for i, r in enumerate(self._reactions):
            if (
                r.doc_id == doc_id
                and r.user_id == user_id
                and r.reaction_type == reaction_type
            ):
                return i
        return None

    # ------------------------------------------------------------------
    # Mutations
    # ------------------------------------------------------------------
    def add(
        self,
        doc_id: str,
        user_id: str,
        reaction_type: ReactionType,
        now: float = 0.0,
    ) -> Optional[Reaction]:
        """Add a reaction.

        Returns the newly added :class:`Reaction`. If ``unique_per_user`` is
        true the prior reaction (if any) from this user on this doc is
        replaced. If the same reaction already exists in non-unique mode it
        is refreshed (timestamp updated) and returned.
        """
        if not isinstance(reaction_type, ReactionType):
            return None
        if not doc_id or not user_id:
            return None

        with self._lock:
            if self._unique_per_user:
                # Replace any existing reaction by this user on this doc.
                indexes = self._find_indexes_for_doc_user(doc_id, user_id)
                # Drop in reverse to keep indexes valid.
                for idx in reversed(indexes):
                    del self._reactions[idx]
                reaction = Reaction(
                    doc_id=doc_id,
                    user_id=user_id,
                    reaction_type=reaction_type,
                    created_at=now,
                )
                self._reactions.append(reaction)
                return reaction

            # Non-unique mode: still dedupe (doc, user, type) — refresh ts.
            existing = self._find_index(doc_id, user_id, reaction_type)
            if existing is not None:
                self._reactions[existing].created_at = now
                return self._reactions[existing]
            reaction = Reaction(
                doc_id=doc_id,
                user_id=user_id,
                reaction_type=reaction_type,
                created_at=now,
            )
            self._reactions.append(reaction)
            return reaction

    def remove(
        self,
        doc_id: str,
        user_id: str,
        reaction_type: Optional[ReactionType] = None,
    ) -> bool:
        """Remove a user's reaction(s) from a doc.

        If ``reaction_type`` is ``None``, remove every reaction by this
        user on this document. Returns ``True`` if anything was removed.
        """
        with self._lock:
            if reaction_type is None:
                indexes = self._find_indexes_for_doc_user(doc_id, user_id)
                if not indexes:
                    return False
                for idx in reversed(indexes):
                    del self._reactions[idx]
                return True

            idx = self._find_index(doc_id, user_id, reaction_type)
            if idx is None:
                return False
            del self._reactions[idx]
            return True

    def remove_all_for_doc(self, doc_id: str) -> int:
        """Remove every reaction on a document. Returns number removed."""
        with self._lock:
            before = len(self._reactions)
            self._reactions = [
                r for r in self._reactions if r.doc_id != doc_id
            ]
            return before - len(self._reactions)

    def remove_all_for_user(self, user_id: str) -> int:
        """Remove every reaction by a user. Returns number removed."""
        with self._lock:
            before = len(self._reactions)
            self._reactions = [
                r for r in self._reactions if r.user_id != user_id
            ]
            return before - len(self._reactions)

    def clear(self) -> None:
        """Drop all reactions."""
        with self._lock:
            self._reactions.clear()

    # ------------------------------------------------------------------
    # Queries
    # ------------------------------------------------------------------
    def reactions_for_doc(self, doc_id: str) -> list[Reaction]:
        with self._lock:
            return [r for r in self._reactions if r.doc_id == doc_id]

    def reactions_by_user(self, user_id: str) -> list[Reaction]:
        with self._lock:
            return [r for r in self._reactions if r.user_id == user_id]

    def summary(self, doc_id: str) -> ReactionSummary:
        with self._lock:
            counts: dict[ReactionType, int] = {}
            users: set[str] = set()
            total = 0
            for r in self._reactions:
                if r.doc_id != doc_id:
                    continue
                counts[r.reaction_type] = counts.get(r.reaction_type, 0) + 1
                users.add(r.user_id)
                total += 1
            top_reaction: Optional[ReactionType] = None
            if counts:
                # Deterministic tie-break: higher count first, then enum name.
                top_reaction = max(
                    counts.items(),
                    key=lambda kv: (kv[1], -list(ReactionType).index(kv[0])),
                )[0]
            return ReactionSummary(
                doc_id=doc_id,
                counts=counts,
                total=total,
                top_reaction=top_reaction,
                unique_reactors=len(users),
            )

    def count(
        self,
        doc_id: str,
        reaction_type: Optional[ReactionType] = None,
    ) -> int:
        with self._lock:
            if reaction_type is None:
                return sum(1 for r in self._reactions if r.doc_id == doc_id)
            return sum(
                1
                for r in self._reactions
                if r.doc_id == doc_id and r.reaction_type == reaction_type
            )

    def top_reactions(
        self, doc_id: str, top_k: int = 3
    ) -> list[tuple[ReactionType, int]]:
        if top_k <= 0:
            return []
        with self._lock:
            counts: dict[ReactionType, int] = {}
            for r in self._reactions:
                if r.doc_id != doc_id:
                    continue
                counts[r.reaction_type] = counts.get(r.reaction_type, 0) + 1
        items = sorted(
            counts.items(),
            key=lambda kv: (-kv[1], list(ReactionType).index(kv[0])),
        )
        return items[:top_k]

    def has_reacted(
        self,
        doc_id: str,
        user_id: str,
        reaction_type: Optional[ReactionType] = None,
    ) -> bool:
        with self._lock:
            for r in self._reactions:
                if r.doc_id != doc_id or r.user_id != user_id:
                    continue
                if reaction_type is None or r.reaction_type == reaction_type:
                    return True
            return False

    def user_activity(self, user_id: str) -> Optional[UserActivity]:
        with self._lock:
            by_type: dict[ReactionType, int] = {}
            total = 0
            last_at = 0.0
            for r in self._reactions:
                if r.user_id != user_id:
                    continue
                by_type[r.reaction_type] = by_type.get(r.reaction_type, 0) + 1
                total += 1
                if r.created_at > last_at:
                    last_at = r.created_at
            if total == 0:
                return None
            return UserActivity(
                user_id=user_id,
                total_reactions=total,
                by_type=by_type,
                last_at=last_at,
            )

    def most_reacted_docs(
        self, top_k: int = 10
    ) -> list[tuple[str, int]]:
        if top_k <= 0:
            return []
        with self._lock:
            counts: dict[str, int] = {}
            for r in self._reactions:
                counts[r.doc_id] = counts.get(r.doc_id, 0) + 1
        items = sorted(counts.items(), key=lambda kv: (-kv[1], kv[0]))
        return items[:top_k]

    def most_active_users(
        self, top_k: int = 10
    ) -> list[tuple[str, int]]:
        if top_k <= 0:
            return []
        with self._lock:
            counts: dict[str, int] = {}
            for r in self._reactions:
                counts[r.user_id] = counts.get(r.user_id, 0) + 1
        items = sorted(counts.items(), key=lambda kv: (-kv[1], kv[0]))
        return items[:top_k]

    # ------------------------------------------------------------------
    # Aggregate properties
    # ------------------------------------------------------------------
    @property
    def total_reactions(self) -> int:
        with self._lock:
            return len(self._reactions)

    @property
    def total_unique_docs(self) -> int:
        with self._lock:
            return len({r.doc_id for r in self._reactions})

    @property
    def total_unique_users(self) -> int:
        with self._lock:
            return len({r.user_id for r in self._reactions})
