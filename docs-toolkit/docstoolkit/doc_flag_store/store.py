"""DocFlagStore — boolean feature flags with per-document overrides.

Provides a thread-safe, pure-stdlib store for managing boolean feature flags
and document-level override values.  No third-party dependencies required.
"""
from __future__ import annotations

import threading
import time
from dataclasses import dataclass, field
from typing import Optional


# ---------------------------------------------------------------------------
# Dataclasses
# ---------------------------------------------------------------------------


@dataclass
class Flag:
    """A feature flag definition."""

    name: str
    enabled: bool = False
    description: str = ""
    rollout_pct: float = 100.0  # 0–100; documented only, not enforced


@dataclass
class FlagOverride:
    """A per-document override for a single flag."""

    doc_id: str
    flag_name: str
    enabled: bool
    set_at: float = 0.0


@dataclass
class FlagStats:
    """Aggregate statistics for a :class:`DocFlagStore`."""

    total_flags: int
    enabled_flags: int       # globally enabled flags
    total_overrides: int
    docs_with_overrides: int


# ---------------------------------------------------------------------------
# Store
# ---------------------------------------------------------------------------


class DocFlagStore:
    """Thread-safe in-memory store for boolean feature flags.

    Flags are global definitions (with a global default ``enabled`` value).
    Per-document overrides can raise or lower a flag independently of the
    global default.  All public methods are protected by a single
    :class:`threading.Lock`.
    """

    def __init__(self) -> None:
        self._lock: threading.Lock = threading.Lock()
        self._flags: dict[str, Flag] = {}
        self._overrides: dict[tuple, FlagOverride] = {}

    # ------------------------------------------------------------------
    # Internal helpers
    # ------------------------------------------------------------------

    @staticmethod
    def _now(now: Optional[float]) -> float:
        return now if now is not None else time.time()

    # ------------------------------------------------------------------
    # Flag management
    # ------------------------------------------------------------------

    def define_flag(self, flag: Flag) -> None:
        """Register or replace a flag definition."""
        with self._lock:
            self._flags[flag.name] = flag

    def undefine_flag(self, name: str) -> bool:
        """Remove a flag and all its overrides.

        Returns ``True`` if the flag existed, ``False`` otherwise.
        """
        with self._lock:
            if name not in self._flags:
                return False
            del self._flags[name]
            # remove every override belonging to this flag
            keys_to_remove = [
                k for k in self._overrides if k[1] == name
            ]
            for k in keys_to_remove:
                del self._overrides[k]
        return True

    def get_flag(self, name: str) -> Optional[Flag]:
        """Return the :class:`Flag` for *name*, or ``None`` if not defined."""
        with self._lock:
            return self._flags.get(name)

    def set_enabled(self, name: str, enabled: bool) -> bool:
        """Update the global default for flag *name*.

        Returns ``True`` if the flag exists and was updated, ``False`` if
        the flag is not defined.
        """
        with self._lock:
            flag = self._flags.get(name)
            if flag is None:
                return False
            self._flags[name] = Flag(
                name=flag.name,
                enabled=enabled,
                description=flag.description,
                rollout_pct=flag.rollout_pct,
            )
        return True

    def list_flags(self) -> list[Flag]:
        """Return all defined flags, sorted by name."""
        with self._lock:
            return sorted(self._flags.values(), key=lambda f: f.name)

    # ------------------------------------------------------------------
    # Override management
    # ------------------------------------------------------------------

    def set_override(
        self,
        doc_id: str,
        flag_name: str,
        enabled: bool,
        now: Optional[float] = None,
    ) -> FlagOverride:
        """Create or replace a per-document override.

        Returns the resulting :class:`FlagOverride`.
        """
        ts = self._now(now)
        override = FlagOverride(
            doc_id=doc_id,
            flag_name=flag_name,
            enabled=enabled,
            set_at=ts,
        )
        with self._lock:
            self._overrides[(doc_id, flag_name)] = override
        return override

    def remove_override(self, doc_id: str, flag_name: str) -> bool:
        """Remove an override.  Returns ``True`` if it existed."""
        with self._lock:
            key = (doc_id, flag_name)
            if key not in self._overrides:
                return False
            del self._overrides[key]
        return True

    def get_override(self, doc_id: str, flag_name: str) -> Optional[FlagOverride]:
        """Return the :class:`FlagOverride` for *(doc_id, flag_name)*, or ``None``."""
        with self._lock:
            return self._overrides.get((doc_id, flag_name))

    # ------------------------------------------------------------------
    # Resolution
    # ------------------------------------------------------------------

    def is_enabled(self, doc_id: str, flag_name: str) -> bool:
        """Return the effective enabled state for a document.

        Priority:
        1. If there is a per-document override, use its value.
        2. Otherwise fall back to the global flag default.
        3. If the flag is not defined at all, return ``False``.
        """
        with self._lock:
            override = self._overrides.get((doc_id, flag_name))
            if override is not None:
                return override.enabled
            flag = self._flags.get(flag_name)
            if flag is None:
                return False
            return flag.enabled

    # ------------------------------------------------------------------
    # Queries
    # ------------------------------------------------------------------

    def overrides_for_doc(self, doc_id: str) -> list[FlagOverride]:
        """Return all overrides for *doc_id*, sorted by flag_name."""
        with self._lock:
            result = [
                ov for k, ov in self._overrides.items() if k[0] == doc_id
            ]
        return sorted(result, key=lambda ov: ov.flag_name)

    def overrides_for_flag(self, flag_name: str) -> list[FlagOverride]:
        """Return all overrides for *flag_name*, sorted by doc_id."""
        with self._lock:
            result = [
                ov for k, ov in self._overrides.items() if k[1] == flag_name
            ]
        return sorted(result, key=lambda ov: ov.doc_id)

    def docs_with_flag_enabled(self, flag_name: str) -> list[str]:
        """Return doc_ids that have an override with ``enabled=True`` for *flag_name*.

        Only scans existing overrides — does not enumerate all documents.
        """
        with self._lock:
            result = [
                ov.doc_id
                for k, ov in self._overrides.items()
                if k[1] == flag_name and ov.enabled
            ]
        return sorted(result)

    # ------------------------------------------------------------------
    # Statistics
    # ------------------------------------------------------------------

    def stats(self) -> FlagStats:
        """Return aggregate statistics about this store."""
        with self._lock:
            total_flags = len(self._flags)
            enabled_flags = sum(1 for f in self._flags.values() if f.enabled)
            total_overrides = len(self._overrides)
            docs_with_overrides = len({k[0] for k in self._overrides})
        return FlagStats(
            total_flags=total_flags,
            enabled_flags=enabled_flags,
            total_overrides=total_overrides,
            docs_with_overrides=docs_with_overrides,
        )
