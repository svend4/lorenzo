"""E317 DocTranslationStore — manage document translations by locale.

Public API
----------
:class:`Translation`       — a translated version of a document field
:class:`TranslationStats`  — aggregate statistics
:class:`DocTranslationStore` — main interface for translation management
"""

from .store import Translation, TranslationStats, DocTranslationStore

__all__ = ["Translation", "TranslationStats", "DocTranslationStore"]
