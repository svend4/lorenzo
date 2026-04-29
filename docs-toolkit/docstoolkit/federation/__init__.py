"""Federation: cross-instance discovery + query routing.

Concept (NPP — Nautilus Portal Protocol):
  - Каждый docs-toolkit instance = portal с registry.json
  - Portal registers свои capabilities + endpoints
  - Query идёт через адаптеры → агрегированный ответ

Использование:
    from docstoolkit.federation import PortalRegistry, query_federation

    reg = PortalRegistry()
    reg.register("alice", "https://alice.example.com/portal")
    reg.register("bob",   "https://bob.example.com/portal")

    results = query_federation("memory architecture", registries=[reg])
    # → собирает результаты от всех peer'ов
"""
from docstoolkit.federation.registry import PortalRegistry, Peer
from docstoolkit.federation.adapter import Adapter, HTTPAdapter, LocalAdapter
from docstoolkit.federation.query import query_federation, FederatedResult

__all__ = [
    "PortalRegistry", "Peer",
    "Adapter", "HTTPAdapter", "LocalAdapter",
    "query_federation", "FederatedResult",
]
