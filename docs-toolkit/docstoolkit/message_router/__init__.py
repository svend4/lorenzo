"""Message router: internal pub/sub with priorities and middleware chain.

See ``router`` module for the implementation.
"""

from __future__ import annotations

from .router import (
    HandlerInfo,
    Message,
    MessagePriority,
    MessageRouter,
    RouterStats,
)

__all__ = [
    "HandlerInfo",
    "Message",
    "MessagePriority",
    "MessageRouter",
    "RouterStats",
]
