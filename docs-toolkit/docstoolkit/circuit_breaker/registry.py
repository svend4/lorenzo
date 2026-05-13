from docstoolkit.circuit_breaker.breaker import CircuitBreaker, CircuitBreakerConfig
from docstoolkit.circuit_breaker.state import CircuitState

class CircuitBreakerRegistry:
    """Registry of named circuit breakers."""

    def __init__(self, default_config: CircuitBreakerConfig | None = None):
        self._breakers: dict = {}
        self._default_config = default_config or CircuitBreakerConfig()

    def get_or_create(self, name: str) -> CircuitBreaker:
        """Get existing or create new breaker with default config."""
        if name not in self._breakers:
            self._breakers[name] = CircuitBreaker(name, self._default_config)
        return self._breakers[name]

    def get(self, name: str) -> CircuitBreaker | None:
        return self._breakers.get(name)

    def list_names(self) -> list:
        return sorted(self._breakers.keys())

    def open_circuits(self) -> list:
        """Return names of circuits currently OPEN."""
        return [name for name, b in self._breakers.items()
                if b.state == CircuitState.OPEN]

    def health_summary(self) -> dict:
        """Return {name: state.value} for all registered breakers."""
        return {name: b.state.value for name, b in self._breakers.items()}

    def reset_all(self) -> None:
        """Force-close all breakers."""
        for b in self._breakers.values():
            b.force_close()
