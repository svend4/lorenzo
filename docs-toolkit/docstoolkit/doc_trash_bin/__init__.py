"""E417 DocTrashBin — soft-delete trash bin with restore capability.

Public API
----------
:class:`TrashedDoc`     — a single trashed document
:class:`TrashStats`     — aggregate statistics
:class:`DocTrashBin`    — main interface for trash management
"""

from .bin import TrashedDoc, TrashStats, DocTrashBin

__all__ = ["TrashedDoc", "TrashStats", "DocTrashBin"]
