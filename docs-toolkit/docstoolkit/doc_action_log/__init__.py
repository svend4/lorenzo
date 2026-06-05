"""E398 DocActionLog — append-only structured action log.

Public API
----------
:class:`ActionEvent`     — a single action event
:class:`ActionStats`     — aggregate statistics
:class:`DocActionLog`    — main interface for action logging
"""

from .log import ActionEvent, ActionStats, DocActionLog

__all__ = ["ActionEvent", "ActionStats", "DocActionLog"]
