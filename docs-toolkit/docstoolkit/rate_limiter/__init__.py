"""Rate limiter: token bucket and sliding window algorithms.

E52 additions: RateLimitStrategy, RateLimitConfig, RateLimitResult (new shape),
TokenBucket (bucket.py), FixedWindowCounter, SlidingWindowCounter,
RateLimiter (registry.py).

Legacy exports kept for backwards-compatibility:
TokenBucket (algorithms), SlidingWindow, RateLimiter (limiter), LimitConfig,
RateLimitStore.
"""
# ---- E52 new types -------------------------------------------------------- #
from docstoolkit.rate_limiter.limiter import (
    RateLimitStrategy,
    RateLimitConfig,
    RateLimitResult,
    # legacy aliases
    LimitConfig,
    RateLimiter as _LegacyRateLimiter,
    _LegacyRateLimitResult,
)
from docstoolkit.rate_limiter.bucket import (
    TokenBucket,
    FixedWindowCounter,
    SlidingWindowCounter,
)
from docstoolkit.rate_limiter.registry import RateLimiter

# ---- Legacy (algorithms + store) ------------------------------------------ #
from docstoolkit.rate_limiter.algorithms import SlidingWindow
from docstoolkit.rate_limiter.algorithms import TokenBucket as _AlgoTokenBucket
from docstoolkit.rate_limiter.store import RateLimitStore

__all__ = [
    # E52
    "RateLimitStrategy",
    "RateLimitConfig",
    "RateLimitResult",
    "TokenBucket",
    "FixedWindowCounter",
    "SlidingWindowCounter",
    "RateLimiter",
    # legacy
    "LimitConfig",
    "_LegacyRateLimiter",
    "_LegacyRateLimitResult",
    "SlidingWindow",
    "RateLimitStore",
]
