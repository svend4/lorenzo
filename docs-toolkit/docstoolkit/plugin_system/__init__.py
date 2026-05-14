"""Plugin system for docs-toolkit.

Provides a structured lifecycle for registering, loading, activating,
and deactivating plugins with optional dependency resolution.

Quick-start::

    from docstoolkit.plugin_system import (
        Plugin, PluginMetadata, PluginStatus,
        PluginRecord, PluginRegistry,
        PluginManager,
    )

    class MyPlugin(Plugin):
        @property
        def metadata(self):
            return PluginMetadata(name="my-plugin", tags=["util"])

        def on_activate(self):
            print("MyPlugin activated!")

    mgr = PluginManager()
    mgr.register(MyPlugin())
    mgr.load("my-plugin")
    mgr.activate("my-plugin")
    print(mgr.active_plugins())
"""
from docstoolkit.plugin_system.plugin import Plugin, PluginMetadata, PluginStatus
from docstoolkit.plugin_system.registry import PluginRecord, PluginRegistry
from docstoolkit.plugin_system.lifecycle import PluginManager

__all__ = [
    # plugin.py
    "Plugin",
    "PluginMetadata",
    "PluginStatus",
    # registry.py
    "PluginRecord",
    "PluginRegistry",
    # lifecycle.py
    "PluginManager",
]
