import time
from dataclasses import dataclass, field
from docstoolkit.rate_limiter.algorithms import TokenBucket, SlidingWindow


@dataclass
class LimitConfig:
    """Configuration for a rate limit rule."""
    key: str               # e.g. "user:alice" or "api:search"
    max_requests: int      # per window
    window_seconds: float  # window duration
    burst: int = 0         # extra burst capacity (added to max for token bucket)


@dataclass
class RateLimitResult:
    """Result of a rate limit check."""
    allowed: bool
    key: str
    remaining: int         # requests remaining in window
    retry_after: float     # seconds until next allowed request (0 if allowed)

    def __bool__(self) -> bool:
        return self.allowed


class RateLimiter:
    """In-memory rate limiter using sliding window per key."""

    def __init__(self):
        self._windows: dict = {}   # {key: SlidingWindow}

    def _get_window(self, config: LimitConfig) -> SlidingWindow:
        if config.key not in self._windows:
            self._windows[config.key] = SlidingWindow(
                max_requests=config.max_requests,
                window_seconds=config.window_seconds,
            )
        return self._windows[config.key]

    def check(self, config: LimitConfig) -> RateLimitResult:
        """Check rate limit for key. Records the request if allowed.

        remaining = window.remaining() after potential allow
        retry_after = 0 if allowed, else window_seconds / max_requests
        """
        now = time.monotonic()
        window = self._get_window(config)
        allowed = window.allow(now=now)
        remaining = window.remaining(now=now)
        if allowed:
            retry_after = 0.0
        else:
            retry_after = (
                config.window_seconds / config.max_requests
                if config.max_requests > 0
                else 0.0
            )
        return RateLimitResult(
            allowed=allowed,
            key=config.key,
            remaining=remaining,
            retry_after=retry_after,
        )

    def reset(self, key: str) -> None:
        """Clear rate limit state for a key."""
        self._windows.pop(key, None)

    def stats(self) -> dict:
        """Return {key: current_count} for all tracked keys."""
        now = time.monotonic()
        return {key: w.current_count(now=now) for key, w in self._windows.items()}
