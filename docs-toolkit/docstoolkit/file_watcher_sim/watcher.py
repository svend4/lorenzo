"""Simulated file watcher: tracks file changes by content hash.

No actual filesystem watching — callers explicitly call ``register`` /
``update`` / ``remove``. Useful for tests, dry-runs, and deterministic
event replay.
"""

from __future__ import annotations

import hashlib
import threading
from dataclasses import dataclass, field
from enum import Enum
from typing import Callable, Dict, List, Optional


class ChangeKind(str, Enum):
    """Kinds of changes that can occur to a tracked file."""

    ADDED = "ADDED"
    MODIFIED = "MODIFIED"
    REMOVED = "REMOVED"
    UNCHANGED = "UNCHANGED"


@dataclass
class FileChange:
    """A single change event for a tracked file."""

    path: str
    kind: ChangeKind
    old_hash: Optional[str]
    new_hash: Optional[str]
    timestamp: float


@dataclass
class WatchSnapshot:
    """Snapshot of all tracked files at a given (virtual) time."""

    files: Dict[str, str] = field(default_factory=dict)
    timestamp: float = 0.0

    @property
    def file_count(self) -> int:
        return len(self.files)


def _hash_content(content: str) -> str:
    """Return sha256 hexdigest of ``content``."""
    return hashlib.sha256(content.encode("utf-8")).hexdigest()


class FileWatcherSim:
    """Simulated file watcher.

    State is held entirely in memory; events are produced only when the
    caller explicitly mutates state via ``update`` or ``remove``.
    Registration does not produce events (it is treated as initial sync).
    """

    def __init__(self) -> None:
        self._lock = threading.Lock()
        # path -> (hash, registered_or_updated_timestamp)
        self._state: Dict[str, tuple] = {}
        self._events: List[FileChange] = []
        self._subscribers: Dict[int, Callable[[FileChange], None]] = {}
        self._next_sub_id = 0

    # ------------------------------------------------------------------
    # Properties
    # ------------------------------------------------------------------

    @property
    def tracked_paths(self) -> List[str]:
        with self._lock:
            return list(self._state.keys())

    @property
    def file_count(self) -> int:
        with self._lock:
            return len(self._state)

    # ------------------------------------------------------------------
    # Registration
    # ------------------------------------------------------------------

    def register(self, path: str, content: str, now: float = 0.0) -> None:
        """Track ``path`` with given ``content``. Does not fire events."""
        h = _hash_content(content)
        with self._lock:
            self._state[path] = (h, now)

    def register_batch(self, files: Dict[str, str], now: float = 0.0) -> None:
        """Register multiple files at once."""
        with self._lock:
            for path, content in files.items():
                self._state[path] = (_hash_content(content), now)

    # ------------------------------------------------------------------
    # Mutations
    # ------------------------------------------------------------------

    def update(self, path: str, content: str, now: float = 0.0) -> FileChange:
        """Record an update.

        Returns a ``FileChange`` describing what happened:
        - ``ADDED`` if path was not previously tracked
        - ``UNCHANGED`` if hash is identical
        - ``MODIFIED`` otherwise

        Fires subscribers on every call (including UNCHANGED? No — only on
        actual change). UNCHANGED events are still appended to the event
        log so ``changes_since`` can observe them, but subscribers are not
        fired for UNCHANGED to avoid spurious wake-ups.
        """
        new_hash = _hash_content(content)
        with self._lock:
            old = self._state.get(path)
            if old is None:
                change = FileChange(
                    path=path,
                    kind=ChangeKind.ADDED,
                    old_hash=None,
                    new_hash=new_hash,
                    timestamp=now,
                )
                self._state[path] = (new_hash, now)
            else:
                old_hash, _ = old
                if old_hash == new_hash:
                    change = FileChange(
                        path=path,
                        kind=ChangeKind.UNCHANGED,
                        old_hash=old_hash,
                        new_hash=new_hash,
                        timestamp=now,
                    )
                    # State timestamp left as-is for unchanged files.
                else:
                    change = FileChange(
                        path=path,
                        kind=ChangeKind.MODIFIED,
                        old_hash=old_hash,
                        new_hash=new_hash,
                        timestamp=now,
                    )
                    self._state[path] = (new_hash, now)
            self._events.append(change)
            subscribers = list(self._subscribers.values())

        # Fire subscribers outside the lock to avoid deadlock if a
        # callback calls back into the watcher.
        if change.kind != ChangeKind.UNCHANGED:
            for cb in subscribers:
                cb(change)
        return change

    def remove(self, path: str, now: float = 0.0) -> Optional[FileChange]:
        """Remove a tracked file.

        Returns ``None`` if ``path`` was not tracked; otherwise returns
        a ``REMOVED`` ``FileChange``.
        """
        with self._lock:
            old = self._state.pop(path, None)
            if old is None:
                return None
            old_hash, _ = old
            change = FileChange(
                path=path,
                kind=ChangeKind.REMOVED,
                old_hash=old_hash,
                new_hash=None,
                timestamp=now,
            )
            self._events.append(change)
            subscribers = list(self._subscribers.values())

        for cb in subscribers:
            cb(change)
        return change

    # ------------------------------------------------------------------
    # Snapshot & diff
    # ------------------------------------------------------------------

    def snapshot(self) -> WatchSnapshot:
        """Return an immutable-ish snapshot of current state."""
        with self._lock:
            files = {path: h for path, (h, _) in self._state.items()}
            last_ts = max((ts for _, ts in self._state.values()), default=0.0)
        return WatchSnapshot(files=files, timestamp=last_ts)

    def diff(
        self, old_snapshot: WatchSnapshot, new_snapshot: WatchSnapshot
    ) -> List[FileChange]:
        """Compute changes between two snapshots.

        Order: ADDED, MODIFIED, REMOVED (deterministic by path within
        each kind).
        """
        old = old_snapshot.files
        new = new_snapshot.files
        added = sorted(set(new) - set(old))
        removed = sorted(set(old) - set(new))
        common = sorted(set(old) & set(new))

        ts = new_snapshot.timestamp
        changes: List[FileChange] = []
        for p in added:
            changes.append(
                FileChange(
                    path=p,
                    kind=ChangeKind.ADDED,
                    old_hash=None,
                    new_hash=new[p],
                    timestamp=ts,
                )
            )
        for p in common:
            if old[p] != new[p]:
                changes.append(
                    FileChange(
                        path=p,
                        kind=ChangeKind.MODIFIED,
                        old_hash=old[p],
                        new_hash=new[p],
                        timestamp=ts,
                    )
                )
        for p in removed:
            changes.append(
                FileChange(
                    path=p,
                    kind=ChangeKind.REMOVED,
                    old_hash=old[p],
                    new_hash=None,
                    timestamp=ts,
                )
            )
        return changes

    # ------------------------------------------------------------------
    # Event log
    # ------------------------------------------------------------------

    def changes_since(self, timestamp: float) -> List[FileChange]:
        """Return all events with ``event.timestamp > timestamp``."""
        with self._lock:
            return [e for e in self._events if e.timestamp > timestamp]

    # ------------------------------------------------------------------
    # Subscribers
    # ------------------------------------------------------------------

    def subscribe(self, callback: Callable[[FileChange], None]) -> int:
        """Subscribe to change events. Returns a subscription id."""
        with self._lock:
            sub_id = self._next_sub_id
            self._next_sub_id += 1
            self._subscribers[sub_id] = callback
        return sub_id

    def unsubscribe(self, sub_id: int) -> bool:
        """Remove a subscription. Returns ``True`` if removed."""
        with self._lock:
            return self._subscribers.pop(sub_id, None) is not None
