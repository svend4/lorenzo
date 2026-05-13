import time
from dataclasses import dataclass
from typing import Callable
from docstoolkit.circuit_breaker.state import CircuitState, CircuitStats

@dataclass
class CircuitBreakerConfig:
    failure_threshold: int = 5       # failures before opening
    success_threshold: int = 2       # successes in HALF_OPEN before closing
    timeout_seconds: float = 30.0    # time OPEN before trying HALF_OPEN
    max_half_open_calls: int = 1     # concurrent HALF_OPEN probe calls

@dataclass
class CallResult:
    """Result of a circuit-breaker-protected call."""
    success: bool
    result: object = None
    error: str = ""
    state_after: CircuitState = CircuitState.CLOSED
    rejected: bool = False


class CircuitBreaker:
    """Circuit breaker for protecting external calls.

    States:
    CLOSED → calls pass through; too many failures → OPEN
    OPEN → calls rejected immediately; after timeout → HALF_OPEN
    HALF_OPEN → limited probe calls; success → CLOSED; failure → OPEN
    """

    def __init__(self, name: str, config: CircuitBreakerConfig | None = None):
        self.name = name
        self._config = config or CircuitBreakerConfig()
        self._state = CircuitState.CLOSED
        self._stats = CircuitStats()
        self._open_since: float = 0.0
        self._half_open_successes: int = 0
        self._half_open_calls: int = 0

    @property
    def state(self) -> CircuitState:
        self._check_timeout()
        return self._state

    @property
    def stats(self) -> CircuitStats:
        return self._stats

    def _check_timeout(self) -> None:
        """Transition OPEN → HALF_OPEN if timeout elapsed."""
        if (self._state == CircuitState.OPEN and
                self._open_since > 0 and
                time.monotonic() - self._open_since >= self._config.timeout_seconds):
            self._state = CircuitState.HALF_OPEN
            self._half_open_successes = 0
            self._half_open_calls = 0

    def call(self, fn: Callable, *args, **kwargs) -> CallResult:
        """Execute fn through circuit breaker.

        OPEN: reject immediately → CallResult(rejected=True, success=False)
        HALF_OPEN: if _half_open_calls >= max_half_open_calls: reject
        Otherwise: execute fn
          - Success: record_success; if HALF_OPEN: increment successes;
            if successes >= success_threshold: CLOSED + reset
          - Exception: record_failure; if >= failure_threshold: OPEN
        """
        self._check_timeout()

        if self._state == CircuitState.OPEN:
            self._stats.record_rejected()
            return CallResult(success=False, rejected=True,
                              state_after=CircuitState.OPEN,
                              error="Circuit is OPEN")

        if (self._state == CircuitState.HALF_OPEN and
                self._half_open_calls >= self._config.max_half_open_calls):
            self._stats.record_rejected()
            return CallResult(success=False, rejected=True,
                              state_after=CircuitState.HALF_OPEN,
                              error="Circuit is HALF_OPEN, max probes reached")

        if self._state == CircuitState.HALF_OPEN:
            self._half_open_calls += 1

        try:
            result = fn(*args, **kwargs)
            self._stats.record_success()
            if self._state == CircuitState.HALF_OPEN:
                self._half_open_successes += 1
                if self._half_open_successes >= self._config.success_threshold:
                    self._state = CircuitState.CLOSED
                    self._stats.reset()
            return CallResult(success=True, result=result, state_after=self._state)
        except Exception as e:
            self._stats.record_failure()
            if self._stats.failure_count >= self._config.failure_threshold:
                self._state = CircuitState.OPEN
                self._open_since = time.monotonic()
                self._half_open_successes = 0
            return CallResult(success=False, error=str(e), state_after=self._state)

    def force_open(self) -> None:
        self._state = CircuitState.OPEN
        self._open_since = time.monotonic()

    def force_close(self) -> None:
        self._state = CircuitState.CLOSED
        self._stats.reset()
        self._half_open_successes = 0
