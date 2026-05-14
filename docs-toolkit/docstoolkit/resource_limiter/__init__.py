"""Resource limiter: track and enforce per-namespace usage limits (E112).

Provides time-windowed, thread-safe, SQLite-backed tracking and enforcement
of resource consumption (API calls, memory bytes, CPU time, custom units)
per namespace/user.

Example usage::

    from docstoolkit.resource_limiter import ResourceLimiter, ResourceLimit

    limiter = ResourceLimiter()
    limiter.add_limit(ResourceLimit(resource="api_calls", limit=100, window=60.0))

    record = limiter.consume("user_42", "api_calls")
    if record.result == LimitResult.DENIED:
        raise RuntimeError("Rate limit exceeded")
"""
from docstoolkit.resource_limiter.limiter import (
    LimitResult,
    ResourceLimit,
    ResourceLimiter,
    UsageRecord,
)

__all__ = [
    "LimitResult",
    "ResourceLimit",
    "ResourceLimiter",
    "UsageRecord",
]
