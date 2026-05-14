"""TTL manager for documents with sliding/fixed expiry modes."""

from __future__ import annotations

import threading
from dataclasses import dataclass, field
from enum import Enum
from typing import Optional


class ExpiryMode(Enum):
    """Expiration behavior for a TTL entry."""

    FIXED = "fixed"
    SLIDING = "sliding"


@dataclass
class TtlEntry:
    """A single TTL entry tracking a document's lifetime."""

    doc_id: str
    created_at: float
    expires_at: float
    last_accessed: float
    mode: ExpiryMode = ExpiryMode.FIXED
    ttl: float = 0.0


@dataclass
class TtlStats:
    """Aggregated statistics about TTL entries."""

    total: int
    active: int
    expired: int
    by_mode: dict = field(default_factory=dict)
    expiring_soon: int = 0


class DocTtl:
    """Document TTL manager with fixed and sliding expiry modes."""

    def __init__(self, default_ttl: float = 3600) -> None:
        self._default_ttl = float(default_ttl)
        self._entries: dict[str, TtlEntry] = {}
        self._lock = threading.Lock()

    # ------------------------------------------------------------------ #
    # Mutators
    # ------------------------------------------------------------------ #
    def add(
        self,
        doc_id: str,
        ttl: Optional[float] = None,
        mode: ExpiryMode = ExpiryMode.FIXED,
        now: float = 0.0,
    ) -> TtlEntry:
        """Add (or replace) a TTL entry for ``doc_id``."""

        effective_ttl = float(ttl) if ttl is not None else self._default_ttl
        with self._lock:
            entry = TtlEntry(
                doc_id=doc_id,
                created_at=float(now),
                expires_at=float(now) + effective_ttl,
                last_accessed=float(now),
                mode=mode,
                ttl=effective_ttl,
            )
            self._entries[doc_id] = entry
            return entry

    def remove(self, doc_id: str) -> bool:
        with self._lock:
            if doc_id in self._entries:
                del self._entries[doc_id]
                return True
            return False

    def clear(self) -> None:
        with self._lock:
            self._entries.clear()

    def set_default_ttl(self, ttl: float) -> None:
        with self._lock:
            self._default_ttl = float(ttl)

    # ------------------------------------------------------------------ #
    # Lookups
    # ------------------------------------------------------------------ #
    def get(self, doc_id: str, now: float = 0.0) -> Optional[TtlEntry]:
        """Return entry only if it is not expired. Does not auto-cleanup."""

        with self._lock:
            entry = self._entries.get(doc_id)
            if entry is None:
                return None
            if now >= entry.expires_at:
                return None
            entry.last_accessed = float(now)
            return entry

    def peek(self, doc_id: str) -> Optional[TtlEntry]:
        with self._lock:
            return self._entries.get(doc_id)

    def is_expired(self, doc_id: str, now: float = 0.0) -> bool:
        with self._lock:
            entry = self._entries.get(doc_id)
            if entry is None:
                return True
            return now >= entry.expires_at

    def is_alive(self, doc_id: str, now: float = 0.0) -> bool:
        with self._lock:
            entry = self._entries.get(doc_id)
            if entry is None:
                return False
            return now < entry.expires_at

    def time_left(self, doc_id: str, now: float = 0.0) -> Optional[float]:
        with self._lock:
            entry = self._entries.get(doc_id)
            if entry is None:
                return None
            return entry.expires_at - now

    # ------------------------------------------------------------------ #
    # Lifetime extensions
    # ------------------------------------------------------------------ #
    def extend(self, doc_id: str, additional_ttl: float, now: float = 0.0) -> bool:
        with self._lock:
            entry = self._entries.get(doc_id)
            if entry is None:
                return False
            entry.expires_at += float(additional_ttl)
            entry.last_accessed = float(now)
            return True

    def refresh(self, doc_id: str, now: float = 0.0) -> bool:
        """Reset expiry to ``now + ttl``."""

        with self._lock:
            entry = self._entries.get(doc_id)
            if entry is None:
                return False
            entry.expires_at = float(now) + entry.ttl
            entry.last_accessed = float(now)
            return True

    def touch(self, doc_id: str, now: float = 0.0) -> bool:
        """Update last_accessed; for SLIDING also reset expiry to now + ttl."""

        with self._lock:
            entry = self._entries.get(doc_id)
            if entry is None:
                return False
            entry.last_accessed = float(now)
            if entry.mode == ExpiryMode.SLIDING:
                entry.expires_at = float(now) + entry.ttl
            return True

    # ------------------------------------------------------------------ #
    # Bulk inspection / cleanup
    # ------------------------------------------------------------------ #
    def expired_doc_ids(self, now: float = 0.0) -> list:
        with self._lock:
            return [
                doc_id
                for doc_id, entry in self._entries.items()
                if now >= entry.expires_at
            ]

    def active_doc_ids(self, now: float = 0.0) -> list:
        with self._lock:
            return [
                doc_id
                for doc_id, entry in self._entries.items()
                if now < entry.expires_at
            ]

    def expiring_within(self, seconds: float, now: float = 0.0) -> list:
        threshold = float(now) + float(seconds)
        with self._lock:
            return [
                doc_id
                for doc_id, entry in self._entries.items()
                if now < entry.expires_at <= threshold
            ]

    def cleanup_expired(self, now: float = 0.0) -> int:
        with self._lock:
            expired = [
                doc_id
                for doc_id, entry in self._entries.items()
                if now >= entry.expires_at
            ]
            for doc_id in expired:
                del self._entries[doc_id]
            return len(expired)

    def count_active(self, now: float = 0.0) -> int:
        with self._lock:
            return sum(
                1 for entry in self._entries.values() if now < entry.expires_at
            )

    @property
    def total_entries(self) -> int:
        with self._lock:
            return len(self._entries)

    def stats(self, now: float = 0.0, expiring_soon_window: float = 300.0) -> TtlStats:
        with self._lock:
            total = len(self._entries)
            active = 0
            expired = 0
            by_mode: dict = {}
            soon_threshold = float(now) + float(expiring_soon_window)
            expiring_soon = 0
            for entry in self._entries.values():
                mode_key = entry.mode.value
                by_mode[mode_key] = by_mode.get(mode_key, 0) + 1
                if now < entry.expires_at:
                    active += 1
                    if entry.expires_at <= soon_threshold:
                        expiring_soon += 1
                else:
                    expired += 1
            return TtlStats(
                total=total,
                active=active,
                expired=expired,
                by_mode=by_mode,
                expiring_soon=expiring_soon,
            )
