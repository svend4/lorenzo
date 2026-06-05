"""E364 DocFieldIndex — secondary indexes on document fields.

A pure-stdlib, thread-safe in-memory store that maintains inverted
indexes on declared fields of records. Provides exact-match and range
lookups plus simple statistics.
"""

from __future__ import annotations

import threading
from dataclasses import dataclass, field
from typing import Any, Optional


@dataclass
class FieldRecord:
    """A single indexed record."""

    doc_id: str
    field_values: dict = field(default_factory=dict)


@dataclass
class IndexStats:
    """Aggregate statistics about a :class:`DocFieldIndex`."""

    total_records: int
    indexed_fields: int
    unique_values_per_field: dict = field(default_factory=dict)


class DocFieldIndex:
    """Maintain secondary inverted indexes over declared fields."""

    def __init__(self) -> None:
        self._records: dict[str, FieldRecord] = {}
        self._indexes: dict[str, dict] = {}
        self._indexed_fields: set[str] = set()
        self._lock = threading.Lock()

    # ------------------------------------------------------------------
    # Field declaration
    # ------------------------------------------------------------------
    def declare_field(self, field_name: str) -> None:
        """Register a field for indexing. Idempotent."""
        with self._lock:
            if field_name in self._indexed_fields:
                return
            self._indexed_fields.add(field_name)
            self._indexes.setdefault(field_name, {})
            # Backfill the new index from existing records.
            for doc_id, rec in self._records.items():
                if field_name in rec.field_values:
                    value = rec.field_values[field_name]
                    self._indexes[field_name].setdefault(value, set()).add(doc_id)

    # ------------------------------------------------------------------
    # Internal helpers (assume lock is held)
    # ------------------------------------------------------------------
    def _remove_from_indexes(self, doc_id: str, rec: FieldRecord) -> None:
        for fname, value in rec.field_values.items():
            if fname not in self._indexed_fields:
                continue
            bucket = self._indexes.get(fname, {}).get(value)
            if bucket is None:
                continue
            bucket.discard(doc_id)
            if not bucket:
                del self._indexes[fname][value]

    def _add_to_indexes(self, doc_id: str, field_values: dict) -> None:
        for fname, value in field_values.items():
            if fname not in self._indexed_fields:
                continue
            self._indexes.setdefault(fname, {}).setdefault(value, set()).add(doc_id)

    # ------------------------------------------------------------------
    # CRUD on records
    # ------------------------------------------------------------------
    def index_record(self, doc_id: str, field_values: dict) -> FieldRecord:
        """Store a record and update inverted indexes for declared fields.

        If the doc_id already exists, its prior values are removed from the
        indexes first.
        """
        with self._lock:
            existing = self._records.get(doc_id)
            if existing is not None:
                self._remove_from_indexes(doc_id, existing)
            rec = FieldRecord(doc_id=doc_id, field_values=dict(field_values))
            self._records[doc_id] = rec
            self._add_to_indexes(doc_id, rec.field_values)
            return rec

    def remove_record(self, doc_id: str) -> bool:
        """Remove a record. Returns True if it existed."""
        with self._lock:
            rec = self._records.pop(doc_id, None)
            if rec is None:
                return False
            self._remove_from_indexes(doc_id, rec)
            return True

    def get_record(self, doc_id: str) -> Optional[FieldRecord]:
        with self._lock:
            return self._records.get(doc_id)

    # ------------------------------------------------------------------
    # Lookups
    # ------------------------------------------------------------------
    def lookup_by_field(self, field_name: str, value: Any) -> list[str]:
        """Return sorted doc_ids whose field value equals ``value``.

        Returns an empty list if the field has not been declared.
        """
        with self._lock:
            if field_name not in self._indexed_fields:
                return []
            bucket = self._indexes.get(field_name, {}).get(value)
            if not bucket:
                return []
            return sorted(bucket)

    def lookup_by_range(
        self, field_name: str, min_value: Any, max_value: Any
    ) -> list[str]:
        """Return sorted doc_ids whose field value is within [min, max]."""
        with self._lock:
            if field_name not in self._indexed_fields:
                return []
            result: set[str] = set()
            for value, ids in self._indexes.get(field_name, {}).items():
                try:
                    if min_value <= value <= max_value:
                        result.update(ids)
                except TypeError:
                    # Skip incomparable values rather than blowing up.
                    continue
            return sorted(result)

    def values_for_field(self, field_name: str) -> list:
        """Return sorted unique values currently indexed for ``field_name``."""
        with self._lock:
            if field_name not in self._indexed_fields:
                return []
            values = list(self._indexes.get(field_name, {}).keys())
            try:
                return sorted(values)
            except TypeError:
                # Mixed types — fall back to string-key sort, stable enough.
                return sorted(values, key=lambda v: (str(type(v)), str(v)))

    def count_for_value(self, field_name: str, value: Any) -> int:
        with self._lock:
            if field_name not in self._indexed_fields:
                return 0
            bucket = self._indexes.get(field_name, {}).get(value)
            return len(bucket) if bucket else 0

    # ------------------------------------------------------------------
    # Mutation
    # ------------------------------------------------------------------
    def update_field(self, doc_id: str, field_name: str, new_value: Any) -> bool:
        """Update a single field on an existing record.

        Returns True if the record exists. The field's index is refreshed.
        """
        with self._lock:
            rec = self._records.get(doc_id)
            if rec is None:
                return False
            old_value = rec.field_values.get(field_name, _MISSING)
            if field_name in self._indexed_fields and old_value is not _MISSING:
                bucket = self._indexes.get(field_name, {}).get(old_value)
                if bucket is not None:
                    bucket.discard(doc_id)
                    if not bucket:
                        del self._indexes[field_name][old_value]
            rec.field_values[field_name] = new_value
            if field_name in self._indexed_fields:
                self._indexes.setdefault(field_name, {}).setdefault(
                    new_value, set()
                ).add(doc_id)
            return True

    # ------------------------------------------------------------------
    # Bulk
    # ------------------------------------------------------------------
    def all_doc_ids(self) -> list[str]:
        with self._lock:
            return sorted(self._records.keys())

    def clear(self) -> int:
        with self._lock:
            count = len(self._records)
            self._records.clear()
            for fname in list(self._indexes.keys()):
                self._indexes[fname] = {}
            return count

    def stats(self) -> IndexStats:
        with self._lock:
            unique_per_field = {
                fname: len(self._indexes.get(fname, {}))
                for fname in self._indexed_fields
            }
            return IndexStats(
                total_records=len(self._records),
                indexed_fields=len(self._indexed_fields),
                unique_values_per_field=unique_per_field,
            )


# Sentinel used to distinguish "field absent" from "field present with value None".
_MISSING = object()
