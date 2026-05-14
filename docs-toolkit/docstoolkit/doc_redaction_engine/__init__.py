"""E327 DocRedactionEngine — pattern-based content redaction for documents.

Public API
----------
:class:`RedactionRule`     — a single redaction rule
:class:`RedactionResult`   — the result of applying redactions
:class:`RedactionStats`    — aggregate statistics
:class:`DocRedactionEngine` — main interface for content redaction
"""

from .engine import RedactionRule, RedactionResult, RedactionStats, DocRedactionEngine

__all__ = ["RedactionRule", "RedactionResult", "RedactionStats", "DocRedactionEngine"]
