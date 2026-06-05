"""E419 DocTagSuggestion — suggest tags based on co-occurrence and popularity.

Public API
----------
:class:`TagSuggestion`    — a suggested tag with confidence
:class:`SuggestionStats`  — aggregate statistics
:class:`DocTagSuggestion` — main interface for tag suggestion
"""

from .suggestion import TagSuggestion, SuggestionStats, DocTagSuggestion

__all__ = ["TagSuggestion", "SuggestionStats", "DocTagSuggestion"]
