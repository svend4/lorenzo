"""Document classification taxonomy and assignment (E347).

Provides a thread-safe registry of classification categories and per-document
classification assignments with confidence scores.

Public API
----------
- ``Category``            — a classification category
- ``Classification``      — a single doc's classification
- ``ClassificationStats`` — aggregate statistics
- ``DocClassification``   — main interface for classification management
"""

from __future__ import annotations

import threading
import time
from dataclasses import dataclass, field
from typing import Optional


# ---------------------------------------------------------------------------
# Data classes
# ---------------------------------------------------------------------------


@dataclass
class Category:
    """A classification category in the taxonomy."""

    category_id: str
    name: str
    description: str = ""
    color: str = "#cccccc"


@dataclass
class Classification:
    """A single document's assignment to a classification category."""

    doc_id: str
    category_id: str
    confidence: float = 1.0
    classified_at: float = 0.0
    classified_by: str = ""


@dataclass
class ClassificationStats:
    """Aggregate statistics for the current classification state."""

    total_categories: int
    total_classifications: int
    unique_docs: int
    avg_confidence: float
    category_counts: dict = field(default_factory=dict)


# ---------------------------------------------------------------------------
# DocClassification
# ---------------------------------------------------------------------------


class DocClassification:
    """Thread-safe document classification manager.

    Stores a taxonomy of :class:`Category` instances and per-document
    :class:`Classification` assignments. A document may belong to multiple
    categories simultaneously; each (doc_id, category_id) pair has at most one
    classification record.
    """

    def __init__(self) -> None:
        self._lock = threading.Lock()
        self._categories: dict[str, Category] = {}
        self._classifications: dict[tuple, Classification] = {}
        self._by_doc: dict[str, set[str]] = {}
        self._by_category: dict[str, set[str]] = {}

    # ------------------------------------------------------------------
    # Category management
    # ------------------------------------------------------------------

    def add_category(self, cat: Category) -> None:
        """Register a category, or replace an existing one with the same id."""
        with self._lock:
            self._categories[cat.category_id] = cat
            # Ensure the category index has a slot even with no docs yet.
            self._by_category.setdefault(cat.category_id, set())

    def remove_category(self, category_id: str) -> bool:
        """Remove a category and all its classifications.

        Returns ``True`` if the category existed.
        """
        with self._lock:
            if category_id not in self._categories:
                return False
            del self._categories[category_id]
            doc_ids = self._by_category.pop(category_id, set())
            for doc_id in doc_ids:
                self._classifications.pop((doc_id, category_id), None)
                doc_cats = self._by_doc.get(doc_id)
                if doc_cats is not None:
                    doc_cats.discard(category_id)
                    if not doc_cats:
                        del self._by_doc[doc_id]
            return True

    def get_category(self, category_id: str) -> Optional[Category]:
        """Return the category with the given id, or ``None``."""
        with self._lock:
            return self._categories.get(category_id)

    def list_categories(self) -> list[Category]:
        """Return all categories sorted by ``name``."""
        with self._lock:
            return sorted(self._categories.values(), key=lambda c: c.name)

    # ------------------------------------------------------------------
    # Classification
    # ------------------------------------------------------------------

    def classify(
        self,
        doc_id: str,
        category_id: str,
        confidence: float = 1.0,
        classified_by: str = "",
        now: Optional[float] = None,
    ) -> Optional[Classification]:
        """Assign ``doc_id`` to ``category_id`` with the given confidence.

        Replaces any prior assignment for the same (doc, category) pair.
        Returns ``None`` if the category is not defined.
        """
        with self._lock:
            if category_id not in self._categories:
                return None
            ts = time.time() if now is None else now
            classification = Classification(
                doc_id=doc_id,
                category_id=category_id,
                confidence=confidence,
                classified_at=ts,
                classified_by=classified_by,
            )
            self._classifications[(doc_id, category_id)] = classification
            self._by_doc.setdefault(doc_id, set()).add(category_id)
            self._by_category.setdefault(category_id, set()).add(doc_id)
            return classification

    def unclassify(self, doc_id: str, category_id: str) -> bool:
        """Remove a (doc, category) classification. Returns ``True`` if it existed."""
        with self._lock:
            key = (doc_id, category_id)
            if key not in self._classifications:
                return False
            del self._classifications[key]
            doc_cats = self._by_doc.get(doc_id)
            if doc_cats is not None:
                doc_cats.discard(category_id)
                if not doc_cats:
                    del self._by_doc[doc_id]
            cat_docs = self._by_category.get(category_id)
            if cat_docs is not None:
                cat_docs.discard(doc_id)
            return True

    def get_classification(
        self, doc_id: str, category_id: str
    ) -> Optional[Classification]:
        """Return the classification for (doc_id, category_id), or ``None``."""
        with self._lock:
            return self._classifications.get((doc_id, category_id))

    def categories_for_doc(self, doc_id: str) -> list[Classification]:
        """Return all classifications for ``doc_id`` sorted by ``category_id``."""
        with self._lock:
            cat_ids = self._by_doc.get(doc_id, set())
            items = [self._classifications[(doc_id, cid)] for cid in cat_ids]
            return sorted(items, key=lambda c: c.category_id)

    def docs_in_category(
        self, category_id: str, min_confidence: float = 0.0
    ) -> list[str]:
        """Return doc ids in ``category_id`` whose confidence ≥ ``min_confidence``.

        The result is sorted alphabetically.
        """
        with self._lock:
            doc_ids = self._by_category.get(category_id, set())
            filtered = [
                doc_id
                for doc_id in doc_ids
                if self._classifications[(doc_id, category_id)].confidence
                >= min_confidence
            ]
            return sorted(filtered)

    def clear_doc(self, doc_id: str) -> int:
        """Remove all classifications for ``doc_id``. Returns the count removed."""
        with self._lock:
            cat_ids = self._by_doc.pop(doc_id, set())
            count = 0
            for cid in cat_ids:
                if self._classifications.pop((doc_id, cid), None) is not None:
                    count += 1
                cat_docs = self._by_category.get(cid)
                if cat_docs is not None:
                    cat_docs.discard(doc_id)
            return count

    # ------------------------------------------------------------------
    # Aggregates
    # ------------------------------------------------------------------

    def top_categories(self, limit: int = 10) -> list[tuple]:
        """Return ``(category_id, doc_count)`` pairs sorted by count desc, id asc."""
        with self._lock:
            counts = [
                (cid, len(docs)) for cid, docs in self._by_category.items()
            ]
        counts.sort(key=lambda item: (-item[1], item[0]))
        return counts[:limit]

    def stats(self) -> ClassificationStats:
        """Return aggregate statistics about the classification state."""
        with self._lock:
            total_categories = len(self._categories)
            total_classifications = len(self._classifications)
            unique_docs = len(self._by_doc)
            if total_classifications:
                avg_confidence = (
                    sum(c.confidence for c in self._classifications.values())
                    / total_classifications
                )
            else:
                avg_confidence = 0.0
            category_counts = {
                cid: len(docs) for cid, docs in self._by_category.items()
            }
        return ClassificationStats(
            total_categories=total_categories,
            total_classifications=total_classifications,
            unique_docs=unique_docs,
            avg_confidence=avg_confidence,
            category_counts=category_counts,
        )
