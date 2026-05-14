"""E364 DocFieldIndex — secondary indexes on document fields.

Public API
----------
:class:`FieldRecord`    — a single indexed record
:class:`IndexStats`     — aggregate statistics
:class:`DocFieldIndex`  — main interface for field-based indexing
"""

from .index import FieldRecord, IndexStats, DocFieldIndex

__all__ = ["FieldRecord", "IndexStats", "DocFieldIndex"]
