"""E372 DocUserPreference — per-user preference storage with defaults.

Public API
----------
:class:`Preference`       — a single user preference value
:class:`PreferenceStats`  — aggregate statistics
:class:`DocUserPreference` — main interface for preference management
"""

from .preference import Preference, PreferenceStats, DocUserPreference

__all__ = ["Preference", "PreferenceStats", "DocUserPreference"]
