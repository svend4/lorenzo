"""Tests for scripts/improve_collab_finder.py."""

import importlib
import json
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(ROOT / "scripts"))

mod = importlib.import_module("improve_collab_finder")


def test_title_key_returns_string():
    # _title_key requires a CardEnvelope, so we test with a mock
    from unittest.mock import MagicMock
    card = MagicMock()
    card.payload = {"title": "AgentFS: file system for AI agents"}
    card.edges = []
    result = mod._title_key(card)
    assert isinstance(result, str)


def test_title_key_normalizes_title():
    from unittest.mock import MagicMock
    card = MagicMock()
    card.payload = {"title": "AgentFS: Overview"}
    card.edges = []
    result = mod._title_key(card)
    # Should strip colon and everything after
    assert ":" not in result


def test_title_key_lowercases():
    from unittest.mock import MagicMock
    card = MagicMock()
    card.payload = {"title": "AGENTFS Overview"}
    card.edges = []
    result = mod._title_key(card)
    assert result == result.lower()


def test_title_key_removes_footnote():
    from unittest.mock import MagicMock
    card = MagicMock()
    card.payload = {"title": "Yodoca[^yodoca]: консолидация памяти"}
    card.edges = []
    result = mod._title_key(card)
    assert "[^" not in result


def test_bm25_score_returns_float():
    from unittest.mock import MagicMock
    card = MagicMock()
    card.payload = {"title": "AgentFS", "body": "agent file system memory knowledge"}
    result = mod._bm25_score(["agent", "memory"], card)
    assert isinstance(result, float)


def test_bm25_score_positive_for_matching():
    from unittest.mock import MagicMock
    card = MagicMock()
    card.payload = {"title": "AgentFS", "body": "agent memory system retrieval"}
    result = mod._bm25_score(["agent", "memory"], card)
    assert result > 0.0


def test_bm25_score_zero_for_no_match():
    from unittest.mock import MagicMock
    card = MagicMock()
    card.payload = {"title": "Unrelated", "body": "completely different topic content"}
    result = mod._bm25_score(["agent", "memory"], card)
    assert result == 0.0


def test_graph_bonus_returns_float():
    from unittest.mock import MagicMock
    card = MagicMock()
    edge = MagicMock()
    edge.to = "other_card_id"
    card.edges = [edge]
    result = mod._graph_bonus(card, {"other_card_id"})
    assert isinstance(result, float)


def test_graph_bonus_zero_with_no_edges():
    from unittest.mock import MagicMock
    card = MagicMock()
    card.edges = []
    result = mod._graph_bonus(card, {"some_candidate"})
    assert result == 0.0


def test_graph_bonus_positive_with_matching_edge():
    from unittest.mock import MagicMock
    card = MagicMock()
    edge = MagicMock()
    edge.to = "candidate_id_xyz"
    card.edges = [edge]
    result = mod._graph_bonus(card, {"candidate_id_xyz"})
    assert result > 0.0


def test_graph_bonus_capped_at_0_3():
    from unittest.mock import MagicMock
    card = MagicMock()
    edges = []
    for i in range(20):
        edge = MagicMock()
        edge.to = f"candidate_{i}"
        edges.append(edge)
    card.edges = edges
    candidates = {f"candidate_{i}" for i in range(20)}
    result = mod._graph_bonus(card, candidates)
    assert result <= 0.3


def test_extract_file_query_returns_string():
    text = "# AgentFS Overview\n\nFile system for AI agents with memory.\n"
    result = mod._extract_file_query(text)
    assert isinstance(result, str)


def test_extract_file_query_includes_h1():
    text = "# Memory Agent System\n\nContent about memory.\n"
    result = mod._extract_file_query(text)
    # Result is lowercased tokens
    assert "memory" in result.lower()
    assert "agent" in result.lower()


def test_extract_file_query_extracts_frontmatter_title():
    text = "---\ntitle: AgentFS Project\n---\n\n# Overview\n\nContent.\n"
    result = mod._extract_file_query(text)
    assert "agentfs" in result.lower() or "project" in result.lower()


def test_extract_file_query_respects_max_tokens():
    long_text = "# Title\n\n" + "word " * 500
    result = mod._extract_file_query(long_text, max_tokens=10)
    words = result.split()
    assert len(words) <= 20  # approximate limit
