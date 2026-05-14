"""CircuitOpenError and CircuitBreakerRegistry."""
from docstoolkit.circuit_breaker.state import CircuitState


class CircuitOpenError(Exception):
    """Raised when a call is attempted on an open circuit breaker."""


class CircuitBreakerRegistry:
    """Registry of named circuit breakers.

    Breakers are created on first access via get().
    """

    def __init__(self, default_config=None):
        self._breakers: dict = {}
        self._default_config = default_config  # may be None; each CircuitBreaker handles None

    def get(self, name: str):
        """Return the named breaker, creating it with default_config if absent."""
        from docstoolkit.circuit_breaker.breaker import CircuitBreaker
        if name not in self._breakers:
            self._breakers[name] = CircuitBreaker(name, self._default_config)
        return self._breakers[name]

    def all(self) -> dict:
        """Return a dict of {name: CircuitBreaker} for all registered breakers."""
        return dict(self._breakers)

    def reset_all(self) -> None:
        """Force-close (reset) all registered breakers."""
        for b in self._breakers.values():
            b.reset()

    def stats_summary(self) -> dict:
        """Return {name: {state, failure_rate, total_calls}} for all breakers."""
        summary = {}
        for name, b in self._breakers.items():
            s = b.stats
            summary[name] = {
                "state": b.state.value,
                "failure_rate": s.failure_rate(),
                "total_calls": s.total_calls,
            }
        return summary
