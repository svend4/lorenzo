"""Locale-aware document operations.

Provides:
- LocaleCode enum for supported locales
- DocTranslation dataclass for translation records
- LocaleStats dataclass for coverage statistics
- DocLocale class for managing translations, canonical versions,
  locale detection, and best-locale selection
"""
from __future__ import annotations

import re
import threading
from dataclasses import dataclass, field
from enum import Enum
from typing import Optional


class LocaleCode(Enum):
    """Supported locale codes."""

    EN = "en"
    RU = "ru"
    ES = "es"
    FR = "fr"
    DE = "de"
    IT = "it"
    PT = "pt"
    ZH = "zh"
    JA = "ja"
    AR = "ar"
    UNKNOWN = "unknown"


@dataclass
class DocTranslation:
    """A single translation of a document."""

    doc_id: str
    locale: LocaleCode
    content: str
    title: Optional[str] = None
    is_canonical: bool = False


@dataclass
class LocaleStats:
    """Coverage statistics across documents and locales."""

    total_docs: int
    total_translations: int
    by_locale: dict = field(default_factory=dict)
    missing_translations: list = field(default_factory=list)
    _required_locales_count: int = 0

    @property
    def coverage(self) -> float:
        """translations / (docs * required_locales). 0.0 if no docs/locales."""
        if self.total_docs == 0 or self._required_locales_count == 0:
            return 0.0
        denom = self.total_docs * self._required_locales_count
        if denom == 0:
            return 0.0
        return self.total_translations / denom


# Heuristics for locale detection
_CYRILLIC_RE = re.compile(r"[Ѐ-ӿ]")
_CJK_RE = re.compile(r"[一-鿿]")
_HIRAGANA_KATAKANA_RE = re.compile(r"[぀-ヿ]")
_ARABIC_RE = re.compile(r"[؀-ۿ]")
_LATIN_RE = re.compile(r"[A-Za-z]")


def _word_count(text: str, words: list) -> int:
    """Count occurrences of whole words (case-insensitive)."""
    lower = text.lower()
    total = 0
    for w in words:
        total += len(re.findall(r"\b" + re.escape(w) + r"\b", lower))
    return total


class DocLocale:
    """Manage document translations across locales.

    Thread-safe registry that tracks translations per (doc_id, locale),
    canonical versions, and supports locale detection plus best-locale
    selection given Accept-Language style preferences.
    """

    def __init__(self, default_locale: LocaleCode = LocaleCode.EN):
        self._default_locale = default_locale
        # doc_id -> {locale: DocTranslation}
        self._translations: dict = {}
        # doc_id -> canonical LocaleCode (if set)
        self._canonical: dict = {}
        # registered doc ids (may have no translations yet)
        self._docs: set = set()
        self._lock = threading.Lock()

    # ----- registration -----
    def register_doc(
        self,
        doc_id: str,
        canonical_locale: Optional[LocaleCode] = None,
    ) -> bool:
        """Register a doc. Returns False if already registered."""
        with self._lock:
            if doc_id in self._docs:
                return False
            self._docs.add(doc_id)
            self._translations.setdefault(doc_id, {})
            if canonical_locale is not None:
                self._canonical[doc_id] = canonical_locale
            return True

    def add_translation(
        self,
        doc_id: str,
        locale: LocaleCode,
        content: str,
        title: Optional[str] = None,
        is_canonical: bool = False,
    ) -> Optional[DocTranslation]:
        """Add (or replace) a translation. Auto-registers doc if needed."""
        with self._lock:
            if doc_id not in self._docs:
                self._docs.add(doc_id)
                self._translations.setdefault(doc_id, {})
            translation = DocTranslation(
                doc_id=doc_id,
                locale=locale,
                content=content,
                title=title,
                is_canonical=is_canonical,
            )
            self._translations[doc_id][locale] = translation
            if is_canonical:
                # mark canonical and clear previous canonical flags
                self._canonical[doc_id] = locale
                for loc, tr in self._translations[doc_id].items():
                    tr.is_canonical = (loc == locale)
            else:
                # keep canonical flag in sync if doc has one
                canonical_loc = self._canonical.get(doc_id)
                if canonical_loc is not None and locale == canonical_loc:
                    translation.is_canonical = True
            return translation

    def remove_translation(self, doc_id: str, locale: LocaleCode) -> bool:
        """Remove a single translation. Returns True if removed."""
        with self._lock:
            if doc_id not in self._translations:
                return False
            if locale not in self._translations[doc_id]:
                return False
            del self._translations[doc_id][locale]
            if self._canonical.get(doc_id) == locale:
                del self._canonical[doc_id]
            return True

    # ----- lookups -----
    def get_translation(
        self,
        doc_id: str,
        locale: LocaleCode,
        fallback: bool = True,
    ) -> Optional[DocTranslation]:
        """Get translation; if missing and fallback=True, return canonical or
        default locale translation if available."""
        with self._lock:
            doc_map = self._translations.get(doc_id)
            if doc_map is None:
                return None
            if locale in doc_map:
                return doc_map[locale]
            if not fallback:
                return None
            # Fallback: canonical → default → any
            canonical_loc = self._canonical.get(doc_id)
            if canonical_loc is not None and canonical_loc in doc_map:
                return doc_map[canonical_loc]
            if self._default_locale in doc_map:
                return doc_map[self._default_locale]
            return None

    def canonical(self, doc_id: str) -> Optional[DocTranslation]:
        """Return canonical translation for a doc, or None."""
        with self._lock:
            canonical_loc = self._canonical.get(doc_id)
            if canonical_loc is None:
                return None
            doc_map = self._translations.get(doc_id, {})
            return doc_map.get(canonical_loc)

    def available_locales(self, doc_id: str) -> list:
        """Return locales available for a doc."""
        with self._lock:
            doc_map = self._translations.get(doc_id, {})
            return list(doc_map.keys())

    def translated_docs(self, locale: LocaleCode) -> list:
        """Return list of doc_ids that have a translation in `locale`."""
        with self._lock:
            return [
                doc_id
                for doc_id, doc_map in self._translations.items()
                if locale in doc_map
            ]

    def missing(
        self,
        doc_id: str,
        required_locales: Optional[list] = None,
    ) -> list:
        """Return locales missing for a doc (vs required_locales)."""
        if required_locales is None:
            required_locales = [self._default_locale]
        with self._lock:
            doc_map = self._translations.get(doc_id, {})
            return [loc for loc in required_locales if loc not in doc_map]

    # ----- detection -----
    def detect_locale(self, text: str) -> LocaleCode:
        """Heuristic locale detection by character ranges and word frequency."""
        if not text:
            return LocaleCode.UNKNOWN

        cyrillic = len(_CYRILLIC_RE.findall(text))
        cjk = len(_CJK_RE.findall(text))
        kana = len(_HIRAGANA_KATAKANA_RE.findall(text))
        arabic = len(_ARABIC_RE.findall(text))
        latin = len(_LATIN_RE.findall(text))

        total_script = cyrillic + cjk + kana + arabic + latin
        if total_script == 0:
            return LocaleCode.UNKNOWN

        # Cyrillic dominant → RU
        if cyrillic > 0 and cyrillic >= max(cjk, kana, arabic, latin):
            return LocaleCode.RU

        # Japanese: presence of hiragana/katakana is the marker
        if kana > 0:
            return LocaleCode.JA

        # Chinese: CJK without kana
        if cjk > 0:
            return LocaleCode.ZH

        # Arabic
        if arabic > 0 and arabic >= latin:
            return LocaleCode.AR

        # Latin-based detection by frequent function words
        if latin > 0:
            en_count = _word_count(text, ["the", "and", "is", "of", "to"])
            es_count = _word_count(text, ["el", "la", "y", "de", "que"])
            fr_count = _word_count(text, ["le", "la", "et", "de", "les"])
            de_count = _word_count(text, ["der", "die", "und", "das", "ist"])
            it_count = _word_count(text, ["il", "la", "e", "che", "di"])
            pt_count = _word_count(text, ["o", "a", "e", "que", "de"])

            scores = {
                LocaleCode.EN: en_count,
                LocaleCode.ES: es_count,
                LocaleCode.FR: fr_count,
                LocaleCode.DE: de_count,
                LocaleCode.IT: it_count,
                LocaleCode.PT: pt_count,
            }
            best = max(scores.items(), key=lambda kv: kv[1])
            if best[1] > 0:
                return best[0]
            # Latin chars but no recognizable function words
            return LocaleCode.UNKNOWN

        return LocaleCode.UNKNOWN

    # ----- selection -----
    def select_best_locale(
        self,
        doc_id: str,
        accept_languages: list,
        default: Optional[LocaleCode] = None,
    ) -> Optional[LocaleCode]:
        """Return best available locale for a doc given preference order."""
        with self._lock:
            doc_map = self._translations.get(doc_id, {})
            for loc in accept_languages:
                if loc in doc_map:
                    return loc
            if default is not None and default in doc_map:
                return default
            if self._default_locale in doc_map:
                return self._default_locale
            canonical_loc = self._canonical.get(doc_id)
            if canonical_loc is not None and canonical_loc in doc_map:
                return canonical_loc
            return None

    def set_canonical(self, doc_id: str, locale: LocaleCode) -> bool:
        """Set the canonical locale for a doc. Returns False if translation
        does not exist."""
        with self._lock:
            doc_map = self._translations.get(doc_id)
            if doc_map is None or locale not in doc_map:
                return False
            self._canonical[doc_id] = locale
            for loc, tr in doc_map.items():
                tr.is_canonical = (loc == locale)
            return True

    # ----- aggregates -----
    def all_locales_used(self) -> set:
        """Return the set of locales that appear in at least one translation."""
        with self._lock:
            used: set = set()
            for doc_map in self._translations.values():
                used.update(doc_map.keys())
            return used

    def docs_count(self, locale: Optional[LocaleCode] = None) -> int:
        """Count docs (optionally only those with a translation in `locale`)."""
        with self._lock:
            if locale is None:
                return len(self._docs)
            return sum(
                1
                for doc_map in self._translations.values()
                if locale in doc_map
            )

    def stats(
        self,
        required_locales: Optional[list] = None,
    ) -> LocaleStats:
        """Compute coverage stats."""
        if required_locales is None:
            required_locales = list(self.all_locales_used())
            if not required_locales:
                required_locales = [self._default_locale]
        with self._lock:
            total_docs = len(self._docs)
            total_translations = sum(
                len(doc_map) for doc_map in self._translations.values()
            )
            by_locale: dict = {}
            for doc_map in self._translations.values():
                for loc in doc_map:
                    by_locale[loc.value] = by_locale.get(loc.value, 0) + 1
            missing: list = []
            for doc_id in self._docs:
                doc_map = self._translations.get(doc_id, {})
                for loc in required_locales:
                    if loc not in doc_map:
                        missing.append((doc_id, loc.value))
            return LocaleStats(
                total_docs=total_docs,
                total_translations=total_translations,
                by_locale=by_locale,
                missing_translations=missing,
                _required_locales_count=len(required_locales),
            )

    def clear(self) -> None:
        """Remove all docs, translations, and canonical info."""
        with self._lock:
            self._translations.clear()
            self._canonical.clear()
            self._docs.clear()

    # ----- properties -----
    @property
    def total_docs(self) -> int:
        with self._lock:
            return len(self._docs)

    @property
    def total_translations(self) -> int:
        with self._lock:
            return sum(len(doc_map) for doc_map in self._translations.values())
