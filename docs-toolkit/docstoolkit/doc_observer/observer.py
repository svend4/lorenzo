"""Pattern-based observer for document changes.

Provides a file-like API for in-memory documents with observer callbacks
fired on add/modify/remove events. Patterns are matched via fnmatch.

Uses only stdlib (threading + fnmatch). Callbacks fire OUTSIDE the lock
so they cannot deadlock with subsequent ``DocObserver`` mutations.
"""
from __future__ import annotations

import fnmatch
import threading
import uuid
from dataclasses import dataclass, field
from enum import Enum
from typing import Callable, Optional


class ChangeType(Enum):
    """Kinds of document changes observed."""

    ADDED = "added"
    MODIFIED = "modified"
    REMOVED = "removed"


@dataclass
class DocChange:
    """A single document change event."""

    doc_id: str
    change_type: ChangeType
    timestamp: float = 0.0
    old_content: Optional[str] = None
    new_content: Optional[str] = None
    metadata: dict = field(default_factory=dict)


@dataclass
class ObserverConfig:
    """Configuration for DocObserver behaviour."""

    notify_on_unchanged: bool = False
    track_history: bool = True
    max_history: int = 100


@dataclass
class Observer:
    """A registered observer."""

    observer_id: str
    pattern: str
    callback: Callable[[DocChange], None]
    change_types: set[ChangeType] = field(
        default_factory=lambda: {
            ChangeType.ADDED,
            ChangeType.MODIFIED,
            ChangeType.REMOVED,
        }
    )
    enabled: bool = True


class DocObserver:
    """In-memory document store with pattern-matched observer callbacks."""

    def __init__(self, config: Optional[ObserverConfig] = None) -> None:
        self.config = config if config is not None else ObserverConfig()
        self._lock = threading.Lock()
        self._docs: dict[str, str] = {}
        self._observers: dict[str, Observer] = {}
        self._history: list[DocChange] = []

    # ------------------------------------------------------------------
    # Document mutations
    # ------------------------------------------------------------------
    def add_doc(self, doc_id: str, content: str, now: float = 0.0) -> bool:
        """Add a new document. Returns False if doc_id already exists."""
        change: Optional[DocChange] = None
        deliveries: list[tuple[Callable[[DocChange], None], DocChange]] = []
        with self._lock:
            if doc_id in self._docs:
                return False
            self._docs[doc_id] = content
            change = DocChange(
                doc_id=doc_id,
                change_type=ChangeType.ADDED,
                timestamp=now,
                old_content=None,
                new_content=content,
            )
            self._record_history(change)
            deliveries = self._collect_deliveries(change)
        self._fire(deliveries)
        return True

    def update_doc(self, doc_id: str, content: str, now: float = 0.0) -> bool:
        """Update existing document. Returns False if doc_id missing."""
        deliveries: list[tuple[Callable[[DocChange], None], DocChange]] = []
        with self._lock:
            if doc_id not in self._docs:
                return False
            old_content = self._docs[doc_id]
            if old_content == content and not self.config.notify_on_unchanged:
                # No change: still True (operation succeeded), no event.
                return True
            self._docs[doc_id] = content
            change = DocChange(
                doc_id=doc_id,
                change_type=ChangeType.MODIFIED,
                timestamp=now,
                old_content=old_content,
                new_content=content,
            )
            self._record_history(change)
            deliveries = self._collect_deliveries(change)
        self._fire(deliveries)
        return True

    def remove_doc(self, doc_id: str, now: float = 0.0) -> bool:
        """Remove a document. Returns False if doc_id missing."""
        deliveries: list[tuple[Callable[[DocChange], None], DocChange]] = []
        with self._lock:
            if doc_id not in self._docs:
                return False
            old_content = self._docs.pop(doc_id)
            change = DocChange(
                doc_id=doc_id,
                change_type=ChangeType.REMOVED,
                timestamp=now,
                old_content=old_content,
                new_content=None,
            )
            self._record_history(change)
            deliveries = self._collect_deliveries(change)
        self._fire(deliveries)
        return True

    # ------------------------------------------------------------------
    # Observer registration
    # ------------------------------------------------------------------
    def register_observer(
        self,
        pattern: str,
        callback: Callable[[DocChange], None],
        change_types: Optional[set[ChangeType]] = None,
    ) -> str:
        """Register an observer. Returns the new observer_id."""
        if change_types is None:
            change_types = {
                ChangeType.ADDED,
                ChangeType.MODIFIED,
                ChangeType.REMOVED,
            }
        observer_id = uuid.uuid4().hex
        observer = Observer(
            observer_id=observer_id,
            pattern=pattern,
            callback=callback,
            change_types=set(change_types),
            enabled=True,
        )
        with self._lock:
            self._observers[observer_id] = observer
        return observer_id

    def unregister_observer(self, observer_id: str) -> bool:
        """Remove an observer. Returns True if it existed."""
        with self._lock:
            if observer_id in self._observers:
                del self._observers[observer_id]
                return True
            return False

    def enable_observer(self, observer_id: str) -> bool:
        """Enable an observer. Returns True if found."""
        with self._lock:
            obs = self._observers.get(observer_id)
            if obs is None:
                return False
            obs.enabled = True
            return True

    def disable_observer(self, observer_id: str) -> bool:
        """Disable an observer. Returns True if found."""
        with self._lock:
            obs = self._observers.get(observer_id)
            if obs is None:
                return False
            obs.enabled = False
            return True

    # ------------------------------------------------------------------
    # Pattern matching
    # ------------------------------------------------------------------
    @staticmethod
    def matches_pattern(doc_id: str, pattern: str) -> bool:
        """Return True if doc_id matches glob-style pattern."""
        return fnmatch.fnmatch(doc_id, pattern)

    # ------------------------------------------------------------------
    # Introspection
    # ------------------------------------------------------------------
    def get_doc(self, doc_id: str) -> Optional[str]:
        """Return current content of doc_id or None."""
        with self._lock:
            return self._docs.get(doc_id)

    def all_docs(self) -> dict[str, str]:
        """Snapshot of all documents."""
        with self._lock:
            return dict(self._docs)

    def history(
        self,
        doc_id: Optional[str] = None,
        limit: Optional[int] = None,
    ) -> list[DocChange]:
        """Return change history, optionally filtered by doc_id and limit."""
        with self._lock:
            if doc_id is None:
                items = list(self._history)
            else:
                items = [c for c in self._history if c.doc_id == doc_id]
        if limit is not None and limit >= 0:
            items = items[-limit:] if limit > 0 else []
        return items

    def observer_count(self, enabled_only: bool = True) -> int:
        """Count of registered observers."""
        with self._lock:
            if enabled_only:
                return sum(1 for o in self._observers.values() if o.enabled)
            return len(self._observers)

    @property
    def doc_count(self) -> int:
        with self._lock:
            return len(self._docs)

    def clear(self) -> None:
        """Remove all docs, observers, and history."""
        with self._lock:
            self._docs.clear()
            self._observers.clear()
            self._history.clear()

    # ------------------------------------------------------------------
    # Internal helpers (caller holds the lock)
    # ------------------------------------------------------------------
    def _record_history(self, change: DocChange) -> None:
        if not self.config.track_history:
            return
        self._history.append(change)
        if self.config.max_history > 0 and len(self._history) > self.config.max_history:
            # Drop oldest entries to enforce cap.
            overflow = len(self._history) - self.config.max_history
            del self._history[:overflow]

    def _collect_deliveries(
        self, change: DocChange
    ) -> list[tuple[Callable[[DocChange], None], DocChange]]:
        deliveries: list[tuple[Callable[[DocChange], None], DocChange]] = []
        for obs in self._observers.values():
            if not obs.enabled:
                continue
            if change.change_type not in obs.change_types:
                continue
            if not fnmatch.fnmatch(change.doc_id, obs.pattern):
                continue
            deliveries.append((obs.callback, change))
        return deliveries

    @staticmethod
    def _fire(
        deliveries: list[tuple[Callable[[DocChange], None], DocChange]],
    ) -> None:
        for cb, change in deliveries:
            try:
                cb(change)
            except Exception:
                pass
