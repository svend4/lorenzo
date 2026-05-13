"""@retry decorator factory."""
from __future__ import annotations

import functools
from typing import Callable

from docstoolkit.retry_policy.backoff import BackoffConfig, BackoffStrategy
from docstoolkit.retry_policy.policy import RetryConfig, RetryExecutor


def retry(
    max_attempts: int = 3,
    backoff_strategy: BackoffStrategy = BackoffStrategy.EXPONENTIAL,
    base_delay: float = 1.0,
    retry_on: list[type] | None = None,
    sleep_fn: Callable[[float], None] | None = None,
) -> Callable:
    """Decorator factory that wraps a function with retry logic.

    Args:
        max_attempts: Total number of call attempts (1 = no retry).
        backoff_strategy: Backoff strategy to use between retries.
        base_delay: Base delay in seconds for the backoff calculator.
        retry_on: Exception types that trigger a retry.  None / empty = all exceptions.
        sleep_fn: Injectable sleep function (default: time.sleep).

    Returns:
        A decorator that applies retry behaviour to the decorated function.

    Raises:
        The last exception raised if all attempts are exhausted.
    """

    def decorator(func: Callable) -> Callable:
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            backoff_cfg = BackoffConfig(
                strategy=backoff_strategy,
                base_delay=base_delay,
            )
            config = RetryConfig(
                max_attempts=max_attempts,
                backoff=backoff_cfg,
                retry_on=retry_on if retry_on is not None else [],
                sleep_fn=sleep_fn,
            )
            executor = RetryExecutor(config)
            result = executor.execute(func, *args, **kwargs)
            if not result.succeeded:
                # Re-raise the last exception by executing the function one final
                # time to obtain a real traceback, OR re-raise a RuntimeError
                # carrying the last_error message.  We use RuntimeError so that
                # callers always get an exception regardless of the error type.
                raise RuntimeError(result.last_error) if result.last_error else RuntimeError(
                    "retry exhausted with no recorded error"
                )
            return result.value

        return wrapper

    return decorator
