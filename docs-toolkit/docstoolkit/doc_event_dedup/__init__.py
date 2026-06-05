"""E431 DocEventDedup — deduplicate document events with TTL.

Public API
----------
:class:`DedupEntry`   — a single dedup record
:class:`DedupStats`   — aggregate statistics
:class:`DocEventDedup` — main interface for event deduplication
"""

from .dedup import DedupEntry, DedupStats, DocEventDedup

__all__ = ["DedupEntry", "DedupStats", "DocEventDedup"]
