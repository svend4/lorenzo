"""Localization implementation (E238).

Translation registry for short UI strings with pluralization, interpolation,
and locale fallback chains.
"""
from __future__ import annotations

import re
import threading
from dataclasses import dataclass, field
from enum import Enum
from typing import Optional


class Plural(Enum):
    """Plural form categories (CLDR-style)."""

    ZERO = "zero"
    ONE = "one"
    FEW = "few"
    MANY = "many"
    OTHER = "other"


@dataclass
class Translation:
    """A translation of a key into a specific locale.

    Attributes:
        key: Translation key (identifier).
        locale: Locale code (e.g. "en", "ru").
        text: Translated text (may contain {placeholders}).
        plural_forms: Optional map of plural categories to localized strings.
    """

    key: str
    locale: str
    text: str
    plural_forms: dict[Plural, str] = field(default_factory=dict)


@dataclass
class LocalizationStats:
    """Aggregate statistics for the localization registry."""

    total_keys: int
    total_translations: int
    locales: list[str]
    coverage_by_locale: dict[str, float]


_PLACEHOLDER_RE = re.compile(r"\{(\w+)\}")


class DocLocalization:
    """In-memory registry of UI translations with pluralization and fallbacks."""

    def __init__(
        self,
        default_locale: str = "en",
        fallback_locale: Optional[str] = None,
    ) -> None:
        self._default_locale = default_locale
        self._fallback_locale = fallback_locale
        # key -> default_text (may be None)
        self._keys: dict[str, Optional[str]] = {}
        # key -> {locale -> Translation}
        self._translations: dict[str, dict[str, Translation]] = {}
        self._fallback_chain: list[str] = []
        self._lock = threading.Lock()

    # ---- key registration ----

    def register_key(self, key: str, default_text: Optional[str] = None) -> bool:
        """Register a translation key. Returns True if newly added."""
        if not key:
            return False
        with self._lock:
            if key in self._keys:
                # update default_text if newly provided
                if default_text is not None:
                    self._keys[key] = default_text
                return False
            self._keys[key] = default_text
            self._translations.setdefault(key, {})
            return True

    # ---- translation registration ----

    def add_translation(
        self,
        key: str,
        locale: str,
        text: str,
        plural_forms: Optional[dict[Plural, str]] = None,
    ) -> Optional[Translation]:
        """Add or replace a translation for (key, locale).

        Returns the new Translation, or None if invalid input.
        Auto-registers the key if it isn't yet registered.
        """
        if not key or not locale or text is None:
            return None
        with self._lock:
            if key not in self._keys:
                self._keys[key] = None
                self._translations[key] = {}
            translation = Translation(
                key=key,
                locale=locale,
                text=text,
                plural_forms=dict(plural_forms) if plural_forms else {},
            )
            self._translations[key][locale] = translation
            return translation

    # ---- fallback / defaults ----

    def set_fallback_chain(self, chain: list[str]) -> None:
        """Set the ordered fallback locale chain."""
        with self._lock:
            self._fallback_chain = list(chain)

    def set_default_locale(self, locale: str) -> None:
        """Set the default locale used when translate() is called without one."""
        with self._lock:
            self._default_locale = locale

    # ---- internal helpers ----

    def _resolve_text(self, key: str, locale: str) -> tuple[Optional[Translation], Optional[str]]:
        """Find a translation following the fallback chain.

        Returns (translation, source_locale). If no translation exists, returns
        (None, None).
        """
        tried: list[str] = []

        def _try(loc: str) -> Optional[Translation]:
            if loc in tried:
                return None
            tried.append(loc)
            entry = self._translations.get(key)
            if entry is not None:
                return entry.get(loc)
            return None

        # 1. requested locale
        t = _try(locale)
        if t is not None:
            return t, locale

        # 2. explicit fallback chain
        for loc in self._fallback_chain:
            t = _try(loc)
            if t is not None:
                return t, loc

        # 3. fallback_locale (constructor)
        if self._fallback_locale is not None:
            t = _try(self._fallback_locale)
            if t is not None:
                return t, self._fallback_locale

        # 4. default_locale
        t = _try(self._default_locale)
        if t is not None:
            return t, self._default_locale

        return None, None

    @staticmethod
    def _interpolate(text: str, values: dict[str, object]) -> str:
        if not values:
            return text

        def _sub(match: re.Match[str]) -> str:
            name = match.group(1)
            if name in values:
                return str(values[name])
            return match.group(0)

        return _PLACEHOLDER_RE.sub(_sub, text)

    # ---- translation lookup ----

    def translate(
        self,
        key: str,
        locale: Optional[str] = None,
        **interpolation: object,
    ) -> str:
        """Translate a key. Falls back through the chain; returns default_text or key."""
        loc = locale if locale is not None else self._default_locale
        with self._lock:
            translation, _ = self._resolve_text(key, loc)
            default_text = self._keys.get(key)

        if translation is not None:
            return self._interpolate(translation.text, interpolation)
        if default_text is not None:
            return self._interpolate(default_text, interpolation)
        # last resort: return the key itself (still interpolating in case)
        return self._interpolate(key, interpolation)

    @staticmethod
    def _pick_plural(count: int) -> Plural:
        """English-style plural selection."""
        if count == 0:
            return Plural.ZERO
        if count == 1:
            return Plural.ONE
        return Plural.OTHER

    def translate_plural(
        self,
        key: str,
        count: int,
        locale: Optional[str] = None,
        **interpolation: object,
    ) -> str:
        """Translate a key with plural-form selection based on count."""
        loc = locale if locale is not None else self._default_locale
        category = self._pick_plural(count)

        with self._lock:
            translation, _ = self._resolve_text(key, loc)
            default_text = self._keys.get(key)

        # try found translation's plural forms first
        if translation is not None:
            forms = translation.plural_forms
            if forms:
                text = forms.get(category)
                if text is None:
                    text = forms.get(Plural.OTHER)
                if text is not None:
                    values = dict(interpolation)
                    values.setdefault("count", count)
                    return self._interpolate(text, values)
            # no plural forms, use plain text
            values = dict(interpolation)
            values.setdefault("count", count)
            return self._interpolate(translation.text, values)

        if default_text is not None:
            values = dict(interpolation)
            values.setdefault("count", count)
            return self._interpolate(default_text, values)
        values = dict(interpolation)
        values.setdefault("count", count)
        return self._interpolate(key, values)

    # ---- introspection ----

    def get_translation(self, key: str, locale: str) -> Optional[Translation]:
        with self._lock:
            entry = self._translations.get(key)
            if entry is None:
                return None
            return entry.get(locale)

    def available_locales(self, key: Optional[str] = None) -> list[str]:
        """List locales. If key given, only locales translated for that key."""
        with self._lock:
            if key is not None:
                entry = self._translations.get(key)
                if entry is None:
                    return []
                return sorted(entry.keys())
            locales: set[str] = set()
            for entry in self._translations.values():
                locales.update(entry.keys())
            return sorted(locales)

    def missing_keys(self, locale: str) -> list[str]:
        """Return keys with no translation in the given locale."""
        with self._lock:
            missing = []
            for key in self._keys:
                entry = self._translations.get(key, {})
                if locale not in entry:
                    missing.append(key)
            return sorted(missing)

    def coverage(self, locale: str) -> float:
        with self._lock:
            total = len(self._keys)
            if total == 0:
                return 0.0
            translated = sum(
                1 for key in self._keys
                if locale in self._translations.get(key, {})
            )
            return translated / total

    def stats(self) -> LocalizationStats:
        with self._lock:
            total_keys = len(self._keys)
            total_translations = sum(
                len(entry) for entry in self._translations.values()
            )
            locales_set: set[str] = set()
            for entry in self._translations.values():
                locales_set.update(entry.keys())
            locales = sorted(locales_set)
            coverage_by_locale: dict[str, float] = {}
            for loc in locales:
                if total_keys == 0:
                    coverage_by_locale[loc] = 0.0
                else:
                    translated = sum(
                        1 for key in self._keys
                        if loc in self._translations.get(key, {})
                    )
                    coverage_by_locale[loc] = translated / total_keys
            return LocalizationStats(
                total_keys=total_keys,
                total_translations=total_translations,
                locales=locales,
                coverage_by_locale=coverage_by_locale,
            )

    # ---- removal ----

    def remove_key(self, key: str) -> bool:
        with self._lock:
            if key not in self._keys:
                return False
            del self._keys[key]
            self._translations.pop(key, None)
            return True

    def remove_translation(self, key: str, locale: str) -> bool:
        with self._lock:
            entry = self._translations.get(key)
            if entry is None or locale not in entry:
                return False
            del entry[locale]
            return True

    # ---- bulk operations ----

    def bulk_load(self, translations: dict[str, dict[str, str]]) -> int:
        """Load translations from {locale: {key: text}} mapping. Returns count added."""
        count = 0
        with self._lock:
            for locale, kv in translations.items():
                if not locale or not isinstance(kv, dict):
                    continue
                for key, text in kv.items():
                    if not key or text is None:
                        continue
                    if key not in self._keys:
                        self._keys[key] = None
                        self._translations[key] = {}
                    self._translations[key][locale] = Translation(
                        key=key, locale=locale, text=text, plural_forms={}
                    )
                    count += 1
        return count

    # ---- properties ----

    @property
    def total_keys(self) -> int:
        with self._lock:
            return len(self._keys)

    @property
    def total_translations(self) -> int:
        with self._lock:
            return sum(len(entry) for entry in self._translations.values())

    def clear(self) -> None:
        with self._lock:
            self._keys.clear()
            self._translations.clear()
            self._fallback_chain.clear()
