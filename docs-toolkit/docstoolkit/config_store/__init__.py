"""Hierarchical, namespaced configuration store backed by SQLite.

Supports dot-notation keys, namespaces, JSON-typed values,
change listeners, and import/export.  Pure stdlib only.

Example::

    from docstoolkit.config_store import ConfigStore, ConfigEntry

    store = ConfigStore()                          # in-memory by default
    store.set("app", "server.port", 8080)
    store.set("app", "server.host", "localhost", description="Bind address")
    port = store.get("app", "server.port")         # 8080
    entries = store.list("app", prefix="server.")  # [server.host, server.port]
    store.close()
"""

from docstoolkit.config_store.store import ConfigEntry, ConfigStore

__all__ = ["ConfigEntry", "ConfigStore"]
