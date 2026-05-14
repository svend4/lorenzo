"""E351 DocRedirectStore — document URL redirect manager.

Public API
----------
:class:`Redirect`          — a single redirect rule
:class:`RedirectStats`     — aggregate statistics
:class:`DocRedirectStore`  — main interface for redirect management
"""

from .store import Redirect, RedirectStats, DocRedirectStore

__all__ = ["Redirect", "RedirectStats", "DocRedirectStore"]
