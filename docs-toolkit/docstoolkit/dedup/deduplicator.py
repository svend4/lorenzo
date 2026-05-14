"""High-level RequestDeduplicator that ties key computation and storage together."""
import time
from dataclasses import dataclass, field
from typing import Optional

from docstoolkit.dedup.key import (
    DeduplicationStrategy,
    DeduplicationKey,
    compute_key,
)
from docstoolkit.dedup.store import DedupEntry, DedupStore


@dataclass
class DeduplicationConfig:
    """Configuration for RequestDeduplicator."""
    strategy: DeduplicationStrategy = DeduplicationStrategy.NORMALIZED
    ttl_seconds: float = 300.0   # how long a key is valid; 0 = immortal
    max_size: int = 10_000       # advisory; eviction keeps store below this


@dataclass
class DeduplicationResult:
    """Outcome of a deduplication check."""
    is_duplicate: bool
    request_id: str                   # the ID assigned to *this* call
    original_request_id: Optional[str]  # first request that owns this key
    key_hash: str


class RequestDeduplicator:
    """Detect and suppress duplicate requests based on payload content.

    Usage::

        dedup = RequestDeduplicator()
        res = dedup.check("SELECT 1")
        if res.is_duplicate:
            cached = dedup.get_result(res.original_request_id)
        else:
            answer = execute_request(...)
            dedup.complete(res.request_id, answer)

    Parameters
    ----------
    config: DeduplicationConfig; defaults constructed if omitted.
    store:  Custom DedupStore; an in-memory SQLite store is created when
            omitted (useful for dependency injection / testing).
    """

    def __init__(
        self,
        config: DeduplicationConfig = None,
        store: DedupStore = None,
    ) -> None:
        self._config = config or DeduplicationConfig()
        self._store = store or DedupStore()

    # ------------------------------------------------------------------
    # Public API
    # ------------------------------------------------------------------

    def check(self, payload: str, request_id: str = None) -> DeduplicationResult:
        """Check whether *payload* is a duplicate of a previously seen request.

        If this is the first time we see the key, the entry is stored so that
        subsequent calls with the same payload are detected as duplicates.

        Parameters
        ----------
        payload:    Raw request payload string.
        request_id: Optional caller-supplied ID; defaults to a new UUID4.

        Returns
        -------
        DeduplicationResult
            ``is_duplicate=True`` when a live entry for the same key already
            exists.  ``original_request_id`` is set to the first request's ID
            in that case.
        """
        dk: DeduplicationKey = compute_key(
            payload, self._config.strategy, request_id
        )

        existing = self._store.get(dk.key_hash)
        if existing is not None:
            return DeduplicationResult(
                is_duplicate=True,
                request_id=dk.request_id,
                original_request_id=existing.request_id,
                key_hash=dk.key_hash,
            )

        # Not a duplicate — register the entry.
        entry = DedupEntry(
            request_id=dk.request_id,
            key_hash=dk.key_hash,
            strategy=dk.strategy,
            result=None,
            created_ts=dk.created_ts,
            ttl_seconds=self._config.ttl_seconds,
        )
        self._store.put(entry)
        return DeduplicationResult(
            is_duplicate=False,
            request_id=dk.request_id,
            original_request_id=None,
            key_hash=dk.key_hash,
        )

    def complete(self, request_id: str, result: str) -> None:
        """Store the completed *result* string for a given *request_id*."""
        self._store.update_result(request_id, result)

    def get_result(self, request_id: str) -> Optional[str]:
        """Retrieve the result previously stored via :meth:`complete`.

        Returns None if the request is unknown, expired, or not yet complete.
        """
        entry = self._store.get_by_request_id(request_id)
        if entry is None:
            return None
        return entry.result

    def evict_expired(self, now: float = None) -> int:
        """Delegate TTL eviction to the underlying store.

        Parameters
        ----------
        now: Reference timestamp for expiry calculation.  Defaults to
             ``time.time()``.  Pass an explicit value in tests to control
             time without sleeping.

        Returns
        -------
        Number of entries removed.
        """
        return self._store.evict_expired(now=now)

    # ------------------------------------------------------------------
    # Accessors
    # ------------------------------------------------------------------

    @property
    def config(self) -> DeduplicationConfig:
        return self._config

    @property
    def store(self) -> DedupStore:
        return self._store
