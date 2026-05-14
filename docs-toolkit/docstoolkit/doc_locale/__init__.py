"""Document Locale module (E220).

Locale-aware document operations: locale detection, translation registry,
canonical translation tracking, and best-locale selection.

Usage:
    from docstoolkit.doc_locale import DocLocale, DocTranslation, LocaleCode, LocaleStats

    dl = DocLocale()
    dl.register_doc("doc1", canonical_locale=LocaleCode.EN)
    dl.add_translation("doc1", LocaleCode.EN, "Hello world", is_canonical=True)
    dl.add_translation("doc1", LocaleCode.RU, "Привет мир")

    translation = dl.get_translation("doc1", LocaleCode.RU)
    locale = dl.detect_locale("Привет мир")
"""
from docstoolkit.doc_locale.locale import (
    DocLocale,
    DocTranslation,
    LocaleCode,
    LocaleStats,
)

__all__ = [
    "DocLocale",
    "DocTranslation",
    "LocaleCode",
    "LocaleStats",
]
