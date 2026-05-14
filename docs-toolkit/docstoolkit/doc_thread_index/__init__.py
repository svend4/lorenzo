"""E442 DocThreadIndex — searchable index of comment threads.

Public API
----------
:class:`ThreadRef`       — reference to a comment thread
:class:`ThreadStats`     — aggregate statistics
:class:`DocThreadIndex`  — main interface for thread index
"""

from .index import ThreadRef, ThreadStats, DocThreadIndex

__all__ = ["ThreadRef", "ThreadStats", "DocThreadIndex"]
