"""DocLocaleDictionary — locale-specific translation dictionary.

Stores ``(locale, key) -> value`` translations and supports fallback chains:
when an exact translation is not available, :meth:`DocLocaleDictionary.lookup`
walks the configured fallback chain (a list of locales in priority order) to
find the first matching translation.

The module is pure stdlib and thread-safe via a single ``threading.Lock``.
"""

from __future__ import annotations

import threading
import time
from dataclasses import dataclass, field
from typing import Optional


@dataclass
class Translation:
    """A single translation entry."""

    key: str
    locale: str
    value: str
    updated_at: float = 0.0


@dataclass
class DictionaryStats:
    """Aggregate counters reported by :meth:`DocLocaleDictionary.stats`."""

    total_translations: int
    unique_keys: int
    unique_locales: int
    coverage_by_locale: dict = field(default_factory=dict)


class DocLocaleDictionary:
    """Maintain a registry of locale translations with fallback chain support.

    Translations are stored under composite ``(locale, key)`` keys.  Two
    secondary indices (``_by_locale``, ``_by_key``) keep look-ups by either
    dimension cheap.  A configurable ``_fallback_chain`` lets
    :meth:`lookup` resolve missing translations against alternative locales.
    """

    def __init__(self) -> None:
        self._lock = threading.Lock()
        self._translations: dict[tuple, Translation] = {}
        self._by_locale: dict[str, set[str]] = {}
        self._by_key: dict[str, set[str]] = {}
        self._fallback_chain: list[str] = []

    # ------------------------------------------------------------ registration

    def set_translation(
        self,
        locale: str,
        key: str,
        value: str,
        now: Optional[float] = None,
    ) -> Translation:
        """Insert or overwrite a translation for ``(locale, key)``."""
        ts = now if now is not None else time.time()
        entry = Translation(key=key, locale=locale, value=value, updated_at=ts)
        with self._lock:
            self._translations[(locale, key)] = entry
            self._by_locale.setdefault(locale, set()).add(key)
            self._by_key.setdefault(key, set()).add(locale)
        return entry

    def delete(self, locale: str, key: str) -> bool:
        """Remove ``(locale, key)``.  Returns ``True`` if it existed."""
        with self._lock:
            if (locale, key) not in self._translations:
                return False
            del self._translations[(locale, key)]
            keys = self._by_locale.get(locale)
            if keys is not None:
                keys.discard(key)
                if not keys:
                    del self._by_locale[locale]
            locales = self._by_key.get(key)
            if locales is not None:
                locales.discard(locale)
                if not locales:
                    del self._by_key[key]
            return True

    # ------------------------------------------------------------------ lookup

    def get_translation(self, locale: str, key: str) -> Optional[str]:
        """Return the value for exact ``(locale, key)`` or ``None``."""
        with self._lock:
            entry = self._translations.get((locale, key))
            return entry.value if entry is not None else None

    def lookup(self, locale: str, key: str) -> Optional[str]:
        """Return the best available translation.

        Tries the exact ``(locale, key)`` first.  On a miss, walks the
        configured fallback chain (skipping ``locale`` itself) and returns
        the first match.  Returns ``None`` if nothing matches.
        """
        with self._lock:
            entry = self._translations.get((locale, key))
            if entry is not None:
                return entry.value
            for fallback in self._fallback_chain:
                if fallback == locale:
                    continue
                alt = self._translations.get((fallback, key))
                if alt is not None:
                    return alt.value
            return None

    # ---------------------------------------------------------- fallback chain

    def set_fallback_chain(self, locales: list[str]) -> None:
        """Replace the fallback chain with a copy of ``locales``."""
        with self._lock:
            self._fallback_chain = list(locales)

    def get_fallback_chain(self) -> list[str]:
        """Return a copy of the current fallback chain."""
        with self._lock:
            return list(self._fallback_chain)

    # --------------------------------------------------------------- inventory

    def keys_for_locale(self, locale: str) -> list[str]:
        """Return all keys defined for ``locale`` (sorted)."""
        with self._lock:
            return sorted(self._by_locale.get(locale, set()))

    def locales_for_key(self, key: str) -> list[str]:
        """Return all locales that translate ``key`` (sorted)."""
        with self._lock:
            return sorted(self._by_key.get(key, set()))

    def missing_translations(
        self, locale: str, reference_locale: str
    ) -> list[str]:
        """Return keys present in ``reference_locale`` but missing in ``locale``."""
        with self._lock:
            ref = self._by_locale.get(reference_locale, set())
            present = self._by_locale.get(locale, set())
            return sorted(ref - present)

    def all_keys(self) -> list[str]:
        """Return the sorted union of all known keys."""
        with self._lock:
            return sorted(self._by_key.keys())

    def all_locales(self) -> list[str]:
        """Return the sorted list of locales with at least one translation."""
        with self._lock:
            return sorted(self._by_locale.keys())

    # ---------------------------------------------------------------- cleanup

    def clear_locale(self, locale: str) -> int:
        """Drop all translations for ``locale``.  Returns the count cleared."""
        with self._lock:
            keys = self._by_locale.pop(locale, set())
            for key in keys:
                self._translations.pop((locale, key), None)
                locales = self._by_key.get(key)
                if locales is not None:
                    locales.discard(locale)
                    if not locales:
                        del self._by_key[key]
            return len(keys)

    def clear_key(self, key: str) -> int:
        """Drop all translations of ``key`` across every locale."""
        with self._lock:
            locales = self._by_key.pop(key, set())
            for locale in locales:
                self._translations.pop((locale, key), None)
                keys = self._by_locale.get(locale)
                if keys is not None:
                    keys.discard(key)
                    if not keys:
                        del self._by_locale[locale]
            return len(locales)

    # ------------------------------------------------------------------ stats

    def stats(self) -> DictionaryStats:
        """Snapshot of registry size and per-locale coverage."""
        with self._lock:
            coverage = {
                locale: len(keys) for locale, keys in self._by_locale.items()
            }
            return DictionaryStats(
                total_translations=len(self._translations),
                unique_keys=len(self._by_key),
                unique_locales=len(self._by_locale),
                coverage_by_locale=coverage,
            )
