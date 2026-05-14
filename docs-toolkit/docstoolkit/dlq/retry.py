import time
from dataclasses import dataclass
from typing import Callable

@dataclass
class RetryPolicy:
    """Retry configuration."""
    max_attempts: int = 3
    backoff_base: float = 1.0     # seconds for first retry
    backoff_multiplier: float = 2.0   # exponential backoff
    max_backoff: float = 60.0     # cap
    jitter: bool = False           # add random jitter (not in stdlib-only mode)

    def wait_time(self, attempt: int) -> float:
        """Compute wait time for attempt N (0-indexed).
        wait = min(backoff_base * (backoff_multiplier ** attempt), max_backoff)
        """
        wait = self.backoff_base * (self.backoff_multiplier ** attempt)
        return min(wait, self.max_backoff)

@dataclass
class RetryResult:
    """Result of a retried operation."""
    success: bool
    attempts: int
    result: object = None    # return value if success
    last_error: str = ""
    total_wait_ms: float = 0.0


def execute_with_retry(
    fn: Callable,
    policy: RetryPolicy | None = None,
    *,
    args: tuple = (),
    kwargs: dict | None = None,
) -> RetryResult:
    """Execute fn with retry according to policy.

    Does NOT actually sleep (for tests); records what wait WOULD have been.
    On each failure: increment attempts, record error.
    On success: return RetryResult(success=True, ...).
    After max_attempts failures: return RetryResult(success=False, ...).
    """
    policy = policy or RetryPolicy()
    kwargs = kwargs or {}
    attempts = 0
    total_wait = 0.0
    last_error = ""

    for attempt in range(policy.max_attempts):
        attempts += 1
        try:
            result = fn(*args, **kwargs)
            return RetryResult(
                success=True,
                attempts=attempts,
                result=result,
                total_wait_ms=total_wait * 1000,
            )
        except Exception as e:
            last_error = str(e)
            if attempt < policy.max_attempts - 1:
                total_wait += policy.wait_time(attempt)

    return RetryResult(
        success=False,
        attempts=attempts,
        last_error=last_error,
        total_wait_ms=total_wait * 1000,
    )
