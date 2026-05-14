"""E363 DocLinkValidator — validate hyperlinks in documents.

Public API
----------
:class:`LinkCheck`         — result of a single link validation
:class:`ValidatorStats`    — aggregate statistics
:class:`DocLinkValidator`  — main interface for link validation
"""

from .validator import LinkCheck, ValidatorStats, DocLinkValidator

__all__ = ["LinkCheck", "ValidatorStats", "DocLinkValidator"]
