"""Quota Tracker module (E158).

Tracks consumption against quotas (per-key, per-period) with reset windows.

Usage:
    from docstoolkit.quota_tracker import QuotaTracker, QuotaPeriod

    qt = QuotaTracker()
    qt.set_limit("user:alice", QuotaPeriod.MINUTE, 100)

    if qt.consume("user:alice", units=1, now=100.0):
        ...  # within quota
"""
from docstoolkit.quota_tracker.tracker import (
    QuotaError,
    QuotaLimit,
    QuotaPeriod,
    QuotaStatus,
    QuotaTracker,
)

__all__ = [
    "QuotaError",
    "QuotaLimit",
    "QuotaPeriod",
    "QuotaStatus",
    "QuotaTracker",
]
