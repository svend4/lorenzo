"""E329 DocOutbox — reliable outbox pattern for outbound document messages.

Public API
----------
:class:`OutboxMessage`   — a single outbound message
:class:`OutboxStats`     — aggregate statistics
:class:`DocOutbox`       — main interface for outbox management
"""

from .outbox import OutboxMessage, OutboxStats, DocOutbox

__all__ = ["OutboxMessage", "OutboxStats", "DocOutbox"]
