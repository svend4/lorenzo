"""DocLabelManager — colored label management for documents."""

from __future__ import annotations

import threading
from dataclasses import dataclass, field
from typing import Optional


@dataclass
class Label:
    """A named label with an optional color and description."""

    name: str
    color: str = "#cccccc"
    description: str = ""


@dataclass
class DocLabels:
    """Labels assigned to a single document."""

    doc_id: str
    labels: list[str] = field(default_factory=list)  # sorted label names
    label_count: int = 0


@dataclass
class LabelStats:
    """Aggregate statistics over the label manager state."""

    total_labels: int = 0        # defined labels
    total_docs: int = 0          # docs with at least one label
    total_assignments: int = 0   # sum of all label assignments


class DocLabelManager:
    """Thread-safe manager for label definitions and document label assignments.

    Internal storage
    ----------------
    _labels     : dict[str, Label]       — name → Label definition
    _doc_labels : dict[str, set[str]]    — doc_id → set of label names
    _label_docs : dict[str, set[str]]    — label name → set of doc_ids
    """

    def __init__(self) -> None:
        self._lock: threading.Lock = threading.Lock()
        self._labels: dict[str, Label] = {}
        self._doc_labels: dict[str, set[str]] = {}
        self._label_docs: dict[str, set[str]] = {}

    # ------------------------------------------------------------------
    # Label definition CRUD
    # ------------------------------------------------------------------

    def define_label(self, label: Label) -> None:
        """Register or update a label definition."""
        with self._lock:
            self._labels[label.name] = label

    def undefine_label(self, name: str) -> bool:
        """Remove label definition AND all its assignments.

        Returns True if the label existed, False otherwise.
        """
        with self._lock:
            if name not in self._labels:
                return False
            del self._labels[name]
            # Remove all assignments for this label
            affected_docs = self._label_docs.pop(name, set())
            for doc_id in affected_docs:
                self._doc_labels.get(doc_id, set()).discard(name)
                # Clean up empty doc entries
                if not self._doc_labels.get(doc_id):
                    self._doc_labels.pop(doc_id, None)
            return True

    def get_label(self, name: str) -> Optional[Label]:
        """Return the Label definition for *name*, or None if not defined."""
        with self._lock:
            return self._labels.get(name)

    def list_labels(self) -> list[Label]:
        """Return all defined labels sorted by name."""
        with self._lock:
            return [self._labels[k] for k in sorted(self._labels)]

    # ------------------------------------------------------------------
    # Assignment operations
    # ------------------------------------------------------------------

    def assign_label(self, doc_id: str, label_name: str) -> bool:
        """Assign *label_name* to *doc_id*.

        Does NOT require the label to be predefined (implicit assignment).

        Returns True if newly assigned, False if already present.
        """
        with self._lock:
            doc_set = self._doc_labels.setdefault(doc_id, set())
            if label_name in doc_set:
                return False
            doc_set.add(label_name)
            self._label_docs.setdefault(label_name, set()).add(doc_id)
            return True

    def unassign_label(self, doc_id: str, label_name: str) -> bool:
        """Remove *label_name* from *doc_id*.

        Returns True if the label was present, False otherwise.
        """
        with self._lock:
            doc_set = self._doc_labels.get(doc_id)
            if not doc_set or label_name not in doc_set:
                return False
            doc_set.discard(label_name)
            if not doc_set:
                del self._doc_labels[doc_id]
            label_set = self._label_docs.get(label_name)
            if label_set:
                label_set.discard(doc_id)
                if not label_set:
                    del self._label_docs[label_name]
            return True

    def unassign_all(self, doc_id: str) -> int:
        """Remove all labels from *doc_id*.

        Returns the number of labels that were removed.
        """
        with self._lock:
            doc_set = self._doc_labels.pop(doc_id, None)
            if not doc_set:
                return 0
            count = len(doc_set)
            for label_name in doc_set:
                label_set = self._label_docs.get(label_name)
                if label_set:
                    label_set.discard(doc_id)
                    if not label_set:
                        del self._label_docs[label_name]
            return count

    def has_label(self, doc_id: str, label_name: str) -> bool:
        """Return True if *doc_id* has *label_name* assigned."""
        with self._lock:
            return label_name in self._doc_labels.get(doc_id, set())

    # ------------------------------------------------------------------
    # Query operations
    # ------------------------------------------------------------------

    def labels_for_doc(self, doc_id: str) -> DocLabels:
        """Return a :class:`DocLabels` with sorted label names for *doc_id*."""
        with self._lock:
            names = sorted(self._doc_labels.get(doc_id, set()))
        return DocLabels(doc_id=doc_id, labels=names, label_count=len(names))

    def docs_with_label(self, label_name: str) -> list[str]:
        """Return sorted list of doc_ids that have *label_name*."""
        with self._lock:
            return sorted(self._label_docs.get(label_name, set()))

    def docs_with_all_labels(self, label_names: list[str]) -> list[str]:
        """Return sorted doc_ids that have ALL of *label_names* assigned.

        Returns all docs when *label_names* is empty.
        """
        with self._lock:
            if not label_names:
                # intersection over empty set of constraints = all docs
                return sorted(self._doc_labels)
            sets = [self._label_docs.get(name, set()) for name in label_names]
            result = sets[0].copy()
            for s in sets[1:]:
                result &= s
        return sorted(result)

    def docs_with_any_label(self, label_names: list[str]) -> list[str]:
        """Return sorted, deduplicated doc_ids that have ANY of *label_names*."""
        with self._lock:
            result: set[str] = set()
            for name in label_names:
                result |= self._label_docs.get(name, set())
        return sorted(result)

    # ------------------------------------------------------------------
    # Mutation operations
    # ------------------------------------------------------------------

    def rename_label(self, old_name: str, new_name: str) -> int:
        """Rename *old_name* to *new_name* globally.

        Updates all doc assignments and the label definition (if it exists).
        Returns the number of docs affected.
        """
        with self._lock:
            if old_name == new_name:
                return 0

            # Move label definition if it exists
            if old_name in self._labels:
                old_label = self._labels.pop(old_name)
                # Preserve existing new_name definition if present; otherwise create
                if new_name not in self._labels:
                    self._labels[new_name] = Label(
                        name=new_name,
                        color=old_label.color,
                        description=old_label.description,
                    )

            # Migrate doc assignments
            affected_docs = self._label_docs.pop(old_name, set())
            if not affected_docs:
                return 0

            new_doc_set = self._label_docs.setdefault(new_name, set())
            for doc_id in affected_docs:
                doc_set = self._doc_labels.get(doc_id)
                if doc_set:
                    doc_set.discard(old_name)
                    doc_set.add(new_name)
                new_doc_set.add(doc_id)

            return len(affected_docs)

    # ------------------------------------------------------------------
    # Statistics
    # ------------------------------------------------------------------

    def stats(self) -> LabelStats:
        """Return aggregate statistics."""
        with self._lock:
            total_labels = len(self._labels)
            total_docs = len(self._doc_labels)
            total_assignments = sum(len(v) for v in self._doc_labels.values())
        return LabelStats(
            total_labels=total_labels,
            total_docs=total_docs,
            total_assignments=total_assignments,
        )
