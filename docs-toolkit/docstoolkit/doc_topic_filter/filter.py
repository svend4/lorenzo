"""E444 DocTopicFilter — filter documents by topic membership.

Pure-stdlib implementation. Thread-safe via a single :class:`threading.Lock`.
"""
from __future__ import annotations

import threading
from dataclasses import dataclass, field
from typing import Optional


# ---------------------------------------------------------------------------
# Dataclasses
# ---------------------------------------------------------------------------

@dataclass
class TopicMembership:
    """A snapshot of a document's topic memberships.

    Attributes
    ----------
    doc_id:
        The document identifier.
    topics:
        Sorted list of topic names the document belongs to.
    weights:
        Mapping ``topic -> weight`` where weight is in ``[0.0, 1.0]``.
    """

    doc_id: str
    topics: list[str] = field(default_factory=list)
    weights: dict = field(default_factory=dict)


@dataclass
class FilterStats:
    """Aggregate statistics for :class:`DocTopicFilter`."""

    total_docs: int
    unique_topics: int
    total_memberships: int


# ---------------------------------------------------------------------------
# DocTopicFilter
# ---------------------------------------------------------------------------

class DocTopicFilter:
    """Thread-safe document-by-topic filter.

    Tracks many-to-many doc<->topic assignments with weights and supports
    OR/AND filtering, Jaccard distance and topic co-membership queries.
    """

    def __init__(self) -> None:
        self._lock = threading.Lock()
        self._doc_topics: dict[str, dict[str, float]] = {}
        self._topic_docs: dict[str, set[str]] = {}

    # ------------------------------------------------------------------
    # Internal helpers (must be called while holding the lock)
    # ------------------------------------------------------------------

    @staticmethod
    def _clamp(weight: float) -> float:
        w = float(weight)
        if w < 0.0:
            return 0.0
        if w > 1.0:
            return 1.0
        return w

    def _remove_topic_for_doc(self, doc_id: str, topic: str) -> bool:
        doc_map = self._doc_topics.get(doc_id)
        if doc_map is None or topic not in doc_map:
            return False
        doc_map.pop(topic, None)
        if not doc_map:
            self._doc_topics.pop(doc_id, None)

        topic_set = self._topic_docs.get(topic)
        if topic_set is not None:
            topic_set.discard(doc_id)
            if not topic_set:
                self._topic_docs.pop(topic, None)
        return True

    # ------------------------------------------------------------------
    # Assignment API
    # ------------------------------------------------------------------

    def assign_topic(self, doc_id: str, topic: str, weight: float = 1.0) -> bool:
        """Assign ``topic`` to ``doc_id`` with ``weight`` (clamped to ``[0,1]``).

        Returns ``True`` if this is a new assignment or the weight changed,
        ``False`` if the weight is unchanged.
        """
        with self._lock:
            w = self._clamp(weight)
            doc_map = self._doc_topics.setdefault(doc_id, {})
            existing = doc_map.get(topic)
            if existing is not None and existing == w:
                return False
            doc_map[topic] = w
            self._topic_docs.setdefault(topic, set()).add(doc_id)
            return True

    def unassign_topic(self, doc_id: str, topic: str) -> bool:
        """Remove ``topic`` from ``doc_id``. Returns ``True`` if removed."""
        with self._lock:
            return self._remove_topic_for_doc(doc_id, topic)

    def set_topics(self, doc_id: str, topic_weights: dict) -> None:
        """Replace all topics of ``doc_id`` with ``topic_weights``.

        If ``topic_weights`` is empty, the document is removed entirely.
        Weights are clamped to ``[0,1]``.
        """
        with self._lock:
            # Remove existing topics for this doc
            old_topics = list(self._doc_topics.get(doc_id, {}).keys())
            for t in old_topics:
                self._remove_topic_for_doc(doc_id, t)

            if not topic_weights:
                return

            new_map: dict[str, float] = {}
            for t, w in topic_weights.items():
                new_map[t] = self._clamp(w)
                self._topic_docs.setdefault(t, set()).add(doc_id)
            self._doc_topics[doc_id] = new_map

    # ------------------------------------------------------------------
    # Inspection API
    # ------------------------------------------------------------------

    def weight_of(self, doc_id: str, topic: str) -> Optional[float]:
        """Weight of ``topic`` for ``doc_id``, or ``None`` if not assigned."""
        with self._lock:
            doc_map = self._doc_topics.get(doc_id)
            if doc_map is None:
                return None
            return doc_map.get(topic)

    def topics_of(self, doc_id: str) -> list[str]:
        """Topics of ``doc_id``, sorted by weight desc then topic asc."""
        with self._lock:
            doc_map = self._doc_topics.get(doc_id)
            if not doc_map:
                return []
            items = list(doc_map.items())
            items.sort(key=lambda kv: (-kv[1], kv[0]))
            return [t for t, _ in items]

    def docs_in_topic(self, topic: str, min_weight: float = 0.0) -> list[str]:
        """Document ids in ``topic`` with weight >= ``min_weight``, sorted."""
        with self._lock:
            doc_ids = self._topic_docs.get(topic)
            if not doc_ids:
                return []
            mw = float(min_weight)
            result: list[str] = []
            for did in doc_ids:
                doc_map = self._doc_topics.get(did)
                if doc_map is None:
                    continue
                w = doc_map.get(topic)
                if w is not None and w >= mw:
                    result.append(did)
            return sorted(result)

    # ------------------------------------------------------------------
    # Filtering
    # ------------------------------------------------------------------

    def filter_any(self, topics: list[str], min_weight: float = 0.0) -> list[str]:
        """Documents matching ANY topic in ``topics`` (OR), sorted."""
        with self._lock:
            mw = float(min_weight)
            result: set[str] = set()
            for t in topics:
                doc_ids = self._topic_docs.get(t)
                if not doc_ids:
                    continue
                for did in doc_ids:
                    doc_map = self._doc_topics.get(did)
                    if doc_map is None:
                        continue
                    w = doc_map.get(t)
                    if w is not None and w >= mw:
                        result.add(did)
            return sorted(result)

    def filter_all(self, topics: list[str], min_weight: float = 0.0) -> list[str]:
        """Documents matching ALL topics in ``topics`` (AND), sorted.

        An empty ``topics`` list returns the empty list.
        """
        with self._lock:
            if not topics:
                return []
            mw = float(min_weight)
            # Start from the smallest topic set for efficiency
            first = topics[0]
            base = self._topic_docs.get(first)
            if not base:
                return []
            candidates = set(base)
            for t in topics[1:]:
                tset = self._topic_docs.get(t)
                if not tset:
                    return []
                candidates &= tset
                if not candidates:
                    return []

            result: list[str] = []
            for did in candidates:
                doc_map = self._doc_topics.get(did, {})
                ok = True
                for t in topics:
                    w = doc_map.get(t)
                    if w is None or w < mw:
                        ok = False
                        break
                if ok:
                    result.append(did)
            return sorted(result)

    # ------------------------------------------------------------------
    # Ranking and relationships
    # ------------------------------------------------------------------

    def top_docs_in_topic(self, topic: str, limit: int = 10) -> list[tuple]:
        """``(doc_id, weight)`` pairs for ``topic`` sorted by weight desc."""
        with self._lock:
            if limit < 0:
                limit = 0
            doc_ids = self._topic_docs.get(topic)
            if not doc_ids:
                return []
            pairs: list[tuple] = []
            for did in doc_ids:
                doc_map = self._doc_topics.get(did)
                if doc_map is None:
                    continue
                w = doc_map.get(topic)
                if w is None:
                    continue
                pairs.append((did, w))
            pairs.sort(key=lambda kv: (-kv[1], kv[0]))
            return pairs[:limit]

    def topic_co_membership(self, topic_a: str, topic_b: str) -> list[str]:
        """Documents that are members of BOTH ``topic_a`` and ``topic_b``."""
        with self._lock:
            a = self._topic_docs.get(topic_a)
            b = self._topic_docs.get(topic_b)
            if not a or not b:
                return []
            return sorted(a & b)

    def topic_distance(self, doc_id_a: str, doc_id_b: str) -> float:
        """Jaccard distance on topic sets. 0.0 = identical, 1.0 = disjoint.

        If either doc has no topics, the distance is 1.0 (disjoint), unless
        both are empty/missing in which case the distance is 0.0.
        """
        with self._lock:
            a = set(self._doc_topics.get(doc_id_a, {}).keys())
            b = set(self._doc_topics.get(doc_id_b, {}).keys())
            if not a and not b:
                return 0.0
            if not a or not b:
                return 1.0
            inter = len(a & b)
            union = len(a | b)
            if union == 0:
                return 0.0
            return 1.0 - (inter / union)

    # ------------------------------------------------------------------
    # Cleanup
    # ------------------------------------------------------------------

    def clear_doc(self, doc_id: str) -> int:
        """Remove all topic assignments for ``doc_id``. Returns count removed."""
        with self._lock:
            doc_map = self._doc_topics.pop(doc_id, None)
            if not doc_map:
                return 0
            count = 0
            for t in list(doc_map.keys()):
                count += 1
                tset = self._topic_docs.get(t)
                if tset is not None:
                    tset.discard(doc_id)
                    if not tset:
                        self._topic_docs.pop(t, None)
            return count

    def clear_topic(self, topic: str) -> int:
        """Remove a topic and all its assignments. Returns count of docs cleared."""
        with self._lock:
            doc_ids = self._topic_docs.pop(topic, None)
            if not doc_ids:
                return 0
            count = 0
            for did in list(doc_ids):
                doc_map = self._doc_topics.get(did)
                if doc_map is None:
                    continue
                if doc_map.pop(topic, None) is not None:
                    count += 1
                if not doc_map:
                    self._doc_topics.pop(did, None)
            return count

    # ------------------------------------------------------------------
    # Bulk listing and stats
    # ------------------------------------------------------------------

    def all_doc_ids(self) -> list[str]:
        """All known document ids, sorted."""
        with self._lock:
            return sorted(self._doc_topics.keys())

    def all_topics(self) -> list[str]:
        """All known topics, sorted."""
        with self._lock:
            return sorted(self._topic_docs.keys())

    def stats(self) -> FilterStats:
        """Aggregate stats: docs, unique topics, total memberships."""
        with self._lock:
            total_memberships = sum(len(m) for m in self._doc_topics.values())
            return FilterStats(
                total_docs=len(self._doc_topics),
                unique_topics=len(self._topic_docs),
                total_memberships=total_memberships,
            )
