"""Plugin base classes and metadata for the docs-toolkit plugin system."""
from __future__ import annotations

from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from enum import Enum


class PluginStatus(Enum):
    """Lifecycle status of a plugin."""
    UNLOADED = "unloaded"
    LOADED = "loaded"
    ACTIVE = "active"
    ERROR = "error"
    DISABLED = "disabled"


@dataclass
class PluginMetadata:
    """Descriptive metadata for a plugin."""
    name: str
    version: str = "0.1.0"
    description: str = ""
    author: str = ""
    dependencies: list[str] = field(default_factory=list)
    tags: list[str] = field(default_factory=list)


class Plugin(ABC):
    """Abstract base class for all docs-toolkit plugins."""

    @property
    @abstractmethod
    def metadata(self) -> PluginMetadata:
        """Return the plugin's metadata."""

    def on_load(self) -> None:
        """Called when the plugin is loaded into the registry. Default: no-op."""

    def on_unload(self) -> None:
        """Called when the plugin is unloaded from the registry. Default: no-op."""

    def on_activate(self) -> None:
        """Called when the plugin is activated."""

    def on_deactivate(self) -> None:
        """Called when the plugin is deactivated."""
