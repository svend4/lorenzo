"""RetryConfig, RetryResult, and RetryExecutor."""
from __future__ import annotations

import time
from dataclasses import dataclass, field
from enum import Enum
from typing import Any, Callable

from docstoolkit.retry_policy.backoff import BackoffCalculator, BackoffConfig


class RetryCondition(Enum):
    ON_EXCEPTION = "on_exception"
    ON_RESULT = "on_result"
    ALWAYS = "always"


@dataclass
class RetryConfig:
    """Configuration for retry behaviour.

    Attributes:
        max_attempts: Total number of call attempts (1 = no retry).
        backoff: Backoff configuration used between retries.
        retry_on: Exception types that trigger a retry.  Empty list means all exceptions.
        stop_on: Exception types that are *not* retried (takes precedence over retry_on).
        result_retry_predicate: Optional callable; retry when predicate(result) is True.
        sleep_fn: Injectable sleep function (default: time.sleep).
    """

    max_attempts: int = 3
    backoff: BackoffConfig = field(default_factory=BackoffConfig)
    retry_on: list[type] = field(default_factory=list)
    stop_on: list[type] = field(default_factory=list)
    result_retry_predicate: Callable[[Any], bool] | None = None
    sleep_fn: Callable[[float], None] | None = None


@dataclass
class RetryResult:
    """Outcome of a retry execution."""

    value: Any
    attempts: int
    succeeded: bool
    last_error: str = ""


class RetryExecutor:
    """Execute a callable with retry logic defined by a RetryConfig."""

    def __init__(self, config: RetryConfig | None = None) -> None:
        self.config = config if config is not None else RetryConfig()

    def execute(self, func: Callable, *args: Any, **kwargs: Any) -> RetryResult:
        cfg = self.config
        calculator = BackoffCalculator(cfg.backoff)
        sleep_fn = cfg.sleep_fn if cfg.sleep_fn is not None else time.sleep

        last_exception: Exception | None = None
        last_error: str = ""

        for attempt_number in range(cfg.max_attempts):
            # attempt_number: 0-based index of the current *call* attempt
            try:
                result = func(*args, **kwargs)
            except Exception as exc:
                last_exception = exc
                last_error = str(exc)

                # Check stop_on first — never retry these
                if cfg.stop_on and isinstance(exc, tuple(cfg.stop_on)):
                    return RetryResult(
                        value=None,
                        attempts=attempt_number + 1,
                        succeeded=False,
                        last_error=last_error,
                    )

                # Check retry_on — empty means retry on all exceptions
                if cfg.retry_on and not isinstance(exc, tuple(cfg.retry_on)):
                    # Not a retryable exception type; propagate immediately
                    return RetryResult(
                        value=None,
                        attempts=attempt_number + 1,
                        succeeded=False,
                        last_error=last_error,
                    )

                # If more attempts remain, sleep before the next attempt
                if attempt_number + 1 < cfg.max_attempts:
                    delay = calculator.delay(attempt_number)
                    if delay > 0:
                        sleep_fn(delay)
                continue

            # No exception raised — check result predicate
            if cfg.result_retry_predicate is not None and cfg.result_retry_predicate(result):
                # Result says "retry"
                last_error = f"result_retry_predicate returned True for result: {result!r}"
                if attempt_number + 1 < cfg.max_attempts:
                    delay = calculator.delay(attempt_number)
                    if delay > 0:
                        sleep_fn(delay)
                continue

            # Success
            return RetryResult(
                value=result,
                attempts=attempt_number + 1,
                succeeded=True,
            )

        # All attempts exhausted
        return RetryResult(
            value=None,
            attempts=cfg.max_attempts,
            succeeded=False,
            last_error=last_error,
        )
