"""E317 DocTranslationStore — core storage for per-field document translations.

Provides:
- Translation    : a translated version of one document field
- TranslationStats : aggregate statistics across the store
- DocTranslationStore : thread-safe registry keyed by (doc_id, locale, field)
"""
from __future__ import annotations

import threading
from dataclasses import dataclass, field
from typing import Optional


@dataclass
class Translation:
    """A translated version of a single document field."""

    doc_id: str
    locale: str
    field: str
    value: str
    translated_at: float = 0.0
    translator: str = ""


@dataclass
class TranslationStats:
    """Aggregate statistics across all translations in the store."""

    total_translations: int
    unique_docs: int
    unique_locales: int
    unique_fields: int


class DocTranslationStore:
    """Thread-safe store for document field translations keyed by locale.

    Internal key: (doc_id, locale, field) → Translation

    Thread safety is provided by a single ``threading.Lock`` held for all
    mutation and read operations.
    """

    def __init__(self) -> None:
        self._store: dict[tuple, Translation] = {}
        self._lock = threading.Lock()

    # ------------------------------------------------------------------
    # Mutation
    # ------------------------------------------------------------------

    def set(
        self,
        doc_id: str,
        locale: str,
        field: str,
        value: str,
        translator: str = "",
        now: Optional[float] = None,
    ) -> Translation:
        """Create or replace a translation entry.

        Parameters
        ----------
        doc_id:
            Identifier of the source document.
        locale:
            Locale code, e.g. ``"en"``, ``"ru"``, ``"de"``.
        field:
            Field name, e.g. ``"title"``, ``"body"``, ``"summary"``.
        value:
            Translated text.
        translator:
            Who or what provided the translation (optional).
        now:
            Timestamp to record as ``translated_at``; uses
            ``time.time()`` when *None*.

        Returns
        -------
        Translation
            The newly stored :class:`Translation` object.
        """
        import time

        ts = now if now is not None else time.time()
        translation = Translation(
            doc_id=doc_id,
            locale=locale,
            field=field,
            value=value,
            translated_at=ts,
            translator=translator,
        )
        key = (doc_id, locale, field)
        with self._lock:
            self._store[key] = translation
        return translation

    def delete(self, doc_id: str, locale: str, field: str) -> bool:
        """Remove a single translation entry.

        Returns
        -------
        bool
            ``True`` if the entry existed and was removed, ``False`` if
            it was not present.
        """
        key = (doc_id, locale, field)
        with self._lock:
            if key in self._store:
                del self._store[key]
                return True
            return False

    def delete_doc(self, doc_id: str) -> int:
        """Remove all translations for *doc_id*.

        Returns
        -------
        int
            Number of entries removed.
        """
        with self._lock:
            keys = [k for k in self._store if k[0] == doc_id]
            for k in keys:
                del self._store[k]
            return len(keys)

    def delete_locale(self, locale: str) -> int:
        """Remove all translations for *locale* across every document.

        Returns
        -------
        int
            Number of entries removed.
        """
        with self._lock:
            keys = [k for k in self._store if k[1] == locale]
            for k in keys:
                del self._store[k]
            return len(keys)

    # ------------------------------------------------------------------
    # Lookups
    # ------------------------------------------------------------------

    def get(self, doc_id: str, locale: str, field: str) -> Optional[Translation]:
        """Return the :class:`Translation` for the given key, or ``None``."""
        key = (doc_id, locale, field)
        with self._lock:
            return self._store.get(key)

    def get_field(
        self,
        doc_id: str,
        field: str,
        locale: str,
        fallback_locale: Optional[str] = None,
    ) -> Optional[str]:
        """Return the translated value for *locale*.

        If the requested locale is not found and *fallback_locale* is
        provided, the fallback locale is tried next.  Returns ``None``
        when neither is available.
        """
        with self._lock:
            tr = self._store.get((doc_id, locale, field))
            if tr is not None:
                return tr.value
            if fallback_locale is not None:
                tr = self._store.get((doc_id, fallback_locale, field))
                if tr is not None:
                    return tr.value
            return None

    # ------------------------------------------------------------------
    # Iteration helpers
    # ------------------------------------------------------------------

    def translations_for_doc(self, doc_id: str) -> list[Translation]:
        """Return all translations for *doc_id*, sorted by (locale, field)."""
        with self._lock:
            entries = [t for k, t in self._store.items() if k[0] == doc_id]
        entries.sort(key=lambda t: (t.locale, t.field))
        return entries

    def translations_for_locale(self, locale: str) -> list[Translation]:
        """Return all translations for *locale*, sorted by (doc_id, field)."""
        with self._lock:
            entries = [t for k, t in self._store.items() if k[1] == locale]
        entries.sort(key=lambda t: (t.doc_id, t.field))
        return entries

    def locales_for_doc(self, doc_id: str) -> list[str]:
        """Return sorted unique locale codes that exist for *doc_id*."""
        with self._lock:
            locales = {k[1] for k in self._store if k[0] == doc_id}
        return sorted(locales)

    def fields_for_doc(self, doc_id: str, locale: str) -> list[str]:
        """Return sorted field names available for the given *doc_id* + *locale*."""
        with self._lock:
            fields = {k[2] for k in self._store if k[0] == doc_id and k[1] == locale}
        return sorted(fields)

    # ------------------------------------------------------------------
    # Global aggregates
    # ------------------------------------------------------------------

    def all_locales(self) -> list[str]:
        """Return sorted unique locale codes present in the store."""
        with self._lock:
            locales = {k[1] for k in self._store}
        return sorted(locales)

    def all_doc_ids(self) -> list[str]:
        """Return sorted unique doc IDs that have at least one translation."""
        with self._lock:
            doc_ids = {k[0] for k in self._store}
        return sorted(doc_ids)

    def stats(self) -> TranslationStats:
        """Return :class:`TranslationStats` for the current store state."""
        with self._lock:
            total = len(self._store)
            docs = {k[0] for k in self._store}
            locales = {k[1] for k in self._store}
            fields = {k[2] for k in self._store}
        return TranslationStats(
            total_translations=total,
            unique_docs=len(docs),
            unique_locales=len(locales),
            unique_fields=len(fields),
        )
