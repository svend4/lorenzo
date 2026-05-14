"""Per-document token-bucket throttling with configurable burst/rate.

Использование:
    from docstoolkit.doc_throttler import DocThrottler, ThrottleConfig

    throttler = DocThrottler(ThrottleConfig(burst_capacity=10, refill_rate=1.0))
    result = throttler.acquire("doc-42")
    if result.allowed:
        ...  # proceed
    else:
        ...  # sleep result.retry_after_seconds
"""
from docstoolkit.doc_throttler.throttler import (
    Bucket,
    DocThrottler,
    ThrottleConfig,
    ThrottleResult,
)

__all__ = [
    "Bucket",
    "DocThrottler",
    "ThrottleConfig",
    "ThrottleResult",
]
