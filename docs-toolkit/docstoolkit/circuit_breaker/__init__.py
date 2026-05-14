"""Circuit breaker: protect external calls from cascading failures."""
from docstoolkit.circuit_breaker.state import CircuitState, CircuitStats
from docstoolkit.circuit_breaker.breaker import CircuitBreaker, CircuitBreakerConfig
from docstoolkit.circuit_breaker.registry import CircuitBreakerRegistry, CircuitOpenError

__all__ = [
    "CircuitState",
    "CircuitStats",
    "CircuitBreaker",
    "CircuitBreakerConfig",
    "CircuitBreakerRegistry",
    "CircuitOpenError",
]
