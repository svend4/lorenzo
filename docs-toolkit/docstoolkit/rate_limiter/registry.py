"""Per-key rate-limiter registry (E52)."""
import threading
from docstoolkit.rate_limiter.limiter import RateLimitConfig, RateLimitResult, RateLimitStrategy
from docstoolkit.rate_limiter.bucket import TokenBucket, FixedWindowCounter, SlidingWindowCounter


class RateLimiter:
    """Per-key rate limiter that creates and manages a bucket/counter per key.

    Strategy selection is driven by :class:`RateLimitConfig`:

    - ``TOKEN_BUCKET``    → :class:`TokenBucket`
    - ``FIXED_WINDOW``    → :class:`FixedWindowCounter`
    - ``SLIDING_WINDOW``  → :class:`SlidingWindowCounter`
    """

    def __init__(self, config: RateLimitConfig = None) -> None:
        self._config = config or RateLimitConfig()
        self._buckets: dict = {}          # key → bucket/counter
        self._lock = threading.Lock()     # protects _buckets dict

    # ---------------------------------------------------------------------- #
    # Internal helpers                                                         #
    # ---------------------------------------------------------------------- #

    def _make_bucket(self):
        """Instantiate a fresh bucket/counter for a new key."""
        cfg = self._config
        strategy = cfg.strategy
        if strategy is RateLimitStrategy.TOKEN_BUCKET:
            capacity = cfg.burst_size
            refill_rate = cfg.requests_per_second
            return TokenBucket(capacity=capacity, refill_rate=refill_rate)
        elif strategy is RateLimitStrategy.FIXED_WINDOW:
            limit = int(cfg.requests_per_second * cfg.window_seconds)
            return FixedWindowCounter(limit=limit, window_seconds=cfg.window_seconds)
        else:  # SLIDING_WINDOW (default)
            limit = int(cfg.requests_per_second * cfg.window_seconds)
            return SlidingWindowCounter(limit=limit, window_seconds=cfg.window_seconds)

    def _get_bucket(self, key: str):
        """Return existing bucket for key, creating one if needed."""
        with self._lock:
            if key not in self._buckets:
                self._buckets[key] = self._make_bucket()
            return self._buckets[key]

    # ---------------------------------------------------------------------- #
    # Public API                                                               #
    # ---------------------------------------------------------------------- #

    def check(self, key: str) -> RateLimitResult:
        """Check the rate limit for *key*.

        Creates a bucket/counter the first time a key is seen.
        Returns a :class:`RateLimitResult` with ``allowed``, ``remaining``,
        ``reset_after`` and ``retry_after`` fields populated.
        """
        bucket = self._get_bucket(key)
        strategy = self._config.strategy
        if strategy is RateLimitStrategy.TOKEN_BUCKET:
            return bucket.consume()
        else:
            return bucket.increment()

    def reset(self, key: str) -> None:
        """Reset the bucket/counter for *key* (no-op if key is unknown)."""
        with self._lock:
            bucket = self._buckets.get(key)
        if bucket is not None:
            bucket.reset()

    def reset_all(self) -> None:
        """Reset all buckets/counters."""
        with self._lock:
            buckets = list(self._buckets.values())
        for bucket in buckets:
            bucket.reset()

    def keys(self) -> list:
        """Return a sorted list of all registered keys."""
        with self._lock:
            return sorted(self._buckets.keys())
