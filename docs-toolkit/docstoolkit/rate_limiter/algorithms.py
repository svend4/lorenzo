import time
from dataclasses import dataclass, field


@dataclass
class TokenBucket:
    """Token bucket rate limiter.

    capacity: max tokens in bucket
    refill_rate: tokens added per second
    _tokens: current token count (starts at capacity)
    _last_refill: timestamp of last refill
    """
    capacity: float
    refill_rate: float   # tokens per second
    _tokens: float = None
    _last_refill: float = None

    def __post_init__(self):
        if self._tokens is None:
            self._tokens = self.capacity
        if self._last_refill is None:
            self._last_refill = time.monotonic()

    def _refill(self, now: float) -> None:
        """Add tokens based on elapsed time since last refill."""
        elapsed = now - self._last_refill
        added = elapsed * self.refill_rate
        self._tokens = min(self.capacity, self._tokens + added)
        self._last_refill = now

    def consume(self, tokens: float = 1.0, now: float | None = None) -> bool:
        """Try to consume tokens. Returns True if allowed, False if rate limited.

        Refills first, then checks if enough tokens available.
        If allowed: subtract tokens and return True.
        If not: return False (don't modify token count).
        """
        if now is None:
            now = time.monotonic()
        self._refill(now)
        if self._tokens >= tokens:
            self._tokens -= tokens
            return True
        return False

    def available(self, now: float | None = None) -> float:
        """Return current available tokens after refill."""
        if now is None:
            now = time.monotonic()
        self._refill(now)
        return self._tokens

    def time_until_available(self, tokens: float = 1.0, now: float | None = None) -> float:
        """Seconds until 'tokens' tokens are available. 0.0 if already available."""
        if now is None:
            now = time.monotonic()
        self._refill(now)
        if self._tokens >= tokens:
            return 0.0
        needed = tokens - self._tokens
        return needed / self.refill_rate if self.refill_rate > 0 else float('inf')


@dataclass
class SlidingWindow:
    """Sliding window rate limiter.

    max_requests: max requests in window
    window_seconds: window duration
    _timestamps: list of request timestamps (monotonic)
    """
    max_requests: int
    window_seconds: float
    _timestamps: list = None

    def __post_init__(self):
        if self._timestamps is None:
            self._timestamps = []

    def _prune(self, now: float) -> None:
        """Remove timestamps older than window."""
        cutoff = now - self.window_seconds
        self._timestamps = [t for t in self._timestamps if t > cutoff]

    def allow(self, now: float | None = None) -> bool:
        """Check if request is allowed. If yes, record it.

        Prune old timestamps, then check count < max_requests.
        If allowed: append now to _timestamps, return True.
        Else: return False.
        """
        if now is None:
            now = time.monotonic()
        self._prune(now)
        if len(self._timestamps) < self.max_requests:
            self._timestamps.append(now)
            return True
        return False

    def current_count(self, now: float | None = None) -> int:
        """Return count of requests in current window."""
        if now is None:
            now = time.monotonic()
        self._prune(now)
        return len(self._timestamps)

    def remaining(self, now: float | None = None) -> int:
        """Return remaining allowed requests in window."""
        return max(0, self.max_requests - self.current_count(now))
