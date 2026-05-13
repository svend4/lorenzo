"""Rate limiter config and result types (E52)."""
import time
from dataclasses import dataclass, field
from enum import Enum

# --------------------------------------------------------------------------- #
#  New E52 types                                                                #
# --------------------------------------------------------------------------- #

class RateLimitStrategy(Enum):
    FIXED_WINDOW = "fixed_window"
    SLIDING_WINDOW = "sliding_window"
    TOKEN_BUCKET = "token_bucket"


@dataclass
class RateLimitConfig:
    """Configuration for the RateLimiter registry."""
    strategy: RateLimitStrategy = RateLimitStrategy.SLIDING_WINDOW
    requests_per_second: float = 10.0
    burst_size: int = 20
    window_seconds: float = 1.0


@dataclass
class RateLimitResult:
    """Result of a rate-limit check (E52 shape).

    allowed       – True if the request is permitted
    remaining     – slots / tokens left in the current window
    reset_after   – seconds until the next slot opens (0.0 if allowed)
    retry_after   – same semantics: 0.0 if allowed, >0 if denied
    """
    allowed: bool
    remaining: int
    reset_after: float
    retry_after: float

    def __bool__(self) -> bool:  # pragma: no cover
        return self.allowed


# --------------------------------------------------------------------------- #
#  Legacy types kept for backwards-compatibility                                #
# --------------------------------------------------------------------------- #

@dataclass
class LimitConfig:
    """Configuration for a rate limit rule (legacy)."""
    key: str
    max_requests: int
    window_seconds: float
    burst: int = 0


@dataclass
class _LegacyRateLimitResult:
    """Result of a rate limit check (legacy shape with key field)."""
    allowed: bool
    key: str
    remaining: int
    retry_after: float

    def __bool__(self) -> bool:
        return self.allowed


class RateLimiter:
    """In-memory rate limiter using sliding window per key (legacy)."""

    def __init__(self):
        # import here to avoid circular import at module level
        from docstoolkit.rate_limiter.algorithms import SlidingWindow
        self._SlidingWindow = SlidingWindow
        self._windows: dict = {}

    def _get_window(self, config: LimitConfig):
        if config.key not in self._windows:
            self._windows[config.key] = self._SlidingWindow(
                max_requests=config.max_requests,
                window_seconds=config.window_seconds,
            )
        return self._windows[config.key]

    def check(self, config: LimitConfig) -> _LegacyRateLimitResult:
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
        return _LegacyRateLimitResult(
            allowed=allowed,
            key=config.key,
            remaining=remaining,
            retry_after=retry_after,
        )

    def reset(self, key: str) -> None:
        self._windows.pop(key, None)

    def stats(self) -> dict:
        now = time.monotonic()
        return {key: w.current_count(now=now) for key, w in self._windows.items()}
