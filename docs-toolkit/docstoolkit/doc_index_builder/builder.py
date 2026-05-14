"""E313 DocIndexBuilder — composite document index with inverted index, exact-match
lookup, multi-field filtering, and sorting.

Pure stdlib, thread-safe via :class:`threading.Lock`, dataclasses throughout.
"""
from __future__ import annotations

import threading
from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional

__all__ = [
    "IndexField",
    "IndexEntry",
    "IndexStats",
    "DocIndexBuilder",
]


# ---------------------------------------------------------------------------
# Dataclasses
# ---------------------------------------------------------------------------


@dataclass
class IndexField:
    """Definition of a field in the index.

    Attributes
    ----------
    name:
        Unique name of the field.
    field_type:
        One of ``"str"``, ``"int"``, ``"float"``, ``"bool"``.
    indexed:
        Whether to build an inverted index for this field, enabling fast
        exact-match :meth:`DocIndexBuilder.lookup` and :meth:`DocIndexBuilder.query`.
    sortable:
        Whether the field can be used with :meth:`DocIndexBuilder.sort_by`.
    """

    name: str
    field_type: str = "str"
    indexed: bool = True
    sortable: bool = False


@dataclass
class IndexEntry:
    """A single indexed document record.

    Attributes
    ----------
    doc_id:
        Unique identifier of the document.
    fields:
        Mapping of field name to its stored value.
    """

    doc_id: str
    fields: dict = field(default_factory=dict)


@dataclass
class IndexStats:
    """Aggregate statistics over a :class:`DocIndexBuilder`.

    Attributes
    ----------
    total_docs:
        Number of documents currently in the index.
    total_fields:
        Number of field definitions registered.
    indexed_fields:
        Number of field definitions where ``indexed=True``.
    """

    total_docs: int
    total_fields: int
    indexed_fields: int


# ---------------------------------------------------------------------------
# DocIndexBuilder
# ---------------------------------------------------------------------------


class DocIndexBuilder:
    """Build and query a composite document index.

    All public methods are thread-safe.  Concurrent :meth:`index_doc` calls
    from multiple threads are serialised via an internal :class:`threading.Lock`.

    Internal storage
    ----------------
    ``_fields``
        ``dict[str, IndexField]`` — field name → definition.
    ``_entries``
        ``dict[str, IndexEntry]`` — doc_id → entry.
    ``_inverted``
        ``dict[str, dict]`` — field_name → {value → set of doc_ids}.
    """

    def __init__(self) -> None:
        self._lock = threading.Lock()
        self._fields: Dict[str, IndexField] = {}
        self._entries: Dict[str, IndexEntry] = {}
        # field_name -> value -> set[doc_id]
        self._inverted: Dict[str, Dict[Any, set]] = {}

    # ------------------------------------------------------------------
    # Field management
    # ------------------------------------------------------------------

    def define_field(self, field: IndexField) -> None:
        """Register a field definition, replacing any previous definition with the same name."""
        with self._lock:
            self._fields[field.name] = field
            if field.indexed and field.name not in self._inverted:
                self._inverted[field.name] = {}

    def remove_field(self, name: str) -> bool:
        """Remove a field definition and all its inverted-index data.

        Returns ``True`` if the field existed, ``False`` otherwise.
        """
        with self._lock:
            if name not in self._fields:
                return False
            del self._fields[name]
            self._inverted.pop(name, None)
            return True

    def get_field(self, name: str) -> Optional[IndexField]:
        """Return the :class:`IndexField` for *name*, or ``None``."""
        with self._lock:
            return self._fields.get(name)

    def list_fields(self) -> List[IndexField]:
        """Return all registered field definitions, sorted by name."""
        with self._lock:
            return [self._fields[n] for n in sorted(self._fields)]

    # ------------------------------------------------------------------
    # Document management
    # ------------------------------------------------------------------

    def _remove_from_inverted(self, entry: IndexEntry) -> None:
        """Remove *entry* from all inverted index buckets (caller holds lock)."""
        for fname, val in entry.fields.items():
            bucket = self._inverted.get(fname)
            if bucket is None:
                continue
            doc_set = bucket.get(val)
            if doc_set is not None:
                doc_set.discard(entry.doc_id)
                if not doc_set:
                    del bucket[val]

    def _add_to_inverted(self, entry: IndexEntry) -> None:
        """Add *entry* to all inverted index buckets (caller holds lock)."""
        for fname, val in entry.fields.items():
            fdef = self._fields.get(fname)
            if fdef is None or not fdef.indexed:
                continue
            bucket = self._inverted.setdefault(fname, {})
            doc_set = bucket.setdefault(val, set())
            doc_set.add(entry.doc_id)

    def index_doc(self, doc_id: str, fields: dict) -> IndexEntry:
        """Store a document entry and update the inverted index.

        If a document with *doc_id* already exists, its old field values are
        cleanly removed from the inverted index before the new values are
        inserted.

        Returns the new :class:`IndexEntry`.
        """
        with self._lock:
            # Remove old entry from inverted index if present.
            old = self._entries.get(doc_id)
            if old is not None:
                self._remove_from_inverted(old)

            entry = IndexEntry(doc_id=doc_id, fields=dict(fields))
            self._entries[doc_id] = entry
            self._add_to_inverted(entry)
            return entry

    def remove_doc(self, doc_id: str) -> bool:
        """Remove a document from the index.

        Returns ``True`` if the document existed, ``False`` otherwise.
        """
        with self._lock:
            entry = self._entries.get(doc_id)
            if entry is None:
                return False
            self._remove_from_inverted(entry)
            del self._entries[doc_id]
            return True

    def get_entry(self, doc_id: str) -> Optional[IndexEntry]:
        """Return the :class:`IndexEntry` for *doc_id*, or ``None``."""
        with self._lock:
            return self._entries.get(doc_id)

    # ------------------------------------------------------------------
    # Query API
    # ------------------------------------------------------------------

    def lookup(self, field_name: str, value: Any) -> List[str]:
        """Return sorted doc_ids that have *value* for *field_name*.

        Uses the inverted index.  Returns an empty list if the field is not
        indexed or the value was never stored.
        """
        with self._lock:
            bucket = self._inverted.get(field_name)
            if bucket is None:
                return []
            doc_set = bucket.get(value)
            if not doc_set:
                return []
            return sorted(doc_set)

    def query(self, filters: dict) -> List[str]:
        """AND-match across multiple fields.

        Each key in *filters* is a field name; the associated value is the
        target for an exact match.  Returns the sorted intersection of
        matching doc_ids.  Returns an empty list for an empty *filters* dict.
        """
        if not filters:
            return []
        with self._lock:
            result_set: Optional[set] = None
            for fname, val in filters.items():
                bucket = self._inverted.get(fname)
                if bucket is None:
                    return []
                doc_set = bucket.get(val)
                if not doc_set:
                    return []
                if result_set is None:
                    result_set = set(doc_set)
                else:
                    result_set &= doc_set
                if not result_set:
                    return []
            if result_set is None:
                return []
            return sorted(result_set)

    def sort_by(self, field_name: str, reverse: bool = False) -> List[str]:
        """Return all doc_ids sorted by the value of *field_name*.

        Documents that do not have *field_name* in their fields sort last
        (after all documents that do carry the field).
        """
        with self._lock:
            has_field: List[tuple] = []
            missing: List[str] = []
            for doc_id, entry in self._entries.items():
                if field_name in entry.fields:
                    has_field.append((entry.fields[field_name], doc_id))
                else:
                    missing.append(doc_id)

            has_field.sort(key=lambda t: (t[0], t[1]), reverse=reverse)
            missing_sorted = sorted(missing)
            # When reverse=True the "missing" group still comes last — i.e.
            # at the end of the reversed list.
            if reverse:
                return [doc_id for _, doc_id in has_field] + missing_sorted
            else:
                return [doc_id for _, doc_id in has_field] + missing_sorted

    def all_doc_ids(self) -> List[str]:
        """Return sorted list of all document ids."""
        with self._lock:
            return sorted(self._entries)

    def stats(self) -> IndexStats:
        """Return aggregate statistics."""
        with self._lock:
            total_fields = len(self._fields)
            indexed_fields = sum(1 for f in self._fields.values() if f.indexed)
            return IndexStats(
                total_docs=len(self._entries),
                total_fields=total_fields,
                indexed_fields=indexed_fields,
            )
