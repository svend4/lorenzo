"""Document concept map: concepts, related-concept graph, and doc associations.

This module provides:
- :class:`Concept`: a single concept (id, name, description, related ids).
- :class:`ConceptStats`: aggregate statistics over the map.
- :class:`DocConceptMap`: thread-safe container linking concepts and documents.

All public operations are protected by a single ``threading.Lock``. The
implementation uses only the Python standard library.
"""

from __future__ import annotations

import threading
from collections import deque
from dataclasses import dataclass, field
from typing import Optional


@dataclass
class Concept:
    """A single concept with optional description and related concept ids."""

    concept_id: str
    name: str
    description: str = ""
    related: list[str] = field(default_factory=list)
    created_at: float = 0.0


@dataclass
class ConceptStats:
    """Aggregate statistics about the concept map."""

    total_concepts: int
    total_associations: int
    unique_docs: int


class DocConceptMap:
    """Thread-safe document <-> concept map."""

    def __init__(self) -> None:
        self._lock = threading.Lock()
        self._concepts: dict[str, Concept] = {}
        # doc_id -> set of concept_ids
        self._doc_concepts: dict[str, set[str]] = {}
        # concept_id -> set of doc_ids
        self._concept_docs: dict[str, set[str]] = {}

    # ------------------------------------------------------------------ #
    # Concept lifecycle                                                  #
    # ------------------------------------------------------------------ #
    def define_concept(
        self,
        concept_id: str,
        name: str,
        description: str = "",
        related: Optional[list[str]] = None,
        now: Optional[float] = None,
    ) -> Concept:
        """Define or overwrite a concept and return it."""
        with self._lock:
            concept = Concept(
                concept_id=concept_id,
                name=name,
                description=description,
                related=list(related) if related else [],
                created_at=float(now) if now is not None else 0.0,
            )
            self._concepts[concept_id] = concept
            # Ensure the inverse index has an entry (may be empty).
            self._concept_docs.setdefault(concept_id, set())
            return concept

    def undefine_concept(self, concept_id: str) -> bool:
        """Remove a concept and all associations to it.

        Also removes ``concept_id`` from any other concept's ``related`` list.
        """
        with self._lock:
            if concept_id not in self._concepts:
                return False
            del self._concepts[concept_id]
            # Drop from inverse index and clean up doc -> concepts mappings.
            docs = self._concept_docs.pop(concept_id, set())
            for doc_id in docs:
                doc_set = self._doc_concepts.get(doc_id)
                if doc_set is not None:
                    doc_set.discard(concept_id)
                    if not doc_set:
                        del self._doc_concepts[doc_id]
            # Clean up related references in remaining concepts.
            for other in self._concepts.values():
                if concept_id in other.related:
                    other.related = [r for r in other.related if r != concept_id]
            return True

    def get_concept(self, concept_id: str) -> Optional[Concept]:
        """Return the concept or ``None``."""
        with self._lock:
            return self._concepts.get(concept_id)

    # ------------------------------------------------------------------ #
    # Related concepts                                                   #
    # ------------------------------------------------------------------ #
    def add_related(self, concept_id: str, related_id: str) -> bool:
        """Add ``related_id`` to ``concept_id``'s related list if not present.

        Returns True if a new relation was added. Returns False if either
        concept is missing or the relation already exists.
        """
        with self._lock:
            concept = self._concepts.get(concept_id)
            if concept is None:
                return False
            if related_id not in self._concepts:
                return False
            if related_id in concept.related:
                return False
            concept.related.append(related_id)
            return True

    def remove_related(self, concept_id: str, related_id: str) -> bool:
        """Remove ``related_id`` from ``concept_id``'s related list."""
        with self._lock:
            concept = self._concepts.get(concept_id)
            if concept is None:
                return False
            if related_id not in concept.related:
                return False
            concept.related = [r for r in concept.related if r != related_id]
            return True

    # ------------------------------------------------------------------ #
    # Document associations                                              #
    # ------------------------------------------------------------------ #
    def associate(self, doc_id: str, concept_id: str) -> bool:
        """Associate a document with a concept.

        Returns True if a new association was created. Returns False when the
        concept is missing or the association already exists.
        """
        with self._lock:
            if concept_id not in self._concepts:
                return False
            doc_set = self._doc_concepts.setdefault(doc_id, set())
            if concept_id in doc_set:
                return False
            doc_set.add(concept_id)
            self._concept_docs.setdefault(concept_id, set()).add(doc_id)
            return True

    def disassociate(self, doc_id: str, concept_id: str) -> bool:
        """Remove a doc <-> concept association.

        Returns True if it existed, False otherwise.
        """
        with self._lock:
            doc_set = self._doc_concepts.get(doc_id)
            if doc_set is None or concept_id not in doc_set:
                return False
            doc_set.discard(concept_id)
            if not doc_set:
                del self._doc_concepts[doc_id]
            concept_set = self._concept_docs.get(concept_id)
            if concept_set is not None:
                concept_set.discard(doc_id)
            return True

    def concepts_for_doc(self, doc_id: str) -> list[Concept]:
        """Return all concepts associated with ``doc_id``, sorted by name."""
        with self._lock:
            ids = self._doc_concepts.get(doc_id, set())
            concepts = [self._concepts[c] for c in ids if c in self._concepts]
            concepts.sort(key=lambda c: c.name)
            return concepts

    def docs_for_concept(self, concept_id: str) -> list[str]:
        """Return all doc ids associated with ``concept_id``, sorted."""
        with self._lock:
            docs = self._concept_docs.get(concept_id, set())
            return sorted(docs)

    # ------------------------------------------------------------------ #
    # Graph queries                                                      #
    # ------------------------------------------------------------------ #
    def related_concepts(
        self,
        concept_id: str,
        transitive: bool = False,
        max_depth: int = 3,
    ) -> list[Concept]:
        """Return concepts related to ``concept_id``.

        If ``transitive`` is False, returns the direct related concepts.
        If True, performs a BFS walk to ``max_depth`` and returns all
        reachable concepts (excluding the seed). Result sorted by name.
        """
        with self._lock:
            seed = self._concepts.get(concept_id)
            if seed is None:
                return []
            if not transitive:
                direct = [
                    self._concepts[r]
                    for r in seed.related
                    if r in self._concepts
                ]
                direct.sort(key=lambda c: c.name)
                return direct

            if max_depth <= 0:
                return []

            visited: set[str] = {concept_id}
            collected: set[str] = set()
            queue: deque[tuple[str, int]] = deque([(concept_id, 0)])
            while queue:
                current, depth = queue.popleft()
                if depth >= max_depth:
                    continue
                node = self._concepts.get(current)
                if node is None:
                    continue
                for r in node.related:
                    if r in visited:
                        continue
                    if r not in self._concepts:
                        continue
                    visited.add(r)
                    collected.add(r)
                    queue.append((r, depth + 1))
            result = [self._concepts[c] for c in collected]
            result.sort(key=lambda c: c.name)
            return result

    def find_concepts_by_name(self, query: str) -> list[Concept]:
        """Return concepts whose ``name`` contains ``query`` (case-insensitive)."""
        with self._lock:
            q = query.lower()
            matches = [
                c for c in self._concepts.values() if q in c.name.lower()
            ]
            matches.sort(key=lambda c: c.name)
            return matches

    def co_occurring_concepts(
        self, concept_id: str, limit: int = 10
    ) -> list[tuple]:
        """Return concepts that share documents with ``concept_id``.

        Result is a list of ``(other_concept_id, count)`` tuples sorted by
        count descending, then by concept_id ascending. Limited to ``limit``.
        """
        with self._lock:
            if concept_id not in self._concepts:
                return []
            docs = self._concept_docs.get(concept_id, set())
            counts: dict[str, int] = {}
            for doc_id in docs:
                for other in self._doc_concepts.get(doc_id, set()):
                    if other == concept_id:
                        continue
                    counts[other] = counts.get(other, 0) + 1
            ranked = sorted(
                counts.items(), key=lambda kv: (-kv[1], kv[0])
            )
            if limit is not None and limit >= 0:
                ranked = ranked[:limit]
            return ranked

    # ------------------------------------------------------------------ #
    # Bulk operations                                                    #
    # ------------------------------------------------------------------ #
    def clear_doc(self, doc_id: str) -> int:
        """Remove all associations for ``doc_id``. Returns the count removed."""
        with self._lock:
            doc_set = self._doc_concepts.pop(doc_id, None)
            if not doc_set:
                return 0
            removed = 0
            for concept_id in doc_set:
                concept_set = self._concept_docs.get(concept_id)
                if concept_set is not None and doc_id in concept_set:
                    concept_set.discard(doc_id)
                    removed += 1
            return removed

    def all_concept_ids(self) -> list[str]:
        """Return all concept ids sorted."""
        with self._lock:
            return sorted(self._concepts.keys())

    def all_doc_ids(self) -> list[str]:
        """Return all doc ids that have associations, sorted."""
        with self._lock:
            return sorted(self._doc_concepts.keys())

    def stats(self) -> ConceptStats:
        """Return aggregate statistics."""
        with self._lock:
            total_associations = sum(
                len(s) for s in self._doc_concepts.values()
            )
            return ConceptStats(
                total_concepts=len(self._concepts),
                total_associations=total_associations,
                unique_docs=len(self._doc_concepts),
            )
