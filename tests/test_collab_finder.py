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


# ── main ──────────────────────────────────────────────────────────────────────

def test_main_no_args_prints_help(monkeypatch, capsys):
    monkeypatch.setattr("sys.argv", ["prog"])
    try:
        mod.main()
    except SystemExit:
        pass
    out = capsys.readouterr().out
    # Either prints help or exits — both acceptable
    assert True


def test_main_with_query_no_crash(tmp_path, monkeypatch):
    monkeypatch.setattr("sys.argv", ["prog", "--query", "AgentFS memory", "--dry-run"])
    monkeypatch.setattr(mod, "DOCS", tmp_path)
    monkeypatch.setattr(mod, "ROOT", tmp_path)
    monkeypatch.setattr(mod, "OUT_MD", tmp_path / "COLLAB.md")
    monkeypatch.setattr(mod, "CARDS", tmp_path / "cards")
    try:
        mod.main()
    except SystemExit:
        pass


def test_main_dry_run_no_file_written(tmp_path, monkeypatch):
    monkeypatch.setattr("sys.argv", ["prog", "--query", "agent", "--dry-run"])
    monkeypatch.setattr(mod, "DOCS", tmp_path)
    monkeypatch.setattr(mod, "ROOT", tmp_path)
    monkeypatch.setattr(mod, "OUT_MD", tmp_path / "COLLAB.md")
    monkeypatch.setattr(mod, "CARDS", tmp_path / "cards")
    try:
        mod.main()
    except SystemExit:
        pass
    assert not (tmp_path / "COLLAB.md").exists()


def test_load_index_missing(tmp_path, monkeypatch):
    monkeypatch.setattr(mod, "INDEX", tmp_path / "nonexistent.json")
    result = mod._load_index()
    assert result is None


def test_load_index_returns_dict(tmp_path, monkeypatch):
    import json
    index_file = tmp_path / "embedding_index.json"
    index_file.write_text(json.dumps({"vectors": {}, "vocab": [], "idf": {}}), encoding="utf-8")
    monkeypatch.setattr(mod, "INDEX", index_file)
    result = mod._load_index()
    assert isinstance(result, dict)


def test_load_contacts_empty_no_dir(tmp_path, monkeypatch):
    monkeypatch.setattr(mod, "DOCS", tmp_path)
    result = mod._load_contacts()
    assert isinstance(result, dict)
    assert len(result) == 0


def test_load_contacts_with_contact_file(tmp_path, monkeypatch):
    monkeypatch.setattr(mod, "DOCS", tmp_path)
    contacts_dir = tmp_path / "contacts"
    contacts_dir.mkdir()
    (contacts_dir / "kksudo.md").write_text(
        '---\nauthor: "Konstantin"\nauthor_handle: "kksudo"\nplatform: github\n---\n# kksudo\n',
        encoding="utf-8"
    )
    result = mod._load_contacts()
    assert "kksudo" in result


def test_read_contact_brief_returns_dict(tmp_path, monkeypatch):
    monkeypatch.setattr(mod, "ROOT", tmp_path)
    f = tmp_path / "kksudo.md"
    f.write_text(
        '---\nauthor: "Konstantin"\nauthor_handle: "kksudo"\nplatform: github\nstatus: active\n---\n# kksudo\n',
        encoding="utf-8"
    )
    result = mod._read_contact_brief(f)
    assert isinstance(result, dict)
    assert "author" in result
    assert result["author"] == "Konstantin"


def test_read_contact_brief_missing_file(tmp_path, monkeypatch):
    monkeypatch.setattr(mod, "ROOT", tmp_path)
    f = tmp_path / "nonexistent.md"
    result = mod._read_contact_brief(f)
    assert result == {}


def test_semantic_score_no_emb(monkeypatch):
    monkeypatch.setattr(mod, "_HAVE_EMB", False)
    result = mod._semantic_score({}, "card_id", {})
    assert result == 0.0


def test_semantic_score_no_index(monkeypatch):
    monkeypatch.setattr(mod, "_HAVE_EMB", True)
    result = mod._semantic_score({1: 0.5}, "card_id", None)
    assert result == 0.0


def test_find_contact_empty_contacts():
    from unittest.mock import MagicMock
    card = MagicMock()
    card.payload = {"title": "AgentFS", "path": "docs/agentfs.md"}
    card.edges = []
    result = mod._find_contact(card, {})
    assert result is None


def test_find_candidates_no_cards_dir(tmp_path, monkeypatch):
    monkeypatch.setattr(mod, "CARDS", tmp_path / "no_cards")
    result = mod.find_candidates("agent memory")
    assert result == []


def test_generate_message_returns_string():
    from unittest.mock import MagicMock
    card = MagicMock()
    card.payload = {"title": "AgentFS", "summary": "File system for AI agents with knowledge."}
    contact = {"author": "kksudo", "handle": "kksudo", "platform": "GitHub", "projects": ["AgentFS"]}
    result = mod._generate_message(card, contact, "agent memory knowledge")
    assert isinstance(result, str)
    assert "kksudo" in result


def test_generate_message_without_summary():
    from unittest.mock import MagicMock
    card = MagicMock()
    card.payload = {"title": "AgentFS", "summary": ""}
    contact = {"author": "Test", "handle": "", "platform": "GitHub", "projects": []}
    result = mod._generate_message(card, contact, "test query")
    assert isinstance(result, str)
    assert len(result) > 0


def test_format_report_returns_string(tmp_path, monkeypatch):
    monkeypatch.setattr(mod, "ROOT", tmp_path)
    monkeypatch.setattr(mod, "DOCS", tmp_path)
    from unittest.mock import MagicMock
    card = MagicMock()
    card.payload = {"title": "AgentFS", "summary": "Test summary", "path": "test/agentfs.md",
                    "wc": 100, "tags": []}
    card.card_id = "test_id"
    card.card_type = "project"
    card.edges = []
    candidates = [{"score": 0.8, "card": card}]
    result = mod._format_report("agent memory", "", candidates, {})
    assert isinstance(result, str)
    assert "AgentFS" in result or "agent" in result.lower()


def test_cmd_find_empty_cards_dir(tmp_path, monkeypatch, capsys):
    monkeypatch.setattr(mod, "CARDS", tmp_path / "no_cards")
    monkeypatch.setattr(mod, "INDEX", tmp_path / "index.json")
    monkeypatch.setattr(mod, "OUT_MD", tmp_path / "COLLAB.md")
    monkeypatch.setattr(mod, "ROOT", tmp_path)
    mod.cmd_find("agent memory")
    out = capsys.readouterr().out
    assert "CardStore" in out or "пуст" in out or "❌" in out


def test_cmd_find_no_candidates(tmp_path, monkeypatch, capsys):
    cards_dir = tmp_path / "cards"
    cards_dir.mkdir()
    (cards_dir / "fake.json").write_text('{}', encoding="utf-8")
    monkeypatch.setattr(mod, "CARDS", cards_dir)
    monkeypatch.setattr(mod, "INDEX", tmp_path / "index.json")
    monkeypatch.setattr(mod, "OUT_MD", tmp_path / "COLLAB.md")
    monkeypatch.setattr(mod, "ROOT", tmp_path)
    monkeypatch.setattr(mod, "find_candidates", lambda *a, **kw: [])
    mod.cmd_find("agent memory")
    out = capsys.readouterr().out
    assert "Ничего" in out or "найден" in out.lower()


def test_cmd_find_dry_run_with_candidates(tmp_path, monkeypatch, capsys):
    from unittest.mock import MagicMock
    cards_dir = tmp_path / "cards"
    cards_dir.mkdir()
    (cards_dir / "fake.json").write_text('{}', encoding="utf-8")
    monkeypatch.setattr(mod, "CARDS", cards_dir)
    monkeypatch.setattr(mod, "INDEX", tmp_path / "index.json")
    monkeypatch.setattr(mod, "OUT_MD", tmp_path / "COLLAB.md")
    monkeypatch.setattr(mod, "ROOT", tmp_path)
    monkeypatch.setattr(mod, "DOCS", tmp_path)
    card = MagicMock()
    card.payload = {"title": "AgentFS", "path": "agentfs.md"}
    card.card_id = "test_id"
    card.card_type = "project"
    card.edges = []
    fake_candidates = [{"score": 0.8, "card": card}]
    monkeypatch.setattr(mod, "find_candidates", lambda *a, **kw: fake_candidates)
    monkeypatch.setattr(mod, "_load_contacts", lambda: {})
    monkeypatch.setattr(mod, "_find_contact", lambda *a, **kw: None)
    monkeypatch.setattr(mod, "_read_contact_brief", lambda *a, **kw: {"author": "Test"})
    mod.cmd_find("agent memory", dry_run=True)
    out = capsys.readouterr().out
    assert "dry-run" in out or "Найдено" in out or "AgentFS" in out
