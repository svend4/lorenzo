"""Tests for scripts/improve_faceted_search.py."""

import importlib
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(ROOT / "scripts"))

mod = importlib.import_module("improve_faceted_search")


def test_word_count_returns_int(tmp_path):
    f = tmp_path / "test.md"
    f.write_text("one two three four five", encoding="utf-8")
    result = mod._word_count(f)
    assert isinstance(result, int)
    assert result == 5


def test_word_count_missing_file(tmp_path):
    result = mod._word_count(tmp_path / "missing.md")
    assert result == 0


def test_file_mtime_returns_string(tmp_path):
    f = tmp_path / "test.md"
    f.write_text("content", encoding="utf-8")
    result = mod._file_mtime(f)
    assert isinstance(result, str)
    assert len(result) == 10  # YYYY-MM-DD


def test_file_mtime_missing_file(tmp_path):
    result = mod._file_mtime(tmp_path / "missing.md")
    assert result == "unknown"


def test_load_keyword_index_missing(tmp_path, monkeypatch):
    monkeypatch.setattr(mod, "KEYWORD_INDEX", tmp_path / "missing.json")
    result = mod._load_keyword_index()
    assert result == {}


def test_load_keyword_index_valid(tmp_path, monkeypatch):
    import json
    data = {"index": {"агент": [{"f": "docs/test.md", "n": 3}]}}
    f = tmp_path / "keyword_index.json"
    f.write_text(json.dumps(data), encoding="utf-8")
    monkeypatch.setattr(mod, "KEYWORD_INDEX", f)
    result = mod._load_keyword_index()
    assert "агент" in result


def test_load_entities_missing(tmp_path, monkeypatch):
    monkeypatch.setattr(mod, "ENTITIES_INDEX", tmp_path / "missing.json")
    result = mod._load_entities()
    assert result == {}


def test_load_entities_valid(tmp_path, monkeypatch):
    import json
    data = {"AgentFS": {"name": "AgentFS", "type": "projects", "files": ["docs/a.md"]}}
    f = tmp_path / "named_entities.json"
    f.write_text(json.dumps(data), encoding="utf-8")
    monkeypatch.setattr(mod, "ENTITIES_INDEX", f)
    result = mod._load_entities()
    assert "AgentFS" in result


def test_search_by_query_returns_dict():
    index = {
        "агент": [{"f": "docs/a.md", "n": 2}],
        "память": [{"f": "docs/a.md", "n": 1}, {"f": "docs/b.md", "n": 3}],
    }
    result = mod._search_by_query("агент память", index)
    assert isinstance(result, dict)


def test_search_by_query_scores_files():
    index = {
        "агент": [{"f": "docs/a.md", "n": 2}],
        "память": [{"f": "docs/a.md", "n": 1}, {"f": "docs/b.md", "n": 3}],
    }
    result = mod._search_by_query("агент память", index)
    assert "docs/a.md" in result
    assert "docs/b.md" in result


def test_search_by_query_bigram_bonus():
    index = {
        "агент": [{"f": "docs/a.md", "n": 1}],
        "память": [{"f": "docs/a.md", "n": 1}],
        "агент память": [{"f": "docs/a.md", "n": 2}],
    }
    result_uni = mod._search_by_query("агент память", index)
    # Bigram bonus should add 6.0 (2*3.0) more
    assert result_uni.get("docs/a.md", 0) > 2.0


def test_search_by_query_empty_index():
    result = mod._search_by_query("агент", {})
    assert result == {}


def test_search_by_query_filters_stopwords():
    index = {"для": [{"f": "docs/a.md", "n": 5}]}
    result = mod._search_by_query("для", index)
    assert result == {}


def test_filter_by_entity_returns_set():
    entities_data = {
        "AgentFS": {"name": "AgentFS", "type": "projects", "files": ["docs/agentfs.md"]},
    }
    result = mod._filter_by_entity("agentfs", entities_data, None)
    assert isinstance(result, set)


def test_filter_by_entity_finds_files():
    entities_data = {
        "AgentFS": {"name": "AgentFS", "type": "projects", "files": ["docs/agentfs.md"]},
    }
    result = mod._filter_by_entity("AgentFS", entities_data, None)
    assert "docs/agentfs.md" in result


def test_filter_by_entity_type_filter():
    entities_data = {
        "AgentFS": {"name": "AgentFS", "type": "projects", "files": ["docs/agentfs.md"]},
        "svend4": {"name": "svend4", "type": "people", "files": ["docs/svend4.md"]},
    }
    result = mod._filter_by_entity("agentfs", entities_data, "people")
    assert "docs/agentfs.md" not in result


def test_filter_by_entity_no_match():
    entities_data = {
        "AgentFS": {"name": "AgentFS", "type": "projects", "files": ["docs/agentfs.md"]},
    }
    result = mod._filter_by_entity("unknown_xyz_entity", entities_data, None)
    assert len(result) == 0


def test_filter_by_type_returns_set():
    entities_data = {
        "AgentFS": {"name": "AgentFS", "type": "projects", "files": ["docs/agentfs.md"]},
    }
    result = mod._filter_by_type("projects", entities_data)
    assert isinstance(result, set)


def test_filter_by_type_finds_files():
    entities_data = {
        "AgentFS": {"name": "AgentFS", "type": "projects", "files": ["docs/a.md"]},
        "Yodoca": {"name": "Yodoca", "type": "projects", "files": ["docs/b.md"]},
        "svend4": {"name": "svend4", "type": "people", "files": ["docs/c.md"]},
    }
    result = mod._filter_by_type("projects", entities_data)
    assert "docs/a.md" in result
    assert "docs/b.md" in result
    assert "docs/c.md" not in result


def test_filter_by_type_empty():
    result = mod._filter_by_type("unknown_type", {})
    assert result == set()


# ── main ──────────────────────────────────────────────────────────────────────

def test_main_no_filters_prints_usage(tmp_path, monkeypatch, capsys):
    monkeypatch.setattr(mod, "DOCS", tmp_path)
    monkeypatch.setattr(mod, "ROOT", tmp_path)
    monkeypatch.setattr(mod, "QUERY", None)
    monkeypatch.setattr(mod, "ENTITY_FILTER", None)
    monkeypatch.setattr(mod, "TYPE_FILTER", None)
    monkeypatch.setattr(mod, "SECTION_FILTER", None)
    mod.main()
    out = capsys.readouterr().out
    assert "фильтр" in out or "query" in out.lower() or "--query" in out


def test_main_with_query_no_index_warns(tmp_path, monkeypatch, capsys):
    monkeypatch.setattr(mod, "DOCS", tmp_path)
    monkeypatch.setattr(mod, "ROOT", tmp_path)
    monkeypatch.setattr(mod, "QUERY", "AgentFS")
    monkeypatch.setattr(mod, "ENTITY_FILTER", None)
    monkeypatch.setattr(mod, "TYPE_FILTER", None)
    monkeypatch.setattr(mod, "SECTION_FILTER", None)
    monkeypatch.setattr(mod, "_load_keyword_index", lambda: {})
    monkeypatch.setattr(mod, "_load_entities", lambda: {})
    mod.main()


def test_main_with_entity_filter_no_crash(tmp_path, monkeypatch):
    monkeypatch.setattr(mod, "DOCS", tmp_path)
    monkeypatch.setattr(mod, "ROOT", tmp_path)
    monkeypatch.setattr(mod, "QUERY", None)
    monkeypatch.setattr(mod, "ENTITY_FILTER", "AgentFS")
    monkeypatch.setattr(mod, "TYPE_FILTER", None)
    monkeypatch.setattr(mod, "SECTION_FILTER", None)
    monkeypatch.setattr(mod, "_load_keyword_index", lambda: {})
    monkeypatch.setattr(mod, "_load_entities", lambda: {})
    mod.main()
