"""E392 DocTopicIndex — pure-stdlib topic-based document index.

Provides a hierarchical topic registry plus doc<->topic assignment tracking.
Thread-safe via a single :class:`threading.Lock`.
"""
from __future__ import annotations

import threading
import time
from collections import deque
from dataclasses import dataclass
from typing import Optional


# ---------------------------------------------------------------------------
# Dataclasses
# ---------------------------------------------------------------------------

@dataclass
class Topic:
    """A topic definition.

    Attributes
    ----------
    topic_id:
        Unique identifier for the topic.
    name:
        Human-readable display name.
    description:
        Optional free-form description.
    parent_topic:
        Optional parent topic_id (forming a hierarchy).
    """

    topic_id: str
    name: str
    description: str = ""
    parent_topic: Optional[str] = None


@dataclass
class TopicAssignment:
    """An assignment of a document to a topic.

    Attributes
    ----------
    doc_id:
        The document identifier.
    topic_id:
        The topic identifier.
    relevance:
        Relevance score in ``[0.0, 1.0]``.
    assigned_at:
        Unix timestamp of assignment (0.0 if not set).
    """

    doc_id: str
    topic_id: str
    relevance: float = 1.0
    assigned_at: float = 0.0


@dataclass
class TopicIndexStats:
    """Aggregate statistics for :class:`DocTopicIndex`."""

    total_topics: int
    total_assignments: int
    unique_docs: int
    root_topic_count: int


# ---------------------------------------------------------------------------
# DocTopicIndex
# ---------------------------------------------------------------------------

class DocTopicIndex:
    """Thread-safe topic registry plus doc<->topic assignments.

    The index manages:

    * a flat dictionary of :class:`Topic` definitions keyed by ``topic_id``,
    * a parent/child hierarchy among topics,
    * many-to-many assignments of documents to topics with a relevance score.
    """

    def __init__(self) -> None:
        self._lock = threading.Lock()

        self._topics: dict[str, Topic] = {}
        self._assignments: dict[tuple[str, str], TopicAssignment] = {}
        self._by_doc: dict[str, set[str]] = {}
        self._by_topic: dict[str, set[str]] = {}
        self._children: dict[str, set[str]] = {}

    # ------------------------------------------------------------------
    # Topic definition
    # ------------------------------------------------------------------

    def define_topic(self, topic: Topic) -> None:
        """Register or replace a topic. Updates the parent/child index."""
        with self._lock:
            existing = self._topics.get(topic.topic_id)
            # Detach from existing parent if applicable
            if existing is not None and existing.parent_topic is not None:
                kids = self._children.get(existing.parent_topic)
                if kids is not None:
                    kids.discard(topic.topic_id)
                    if not kids:
                        self._children.pop(existing.parent_topic, None)

            self._topics[topic.topic_id] = topic

            # Attach to new parent
            if topic.parent_topic is not None:
                self._children.setdefault(topic.parent_topic, set()).add(topic.topic_id)

    def undefine_topic(self, topic_id: str) -> bool:
        """Remove a topic and its assignments. Orphans any children
        (their ``parent_topic`` is reset to ``None``).

        Returns ``True`` if the topic existed, otherwise ``False``.
        """
        with self._lock:
            topic = self._topics.pop(topic_id, None)
            if topic is None:
                return False

            # Detach from parent's child set
            if topic.parent_topic is not None:
                kids = self._children.get(topic.parent_topic)
                if kids is not None:
                    kids.discard(topic_id)
                    if not kids:
                        self._children.pop(topic.parent_topic, None)

            # Orphan children: set their parent_topic to None
            child_ids = list(self._children.pop(topic_id, set()))
            for child_id in child_ids:
                child = self._topics.get(child_id)
                if child is not None:
                    child.parent_topic = None

            # Remove assignments
            doc_ids = list(self._by_topic.pop(topic_id, set()))
            for did in doc_ids:
                self._assignments.pop((did, topic_id), None)
                topic_set = self._by_doc.get(did)
                if topic_set is not None:
                    topic_set.discard(topic_id)
                    if not topic_set:
                        self._by_doc.pop(did, None)

            return True

    def get_topic(self, topic_id: str) -> Optional[Topic]:
        """Return the topic with the given id, or ``None``."""
        with self._lock:
            return self._topics.get(topic_id)

    def list_topics(self) -> list[Topic]:
        """All topics, sorted by ``topic_id``."""
        with self._lock:
            return sorted(self._topics.values(), key=lambda t: t.topic_id)

    def root_topics(self) -> list[Topic]:
        """Topics with no parent, sorted by ``name``."""
        with self._lock:
            roots = [t for t in self._topics.values() if t.parent_topic is None]
            return sorted(roots, key=lambda t: t.name)

    def child_topics(self, parent_id: str) -> list[Topic]:
        """Direct children of ``parent_id``, sorted by ``name``."""
        with self._lock:
            child_ids = self._children.get(parent_id, set())
            children = [self._topics[c] for c in child_ids if c in self._topics]
            return sorted(children, key=lambda t: t.name)

    def descendant_topics(self, parent_id: str) -> list[Topic]:
        """All descendants of ``parent_id`` via BFS. Each BFS level is
        traversed in ``topic_id`` sort order so the output is deterministic.
        """
        with self._lock:
            if parent_id not in self._topics:
                return []
            out: list[Topic] = []
            seen: set[str] = {parent_id}
            queue: deque[str] = deque()

            initial = sorted(self._children.get(parent_id, set()))
            for cid in initial:
                queue.append(cid)
                seen.add(cid)

            while queue:
                # Process one BFS level
                level_size = len(queue)
                level_ids: list[str] = []
                for _ in range(level_size):
                    level_ids.append(queue.popleft())
                level_ids.sort()
                for cid in level_ids:
                    topic = self._topics.get(cid)
                    if topic is not None:
                        out.append(topic)
                    next_kids = sorted(self._children.get(cid, set()))
                    for nk in next_kids:
                        if nk not in seen:
                            seen.add(nk)
                            queue.append(nk)
            return out

    # ------------------------------------------------------------------
    # Assignments
    # ------------------------------------------------------------------

    def assign_topic(
        self,
        doc_id: str,
        topic_id: str,
        relevance: float = 1.0,
        now: Optional[float] = None,
    ) -> Optional[TopicAssignment]:
        """Assign a document to a topic. Returns ``None`` if the topic
        isn't defined. ``relevance`` is clamped to ``[0.0, 1.0]``.
        """
        with self._lock:
            if topic_id not in self._topics:
                return None

            r = float(relevance)
            if r < 0.0:
                r = 0.0
            elif r > 1.0:
                r = 1.0

            ts = float(now) if now is not None else time.time()

            assignment = TopicAssignment(
                doc_id=doc_id,
                topic_id=topic_id,
                relevance=r,
                assigned_at=ts,
            )
            self._assignments[(doc_id, topic_id)] = assignment
            self._by_doc.setdefault(doc_id, set()).add(topic_id)
            self._by_topic.setdefault(topic_id, set()).add(doc_id)
            return assignment

    def unassign_topic(self, doc_id: str, topic_id: str) -> bool:
        """Remove the assignment of ``doc_id`` from ``topic_id``.
        Returns ``True`` if the assignment existed.
        """
        with self._lock:
            removed = self._assignments.pop((doc_id, topic_id), None)
            if removed is None:
                return False

            doc_topics = self._by_doc.get(doc_id)
            if doc_topics is not None:
                doc_topics.discard(topic_id)
                if not doc_topics:
                    self._by_doc.pop(doc_id, None)

            topic_docs = self._by_topic.get(topic_id)
            if topic_docs is not None:
                topic_docs.discard(doc_id)
                if not topic_docs:
                    self._by_topic.pop(topic_id, None)
            return True

    def topics_for_doc(self, doc_id: str) -> list[TopicAssignment]:
        """Assignments for ``doc_id``, sorted by ``relevance`` desc then
        ``topic_id`` asc.
        """
        with self._lock:
            topic_ids = self._by_doc.get(doc_id)
            if not topic_ids:
                return []
            results: list[TopicAssignment] = []
            for tid in topic_ids:
                a = self._assignments.get((doc_id, tid))
                if a is not None:
                    results.append(a)
            results.sort(key=lambda a: (-a.relevance, a.topic_id))
            return results

    def docs_for_topic(
        self,
        topic_id: str,
        min_relevance: float = 0.0,
        include_descendants: bool = False,
    ) -> list[str]:
        """Document ids assigned to ``topic_id`` (and optionally its
        descendants), filtered by ``min_relevance``. Returned sorted.
        """
        with self._lock:
            topic_ids: list[str] = [topic_id]
            if include_descendants:
                # Inline BFS, since we already hold the lock
                seen: set[str] = {topic_id}
                queue: deque[str] = deque([topic_id])
                while queue:
                    cur = queue.popleft()
                    for child in self._children.get(cur, set()):
                        if child not in seen:
                            seen.add(child)
                            topic_ids.append(child)
                            queue.append(child)

            doc_ids: set[str] = set()
            for tid in topic_ids:
                for did in self._by_topic.get(tid, set()):
                    a = self._assignments.get((did, tid))
                    if a is None:
                        continue
                    if a.relevance >= min_relevance:
                        doc_ids.add(did)
            return sorted(doc_ids)

    def top_topics(self, limit: int = 10) -> list[tuple[str, int]]:
        """``(topic_id, doc_count)`` pairs, sorted by count desc then
        ``topic_id`` asc. Topics with no assignments are excluded.
        """
        with self._lock:
            if limit < 0:
                limit = 0
            pairs = [(tid, len(docs)) for tid, docs in self._by_topic.items() if docs]
            pairs.sort(key=lambda kv: (-kv[1], kv[0]))
            return pairs[:limit]

    def clear_doc(self, doc_id: str) -> int:
        """Remove all assignments for ``doc_id``. Returns the count removed."""
        with self._lock:
            topic_ids = list(self._by_doc.pop(doc_id, set()))
            count = 0
            for tid in topic_ids:
                if self._assignments.pop((doc_id, tid), None) is not None:
                    count += 1
                topic_docs = self._by_topic.get(tid)
                if topic_docs is not None:
                    topic_docs.discard(doc_id)
                    if not topic_docs:
                        self._by_topic.pop(tid, None)
            return count

    # ------------------------------------------------------------------
    # Stats
    # ------------------------------------------------------------------

    def stats(self) -> TopicIndexStats:
        """Aggregate stats: topics, assignments, unique docs, roots."""
        with self._lock:
            root_count = sum(
                1 for t in self._topics.values() if t.parent_topic is None
            )
            return TopicIndexStats(
                total_topics=len(self._topics),
                total_assignments=len(self._assignments),
                unique_docs=len(self._by_doc),
                root_topic_count=root_count,
            )
