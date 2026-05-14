"""E372 DocUserPreference — preference storage implementation.

A small thread-safe store for per-user preferences with optional defaults.
Pure standard-library; no third-party dependencies.
"""

from __future__ import annotations

import threading
import time
from dataclasses import dataclass, field
from typing import Optional


@dataclass
class Preference:
    """A single user preference value."""

    user_id: str
    key: str
    value: object
    updated_at: float = 0.0


@dataclass
class PreferenceStats:
    """Aggregate statistics for a :class:`DocUserPreference` store."""

    total_preferences: int
    unique_users: int
    unique_keys: int
    default_count: int


class DocUserPreference:
    """Per-user preference storage with defaults.

    Thread-safe via an internal :class:`threading.Lock`.
    """

    def __init__(self) -> None:
        self._prefs: dict[tuple, Preference] = {}
        self._defaults: dict[str, object] = {}
        self._by_user: dict[str, set[str]] = {}
        self._lock = threading.Lock()

    # ------------------------------------------------------------------ #
    # Defaults
    # ------------------------------------------------------------------ #
    def set_default(self, key: str, value) -> None:
        """Set (or replace) the default value for ``key``."""
        with self._lock:
            self._defaults[key] = value

    def get_default(self, key: str) -> object:
        """Return the default value for ``key``, or ``None`` if unset."""
        with self._lock:
            return self._defaults.get(key)

    def defaults(self) -> dict:
        """Return a shallow copy of all defaults."""
        with self._lock:
            return dict(self._defaults)

    def remove_default(self, key: str) -> bool:
        """Remove the default for ``key``. Returns True if it existed."""
        with self._lock:
            if key in self._defaults:
                del self._defaults[key]
                return True
            return False

    # ------------------------------------------------------------------ #
    # Preferences
    # ------------------------------------------------------------------ #
    def set_preference(
        self, user_id: str, key: str, value, now: Optional[float] = None
    ) -> Preference:
        """Set (or replace) the preference ``key`` for ``user_id``."""
        ts = now if now is not None else time.time()
        with self._lock:
            pref = Preference(user_id=user_id, key=key, value=value, updated_at=ts)
            self._prefs[(user_id, key)] = pref
            self._by_user.setdefault(user_id, set()).add(key)
            return pref

    def get_preference(self, user_id: str, key: str) -> object:
        """Return the effective value: user value if set, else default, else None."""
        with self._lock:
            pref = self._prefs.get((user_id, key))
            if pref is not None:
                return pref.value
            return self._defaults.get(key)

    def get_raw(self, user_id: str, key: str) -> Optional[Preference]:
        """Return the raw :class:`Preference` for the user, or ``None``."""
        with self._lock:
            return self._prefs.get((user_id, key))

    def delete_preference(self, user_id: str, key: str) -> bool:
        """Remove the user's preference. Returns True if it existed."""
        with self._lock:
            return self._delete_locked(user_id, key)

    def _delete_locked(self, user_id: str, key: str) -> bool:
        if (user_id, key) in self._prefs:
            del self._prefs[(user_id, key)]
            keys = self._by_user.get(user_id)
            if keys is not None:
                keys.discard(key)
                if not keys:
                    del self._by_user[user_id]
            return True
        return False

    def preferences_for_user(self, user_id: str) -> list[Preference]:
        """Return all preferences for ``user_id``, sorted by key."""
        with self._lock:
            keys = self._by_user.get(user_id, set())
            prefs = [self._prefs[(user_id, k)] for k in keys]
            prefs.sort(key=lambda p: p.key)
            return prefs

    def users_with_preference(self, key: str) -> list[str]:
        """Return sorted list of user_ids who have set ``key``."""
        with self._lock:
            users = [uid for (uid, k) in self._prefs if k == key]
            users.sort()
            return users

    def reset_to_default(self, user_id: str, key: str) -> bool:
        """Delete the user's override for ``key``. Returns True if existed."""
        with self._lock:
            return self._delete_locked(user_id, key)

    def clear_user(self, user_id: str) -> int:
        """Remove all preferences for ``user_id``. Returns count removed."""
        with self._lock:
            keys = list(self._by_user.get(user_id, set()))
            count = 0
            for k in keys:
                if self._delete_locked(user_id, k):
                    count += 1
            return count

    def all_keys(self) -> list[str]:
        """Sorted union of all preference keys and default keys."""
        with self._lock:
            keyset: set[str] = set(self._defaults.keys())
            for (_uid, k) in self._prefs:
                keyset.add(k)
            return sorted(keyset)

    def stats(self) -> PreferenceStats:
        """Return aggregate statistics about the store."""
        with self._lock:
            users = {uid for (uid, _k) in self._prefs}
            keys = {k for (_uid, k) in self._prefs}
            return PreferenceStats(
                total_preferences=len(self._prefs),
                unique_users=len(users),
                unique_keys=len(keys),
                default_count=len(self._defaults),
            )
