"""E414 DocLabelFilter — filter documents by labels with set operations."""

from __future__ import annotations

import threading
from dataclasses import dataclass, field


@dataclass
class LabelSet:
    """Set of labels for a single document."""

    doc_id: str
    labels: list[str] = field(default_factory=list)


@dataclass
class FilterStats:
    """Aggregate statistics over the label filter state."""

    total_docs: int
    unique_labels: int
    total_label_assignments: int


class DocLabelFilter:
    """Thread-safe filter that maps documents to labels and supports
    set-based queries (any / all / none / combo).

    Internal storage
    ----------------
    _doc_labels : dict[str, set[str]] — doc_id → set of labels
    _label_docs : dict[str, set[str]] — label  → set of doc_ids
    """

    def __init__(self) -> None:
        self._lock: threading.Lock = threading.Lock()
        self._doc_labels: dict[str, set[str]] = {}
        self._label_docs: dict[str, set[str]] = {}

    # ------------------------------------------------------------------
    # Mutating: add / remove / set / clear
    # ------------------------------------------------------------------

    def add_labels(self, doc_id: str, labels: list[str]) -> int:
        """Add *labels* to *doc_id*.

        Returns the number of labels that were newly added (already-present
        labels are skipped).
        """
        with self._lock:
            doc_set = self._doc_labels.setdefault(doc_id, set())
            added = 0
            for lbl in labels:
                if lbl not in doc_set:
                    doc_set.add(lbl)
                    self._label_docs.setdefault(lbl, set()).add(doc_id)
                    added += 1
            if not doc_set:
                # Nothing was actually added and nothing was there.
                self._doc_labels.pop(doc_id, None)
            return added

    def remove_labels(self, doc_id: str, labels: list[str]) -> int:
        """Remove *labels* from *doc_id*.

        Returns the number of labels actually removed.
        """
        with self._lock:
            doc_set = self._doc_labels.get(doc_id)
            if not doc_set:
                return 0
            removed = 0
            for lbl in labels:
                if lbl in doc_set:
                    doc_set.discard(lbl)
                    removed += 1
                    label_set = self._label_docs.get(lbl)
                    if label_set is not None:
                        label_set.discard(doc_id)
                        if not label_set:
                            del self._label_docs[lbl]
            if not doc_set:
                del self._doc_labels[doc_id]
            return removed

    def set_labels(self, doc_id: str, labels: list[str]) -> LabelSet:
        """Replace all labels for *doc_id* with *labels* (deduplicated).

        Returns a :class:`LabelSet` reflecting the new state (sorted).
        """
        with self._lock:
            new_set = set(labels)
            old_set = self._doc_labels.get(doc_id, set())

            # Remove labels that are no longer assigned
            for lbl in old_set - new_set:
                label_set = self._label_docs.get(lbl)
                if label_set is not None:
                    label_set.discard(doc_id)
                    if not label_set:
                        del self._label_docs[lbl]

            # Add the new ones
            for lbl in new_set - old_set:
                self._label_docs.setdefault(lbl, set()).add(doc_id)

            if new_set:
                self._doc_labels[doc_id] = new_set
            else:
                self._doc_labels.pop(doc_id, None)

            sorted_labels = sorted(new_set)
        return LabelSet(doc_id=doc_id, labels=sorted_labels)

    def clear_doc(self, doc_id: str) -> int:
        """Remove all labels from *doc_id*.

        Returns the number of labels that were cleared.
        """
        with self._lock:
            doc_set = self._doc_labels.pop(doc_id, None)
            if not doc_set:
                return 0
            count = len(doc_set)
            for lbl in doc_set:
                label_set = self._label_docs.get(lbl)
                if label_set is not None:
                    label_set.discard(doc_id)
                    if not label_set:
                        del self._label_docs[lbl]
            return count

    # ------------------------------------------------------------------
    # Inspection
    # ------------------------------------------------------------------

    def get_labels(self, doc_id: str) -> list[str]:
        """Return sorted labels assigned to *doc_id*."""
        with self._lock:
            return sorted(self._doc_labels.get(doc_id, set()))

    def docs_with_label(self, label: str) -> list[str]:
        """Return sorted doc_ids that have *label* assigned."""
        with self._lock:
            return sorted(self._label_docs.get(label, set()))

    def all_labels(self) -> list[str]:
        """Return all unique labels currently in use, sorted."""
        with self._lock:
            return sorted(self._label_docs)

    def all_doc_ids(self) -> list[str]:
        """Return sorted doc_ids that have at least one label."""
        with self._lock:
            return sorted(self._doc_labels)

    # ------------------------------------------------------------------
    # Filtering: set operations
    # ------------------------------------------------------------------

    def filter_any(self, labels: list[str]) -> list[str]:
        """Return sorted doc_ids that have AT LEAST ONE of *labels* (OR).

        Returns an empty list when *labels* is empty.
        """
        with self._lock:
            if not labels:
                return []
            result: set[str] = set()
            for lbl in labels:
                result |= self._label_docs.get(lbl, set())
        return sorted(result)

    def filter_all(self, labels: list[str]) -> list[str]:
        """Return sorted doc_ids that have ALL of *labels* (AND).

        Returns all docs (with at least one label) when *labels* is empty.
        """
        with self._lock:
            if not labels:
                return sorted(self._doc_labels)
            # If any required label has no docs, intersection is empty.
            sets = [self._label_docs.get(lbl, set()) for lbl in labels]
            if any(not s for s in sets):
                return []
            result = sets[0].copy()
            for s in sets[1:]:
                result &= s
        return sorted(result)

    def filter_none(self, labels: list[str]) -> list[str]:
        """Return sorted doc_ids that have NONE of *labels* (NOT).

        Considers only docs with at least one label.  Returns all such
        docs when *labels* is empty.
        """
        with self._lock:
            all_docs = set(self._doc_labels)
            excluded: set[str] = set()
            for lbl in labels:
                excluded |= self._label_docs.get(lbl, set())
            result = all_docs - excluded
        return sorted(result)

    def filter_combo(
        self,
        must_have: list[str],
        must_not_have: list[str],
    ) -> list[str]:
        """Return sorted doc_ids that have ALL of *must_have* and NONE of
        *must_not_have*.

        Empty *must_have* matches every doc with at least one label.
        Empty *must_not_have* applies no exclusion.
        """
        with self._lock:
            if must_have:
                sets = [self._label_docs.get(lbl, set()) for lbl in must_have]
                if any(not s for s in sets):
                    return []
                included = sets[0].copy()
                for s in sets[1:]:
                    included &= s
            else:
                included = set(self._doc_labels)

            excluded: set[str] = set()
            for lbl in must_not_have:
                excluded |= self._label_docs.get(lbl, set())
            result = included - excluded
        return sorted(result)

    # ------------------------------------------------------------------
    # Aggregates
    # ------------------------------------------------------------------

    def top_labels(self, limit: int = 10) -> list[tuple]:
        """Return the *limit* most-used labels as ``(label, count)`` tuples.

        Sorted by count descending, then by label ascending for stability.
        """
        with self._lock:
            items = [(lbl, len(docs)) for lbl, docs in self._label_docs.items()]
        items.sort(key=lambda x: (-x[1], x[0]))
        if limit < 0:
            limit = 0
        return items[:limit]

    def stats(self) -> FilterStats:
        """Return aggregate statistics."""
        with self._lock:
            total_docs = len(self._doc_labels)
            unique_labels = len(self._label_docs)
            total_assignments = sum(len(v) for v in self._doc_labels.values())
        return FilterStats(
            total_docs=total_docs,
            unique_labels=unique_labels,
            total_label_assignments=total_assignments,
        )
