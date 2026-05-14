"""Document Localization module (E238).

UI string translation registry with pluralization, interpolation, and fallback chains.

Unlike doc_locale (E220) which is for whole-doc translations, this module is for
short UI strings with placeholder interpolation and plural-form selection.

Usage:
    from docstoolkit.doc_localization import DocLocalization, Translation, Plural, LocalizationStats

    dl = DocLocalization(default_locale="en")
    dl.register_key("greeting", default_text="Hello")
    dl.add_translation("greeting", "ru", "Привет")
    dl.add_translation("greeting", "es", "Hola")

    text = dl.translate("greeting", "ru")  # "Привет"
    text = dl.translate("welcome", "en", name="Alice")  # interpolation
    text = dl.translate_plural("items", count=5, "en")
"""
from docstoolkit.doc_localization.localization import (
    DocLocalization,
    LocalizationStats,
    Plural,
    Translation,
)

__all__ = [
    "DocLocalization",
    "LocalizationStats",
    "Plural",
    "Translation",
]
