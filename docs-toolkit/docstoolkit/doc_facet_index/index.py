"""DocFacetIndex implementation — inverted index for faceted document search.

Pure stdlib, thread-safe via :class:`threading.Lock`, dataclasses throughout.
"""

from __future__ import annotations

import threading
from dataclasses import dataclass, field
from typing import Dict, List, Optional, Set


@dataclass
class FacetValue:
    """A single facet value with its document count."""

    value: str
    count: int


@dataclass
class FacetResult:
    """Breakdown of values for one facet.

    ``values`` are sorted by count descending, then value ascending.
    """

    facet: str
    values: List[FacetValue] = field(default_factory=list)


@dataclass
class FacetStats:
    """Aggregate statistics for the facet index."""

    total_docs: int
    total_facets: int
    total_facet_assignments: int


class DocFacetIndex:
    """Inverted index over (doc_id, facet, value) assignments.

    Thread-safe — every public mutating or reading method acquires an
    internal :class:`threading.Lock`.
    """

    def __init__(self) -> None:
        # doc_id → {facet → set of values}
        self._doc_facets: Dict[str, Dict[str, Set[str]]] = {}
        # facet → {value → set of doc_ids}
        self._facet_index: Dict[str, Dict[str, Set[str]]] = {}
        self._lock = threading.Lock()

    # ------------------------------------------------------------------ writes

    def add_facet(self, doc_id: str, facet: str, value: str) -> bool:
        """Assign ``value`` of ``facet`` to ``doc_id``.

        Returns ``True`` if the assignment was newly added, ``False`` if it
        already existed.
        """
        with self._lock:
            doc_bucket = self._doc_facets.setdefault(doc_id, {})
            value_set = doc_bucket.setdefault(facet, set())
            if value in value_set:
                return False
            value_set.add(value)

            facet_bucket = self._facet_index.setdefault(facet, {})
            doc_set = facet_bucket.setdefault(value, set())
            doc_set.add(doc_id)
            return True

    def remove_facet(self, doc_id: str, facet: str, value: str) -> bool:
        """Remove a single assignment.

        Returns ``True`` if something was removed, ``False`` otherwise.
        """
        with self._lock:
            doc_bucket = self._doc_facets.get(doc_id)
            if not doc_bucket:
                return False
            value_set = doc_bucket.get(facet)
            if not value_set or value not in value_set:
                return False
            value_set.discard(value)
            if not value_set:
                doc_bucket.pop(facet, None)
            if not doc_bucket:
                self._doc_facets.pop(doc_id, None)

            facet_bucket = self._facet_index.get(facet)
            if facet_bucket is not None:
                doc_set = facet_bucket.get(value)
                if doc_set is not None:
                    doc_set.discard(doc_id)
                    if not doc_set:
                        facet_bucket.pop(value, None)
                if not facet_bucket:
                    self._facet_index.pop(facet, None)
            return True

    def clear_doc(self, doc_id: str) -> int:
        """Remove all facet assignments for ``doc_id``.

        Returns the number of (facet, value) assignments removed.
        """
        with self._lock:
            doc_bucket = self._doc_facets.pop(doc_id, None)
            if not doc_bucket:
                return 0
            removed = 0
            for facet, values in doc_bucket.items():
                facet_bucket = self._facet_index.get(facet)
                for value in values:
                    removed += 1
                    if facet_bucket is None:
                        continue
                    doc_set = facet_bucket.get(value)
                    if doc_set is None:
                        continue
                    doc_set.discard(doc_id)
                    if not doc_set:
                        facet_bucket.pop(value, None)
                if facet_bucket is not None and not facet_bucket:
                    self._facet_index.pop(facet, None)
            return removed

    def clear_facet(self, facet: str) -> int:
        """Remove every assignment for ``facet`` across all documents.

        Returns the number of (doc_id, value) assignments removed.
        """
        with self._lock:
            facet_bucket = self._facet_index.pop(facet, None)
            if not facet_bucket:
                return 0
            removed = 0
            for value, doc_set in facet_bucket.items():
                for doc_id in doc_set:
                    removed += 1
                    doc_bucket = self._doc_facets.get(doc_id)
                    if doc_bucket is None:
                        continue
                    value_set = doc_bucket.get(facet)
                    if value_set is None:
                        continue
                    value_set.discard(value)
                    if not value_set:
                        doc_bucket.pop(facet, None)
                    if not doc_bucket:
                        self._doc_facets.pop(doc_id, None)
            return removed

    # ------------------------------------------------------------------- reads

    def facets_for_doc(self, doc_id: str) -> Dict[str, List[str]]:
        """Return ``{facet → sorted list of values}`` for ``doc_id``.

        Returns an empty dict if the document is not indexed.
        """
        with self._lock:
            doc_bucket = self._doc_facets.get(doc_id)
            if not doc_bucket:
                return {}
            return {facet: sorted(values) for facet, values in doc_bucket.items()}

    def docs_with_facet(self, facet: str, value: str) -> List[str]:
        """Return sorted list of doc_ids tagged with ``facet=value``."""
        with self._lock:
            facet_bucket = self._facet_index.get(facet)
            if not facet_bucket:
                return []
            doc_set = facet_bucket.get(value)
            if not doc_set:
                return []
            return sorted(doc_set)

    def docs_matching(self, criteria: Dict[str, str]) -> List[str]:
        """Return sorted doc_ids that match every ``facet=value`` in criteria.

        An empty criteria dict returns all known doc_ids.
        """
        with self._lock:
            if not criteria:
                return sorted(self._doc_facets.keys())
            sets: List[Set[str]] = []
            for facet, value in criteria.items():
                facet_bucket = self._facet_index.get(facet)
                if not facet_bucket:
                    return []
                doc_set = facet_bucket.get(value)
                if not doc_set:
                    return []
                sets.append(doc_set)
            if not sets:
                return []
            result = set(sets[0])
            for s in sets[1:]:
                result &= s
                if not result:
                    return []
            return sorted(result)

    def facet_result(
        self,
        facet: str,
        candidate_docs: Optional[List[str]] = None,
    ) -> FacetResult:
        """Compute a :class:`FacetResult` for ``facet``.

        If ``candidate_docs`` is provided, counts are restricted to that set.
        Otherwise all documents that carry the facet are counted.
        """
        with self._lock:
            facet_bucket = self._facet_index.get(facet)
            if not facet_bucket:
                return FacetResult(facet=facet, values=[])
            candidate_set: Optional[Set[str]] = (
                set(candidate_docs) if candidate_docs is not None else None
            )
            counted: List[FacetValue] = []
            for value, doc_set in facet_bucket.items():
                if candidate_set is None:
                    n = len(doc_set)
                else:
                    n = len(doc_set & candidate_set)
                if n > 0:
                    counted.append(FacetValue(value=value, count=n))
            counted.sort(key=lambda fv: (-fv.count, fv.value))
            return FacetResult(facet=facet, values=counted)

    def all_facets(self) -> List[str]:
        """Return all known facet names, sorted."""
        with self._lock:
            return sorted(self._facet_index.keys())

    def values_of(self, facet: str) -> List[str]:
        """Return sorted values currently registered for ``facet``."""
        with self._lock:
            facet_bucket = self._facet_index.get(facet)
            if not facet_bucket:
                return []
            return sorted(facet_bucket.keys())

    def stats(self) -> FacetStats:
        """Return aggregate index statistics."""
        with self._lock:
            total_docs = len(self._doc_facets)
            total_facets = len(self._facet_index)
            assignments = 0
            for doc_bucket in self._doc_facets.values():
                for values in doc_bucket.values():
                    assignments += len(values)
            return FacetStats(
                total_docs=total_docs,
                total_facets=total_facets,
                total_facet_assignments=assignments,
            )
