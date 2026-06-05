"""CircuitBreaker v2 — thread-safe circuit breaker with virtual-time support."""
import threading
import time
from dataclasses import dataclass
from enum import Enum
from typing import Callable


class CircuitState(str, Enum):
    """States of a circuit breaker."""
    CLOSED = "closed"
    OPEN = "open"
    HALF_OPEN = "half_open"


@dataclass
class BreakerConfig:
    """Configuration for CircuitBreaker v2."""
    failure_threshold: int = 5       # failures in CLOSED to trip to OPEN
    recovery_timeout: float = 30.0   # seconds OPEN before trying HALF_OPEN
    success_threshold: int = 2       # successes in HALF_OPEN to close
    half_open_max_calls: int = 1     # max concurrent calls allowed in HALF_OPEN


class CircuitBreakerError(Exception):
    """Raised when the circuit is OPEN and a call is attempted."""


class CircuitBreaker:
    """Thread-safe circuit breaker with CLOSED / OPEN / HALF_OPEN states.

    State transitions
    -----------------
    CLOSED  + failure_count >= failure_threshold  → OPEN  (reset success_count)
    OPEN    + time since last failure >= recovery_timeout → HALF_OPEN
    HALF_OPEN + success_count >= success_threshold → CLOSED  (reset counts)
    HALF_OPEN + any failure                        → OPEN   (reset success_count)

    Virtual time
    ------------
    Override ``_now()`` (e.g. via subclass or monkeypatch) to inject a
    monotonic clock for deterministic tests — no sleep required.
    """

    def __init__(self, config: "BreakerConfig | None" = None) -> None:
        self._config: BreakerConfig = config if config is not None else BreakerConfig()
        self._state: CircuitState = CircuitState.CLOSED
        self._failure_count: int = 0
        self._success_count: int = 0
        self._last_failure_time: "float | None" = None  # None = no failure yet
        # active calls currently executing inside HALF_OPEN
        self._half_open_active: int = 0
        self._lock = threading.Lock()

    # ------------------------------------------------------------------
    # Clock — override for deterministic tests
    # ------------------------------------------------------------------

    def _now(self) -> float:  # pragma: no cover
        """Return current monotonic time. Override in tests for virtual time."""
        return time.monotonic()

    # ------------------------------------------------------------------
    # Properties
    # ------------------------------------------------------------------

    @property
    def state(self) -> CircuitState:
        """Current state; accessing may trigger OPEN → HALF_OPEN transition."""
        with self._lock:
            self._maybe_recover()
            return self._state

    @property
    def failure_count(self) -> int:
        """Number of failures recorded since last reset or CLOSED transition."""
        with self._lock:
            return self._failure_count

    @property
    def success_count(self) -> int:
        """Number of successes recorded since last reset or OPEN transition."""
        with self._lock:
            return self._success_count

    # ------------------------------------------------------------------
    # Public API
    # ------------------------------------------------------------------

    def call(self, fn: Callable, *args, **kwargs):
        """Execute *fn* through the circuit breaker.

        CLOSED   — executes normally; exceptions increment failure_count.
        OPEN     — raises CircuitBreakerError immediately (fn not called),
                   unless recovery_timeout has elapsed, in which case the
                   circuit transitions to HALF_OPEN first and then allows
                   the call (subject to half_open_max_calls).
        HALF_OPEN — allows up to half_open_max_calls concurrent calls;
                   excess calls raise CircuitBreakerError.
                   Success increments success_count; when success_count
                   reaches success_threshold the circuit closes.
                   Any failure returns the circuit to OPEN.

        Returns the return value of *fn* on success.
        Re-raises the exception from *fn* (after recording the failure).
        """
        with self._lock:
            self._maybe_recover()

            if self._state == CircuitState.OPEN:
                raise CircuitBreakerError(
                    "Circuit is OPEN — call rejected"
                )

            if self._state == CircuitState.HALF_OPEN:
                if self._half_open_active >= self._config.half_open_max_calls:
                    raise CircuitBreakerError(
                        "Circuit is HALF_OPEN — max concurrent calls reached"
                    )
                self._half_open_active += 1

        # Execute *outside* the lock so threads are not serialised.
        try:
            result = fn(*args, **kwargs)
        except Exception:
            with self._lock:
                was_half_open = self._state == CircuitState.HALF_OPEN
                self._apply_failure()
                # _apply_failure may have transitioned HALF_OPEN → OPEN;
                # decrement the active-call counter regardless.
                if was_half_open:
                    self._half_open_active = max(0, self._half_open_active - 1)
            raise

        with self._lock:
            was_half_open = self._state == CircuitState.HALF_OPEN
            self._apply_success()
            # _apply_success may have transitioned HALF_OPEN → CLOSED;
            # decrement the active-call counter regardless.
            if was_half_open:
                self._half_open_active = max(0, self._half_open_active - 1)

        return result

    def record_success(self) -> None:
        """Manually record a success (does not execute any function)."""
        with self._lock:
            self._apply_success()

    def record_failure(self) -> None:
        """Manually record a failure (does not execute any function)."""
        with self._lock:
            self._apply_failure()

    def reset(self) -> None:
        """Force the circuit to CLOSED state and clear all counters."""
        with self._lock:
            self._state = CircuitState.CLOSED
            self._failure_count = 0
            self._success_count = 0
            self._last_failure_time = None
            self._half_open_active = 0

    def stats(self) -> dict:
        """Return a snapshot dict with state, failure_count, success_count,
        and last_failure_time (0.0 when no failure has been recorded)."""
        with self._lock:
            return {
                "state": self._state,
                "failure_count": self._failure_count,
                "success_count": self._success_count,
                "last_failure_time": self._last_failure_time if self._last_failure_time is not None else 0.0,
            }

    # ------------------------------------------------------------------
    # Internal helpers (must be called with _lock held)
    # ------------------------------------------------------------------

    def _maybe_recover(self) -> None:
        """If OPEN and recovery_timeout elapsed, transition to HALF_OPEN."""
        if (
            self._state == CircuitState.OPEN
            and self._last_failure_time is not None
            and self._now() - self._last_failure_time >= self._config.recovery_timeout
        ):
            self._state = CircuitState.HALF_OPEN
            self._half_open_active = 0
            # Keep failure_count intact so stats are readable; success_count
            # was already zeroed when we moved to OPEN.

    def _apply_success(self) -> None:
        """Record a success and drive state transitions."""
        self._success_count += 1

        if self._state == CircuitState.HALF_OPEN:
            if self._success_count >= self._config.success_threshold:
                # Transition HALF_OPEN → CLOSED
                self._state = CircuitState.CLOSED
                self._failure_count = 0
                self._success_count = 0
                self._last_failure_time = None
                self._half_open_active = 0

    def _apply_failure(self) -> None:
        """Record a failure and drive state transitions."""
        self._failure_count += 1
        self._last_failure_time = self._now()

        if self._state == CircuitState.CLOSED:
            if self._failure_count >= self._config.failure_threshold:
                self._state = CircuitState.OPEN
                self._success_count = 0   # per spec: reset success_count on OPEN

        elif self._state == CircuitState.HALF_OPEN:
            # Any failure in HALF_OPEN → OPEN
            self._state = CircuitState.OPEN
            self._success_count = 0       # per spec: reset success_count
