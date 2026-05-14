"""Combined throttling + quota system per user/per-action with multiple windows."""
from __future__ import annotations

from .throttle_quota import (
    DocThrottleQuota,
    QuotaCheckResult,
    QuotaSpec,
    TimeWindow,
    UsageRecord,
)

__all__ = [
    "DocThrottleQuota",
    "QuotaCheckResult",
    "QuotaSpec",
    "TimeWindow",
    "UsageRecord",
]
