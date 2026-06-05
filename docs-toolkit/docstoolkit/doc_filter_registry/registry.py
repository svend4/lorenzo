"""DocFilterRegistry — saved filter/query registry for documents.

All state is kept in memory with a single :class:`threading.Lock` guarding
every mutation and read that touches internal dicts, so the registry is safe
to use from multiple threads without any external synchronisation.

UUID identifiers are generated with :func:`uuid.uuid4` (stdlib only).
Timestamps are ``float`` Unix seconds; pass ``now`` in tests for determinism.
"""

from __future__ import annotations

import threading
import time
import uuid
from dataclasses import dataclass, field
from typing import Optional


# ---------------------------------------------------------------------------
# helpers
# ---------------------------------------------------------------------------

def _now(now: Optional[float]) -> float:
    """Return *now* if provided, else :func:`time.time`."""
    if now is not None:
        return now
    return time.time()


# ---------------------------------------------------------------------------
# dataclasses
# ---------------------------------------------------------------------------

@dataclass
class SavedFilter:
    """A single saved filter / query.

    Parameters
    ----------
    filter_id:
        Unique UUID identifying this filter.
    name:
        Human-readable name.
    owner:
        User id of the owner.
    query:
        Arbitrary filter criteria as a ``dict``.
    created_at:
        Unix timestamp of creation (default 0.0, set by registry).
    updated_at:
        Unix timestamp of last update (default 0.0, set by registry).
    shared:
        Whether this filter is visible to all users.
    use_count:
        Number of times :meth:`DocFilterRegistry.record_use` has been called
        for this filter.
    """

    filter_id: str
    name: str
    owner: str
    query: dict = field(default_factory=dict)
    created_at: float = 0.0
    updated_at: float = 0.0
    shared: bool = False
    use_count: int = 0


@dataclass
class FilterStats:
    """Aggregate statistics for the registry.

    Parameters
    ----------
    total_filters:
        Total number of saved filters.
    shared_filters:
        Number of filters with ``shared=True``.
    unique_owners:
        Number of distinct owners with at least one filter.
    total_uses:
        Sum of ``use_count`` across all filters.
    """

    total_filters: int
    shared_filters: int
    unique_owners: int
    total_uses: int


# ---------------------------------------------------------------------------
# registry
# ---------------------------------------------------------------------------

class DocFilterRegistry:
    """Thread-safe in-memory registry of saved document filters.

    All public methods acquire ``_lock`` for the duration of their
    critical section, so concurrent callers will never observe partial
    state.

    Internal storage
    ----------------
    ``_filters``  — ``filter_id → SavedFilter``
    ``_by_owner`` — ``owner     → [filter_id, ...]``
    """

    def __init__(self) -> None:
        self._lock: threading.Lock = threading.Lock()
        self._filters: dict[str, SavedFilter] = {}
        self._by_owner: dict[str, list[str]] = {}

    # ------------------------------------------------------------------
    # CRUD
    # ------------------------------------------------------------------

    def save_filter(
        self,
        name: str,
        owner: str,
        query: dict,
        shared: bool = False,
        now: Optional[float] = None,
    ) -> SavedFilter:
        """Create and store a new :class:`SavedFilter`.

        The ``query`` dict is shallow-copied so subsequent mutation by the
        caller does not leak into the registry.
        """

        ts = _now(now)
        flt = SavedFilter(
            filter_id=str(uuid.uuid4()),
            name=name,
            owner=owner,
            query=dict(query),
            created_at=ts,
            updated_at=ts,
            shared=shared,
        )
        with self._lock:
            self._filters[flt.filter_id] = flt
            self._by_owner.setdefault(owner, []).append(flt.filter_id)
        return flt

    def update_filter(
        self,
        filter_id: str,
        name: Optional[str] = None,
        query: Optional[dict] = None,
        shared: Optional[bool] = None,
        now: Optional[float] = None,
    ) -> Optional[SavedFilter]:
        """Apply partial updates to an existing filter.

        Only fields whose argument is not ``None`` are touched.  Returns the
        updated :class:`SavedFilter`, or ``None`` if no filter with
        *filter_id* exists.
        """

        with self._lock:
            flt = self._filters.get(filter_id)
            if flt is None:
                return None
            if name is not None:
                flt.name = name
            if query is not None:
                flt.query = dict(query)
            if shared is not None:
                flt.shared = shared
            flt.updated_at = _now(now)
            return flt

    def delete_filter(self, filter_id: str) -> bool:
        """Remove a filter.

        Returns
        -------
        bool
            ``True`` if the filter existed and was removed; ``False`` otherwise.
        """

        with self._lock:
            flt = self._filters.pop(filter_id, None)
            if flt is None:
                return False
            owner_ids = self._by_owner.get(flt.owner)
            if owner_ids is not None:
                try:
                    owner_ids.remove(filter_id)
                except ValueError:
                    pass
                if not owner_ids:
                    self._by_owner.pop(flt.owner, None)
            return True

    def get_filter(self, filter_id: str) -> Optional[SavedFilter]:
        """Return the :class:`SavedFilter` for *filter_id*, or ``None``."""

        with self._lock:
            return self._filters.get(filter_id)

    # ------------------------------------------------------------------
    # usage tracking
    # ------------------------------------------------------------------

    def record_use(self, filter_id: str) -> bool:
        """Increment ``use_count`` for *filter_id*.

        Returns
        -------
        bool
            ``True`` if the filter was found and updated; ``False`` otherwise.
        """

        with self._lock:
            flt = self._filters.get(filter_id)
            if flt is None:
                return False
            flt.use_count += 1
            return True

    # ------------------------------------------------------------------
    # queries
    # ------------------------------------------------------------------

    def filters_for_owner(self, owner: str) -> list[SavedFilter]:
        """Return all filters owned by *owner*, sorted by ``name`` ascending."""

        with self._lock:
            ids = list(self._by_owner.get(owner, []))
            filters = [self._filters[fid] for fid in ids if fid in self._filters]
        filters.sort(key=lambda f: f.name)
        return filters

    def shared_filters(self) -> list[SavedFilter]:
        """Return all shared filters, sorted by ``name`` ascending."""

        with self._lock:
            filters = [f for f in self._filters.values() if f.shared]
        filters.sort(key=lambda f: f.name)
        return filters

    def visible_to(self, user_id: str) -> list[SavedFilter]:
        """Return filters visible to *user_id*: their own + all shared filters.

        Deduplicated by ``filter_id`` (a user's own shared filter appears once),
        sorted by ``name`` ascending.
        """

        with self._lock:
            seen: dict[str, SavedFilter] = {}
            for fid in self._by_owner.get(user_id, []):
                flt = self._filters.get(fid)
                if flt is not None:
                    seen[flt.filter_id] = flt
            for flt in self._filters.values():
                if flt.shared:
                    seen[flt.filter_id] = flt
        filters = list(seen.values())
        filters.sort(key=lambda f: f.name)
        return filters

    def most_used(self, limit: int = 10) -> list[SavedFilter]:
        """Return the top *limit* filters by ``use_count`` descending.

        Ties are broken by ``name`` ascending.
        """

        with self._lock:
            filters = list(self._filters.values())
        filters.sort(key=lambda f: (-f.use_count, f.name))
        if limit < 0:
            limit = 0
        return filters[:limit]

    def rename_filter(self, filter_id: str, new_name: str) -> bool:
        """Rename a filter.

        Returns
        -------
        bool
            ``True`` if found and renamed; ``False`` otherwise.
        """

        with self._lock:
            flt = self._filters.get(filter_id)
            if flt is None:
                return False
            flt.name = new_name
            return True

    def all_owners(self) -> list[str]:
        """Return sorted list of distinct owners with at least one filter."""

        with self._lock:
            owners = [o for o, ids in self._by_owner.items() if ids]
        owners.sort()
        return owners

    # ------------------------------------------------------------------
    # aggregates
    # ------------------------------------------------------------------

    def stats(self) -> FilterStats:
        """Return aggregate :class:`FilterStats` for the registry."""

        with self._lock:
            filters = list(self._filters.values())
            owners = {o for o, ids in self._by_owner.items() if ids}

        total = len(filters)
        shared = sum(1 for f in filters if f.shared)
        total_uses = sum(f.use_count for f in filters)
        return FilterStats(
            total_filters=total,
            shared_filters=shared,
            unique_owners=len(owners),
            total_uses=total_uses,
        )
