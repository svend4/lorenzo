"""E369 DocClipboardStore — per-user clipboard for document fragments.

Thread-safe, pure stdlib, no third-party dependencies.
"""

from __future__ import annotations

import threading
import time
from dataclasses import dataclass, field
from typing import Optional


@dataclass
class ClipboardEntry:
    """A single clipboard entry."""

    entry_id: int
    user_id: str
    content: str
    source_doc_id: str = ""
    copied_at: float = 0.0
    pinned: bool = False


@dataclass
class ClipboardStats:
    """Aggregate clipboard statistics."""

    total_entries: int
    unique_users: int
    pinned_count: int


class DocClipboardStore:
    """Per-user clipboard for document fragments.

    Maintains a bounded trail of clipboard entries per user. When the trail
    exceeds ``max_per_user``, oldest non-pinned entries are evicted.
    """

    def __init__(self, max_per_user: int = 20) -> None:
        if max_per_user < 1:
            raise ValueError("max_per_user must be >= 1")
        self._entries: dict[int, ClipboardEntry] = {}
        self._by_user: dict[str, list[int]] = {}
        self._next_id: int = 1
        self._max_per_user: int = max_per_user
        self._lock = threading.Lock()

    # ----------------------------- mutators --------------------------------
    def copy(
        self,
        user_id: str,
        content: str,
        source_doc_id: str = "",
        now: Optional[float] = None,
    ) -> ClipboardEntry:
        """Add a new clipboard entry for the user.

        Trims oldest non-pinned entries when the user's trail exceeds the
        configured maximum.
        """
        with self._lock:
            ts = now if now is not None else time.time()
            entry = ClipboardEntry(
                entry_id=self._next_id,
                user_id=user_id,
                content=content,
                source_doc_id=source_doc_id,
                copied_at=ts,
                pinned=False,
            )
            self._next_id += 1
            self._entries[entry.entry_id] = entry
            trail = self._by_user.setdefault(user_id, [])
            trail.append(entry.entry_id)
            self._trim_user(user_id)
            return entry

    def _trim_user(self, user_id: str) -> None:
        """Drop oldest non-pinned entries until the trail fits the cap."""
        trail = self._by_user.get(user_id, [])
        # Walk from oldest to newest, removing non-pinned entries until the
        # trail is at most max_per_user long.
        i = 0
        while len(trail) > self._max_per_user and i < len(trail):
            eid = trail[i]
            entry = self._entries.get(eid)
            if entry is not None and not entry.pinned:
                del self._entries[eid]
                trail.pop(i)
                # do not advance i — list shrunk
                continue
            i += 1

    def pin(self, entry_id: int) -> bool:
        """Mark the entry as pinned. Returns True if the entry existed."""
        with self._lock:
            entry = self._entries.get(entry_id)
            if entry is None:
                return False
            entry.pinned = True
            return True

    def unpin(self, entry_id: int) -> bool:
        """Mark the entry as unpinned. Returns True if the entry existed."""
        with self._lock:
            entry = self._entries.get(entry_id)
            if entry is None:
                return False
            entry.pinned = False
            return True

    def delete(self, entry_id: int) -> bool:
        """Remove an entry. Returns True if it existed."""
        with self._lock:
            entry = self._entries.pop(entry_id, None)
            if entry is None:
                return False
            trail = self._by_user.get(entry.user_id)
            if trail is not None and entry_id in trail:
                trail.remove(entry_id)
            return True

    def clear_user(self, user_id: str, include_pinned: bool = False) -> int:
        """Remove the user's clipboard entries. Returns count removed."""
        with self._lock:
            trail = self._by_user.get(user_id, [])
            if not trail:
                return 0
            removed = 0
            remaining: list[int] = []
            for eid in trail:
                entry = self._entries.get(eid)
                if entry is None:
                    continue
                if entry.pinned and not include_pinned:
                    remaining.append(eid)
                    continue
                del self._entries[eid]
                removed += 1
            if remaining:
                self._by_user[user_id] = remaining
            else:
                self._by_user.pop(user_id, None)
            return removed

    # ----------------------------- accessors -------------------------------
    def get(self, entry_id: int) -> Optional[ClipboardEntry]:
        """Return the entry by id, or None if missing."""
        with self._lock:
            return self._entries.get(entry_id)

    def entries_for(
        self,
        user_id: str,
        pinned_only: bool = False,
        limit: Optional[int] = None,
    ) -> list[ClipboardEntry]:
        """Return the user's entries, most recent first."""
        with self._lock:
            trail = self._by_user.get(user_id, [])
            # most recent first = reversed insertion order
            out: list[ClipboardEntry] = []
            for eid in reversed(trail):
                entry = self._entries.get(eid)
                if entry is None:
                    continue
                if pinned_only and not entry.pinned:
                    continue
                out.append(entry)
                if limit is not None and len(out) >= limit:
                    break
            return out

    def latest(self, user_id: str) -> Optional[ClipboardEntry]:
        """Return the most recent entry for the user, or None."""
        with self._lock:
            trail = self._by_user.get(user_id, [])
            for eid in reversed(trail):
                entry = self._entries.get(eid)
                if entry is not None:
                    return entry
            return None

    def search(self, user_id: str, query: str) -> list[ClipboardEntry]:
        """Case-insensitive substring search over the user's entries."""
        q = query.lower()
        with self._lock:
            trail = self._by_user.get(user_id, [])
            out: list[ClipboardEntry] = []
            for eid in reversed(trail):
                entry = self._entries.get(eid)
                if entry is None:
                    continue
                if q in entry.content.lower():
                    out.append(entry)
            return out

    def pinned_entries(self, user_id: str) -> list[ClipboardEntry]:
        """Return all pinned entries for the user, newest first."""
        with self._lock:
            trail = self._by_user.get(user_id, [])
            items = [
                self._entries[eid]
                for eid in trail
                if eid in self._entries and self._entries[eid].pinned
            ]
            items.sort(key=lambda e: e.copied_at, reverse=True)
            return items

    def users_with_clipboards(self) -> list[str]:
        """Return sorted list of users with at least one entry."""
        with self._lock:
            return sorted(u for u, trail in self._by_user.items() if trail)

    def stats(self) -> ClipboardStats:
        """Return aggregate statistics."""
        with self._lock:
            total = len(self._entries)
            users = sum(1 for trail in self._by_user.values() if trail)
            pinned = sum(1 for e in self._entries.values() if e.pinned)
            return ClipboardStats(
                total_entries=total,
                unique_users=users,
                pinned_count=pinned,
            )
