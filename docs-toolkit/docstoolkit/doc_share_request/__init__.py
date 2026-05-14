"""E406 DocShareRequest — share request workflow.

Public API
----------
:class:`ShareRequest`      — a single share request
:class:`ShareRequestStats` — aggregate statistics
:class:`DocShareRequest`   — main interface for share request management
"""

from .request import ShareRequest, ShareRequestStats, DocShareRequest

__all__ = ["ShareRequest", "ShareRequestStats", "DocShareRequest"]
