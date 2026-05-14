"""Token bucket and window counter primitives (E52)."""
import time
import threading
from collections import deque
from docstoolkit.rate_limiter.limiter import RateLimitResult


class TokenBucket:
    """Thread-safe token-bucket rate limiter.

    capacity    – maximum number of tokens the bucket can hold (also the burst size)
    refill_rate – tokens added per second
    """

    def __init__(self, capacity: int, refill_rate: float) -> None:
        self._capacity = capacity
        self._refill_rate = refill_rate
        self._tokens: float = float(capacity)
        self._last_refill: float = time.monotonic()
        self._lock = threading.Lock()

    # ---------------------------------------------------------------------- #
    # Internal helpers                                                         #
    # ---------------------------------------------------------------------- #

    def _refill(self, now: float) -> None:
        """Add tokens proportional to elapsed time. Must be called under lock."""
        elapsed = now - self._last_refill
        if elapsed > 0:
            added = elapsed * self._refill_rate
            self._tokens = min(float(self._capacity), self._tokens + added)
            self._last_refill = now

    # ---------------------------------------------------------------------- #
    # Public API                                                               #
    # ---------------------------------------------------------------------- #

    def consume(self, tokens: int = 1) -> RateLimitResult:
        """Try to consume *tokens* from the bucket.

        Returns a :class:`RateLimitResult`:
        - ``allowed=True``  when enough tokens are available (tokens deducted)
        - ``allowed=False`` when not enough tokens are available (no change)
        """
        with self._lock:
            now = time.monotonic()
            self._refill(now)
            if self._tokens >= tokens:
                self._tokens -= tokens
                remaining = int(self._tokens)
                return RateLimitResult(
                    allowed=True,
                    remaining=remaining,
                    reset_after=0.0,
                    retry_after=0.0,
                )
            else:
                # How long until *tokens* tokens are available?
                needed = tokens - self._tokens
                if self._refill_rate > 0:
                    wait = needed / self._refill_rate
                else:
                    wait = float("inf")
                return RateLimitResult(
                    allowed=False,
                    remaining=int(self._tokens),
                    reset_after=wait,
                    retry_after=wait,
                )

    def available(self) -> int:
        """Return the number of whole tokens currently available."""
        with self._lock:
            self._refill(time.monotonic())
            return int(self._tokens)

    def reset(self) -> None:
        """Refill the bucket to full capacity."""
        with self._lock:
            self._tokens = float(self._capacity)
            self._last_refill = time.monotonic()


class FixedWindowCounter:
    """Thread-safe fixed-window request counter.

    Counts requests inside the current window and resets when the window
    expires.

    limit          – maximum requests per window
    window_seconds – duration of each fixed window in seconds
    """

    def __init__(self, limit: int, window_seconds: float) -> None:
        self._limit = limit
        self._window_seconds = window_seconds
        self._count: int = 0
        self._window_start: float = time.monotonic()
        self._lock = threading.Lock()

    def _maybe_reset(self, now: float) -> None:
        """Reset counter if the current window has expired. Must be called under lock."""
        if now - self._window_start >= self._window_seconds:
            self._count = 0
            self._window_start = now

    def increment(self) -> RateLimitResult:
        """Record one request and return a :class:`RateLimitResult`.

        Resets the counter automatically when the window has expired.
        """
        with self._lock:
            now = time.monotonic()
            self._maybe_reset(now)
            if self._count < self._limit:
                self._count += 1
                remaining = self._limit - self._count
                time_used = now - self._window_start
                reset_after = max(0.0, self._window_seconds - time_used)
                return RateLimitResult(
                    allowed=True,
                    remaining=remaining,
                    reset_after=reset_after,
                    retry_after=0.0,
                )
            else:
                time_used = now - self._window_start
                reset_after = max(0.0, self._window_seconds - time_used)
                return RateLimitResult(
                    allowed=False,
                    remaining=0,
                    reset_after=reset_after,
                    retry_after=reset_after,
                )

    def reset(self) -> None:
        """Reset the counter and start a new window from now."""
        with self._lock:
            self._count = 0
            self._window_start = time.monotonic()


class SlidingWindowCounter:
    """Thread-safe sliding-window request counter using a timestamp deque.

    limit          – maximum requests in the rolling window
    window_seconds – size of the rolling window in seconds
    """

    def __init__(self, limit: int, window_seconds: float) -> None:
        self._limit = limit
        self._window_seconds = window_seconds
        self._timestamps: deque = deque()
        self._lock = threading.Lock()

    def _evict(self, now: float) -> None:
        """Remove timestamps older than the window. Must be called under lock."""
        cutoff = now - self._window_seconds
        while self._timestamps and self._timestamps[0] <= cutoff:
            self._timestamps.popleft()

    def increment(self) -> RateLimitResult:
        """Record one request and return a :class:`RateLimitResult`."""
        with self._lock:
            now = time.monotonic()
            self._evict(now)
            count = len(self._timestamps)
            if count < self._limit:
                self._timestamps.append(now)
                remaining = self._limit - count - 1
                return RateLimitResult(
                    allowed=True,
                    remaining=remaining,
                    reset_after=0.0,
                    retry_after=0.0,
                )
            else:
                # Oldest timestamp tells us when the window first slot opens
                oldest = self._timestamps[0]
                reset_after = max(0.0, oldest + self._window_seconds - now)
                return RateLimitResult(
                    allowed=False,
                    remaining=0,
                    reset_after=reset_after,
                    retry_after=reset_after,
                )

    def reset(self) -> None:
        """Clear all recorded timestamps."""
        with self._lock:
            self._timestamps.clear()
