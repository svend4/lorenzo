"""CircuitBreakerConfig and CircuitBreaker."""
import copy
import threading
import time
from dataclasses import dataclass

from docstoolkit.circuit_breaker.state import CircuitState, CircuitStats


@dataclass
class CircuitBreakerConfig:
    """Configuration for a CircuitBreaker."""
    failure_threshold: int = 5       # consecutive failures before OPEN
    recovery_timeout: float = 60.0   # seconds OPEN before trying HALF_OPEN
    half_open_max_calls: int = 3     # calls allowed in HALF_OPEN
    success_threshold: int = 2       # consecutive successes in HALF_OPEN to CLOSE


class CircuitBreaker:
    """Circuit breaker protecting external calls from cascading failures.

    State machine:
      CLOSED  → too many consecutive failures → OPEN
      OPEN    → recovery_timeout elapsed      → HALF_OPEN
      HALF_OPEN → success_threshold successes → CLOSED
      HALF_OPEN → any failure                → OPEN
    """

    def __init__(self, name: str, config: "CircuitBreakerConfig | None" = None):
        self.name = name
        self._config = config if config is not None else CircuitBreakerConfig()
        self._state: CircuitState = CircuitState.CLOSED
        self._stats: CircuitStats = CircuitStats()
        self._open_since: float = 0.0
        self._half_open_calls: int = 0
        self._lock = threading.Lock()

    # ------------------------------------------------------------------
    # Properties
    # ------------------------------------------------------------------

    @property
    def state(self) -> CircuitState:
        """Current state (may trigger OPEN→HALF_OPEN timeout check)."""
        with self._lock:
            self._maybe_transition_to_half_open()
            return self._state

    @property
    def stats(self) -> CircuitStats:
        """Return a shallow copy of the current stats."""
        with self._lock:
            return copy.copy(self._stats)

    # ------------------------------------------------------------------
    # Public interface
    # ------------------------------------------------------------------

    def call(self, func, *args, **kwargs):
        """Execute *func* through the circuit breaker.

        Raises CircuitOpenError if the circuit is OPEN or if HALF_OPEN
        and the half_open_max_calls limit has been reached.

        On success: updates stats; if HALF_OPEN and consecutive_successes
        reaches success_threshold, transitions back to CLOSED.

        On failure: updates stats; if CLOSED and consecutive_failures
        reaches failure_threshold → OPEN; if HALF_OPEN → OPEN.

        Returns whatever *func* returns.
        """
        from docstoolkit.circuit_breaker.registry import CircuitOpenError

        with self._lock:
            self._maybe_transition_to_half_open()

            if self._state == CircuitState.OPEN:
                raise CircuitOpenError(
                    f"Circuit '{self.name}' is OPEN — failing fast"
                )

            if self._state == CircuitState.HALF_OPEN:
                if self._half_open_calls >= self._config.half_open_max_calls:
                    raise CircuitOpenError(
                        f"Circuit '{self.name}' is HALF_OPEN — max probe calls reached"
                    )
                self._half_open_calls += 1

        # Execute outside the lock so concurrent calls are not serialised
        try:
            result = func(*args, **kwargs)
        except Exception:
            with self._lock:
                self._record_failure()
            raise

        with self._lock:
            self._record_success()

        return result

    def reset(self) -> None:
        """Force circuit back to CLOSED and zero all stats."""
        with self._lock:
            self._state = CircuitState.CLOSED
            self._stats.reset()
            self._open_since = 0.0
            self._half_open_calls = 0

    def trip(self) -> None:
        """Force circuit to OPEN (useful for testing)."""
        with self._lock:
            self._state = CircuitState.OPEN
            self._open_since = time.monotonic()

    # ------------------------------------------------------------------
    # Internal helpers (must be called with lock held)
    # ------------------------------------------------------------------

    def _maybe_transition_to_half_open(self) -> None:
        """If OPEN and recovery_timeout has elapsed, move to HALF_OPEN."""
        if (
            self._state == CircuitState.OPEN
            and self._open_since > 0
            and time.monotonic() - self._open_since >= self._config.recovery_timeout
        ):
            self._state = CircuitState.HALF_OPEN
            self._half_open_calls = 0

    def _record_success(self) -> None:
        s = self._stats
        s.total_calls += 1
        s.successes += 1
        s.consecutive_successes += 1
        s.consecutive_failures = 0

        if self._state == CircuitState.HALF_OPEN:
            if s.consecutive_successes >= self._config.success_threshold:
                self._state = CircuitState.CLOSED
                self._stats.reset()
                self._half_open_calls = 0

    def _record_failure(self) -> None:
        import time as _time
        s = self._stats
        s.total_calls += 1
        s.failures += 1
        s.consecutive_failures += 1
        s.consecutive_successes = 0
        s.last_failure_time = _time.monotonic()

        if self._state == CircuitState.CLOSED:
            if s.consecutive_failures >= self._config.failure_threshold:
                self._state = CircuitState.OPEN
                self._open_since = _time.monotonic()
        elif self._state == CircuitState.HALF_OPEN:
            self._state = CircuitState.OPEN
            self._open_since = _time.monotonic()
