"""doc_metrics — collect and report document-level engagement metrics.

Public surface
--------------
EventType            — VIEW / EDIT / COMMENT / SHARE / EXPORT / DOWNLOAD / REACTION
DocEvent             — single recorded event for a document
DocMetricsSnapshot   — immutable counts/uniques for a single doc
EngagementScore      — weighted engagement score for a single doc
DocMetrics           — store and query engine for document events
"""
from __future__ import annotations

from docstoolkit.doc_metrics.metrics import (
    DocEvent,
    DocMetrics,
    DocMetricsSnapshot,
    EngagementScore,
    EventType,
)

__all__ = [
    "EventType",
    "DocEvent",
    "DocMetricsSnapshot",
    "EngagementScore",
    "DocMetrics",
]
