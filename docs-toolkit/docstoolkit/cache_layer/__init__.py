"""Cache layer abstraction: backends, serializers, and high-level CacheLayer."""
from docstoolkit.cache_layer.backend import (
    CacheBackend,
    MemoryBackend,
    SqliteBackend,
)
from docstoolkit.cache_layer.serializer import (
    JsonSerializer,
    PickleSerializer,
    Serializer,
    StringSerializer,
)
from docstoolkit.cache_layer.cache import (
    CacheConfig,
    CacheLayer,
    CacheStats,
)

__all__ = [
    # Backends
    "CacheBackend",
    "MemoryBackend",
    "SqliteBackend",
    # Serializers
    "Serializer",
    "JsonSerializer",
    "PickleSerializer",
    "StringSerializer",
    # High-level cache
    "CacheConfig",
    "CacheStats",
    "CacheLayer",
]
