"""Append-only event store for document events (E283).

Provides stream-based querying with per-stream sequence numbers and global
event identifiers.  Pure stdlib, thread-safe.

See ``store`` module for the full implementation.

Quick-start::

    from docstoolkit.doc_event_store import DocEventStore

    store = DocEventStore()
    e = store.append("doc:1", "created", {"title": "Hello"})
    print(store.stream_info("doc:1"))
    print(store.stats())
"""

from __future__ import annotations

from .store import (
    DocEvent,
    DocEventStore,
    EventStoreStats,
    StreamInfo,
)

__all__ = [
    "DocEvent",
    "DocEventStore",
    "EventStoreStats",
    "StreamInfo",
]
