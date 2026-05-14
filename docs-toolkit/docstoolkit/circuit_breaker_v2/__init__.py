"""Circuit breaker v2 — improved thread-safe implementation with virtual-time support."""
from docstoolkit.circuit_breaker_v2.breaker import (
    CircuitState,
    BreakerConfig,
    CircuitBreakerError,
    CircuitBreaker,
)

__all__ = [
    "CircuitState",
    "BreakerConfig",
    "CircuitBreakerError",
    "CircuitBreaker",
]
