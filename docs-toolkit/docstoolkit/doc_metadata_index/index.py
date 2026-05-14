"""E397 DocMetadataIndex — indexed key-value metadata for documents.

Pure stdlib, thread-safe via :class:`threading.Lock`, dataclasses
throughout.  Maintains three internal indexes:

* ``_entries``  — ``(doc_id, key) -> MetaEntry``  (primary store)
* ``_by_doc``   — ``doc_id -> {key, ...}``        (per-doc lookup)
* ``_inverted`` — ``(key, value) -> {doc_id, ...}``  (value lookup)
"""
from __future__ import annotations

import threading
import time
from dataclasses import dataclass, field
from typing import Dict, List, Optional, Set, Tuple


# ---------------------------------------------------------------------------
# Dataclasses
# ---------------------------------------------------------------------------


@dataclass
class MetaEntry:
    """A single metadata entry for a document."""

    doc_id: str
    key: str
    value: str
    updated_at: float = 0.0


@dataclass
class MetaStats:
    """Aggregate statistics about the metadata index."""

    total_entries: int
    unique_docs: int
    unique_keys: int


# ---------------------------------------------------------------------------
# Index
# ---------------------------------------------------------------------------


class DocMetadataIndex:
    """Thread-safe in-memory index of document metadata.

    Each ``(doc_id, key)`` pair maps to exactly one :class:`MetaEntry`.
    Calling :meth:`set_meta` again with the same pair replaces the value
    and keeps the inverted index consistent.
    """

    def __init__(self) -> None:
        self._entries: Dict[Tuple[str, str], MetaEntry] = {}
        self._by_doc: Dict[str, Set[str]] = {}
        self._inverted: Dict[Tuple[str, str], Set[str]] = {}
        self._lock = threading.Lock()

    # ------------------------------------------------------------------
    # Internal helpers
    # ------------------------------------------------------------------

    @staticmethod
    def _now(now: Optional[float]) -> float:
        return float(now) if now is not None else time.time()

    def _remove_from_inverted(self, key: str, value: str, doc_id: str) -> None:
        bucket = self._inverted.get((key, value))
        if bucket is None:
            return
        bucket.discard(doc_id)
        if not bucket:
            del self._inverted[(key, value)]

    def _add_to_inverted(self, key: str, value: str, doc_id: str) -> None:
        self._inverted.setdefault((key, value), set()).add(doc_id)

    def _remove_from_by_doc(self, doc_id: str, key: str) -> None:
        keys = self._by_doc.get(doc_id)
        if keys is None:
            return
        keys.discard(key)
        if not keys:
            del self._by_doc[doc_id]

    def _add_to_by_doc(self, doc_id: str, key: str) -> None:
        self._by_doc.setdefault(doc_id, set()).add(key)

    # ------------------------------------------------------------------
    # CRUD
    # ------------------------------------------------------------------

    def set_meta(
        self,
        doc_id: str,
        key: str,
        value: str,
        now: Optional[float] = None,
    ) -> MetaEntry:
        """Create or replace a metadata entry and update all indexes."""
        ts = self._now(now)
        with self._lock:
            composite = (doc_id, key)
            existing = self._entries.get(composite)
            if existing is not None:
                # Only remove the inverted bucket for the old value;
                # the key is still present on the doc.
                self._remove_from_inverted(existing.key, existing.value, doc_id)
            entry = MetaEntry(
                doc_id=doc_id,
                key=key,
                value=value,
                updated_at=ts,
            )
            self._entries[composite] = entry
            self._add_to_by_doc(doc_id, key)
            self._add_to_inverted(key, value, doc_id)
            return entry

    def get_meta(self, doc_id: str, key: str) -> Optional[str]:
        """Return the value for ``(doc_id, key)`` or ``None``."""
        with self._lock:
            entry = self._entries.get((doc_id, key))
            return entry.value if entry is not None else None

    def get_entry(self, doc_id: str, key: str) -> Optional[MetaEntry]:
        """Return the full :class:`MetaEntry` for ``(doc_id, key)``."""
        with self._lock:
            entry = self._entries.get((doc_id, key))
            if entry is None:
                return None
            # Defensive copy so callers can't mutate internal state.
            return MetaEntry(
                doc_id=entry.doc_id,
                key=entry.key,
                value=entry.value,
                updated_at=entry.updated_at,
            )

    def delete_meta(self, doc_id: str, key: str) -> bool:
        """Delete a single entry.  Returns ``True`` if it existed."""
        with self._lock:
            composite = (doc_id, key)
            entry = self._entries.pop(composite, None)
            if entry is None:
                return False
            self._remove_from_inverted(entry.key, entry.value, doc_id)
            self._remove_from_by_doc(doc_id, key)
            return True

    # ------------------------------------------------------------------
    # Lookups
    # ------------------------------------------------------------------

    def meta_for_doc(self, doc_id: str) -> dict:
        """Return a copy of all ``{key: value}`` for the given document."""
        with self._lock:
            keys = self._by_doc.get(doc_id)
            if not keys:
                return {}
            return {
                k: self._entries[(doc_id, k)].value
                for k in keys
            }

    def docs_with(self, key: str, value: str) -> List[str]:
        """Return sorted ``doc_id`` list whose ``key`` equals ``value``."""
        with self._lock:
            bucket = self._inverted.get((key, value))
            if not bucket:
                return []
            return sorted(bucket)

    def docs_with_key(self, key: str) -> List[str]:
        """Return sorted ``doc_id`` list that contain ``key`` (any value)."""
        with self._lock:
            result: Set[str] = set()
            for (k, _v), bucket in self._inverted.items():
                if k == key:
                    result.update(bucket)
            return sorted(result)

    def values_for_key(self, key: str) -> List[str]:
        """Return a sorted list of unique values stored under ``key``."""
        with self._lock:
            values = {v for (k, v) in self._inverted.keys() if k == key}
            return sorted(values)

    def find_by_filter(self, filters: dict) -> List[str]:
        """Return sorted ``doc_id`` matching every ``{key: value}`` pair.

        An empty ``filters`` dict returns an empty list.
        """
        if not filters:
            return []
        with self._lock:
            buckets: List[Set[str]] = []
            for key, value in filters.items():
                bucket = self._inverted.get((key, value))
                if not bucket:
                    return []
                buckets.append(bucket)
            # AND-intersection of all buckets.
            result = set(buckets[0])
            for b in buckets[1:]:
                result &= b
                if not result:
                    return []
            return sorted(result)

    # ------------------------------------------------------------------
    # Bulk removal
    # ------------------------------------------------------------------

    def clear_doc(self, doc_id: str) -> int:
        """Remove every entry belonging to ``doc_id``.  Returns the count."""
        with self._lock:
            keys = self._by_doc.pop(doc_id, None)
            if not keys:
                return 0
            count = 0
            for key in list(keys):
                entry = self._entries.pop((doc_id, key), None)
                if entry is not None:
                    self._remove_from_inverted(entry.key, entry.value, doc_id)
                    count += 1
            return count

    def clear_key(self, key: str) -> int:
        """Remove ``key`` from every document.  Returns the count."""
        with self._lock:
            # Collect victims first to avoid mutating during iteration.
            victims = [
                (doc_id, k)
                for (doc_id, k) in self._entries.keys()
                if k == key
            ]
            count = 0
            for composite in victims:
                entry = self._entries.pop(composite, None)
                if entry is None:
                    continue
                doc_id = composite[0]
                self._remove_from_inverted(entry.key, entry.value, doc_id)
                self._remove_from_by_doc(doc_id, key)
                count += 1
            return count

    # ------------------------------------------------------------------
    # Enumeration
    # ------------------------------------------------------------------

    def all_keys(self) -> List[str]:
        """Return a sorted list of every distinct key in the index."""
        with self._lock:
            return sorted({k for (_d, k) in self._entries.keys()})

    def all_doc_ids(self) -> List[str]:
        """Return a sorted list of every doc with at least one entry."""
        with self._lock:
            return sorted(self._by_doc.keys())

    def stats(self) -> MetaStats:
        """Return aggregate statistics about the index."""
        with self._lock:
            total = len(self._entries)
            unique_docs = len(self._by_doc)
            unique_keys = len({k for (_d, k) in self._entries.keys()})
            return MetaStats(
                total_entries=total,
                unique_docs=unique_docs,
                unique_keys=unique_keys,
            )
