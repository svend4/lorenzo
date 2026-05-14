"""E374 DocTagBlacklist implementation."""

from __future__ import annotations

import fnmatch
import threading
import time
from dataclasses import dataclass, field
from typing import Optional


_WILDCARD_CHARS = set("*?[")


def _has_wildcard(pattern: str) -> bool:
    return any(ch in _WILDCARD_CHARS for ch in pattern)


@dataclass
class BlacklistEntry:
    """A single blacklist entry."""

    pattern: str
    reason: str = ""
    added_at: float = 0.0
    added_by: str = ""
    case_sensitive: bool = True


@dataclass
class BlacklistStats:
    """Aggregate blacklist statistics."""

    total_entries: int
    exact_count: int
    pattern_count: int
    case_insensitive_count: int


class DocTagBlacklist:
    """Manage a collection of disallowed tag patterns (E374)."""

    def __init__(self) -> None:
        self._entries: dict[str, BlacklistEntry] = {}
        self._lock = threading.Lock()

    def add(
        self,
        pattern: str,
        reason: str = "",
        added_by: str = "",
        case_sensitive: bool = True,
        now: Optional[float] = None,
    ) -> BlacklistEntry:
        """Add or replace a blacklist entry for *pattern*."""
        ts = time.time() if now is None else now
        entry = BlacklistEntry(
            pattern=pattern,
            reason=reason,
            added_at=ts,
            added_by=added_by,
            case_sensitive=case_sensitive,
        )
        with self._lock:
            self._entries[pattern] = entry
        return entry

    def remove(self, pattern: str) -> bool:
        """Remove an entry. Return True if it existed."""
        with self._lock:
            return self._entries.pop(pattern, None) is not None

    def _match(self, tag: str, entry: BlacklistEntry) -> bool:
        if entry.case_sensitive:
            return fnmatch.fnmatchcase(tag, entry.pattern)
        return fnmatch.fnmatchcase(tag.lower(), entry.pattern.lower())

    def is_blacklisted(self, tag: str) -> bool:
        """Return True if *tag* matches any blacklist entry."""
        with self._lock:
            entries = list(self._entries.values())
        for entry in entries:
            if self._match(tag, entry):
                return True
        return False

    def matching_patterns(self, tag: str) -> list[str]:
        """Return sorted list of patterns that match *tag*."""
        with self._lock:
            entries = list(self._entries.values())
        matched = [e.pattern for e in entries if self._match(tag, e)]
        return sorted(matched)

    def filter_tags(self, tags: list[str]) -> tuple:
        """Split *tags* into (allowed_sorted, blocked_sorted)."""
        with self._lock:
            entries = list(self._entries.values())
        allowed: list[str] = []
        blocked: list[str] = []
        for tag in tags:
            if any(self._match(tag, e) for e in entries):
                blocked.append(tag)
            else:
                allowed.append(tag)
        return (sorted(allowed), sorted(blocked))

    def get(self, pattern: str) -> Optional[BlacklistEntry]:
        """Return the entry for *pattern* or None."""
        with self._lock:
            return self._entries.get(pattern)

    def list_entries(self) -> list[BlacklistEntry]:
        """Return all entries sorted by pattern."""
        with self._lock:
            entries = list(self._entries.values())
        return sorted(entries, key=lambda e: e.pattern)

    def clear(self) -> int:
        """Remove all entries; return the number cleared."""
        with self._lock:
            count = len(self._entries)
            self._entries.clear()
        return count

    def stats(self) -> BlacklistStats:
        """Compute aggregate statistics."""
        with self._lock:
            entries = list(self._entries.values())
        total = len(entries)
        pattern_count = sum(1 for e in entries if _has_wildcard(e.pattern))
        exact_count = total - pattern_count
        case_insensitive_count = sum(1 for e in entries if not e.case_sensitive)
        return BlacklistStats(
            total_entries=total,
            exact_count=exact_count,
            pattern_count=pattern_count,
            case_insensitive_count=case_insensitive_count,
        )
