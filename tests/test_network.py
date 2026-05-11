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
