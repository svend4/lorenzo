"""E412 DocQuotaTracker — track usage against quotas per (key, resource).

Pure stdlib, no third-party dependencies. Thread-safe via ``threading.Lock``.
"""
from __future__ import annotations

import threading
import time as _time
from dataclasses import dataclass
from typing import Dict, List, Optional, Tuple


@dataclass
class QuotaDefinition:
    """A defined quota for a particular resource."""

    resource: str
    limit: int
    description: str = ""


@dataclass
class QuotaUsage:
    """Current usage entry for a (key, resource) pair."""

    key: str
    resource: str
    current: int = 0
    last_updated_at: float = 0.0


@dataclass
class QuotaStats:
    """Aggregate statistics across the tracker."""

    total_definitions: int
    total_keys: int
    keys_at_limit: int
    keys_over_limit: int


class DocQuotaTracker:
    """Track usage against quotas per (key, resource).

    Quotas are defined per ``resource``. Usage is recorded per
    ``(key, resource)`` pair, where ``key`` is typically a user_id, org_id,
    or any other arbitrary identifier.

    All public mutators take an optional ``now`` parameter (seconds since
    epoch). If omitted, ``time.time()`` is used.

    Thread-safety: all public methods acquire a single ``threading.Lock``.
    """

    def __init__(self) -> None:
        self._lock = threading.Lock()
        self._definitions: Dict[str, QuotaDefinition] = {}
        self._usage: Dict[Tuple[str, str], QuotaUsage] = {}

    # ------------------------------------------------------------------ #
    # Definition management
    # ------------------------------------------------------------------ #
    def define_quota(self, definition: QuotaDefinition) -> None:
        """Register or replace a quota definition for a resource."""
        with self._lock:
            self._definitions[definition.resource] = definition

    def remove_quota(self, resource: str) -> bool:
        """Remove a definition. Returns True if it existed."""
        with self._lock:
            return self._definitions.pop(resource, None) is not None

    def get_definition(self, resource: str) -> Optional[QuotaDefinition]:
        """Return the definition for a resource, or ``None`` if absent."""
        with self._lock:
            return self._definitions.get(resource)

    def list_definitions(self) -> List[QuotaDefinition]:
        """Return all definitions, sorted by resource name."""
        with self._lock:
            return sorted(self._definitions.values(), key=lambda d: d.resource)

    # ------------------------------------------------------------------ #
    # Usage mutators
    # ------------------------------------------------------------------ #
    def _now(self, now: Optional[float]) -> float:
        return _time.time() if now is None else now

    def increment(
        self,
        key: str,
        resource: str,
        amount: int = 1,
        now: Optional[float] = None,
    ) -> Optional[QuotaUsage]:
        """Increment usage. Returns ``None`` if resource isn't defined.

        Creates a ``QuotaUsage`` entry if one doesn't exist for the pair.
        """
        ts = self._now(now)
        with self._lock:
            if resource not in self._definitions:
                return None
            usage = self._usage.get((key, resource))
            if usage is None:
                usage = QuotaUsage(key=key, resource=resource, current=0)
                self._usage[(key, resource)] = usage
            usage.current += amount
            usage.last_updated_at = ts
            return usage

    def decrement(
        self,
        key: str,
        resource: str,
        amount: int = 1,
        now: Optional[float] = None,
    ) -> Optional[QuotaUsage]:
        """Decrement usage, floored at 0. ``None`` if resource not defined."""
        ts = self._now(now)
        with self._lock:
            if resource not in self._definitions:
                return None
            usage = self._usage.get((key, resource))
            if usage is None:
                usage = QuotaUsage(key=key, resource=resource, current=0)
                self._usage[(key, resource)] = usage
            usage.current = max(0, usage.current - amount)
            usage.last_updated_at = ts
            return usage

    def set_usage(
        self,
        key: str,
        resource: str,
        value: int,
        now: Optional[float] = None,
    ) -> Optional[QuotaUsage]:
        """Set usage to an explicit value. ``None`` if not defined."""
        ts = self._now(now)
        with self._lock:
            if resource not in self._definitions:
                return None
            usage = self._usage.get((key, resource))
            if usage is None:
                usage = QuotaUsage(key=key, resource=resource, current=0)
                self._usage[(key, resource)] = usage
            usage.current = max(0, value)
            usage.last_updated_at = ts
            return usage

    # ------------------------------------------------------------------ #
    # Read-only queries
    # ------------------------------------------------------------------ #
    def get_usage(self, key: str, resource: str) -> Optional[QuotaUsage]:
        """Return usage entry for the pair, or ``None`` if absent."""
        with self._lock:
            return self._usage.get((key, resource))

    def check(self, key: str, resource: str, amount: int = 1) -> bool:
        """Return True if ``current + amount <= limit``.

        Returns False if the resource is undefined. If no usage exists yet,
        ``current`` is treated as 0.
        """
        with self._lock:
            definition = self._definitions.get(resource)
            if definition is None:
                return False
            usage = self._usage.get((key, resource))
            current = usage.current if usage is not None else 0
            return current + amount <= definition.limit

    def available(self, key: str, resource: str) -> Optional[int]:
        """``limit - current``; ``None`` if not defined. Can be negative."""
        with self._lock:
            definition = self._definitions.get(resource)
            if definition is None:
                return None
            usage = self._usage.get((key, resource))
            current = usage.current if usage is not None else 0
            return definition.limit - current

    def usage_for_key(self, key: str) -> List[QuotaUsage]:
        """All usage entries for a key, sorted by resource."""
        with self._lock:
            entries = [u for (k, _r), u in self._usage.items() if k == key]
            return sorted(entries, key=lambda u: u.resource)

    def keys_at_limit(self, resource: str) -> List[str]:
        """Sorted keys that are at or over the resource's limit.

        Returns an empty list if the resource isn't defined.
        """
        with self._lock:
            definition = self._definitions.get(resource)
            if definition is None:
                return []
            keys: List[str] = []
            for (k, r), u in self._usage.items():
                if r != resource:
                    continue
                if u.current >= definition.limit:
                    keys.append(k)
            return sorted(keys)

    # ------------------------------------------------------------------ #
    # Bulk operations
    # ------------------------------------------------------------------ #
    def reset_key(self, key: str) -> int:
        """Zero out every usage entry for a key. Returns count touched."""
        with self._lock:
            n = 0
            for (k, _r), u in self._usage.items():
                if k == key:
                    u.current = 0
                    n += 1
            return n

    def clear_resource(self, resource: str) -> int:
        """Remove every usage entry for a resource. Returns count removed."""
        with self._lock:
            to_delete = [
                pair for pair in self._usage.keys() if pair[1] == resource
            ]
            for pair in to_delete:
                del self._usage[pair]
            return len(to_delete)

    # ------------------------------------------------------------------ #
    # Stats
    # ------------------------------------------------------------------ #
    def stats(self) -> QuotaStats:
        """Snapshot of aggregate counters."""
        with self._lock:
            unique_keys = {k for (k, _r) in self._usage.keys()}
            at_limit = 0
            over_limit = 0
            for (_k, r), u in self._usage.items():
                definition = self._definitions.get(r)
                if definition is None:
                    continue
                if u.current > definition.limit:
                    over_limit += 1
                elif u.current == definition.limit:
                    at_limit += 1
            return QuotaStats(
                total_definitions=len(self._definitions),
                total_keys=len(unique_keys),
                keys_at_limit=at_limit,
                keys_over_limit=over_limit,
            )
