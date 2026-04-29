"""Тесты federation."""
import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).parent.parent))

from docstoolkit.federation import PortalRegistry, query_federation
from docstoolkit.federation.adapter import (
    HTTPAdapter, LocalAdapter, MockAdapter, make_adapter,
)
from docstoolkit.federation.registry import Peer


def test_peer_dataclass():
    p = Peer(name="x", url="http://x", kind="http",
             capabilities=["search", "rag"])
    assert p.name == "x"
    assert "search" in p.capabilities


def test_registry_save_load(tmp_path):
    reg = PortalRegistry(path=tmp_path / "fed.json")
    reg.register("alice", "http://alice", capabilities=["search"])
    reg.register("bob", "http://bob")

    assert len(reg.list()) == 2
    assert reg.get("alice").url == "http://alice"

    # Re-load from file
    reg2 = PortalRegistry(path=tmp_path / "fed.json")
    assert len(reg2.list()) == 2


def test_registry_unregister(tmp_path):
    reg = PortalRegistry(path=tmp_path / "fed.json")
    reg.register("x", "http://x")
    assert reg.unregister("x") is True
    assert reg.get("x") is None
    assert reg.unregister("x") is False  # already removed


def test_mock_adapter():
    a = MockAdapter(results=[
        {"title": "T1", "path": "p1.md", "score": 0.9},
        {"title": "T2", "path": "p2.md", "score": 0.5},
    ])
    results = a.search("test", top_k=10)
    assert len(results) == 2
    assert a.health()["ok"] is True


def test_make_adapter_dispatch():
    p_http = Peer("h", "http://x", kind="http")
    p_local = Peer("l", "local://", kind="local")
    p_mock = Peer("m", "mock://", kind="mock")

    assert isinstance(make_adapter(p_http), HTTPAdapter)
    assert isinstance(make_adapter(p_local), LocalAdapter)
    assert isinstance(make_adapter(p_mock), MockAdapter)


def test_query_federation_with_mocks(tmp_path):
    reg = PortalRegistry(path=tmp_path / "fed.json")
    # Register peers с фиктивными URL
    reg.register("p1", "mock://1", kind="mock")
    reg.register("p2", "mock://2", kind="mock")

    result = query_federation("test", registries=[reg])
    assert result.peers_queried == 2
    assert result.duration_ms >= 0


def test_query_federation_empty():
    """Без peers возвращает пустой результат."""
    result = query_federation("x", registries=[])
    assert result.peers_queried == 0
    assert result.results == []


def test_http_adapter_handles_error():
    """HTTPAdapter не падает при недоступном peer."""
    a = HTTPAdapter("http://nonexistent.invalid.example", timeout=1)
    results = a.search("test")
    assert results == []
