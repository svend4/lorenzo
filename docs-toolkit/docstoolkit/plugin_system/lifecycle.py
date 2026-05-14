"""Plugin lifecycle manager: load, unload, activate, deactivate, disable."""
from __future__ import annotations

from docstoolkit.plugin_system.plugin import Plugin, PluginStatus
from docstoolkit.plugin_system.registry import PluginRecord, PluginRegistry


class PluginManager:
    """Orchestrates the full lifecycle of registered plugins."""

    def __init__(self, registry: PluginRegistry | None = None) -> None:
        self.registry: PluginRegistry = registry if registry is not None else PluginRegistry()

    # ------------------------------------------------------------------
    # Convenience: forward register to the underlying registry
    # ------------------------------------------------------------------

    def register(self, plugin: Plugin) -> None:
        """Register a plugin in the underlying registry."""
        self.registry.register(plugin)

    # ------------------------------------------------------------------
    # Single-plugin lifecycle transitions
    # ------------------------------------------------------------------

    def load(self, name: str) -> bool:
        """Load a plugin: call on_load(), set status to LOADED.

        If on_load() raises, status is set to ERROR and the exception
        message is stored in the record.  Returns True on success.
        """
        record = self.registry.get(name)
        if record is None:
            return False
        try:
            record.plugin.on_load()
            record.status = PluginStatus.LOADED
            record.error = ""
            return True
        except Exception as exc:
            record.status = PluginStatus.ERROR
            record.error = str(exc)
            return False

    def unload(self, name: str) -> bool:
        """Unload a plugin: call on_unload(), set status to UNLOADED.

        Returns True on success, False if the plugin is not registered.
        """
        record = self.registry.get(name)
        if record is None:
            return False
        record.plugin.on_unload()
        record.status = PluginStatus.UNLOADED
        record.error = ""
        return True

    def activate(self, name: str) -> bool:
        """Activate a LOADED plugin: call on_activate(), set status to ACTIVE.

        The plugin must be in LOADED status; returns False otherwise.
        """
        record = self.registry.get(name)
        if record is None:
            return False
        if record.status != PluginStatus.LOADED:
            return False
        record.plugin.on_activate()
        record.status = PluginStatus.ACTIVE
        return True

    def deactivate(self, name: str) -> bool:
        """Deactivate an ACTIVE plugin: call on_deactivate(), set status to LOADED.

        Returns False if the plugin is not registered or not ACTIVE.
        """
        record = self.registry.get(name)
        if record is None:
            return False
        if record.status != PluginStatus.ACTIVE:
            return False
        record.plugin.on_deactivate()
        record.status = PluginStatus.LOADED
        return True

    def disable(self, name: str) -> bool:
        """Disable a plugin by setting its status to DISABLED (no lifecycle calls).

        Returns False if the plugin is not registered.
        """
        record = self.registry.get(name)
        if record is None:
            return False
        record.status = PluginStatus.DISABLED
        return True

    # ------------------------------------------------------------------
    # Bulk operations
    # ------------------------------------------------------------------

    def load_all(self) -> dict[str, bool]:
        """Load every UNLOADED plugin. Returns {name: success}."""
        results: dict[str, bool] = {}
        for record in self.registry.list_by_status(PluginStatus.UNLOADED):
            name = record.plugin.metadata.name
            results[name] = self.load(name)
        return results

    def activate_all(self) -> dict[str, bool]:
        """Activate every LOADED plugin. Returns {name: success}."""
        results: dict[str, bool] = {}
        for record in self.registry.list_by_status(PluginStatus.LOADED):
            name = record.plugin.metadata.name
            results[name] = self.activate(name)
        return results

    # ------------------------------------------------------------------
    # Queries
    # ------------------------------------------------------------------

    def active_plugins(self) -> list[Plugin]:
        """Return Plugin instances whose current status is ACTIVE."""
        return [
            r.plugin for r in self.registry.list_by_status(PluginStatus.ACTIVE)
        ]

    # ------------------------------------------------------------------
    # Dependency resolution
    # ------------------------------------------------------------------

    def resolve_dependencies(self, name: str) -> list[str]:
        """Return an ordered list of dependency names that must be loaded
        before *name* (topological sort via DFS).

        Raises:
            ValueError: if a circular dependency is detected.
            ValueError: if a required plugin is not registered.
        """
        order: list[str] = []
        visited: set[str] = set()
        in_stack: set[str] = set()

        def _visit(current: str) -> None:
            if current in in_stack:
                raise ValueError(
                    f"Circular dependency detected involving plugin '{current}'."
                )
            if current in visited:
                return

            in_stack.add(current)

            record = self.registry.get(current)
            if record is None:
                raise ValueError(
                    f"Plugin '{current}' is not registered but is required as a dependency."
                )

            for dep in record.plugin.metadata.dependencies:
                _visit(dep)

            in_stack.discard(current)
            visited.add(current)

            # Only append dependencies (not the plugin itself) to the result
            if current != name:
                order.append(current)

        # Manually walk the direct deps of the target so that *name* itself
        # is excluded from the returned list while still detecting cycles.
        root_record = self.registry.get(name)
        if root_record is None:
            raise ValueError(f"Plugin '{name}' is not registered.")

        for dep in root_record.plugin.metadata.dependencies:
            _visit(dep)

        return order
