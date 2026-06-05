"""E369 DocClipboardStore — per-user clipboard for document fragments.

Public API
----------
:class:`ClipboardEntry`    — a single clipboard entry
:class:`ClipboardStats`    — aggregate statistics
:class:`DocClipboardStore` — main interface for clipboard management
"""

from .store import ClipboardEntry, ClipboardStats, DocClipboardStore

__all__ = ["ClipboardEntry", "ClipboardStats", "DocClipboardStore"]
