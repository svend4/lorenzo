"""Plugin registry: tracks all registered plugins and their statuses."""
from __future__ import annotations

from dataclasses import dataclass, field

from docstoolkit.plugin_system.plugin import Plugin, PluginStatus


@dataclass
class PluginRecord:
    """Stores a plugin instance together with its current status and error info."""
    plugin: Plugin
    status: PluginStatus = PluginStatus.UNLOADED
    error: str = ""


class PluginRegistry:
    """Central store for plugin instances."""

    def __init__(self) -> None:
        self._records: dict[str, PluginRecord] = {}

    # ------------------------------------------------------------------
    # Mutation helpers
    # ------------------------------------------------------------------

    def register(self, plugin: Plugin) -> None:
        """Add a plugin to the registry with UNLOADED status.

        Raises:
            ValueError: if a plugin with the same name is already registered.
        """
        name = plugin.metadata.name
        if name in self._records:
            raise ValueError(
                f"Plugin '{name}' is already registered. "
                "Unregister it first before re-registering."
            )
        self._records[name] = PluginRecord(plugin=plugin)

    def unregister(self, name: str) -> bool:
        """Remove a plugin from the registry.

        Returns:
            True if the plugin was found and removed, False otherwise.
        """
        if name in self._records:
            del self._records[name]
            return True
        return False

    # ------------------------------------------------------------------
    # Query helpers
    # ------------------------------------------------------------------

    def get(self, name: str) -> PluginRecord | None:
        """Return the PluginRecord for *name*, or None if not registered."""
        return self._records.get(name)

    def list_all(self) -> list[PluginRecord]:
        """Return all registered PluginRecords."""
        return list(self._records.values())

    def list_by_status(self, status: PluginStatus) -> list[PluginRecord]:
        """Return all PluginRecords whose current status matches *status*."""
        return [r for r in self._records.values() if r.status == status]

    def list_by_tag(self, tag: str) -> list[PluginRecord]:
        """Return all PluginRecords whose plugin metadata includes *tag*."""
        return [
            r for r in self._records.values()
            if tag in r.plugin.metadata.tags
        ]
