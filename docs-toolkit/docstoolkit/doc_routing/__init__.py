"""Document routing: route docs to handlers based on metadata or content.

See ``routing`` module for the implementation.
"""

from __future__ import annotations

from .routing import (
    DocRouting,
    RouteMatch,
    RouteRule,
    RouterStats,
)

__all__ = [
    "DocRouting",
    "RouteMatch",
    "RouteRule",
    "RouterStats",
]
