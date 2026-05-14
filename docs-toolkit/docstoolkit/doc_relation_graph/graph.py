"""E355 DocRelationGraph — typed relationships between documents.

A pure-stdlib, thread-safe in-memory store of typed directed relations
between document identifiers.  Each relation has a UUID, a type (such as
``"references"``, ``"supersedes"`` or ``"depends_on"``), a weight and
optional metadata.

Indexes are maintained for fast lookup by source, target and relation
type.  All mutating operations are guarded by a :class:`threading.Lock`.
"""
from __future__ import annotations

import threading
import uuid
from dataclasses import dataclass, field
from typing import Optional


# ---------------------------------------------------------------------------
# Dataclasses
# ---------------------------------------------------------------------------


@dataclass
class Relation:
    """A single typed relation between two documents."""

    relation_id: str
    from_doc: str
    to_doc: str
    relation_type: str
    weight: float = 1.0
    created_at: float = 0.0
    metadata: dict = field(default_factory=dict)


@dataclass
class RelationStats:
    """Aggregate statistics about a :class:`DocRelationGraph`."""

    total_relations: int
    unique_docs: int
    unique_types: int
    type_counts: dict = field(default_factory=dict)


# ---------------------------------------------------------------------------
# Graph
# ---------------------------------------------------------------------------


class DocRelationGraph:
    """In-memory store of typed directed relations between documents.

    Parameters
    ----------
    None.

    Notes
    -----
    Thread-safe — every public method that mutates or reads internal
    state acquires a single :class:`threading.Lock`.
    """

    def __init__(self) -> None:
        self._lock = threading.Lock()
        self._relations: dict = {}            # relation_id -> Relation
        self._by_from: dict = {}              # from_doc -> list[relation_id]
        self._by_to: dict = {}                # to_doc -> list[relation_id]
        self._by_type: dict = {}              # relation_type -> set[relation_id]

    # ------------------------------------------------------------------
    # Internal helpers (must be called with the lock held)
    # ------------------------------------------------------------------

    def _index_add(self, rel: Relation) -> None:
        self._relations[rel.relation_id] = rel
        self._by_from.setdefault(rel.from_doc, []).append(rel.relation_id)
        self._by_to.setdefault(rel.to_doc, []).append(rel.relation_id)
        self._by_type.setdefault(rel.relation_type, set()).add(rel.relation_id)

    def _index_remove(self, rel: Relation) -> None:
        del self._relations[rel.relation_id]
        from_list = self._by_from.get(rel.from_doc)
        if from_list is not None:
            try:
                from_list.remove(rel.relation_id)
            except ValueError:
                pass
            if not from_list:
                del self._by_from[rel.from_doc]
        to_list = self._by_to.get(rel.to_doc)
        if to_list is not None:
            try:
                to_list.remove(rel.relation_id)
            except ValueError:
                pass
            if not to_list:
                del self._by_to[rel.to_doc]
        type_set = self._by_type.get(rel.relation_type)
        if type_set is not None:
            type_set.discard(rel.relation_id)
            if not type_set:
                del self._by_type[rel.relation_type]

    @staticmethod
    def _sorted_by_created(rels: list) -> list:
        return sorted(rels, key=lambda r: (r.created_at, r.relation_id))

    # ------------------------------------------------------------------
    # Mutating API
    # ------------------------------------------------------------------

    def add_relation(
        self,
        from_doc: str,
        to_doc: str,
        relation_type: str,
        weight: float = 1.0,
        metadata: Optional[dict] = None,
        now: Optional[float] = None,
    ) -> Relation:
        """Create and store a new :class:`Relation`.

        A fresh UUID is generated for the relation.  ``metadata`` is
        copied defensively.  ``now`` defaults to ``0.0``.
        """
        meta = dict(metadata) if metadata else {}
        created_at = 0.0 if now is None else float(now)
        rel = Relation(
            relation_id=str(uuid.uuid4()),
            from_doc=from_doc,
            to_doc=to_doc,
            relation_type=relation_type,
            weight=float(weight),
            created_at=created_at,
            metadata=meta,
        )
        with self._lock:
            self._index_add(rel)
        return rel

    def remove_relation(self, relation_id: str) -> bool:
        """Remove a relation by id.

        Returns ``True`` if the relation existed, ``False`` otherwise.
        """
        with self._lock:
            rel = self._relations.get(relation_id)
            if rel is None:
                return False
            self._index_remove(rel)
            return True

    def update_weight(self, relation_id: str, new_weight: float) -> bool:
        """Update the ``weight`` of an existing relation.

        Returns ``True`` if the relation was found, ``False`` otherwise.
        """
        with self._lock:
            rel = self._relations.get(relation_id)
            if rel is None:
                return False
            rel.weight = float(new_weight)
            return True

    # ------------------------------------------------------------------
    # Read API
    # ------------------------------------------------------------------

    def get_relation(self, relation_id: str) -> Optional[Relation]:
        """Return a relation by id, or ``None``."""
        with self._lock:
            return self._relations.get(relation_id)

    def outgoing(
        self, doc_id: str, relation_type: Optional[str] = None
    ) -> list:
        """Return outgoing relations from ``doc_id``, sorted by ``created_at``.

        If ``relation_type`` is given, only relations of that type are
        returned.
        """
        with self._lock:
            ids = list(self._by_from.get(doc_id, ()))
            rels = [self._relations[rid] for rid in ids]
        if relation_type is not None:
            rels = [r for r in rels if r.relation_type == relation_type]
        return self._sorted_by_created(rels)

    def incoming(
        self, doc_id: str, relation_type: Optional[str] = None
    ) -> list:
        """Return incoming relations to ``doc_id``, sorted by ``created_at``.

        If ``relation_type`` is given, only relations of that type are
        returned.
        """
        with self._lock:
            ids = list(self._by_to.get(doc_id, ()))
            rels = [self._relations[rid] for rid in ids]
        if relation_type is not None:
            rels = [r for r in rels if r.relation_type == relation_type]
        return self._sorted_by_created(rels)

    def between(self, from_doc: str, to_doc: str) -> list:
        """Return all relations from ``from_doc`` to ``to_doc``.

        Sorted by ``created_at``.
        """
        with self._lock:
            ids = list(self._by_from.get(from_doc, ()))
            rels = [
                self._relations[rid]
                for rid in ids
                if self._relations[rid].to_doc == to_doc
            ]
        return self._sorted_by_created(rels)

    def relations_of_type(self, relation_type: str) -> list:
        """Return all relations of the given type, sorted by ``created_at``."""
        with self._lock:
            ids = list(self._by_type.get(relation_type, ()))
            rels = [self._relations[rid] for rid in ids]
        return self._sorted_by_created(rels)

    def related_docs(self, doc_id: str, direction: str = "both") -> list:
        """Return sorted unique document ids related to ``doc_id``.

        ``direction``:
            * ``"out"`` — only documents pointed to by outgoing relations
            * ``"in"``  — only documents that point to ``doc_id``
            * ``"both"`` — union of both sets (default)

        ``doc_id`` itself is excluded from the result.
        """
        if direction not in ("out", "in", "both"):
            raise ValueError(
                "direction must be 'out', 'in' or 'both', "
                f"got: {direction!r}"
            )
        with self._lock:
            out_ids = list(self._by_from.get(doc_id, ()))
            in_ids = list(self._by_to.get(doc_id, ()))
            related: set = set()
            if direction in ("out", "both"):
                for rid in out_ids:
                    related.add(self._relations[rid].to_doc)
            if direction in ("in", "both"):
                for rid in in_ids:
                    related.add(self._relations[rid].from_doc)
        related.discard(doc_id)
        return sorted(related)

    def all_relation_types(self) -> list:
        """Return all distinct relation types, sorted."""
        with self._lock:
            return sorted(self._by_type.keys())

    def top_referenced_docs(self, limit: int = 10) -> list:
        """Return ``(doc_id, incoming_count)`` pairs for the most-referenced docs.

        Sorted by count descending, then by ``doc_id`` ascending.  Only
        docs with at least one incoming relation appear.  ``limit``
        caps the number of returned items; pass ``0`` for "all".
        """
        with self._lock:
            counts = [
                (doc_id, len(rids))
                for doc_id, rids in self._by_to.items()
                if rids
            ]
        counts.sort(key=lambda pair: (-pair[1], pair[0]))
        if limit and limit > 0:
            return counts[:limit]
        return counts

    def stats(self) -> RelationStats:
        """Return aggregate :class:`RelationStats`."""
        with self._lock:
            total = len(self._relations)
            docs: set = set()
            docs.update(self._by_from.keys())
            docs.update(self._by_to.keys())
            type_counts = {
                rtype: len(rids) for rtype, rids in self._by_type.items()
            }
        return RelationStats(
            total_relations=total,
            unique_docs=len(docs),
            unique_types=len(type_counts),
            type_counts=type_counts,
        )
