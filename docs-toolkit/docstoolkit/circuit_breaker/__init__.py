"""Circuit breaker: protect external calls from cascading failures."""
from docstoolkit.circuit_breaker.state import CircuitState, CircuitStats
from docstoolkit.circuit_breaker.breaker import CircuitBreaker, CircuitBreakerConfig, CallResult
from docstoolkit.circuit_breaker.registry import CircuitBreakerRegistry

__all__ = [
    "CircuitState", "CircuitStats",
    "CircuitBreaker", "CircuitBreakerConfig", "CallResult",
    "CircuitBreakerRegistry",
]
