"""High-level SemanticSimilarityCache with config and lookup results."""
import time
from dataclasses import dataclass, field
from typing import Optional

from docstoolkit.sim_cache.fingerprint import (
    Fingerprint,
    FingerprintBuilder,
    FingerprintMethod,
)
from docstoolkit.sim_cache.store import SimCacheStore, SimilarityEntry


@dataclass
class SimCacheConfig:
    """Configuration for SemanticSimilarityCache."""
    method: FingerprintMethod = FingerprintMethod.SIMHASH
    threshold: float = 0.9
    max_size: int = 1000
    ttl_seconds: float = 3600.0


@dataclass
class SimCacheLookupResult:
    """Result returned by SemanticSimilarityCache.get()."""
    hit: bool
    entry_id: Optional[str]
    similarity: float
    result: Optional[str]


class SemanticSimilarityCache:
    """Cache that uses fingerprint-based similarity instead of exact-key matching."""

    def __init__(
        self,
        config: SimCacheConfig = None,
        store: SimCacheStore = None,
    ):
        self._config = config or SimCacheConfig()
        self._store = store or SimCacheStore()

    # ------------------------------------------------------------------
    # Public API
    # ------------------------------------------------------------------

    def get(self, text: str) -> SimCacheLookupResult:
        """Look up *text* by semantic similarity.

        Returns a SimCacheLookupResult.  ``hit`` is True when a stored entry
        with similarity >= config.threshold is found.
        """
        fp = FingerprintBuilder.build(text, self._config.method)
        candidates = self._store.find_similar(fp, threshold=self._config.threshold)
        if not candidates:
            return SimCacheLookupResult(hit=False, entry_id=None, similarity=0.0, result=None)

        # Best candidate is first (sorted desc by similarity in store)
        best = candidates[0]

        # Check TTL
        age = time.time() - best.created_ts
        if age >= self._config.ttl_seconds:
            return SimCacheLookupResult(hit=False, entry_id=None, similarity=0.0, result=None)

        self._store.increment_hits(best.entry_id)

        # Re-compute similarity for the result (best is already the highest)
        stored_fp = best.fingerprint
        similarity = fp.similarity(stored_fp)

        return SimCacheLookupResult(
            hit=True,
            entry_id=best.entry_id,
            similarity=similarity,
            result=best.result,
        )

    def set(self, text: str, result: str) -> str:
        """Store *result* under a fingerprint of *text*.

        Evicts expired and LRU entries before adding.
        Returns the new entry_id.
        """
        # Evict before adding to respect max_size and TTL
        self._store.evict_expired(self._config.ttl_seconds)
        self._store.evict_lru(self._config.max_size - 1)

        fp = FingerprintBuilder.build(text, self._config.method)
        entry = SimilarityEntry(text=text, fingerprint=fp, result=result)
        self._store.add(entry)
        return entry.entry_id

    def size(self) -> int:
        """Return the number of entries currently in the cache."""
        return self._store.count()

    def stats(self) -> dict:
        """Return aggregate statistics from the underlying store."""
        return self._store.stats()
