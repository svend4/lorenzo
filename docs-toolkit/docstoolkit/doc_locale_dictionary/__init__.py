"""E410 DocLocaleDictionary — locale-specific translation dictionary.

Public API
----------
:class:`Translation`       — a single locale translation
:class:`DictionaryStats`   — aggregate statistics
:class:`DocLocaleDictionary` — main interface for locale dictionary
"""

from .dictionary import Translation, DictionaryStats, DocLocaleDictionary

__all__ = ["Translation", "DictionaryStats", "DocLocaleDictionary"]
