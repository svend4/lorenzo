"""Binding definitions for the DI container."""
from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum
from typing import Any


class BindingScope(Enum):
    """Lifecycle scope for a registered binding."""

    TRANSIENT = "transient"  # new instance on every resolve
    SINGLETON = "singleton"  # one shared instance per container
    REQUEST = "request"      # per-request; treated as TRANSIENT in this impl


@dataclass
class Binding:
    """Describes how to create/cache a dependency."""

    interface: type
    implementation: type | Any  # type (class) or callable
    scope: BindingScope = BindingScope.TRANSIENT
    instance: Any = field(default=None, repr=False)  # cached for SINGLETON
    tags: list[str] = field(default_factory=list)

    def is_singleton(self) -> bool:
        """Return True if this binding uses SINGLETON scope."""
        return self.scope is BindingScope.SINGLETON
