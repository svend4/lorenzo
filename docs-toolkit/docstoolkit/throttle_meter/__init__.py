"""Token-bucket-style throttling with burst capacity and refill rate per key.

Использование:
    from docstoolkit.throttle_meter import ThrottleMeter, ThrottleConfig

    tm = ThrottleMeter()
    tm.configure("api:user1", capacity=10, refill_rate=1.0)

    result = tm.acquire("api:user1", tokens=1, now=time.time())
    if result.allowed:
        ...  # proceed
    else:
        time.sleep(result.retry_after_seconds)
"""
from docstoolkit.throttle_meter.meter import (
    Bucket,
    ThrottleConfig,
    ThrottleMeter,
    ThrottleResult,
)

__all__ = [
    "Bucket",
    "ThrottleConfig",
    "ThrottleMeter",
    "ThrottleResult",
]
