"""Request deduplication module for docs-toolkit (E13)."""
from docstoolkit.dedup.key import (
    DeduplicationStrategy,
    DeduplicationKey,
    compute_key,
)
from docstoolkit.dedup.store import DedupEntry, DedupStore
from docstoolkit.dedup.deduplicator import (
    DeduplicationConfig,
    DeduplicationResult,
    RequestDeduplicator,
)

__all__ = [
    # key
    "DeduplicationStrategy",
    "DeduplicationKey",
    "compute_key",
    # store
    "DedupEntry",
    "DedupStore",
    # deduplicator
    "DeduplicationConfig",
    "DeduplicationResult",
    "RequestDeduplicator",
]
