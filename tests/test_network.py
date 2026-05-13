"""Tests for scripts/improve_network.py."""

import importlib
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(ROOT / "scripts"))

mod = importlib.import_module("improve_network")


def test_find_mentions_returns_int():
    result = mod.find_mentions("kksudo wrote AgentFS and kksudo maintains it", "kksudo")
    assert isinstance(result, int)


def test_find_mentions_counts_correctly():
    result = mod.find_mentions("kksudo wrote AgentFS and kksudo maintains it", "kksudo")
    assert result == 2


def test_find_mentions_zero():
    result = mod.find_mentions("some text without the name", "kksudo")
    assert result == 0


def test_find_mentions_case_insensitive():
    result = mod.find_mentions("KKSUDO created AgentFS and kksudo maintains it", "kksudo")
    assert result == 2


def test_centrality_returns_int():
    co_matrix = {("A", "B"): 3, ("B", "C"): 2}
    result = mod.centrality(co_matrix, "B")
    assert isinstance(result, int)


def test_centrality_sums_edges():
    co_matrix = {("A", "B"): 3, ("B", "C"): 2}
    result = mod.centrality(co_matrix, "B")
    assert result == 5


def test_centrality_zero_for_unknown():
    co_matrix = {("A", "B"): 3}
    result = mod.centrality(co_matrix, "Z")
    assert result == 0


def test_authors_dict_exists():
    assert isinstance(mod.AUTHORS, dict)
    assert len(mod.AUTHORS) > 0


def test_projects_list_exists():
    assert isinstance(mod.PROJECTS, list)
    assert len(mod.PROJECTS) > 0


def test_all_nodes_includes_authors():
    for name in mod.AUTHORS.values():
        assert name in mod.ALL_NODES


def test_all_nodes_includes_projects():
    for proj in mod.PROJECTS:
        assert proj in mod.ALL_NODES


# ── main ──────────────────────────────────────────────────────────────────────

def test_main_creates_network_md(tmp_path, monkeypatch):
    monkeypatch.setattr(mod, "DOCS", tmp_path)
    monkeypatch.setattr(mod, "ROOT", tmp_path)
    (tmp_path / "doc.md").write_text("# AgentFS\n\nkksudo builds AgentFS memory.", encoding="utf-8")
    mod.main()
    assert (tmp_path / "NETWORK.md").exists()


def test_main_creates_dot_file(tmp_path, monkeypatch):
    monkeypatch.setattr(mod, "DOCS", tmp_path)
    monkeypatch.setattr(mod, "ROOT", tmp_path)
    (tmp_path / "doc.md").write_text("# AgentFS\n\nAgentFS and Svyazi together.", encoding="utf-8")
    mod.main()
    assert (tmp_path / "network.dot").exists()


def test_main_network_md_has_content(tmp_path, monkeypatch):
    monkeypatch.setattr(mod, "DOCS", tmp_path)
    monkeypatch.setattr(mod, "ROOT", tmp_path)
    (tmp_path / "doc.md").write_text("# AgentFS\n\nkksudo AgentFS Svyazi memory.", encoding="utf-8")
    mod.main()
    text = (tmp_path / "NETWORK.md").read_text(encoding="utf-8")
    assert "Сеть" in text or "сеть" in text or "Авторы" in text or "Узлов" in text


def test_main_empty_docs(tmp_path, monkeypatch):
    monkeypatch.setattr(mod, "DOCS", tmp_path)
    monkeypatch.setattr(mod, "ROOT", tmp_path)
    mod.main()
    assert (tmp_path / "NETWORK.md").exists()
