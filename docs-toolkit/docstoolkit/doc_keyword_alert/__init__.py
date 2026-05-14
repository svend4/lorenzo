"""E381 DocKeywordAlert — keyword-triggered alerts for document content.

Public API
----------
:class:`KeywordRule`      — a keyword alert rule
:class:`KeywordMatch`     — a single match instance
:class:`AlertStats`       — aggregate statistics
:class:`DocKeywordAlert`  — main interface for keyword alerts
"""

from .alert import KeywordRule, KeywordMatch, AlertStats, DocKeywordAlert

__all__ = ["KeywordRule", "KeywordMatch", "AlertStats", "DocKeywordAlert"]
