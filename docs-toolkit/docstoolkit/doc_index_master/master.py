"""Master index registry coordinating multiple specialized indexes.

A :class:`DocIndexMaster` keeps a thread-safe registry of named indexes.
Each registered index is described by an :class:`IndexEntry` and may be
attached to an :data:`IndexUpdater` callable that knows how to apply
``upsert`` / ``delete`` actions for a single document.  The master can then
dispatch a document mutation to all (or a filtered subset of) indexes,
track their health, and emit aggregate statistics.

Only stdlib pieces are used (``threading``, ``dataclasses``, ``enum``).
Updater callbacks are always invoked outside the registry lock so that a
slow or blocking index never starves callers reading the registry state.
"""

from __future__ import annotations

import threading
from dataclasses import dataclass, field
from enum import Enum
from typing import Any, Callable, Dict, List, Optional, Protocol


class IndexType(Enum):
    """Kinds of indexes the master can coordinate."""

    SEARCH = "search"
    TAGS = "tags"
    METADATA = "metadata"
    FULL_TEXT = "full_text"
    GRAPH = "graph"
    CUSTOM = "custom"


class IndexHealth(Enum):
    """Health/lifecycle state for a registered index."""

    HEALTHY = "healthy"
    STALE = "stale"
    REBUILDING = "rebuilding"
    ERROR = "error"


class IndexUpdater(Protocol):
    """Callable contract implemented by index updaters.

    ``action`` is one of ``"upsert"`` or ``"delete"``.  Implementations
    should return ``True`` on success (or any truthy value); raising an
    exception is treated as a failure by :class:`DocIndexMaster`.
    """

    def __call__(
        self,
        doc_id: str,
        content: Optional[str] = None,
        action: str = "upsert",
    ) -> bool:  # pragma: no cover - protocol body
        ...


@dataclass
class IndexEntry:
    """Registry record describing a single index."""

    name: str
    index_type: IndexType
    version: int = 0
    last_updated: float = 0.0
    health: IndexHealth = IndexHealth.HEALTHY
    entry_count: int = 0
    metadata: dict = field(default_factory=dict)


@dataclass
class RegistryStats:
    """Aggregate snapshot of the registry."""

    total_indexes: int
    healthy_count: int
    stale_count: int
    error_count: int
    total_entries: int
    by_type: Dict[str, int]


class DocIndexMaster:
    """Thread-safe registry coordinating multiple specialized indexes."""

    def __init__(self) -> None:
        self._lock = threading.Lock()
        self._entries: Dict[str, IndexEntry] = {}
        self._updaters: Dict[str, Optional[Callable]] = {}

    # ------------------------------------------------------------------ #
    # Registration
    # ------------------------------------------------------------------ #
    def register_index(
        self,
        name: str,
        index_type: IndexType,
        updater: Optional[Callable] = None,
        metadata: Optional[dict] = None,
        now: float = 0.0,
    ) -> IndexEntry:
        """Register a new index. Raises ``ValueError`` if the name already exists."""
        with self._lock:
            if name in self._entries:
                raise ValueError(f"index {name!r} already registered")
            entry = IndexEntry(
                name=name,
                index_type=index_type,
                version=0,
                last_updated=now,
                health=IndexHealth.HEALTHY,
                entry_count=0,
                metadata=dict(metadata) if metadata else {},
            )
            self._entries[name] = entry
            self._updaters[name] = updater
            return entry

    def unregister_index(self, name: str) -> bool:
        with self._lock:
            if name not in self._entries:
                return False
            del self._entries[name]
            self._updaters.pop(name, None)
            return True

    # ------------------------------------------------------------------ #
    # Health transitions
    # ------------------------------------------------------------------ #
    def mark_stale(self, name: str) -> bool:
        with self._lock:
            entry = self._entries.get(name)
            if entry is None:
                return False
            entry.health = IndexHealth.STALE
            return True

    def mark_healthy(
        self,
        name: str,
        entry_count: Optional[int] = None,
        now: float = 0.0,
    ) -> bool:
        with self._lock:
            entry = self._entries.get(name)
            if entry is None:
                return False
            entry.health = IndexHealth.HEALTHY
            entry.version += 1
            entry.last_updated = now
            if entry_count is not None:
                entry.entry_count = entry_count
            return True

    def mark_rebuilding(self, name: str) -> bool:
        with self._lock:
            entry = self._entries.get(name)
            if entry is None:
                return False
            entry.health = IndexHealth.REBUILDING
            entry.entry_count = 0
            return True

    def mark_error(self, name: str, reason: Optional[str] = None) -> bool:
        with self._lock:
            entry = self._entries.get(name)
            if entry is None:
                return False
            entry.health = IndexHealth.ERROR
            if reason is not None:
                entry.metadata["error_reason"] = reason
            return True

    # ------------------------------------------------------------------ #
    # Dispatch
    # ------------------------------------------------------------------ #
    def _collect_targets(
        self,
        target_types: Optional[List[IndexType]],
    ) -> List[tuple]:
        """Return list of (name, updater) for indexes matching ``target_types``."""
        with self._lock:
            targets: List[tuple] = []
            for name, entry in self._entries.items():
                if target_types is not None and entry.index_type not in target_types:
                    continue
                updater = self._updaters.get(name)
                if updater is None:
                    continue
                targets.append((name, updater))
            return targets

    def _record_dispatch_result(self, name: str, ok: bool, now: float) -> None:
        with self._lock:
            entry = self._entries.get(name)
            if entry is None:
                return
            if ok:
                entry.version += 1
                entry.last_updated = now
            else:
                entry.health = IndexHealth.ERROR

    def dispatch_upsert(
        self,
        doc_id: str,
        content: Optional[str] = None,
        target_types: Optional[List[IndexType]] = None,
        now: float = 0.0,
    ) -> Dict[str, bool]:
        results: Dict[str, bool] = {}
        for name, updater in self._collect_targets(target_types):
            try:
                updater(doc_id, content, "upsert")
                results[name] = True
            except Exception:
                results[name] = False
            self._record_dispatch_result(name, results[name], now)
        return results

    def dispatch_delete(
        self,
        doc_id: str,
        target_types: Optional[List[IndexType]] = None,
        now: float = 0.0,
    ) -> Dict[str, bool]:
        results: Dict[str, bool] = {}
        for name, updater in self._collect_targets(target_types):
            try:
                updater(doc_id, None, "delete")
                results[name] = True
            except Exception:
                results[name] = False
            self._record_dispatch_result(name, results[name], now)
        return results

    # ------------------------------------------------------------------ #
    # Queries
    # ------------------------------------------------------------------ #
    def get_index(self, name: str) -> Optional[IndexEntry]:
        with self._lock:
            return self._entries.get(name)

    def indexes_by_type(self, index_type: IndexType) -> List[IndexEntry]:
        with self._lock:
            return [e for e in self._entries.values() if e.index_type == index_type]

    def unhealthy_indexes(self) -> List[IndexEntry]:
        with self._lock:
            return [
                e for e in self._entries.values() if e.health != IndexHealth.HEALTHY
            ]

    def stale_indexes(self) -> List[IndexEntry]:
        with self._lock:
            return [
                e for e in self._entries.values() if e.health == IndexHealth.STALE
            ]

    def rebuilding_indexes(self) -> List[IndexEntry]:
        with self._lock:
            return [
                e
                for e in self._entries.values()
                if e.health == IndexHealth.REBUILDING
            ]

    # ------------------------------------------------------------------ #
    # Misc mutators
    # ------------------------------------------------------------------ #
    def bump_version(self, name: str, now: float = 0.0) -> bool:
        with self._lock:
            entry = self._entries.get(name)
            if entry is None:
                return False
            entry.version += 1
            entry.last_updated = now
            return True

    def set_metadata(self, name: str, key: str, value: Any) -> bool:
        with self._lock:
            entry = self._entries.get(name)
            if entry is None:
                return False
            entry.metadata[key] = value
            return True

    # ------------------------------------------------------------------ #
    # Stats / utilities
    # ------------------------------------------------------------------ #
    def stats(self) -> RegistryStats:
        with self._lock:
            healthy = stale = error = total_entries = 0
            by_type: Dict[str, int] = {}
            for entry in self._entries.values():
                total_entries += entry.entry_count
                if entry.health == IndexHealth.HEALTHY:
                    healthy += 1
                elif entry.health == IndexHealth.STALE:
                    stale += 1
                elif entry.health == IndexHealth.ERROR:
                    error += 1
                key = entry.index_type.value
                by_type[key] = by_type.get(key, 0) + 1
            return RegistryStats(
                total_indexes=len(self._entries),
                healthy_count=healthy,
                stale_count=stale,
                error_count=error,
                total_entries=total_entries,
                by_type=by_type,
            )

    @property
    def index_count(self) -> int:
        with self._lock:
            return len(self._entries)

    def clear(self) -> None:
        with self._lock:
            self._entries.clear()
            self._updaters.clear()

    def all_names(self) -> List[str]:
        with self._lock:
            return list(self._entries.keys())
