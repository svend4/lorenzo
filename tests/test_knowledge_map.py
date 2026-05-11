"""Tests for scripts/improve_knowledge_map.py."""

import importlib
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(ROOT / "scripts"))

mod = importlib.import_module("improve_knowledge_map")


def test_read_md_missing(tmp_path, monkeypatch):
    monkeypatch.setattr(mod, "DOCS", tmp_path)
    result = mod._read_md("missing.md")
    assert result == ""


def test_read_md_existing(tmp_path, monkeypatch):
    monkeypatch.setattr(mod, "DOCS", tmp_path)
    f = tmp_path / "test.md"
    f.write_text("# Hello\nworld", encoding="utf-8")
    result = mod._read_md("test.md")
    assert "Hello" in result


def test_read_json_missing(tmp_path, monkeypatch):
    monkeypatch.setattr(mod, "DOCS", tmp_path)
    result = mod._read_json("missing.json")
    assert result == {}


def test_read_json_valid(tmp_path, monkeypatch):
    import json
    monkeypatch.setattr(mod, "DOCS", tmp_path)
    f = tmp_path / "data.json"
    f.write_text(json.dumps({"key": "value"}), encoding="utf-8")
    result = mod._read_json("data.json")
    assert result == {"key": "value"}


def test_read_json_invalid(tmp_path, monkeypatch):
    monkeypatch.setattr(mod, "DOCS", tmp_path)
    f = tmp_path / "bad.json"
    f.write_text("not json", encoding="utf-8")
    result = mod._read_json("bad.json")
    assert result == {}


def test_extract_score_finds_value():
    text = "Health score: **87/100**"
    result = mod._extract_score(text, "Health score")
    assert result == "87/100"


def test_extract_score_missing_returns_dash():
    result = mod._extract_score("no score here", "Metrics")
    assert result == "—"


def test_extract_score_percentage():
    text = "Coverage: **92%**"
    result = mod._extract_score(text, "Coverage")
    assert "92" in result


def test_section_stats_returns_list(tmp_path, monkeypatch):
    monkeypatch.setattr(mod, "DOCS", tmp_path)
    subdir = tmp_path / "01-svyazi"
    subdir.mkdir()
    (subdir / "doc.md").write_text("one two three", encoding="utf-8")
    result = mod._section_stats(tmp_path)
    assert isinstance(result, list)


def test_section_stats_counts_files(tmp_path, monkeypatch):
    monkeypatch.setattr(mod, "DOCS", tmp_path)
    subdir = tmp_path / "01-svyazi"
    subdir.mkdir()
    (subdir / "doc1.md").write_text("alpha beta gamma", encoding="utf-8")
    (subdir / "doc2.md").write_text("delta epsilon zeta", encoding="utf-8")
    result = mod._section_stats(tmp_path)
    assert len(result) == 1
    assert result[0]["files"] == 2
    assert result[0]["name"] == "01-svyazi"


def test_section_stats_calculates_words(tmp_path, monkeypatch):
    monkeypatch.setattr(mod, "DOCS", tmp_path)
    subdir = tmp_path / "01-test"
    subdir.mkdir()
    (subdir / "doc.md").write_text("one two three four five", encoding="utf-8")
    result = mod._section_stats(tmp_path)
    assert result[0]["words"] == 5


def test_section_stats_skips_hidden(tmp_path, monkeypatch):
    monkeypatch.setattr(mod, "DOCS", tmp_path)
    hidden = tmp_path / ".hidden"
    hidden.mkdir()
    (hidden / "doc.md").write_text("content", encoding="utf-8")
    result = mod._section_stats(tmp_path)
    assert all(s["name"] != ".hidden" for s in result)


def test_section_stats_avg_words(tmp_path, monkeypatch):
    monkeypatch.setattr(mod, "DOCS", tmp_path)
    subdir = tmp_path / "section"
    subdir.mkdir()
    (subdir / "a.md").write_text("one two three four", encoding="utf-8")
    (subdir / "b.md").write_text("five six", encoding="utf-8")
    result = mod._section_stats(tmp_path)
    assert result[0]["avg_words"] == 3  # (4+2) // 2


def test_corpus_stats_returns_dict(tmp_path, monkeypatch):
    monkeypatch.setattr(mod, "DOCS", tmp_path)
    (tmp_path / "doc.md").write_text("hello world", encoding="utf-8")
    result = mod._corpus_stats(tmp_path)
    assert isinstance(result, dict)
    assert "files" in result
    assert "words" in result


def test_corpus_stats_counts(tmp_path, monkeypatch):
    monkeypatch.setattr(mod, "DOCS", tmp_path)
    (tmp_path / "a.md").write_text("one two three", encoding="utf-8")
    (tmp_path / "b.md").write_text("four five", encoding="utf-8")
    result = mod._corpus_stats(tmp_path)
    assert result["files"] == 2
    assert result["words"] == 5


def test_skip_count_is_set():
    assert hasattr(mod, "SKIP_COUNT")
    assert isinstance(mod.SKIP_COUNT, set)
    assert "KNOWLEDGE_MAP.md" in mod.SKIP_COUNT


# ── main ──────────────────────────────────────────────────────────────────────

def test_main_creates_knowledge_map_md(tmp_path, monkeypatch):
    monkeypatch.setattr(mod, "DOCS", tmp_path)
    monkeypatch.setattr(mod, "ROOT", tmp_path)
    (tmp_path / "doc.md").write_text("# AgentFS\n\nContent here.", encoding="utf-8")
    mod.main()
    assert (tmp_path / "KNOWLEDGE_MAP.md").exists()


def test_main_knowledge_map_has_content(tmp_path, monkeypatch):
    monkeypatch.setattr(mod, "DOCS", tmp_path)
    monkeypatch.setattr(mod, "ROOT", tmp_path)
    (tmp_path / "doc.md").write_text("# AgentFS\n\nContent here.", encoding="utf-8")
    mod.main()
    text = (tmp_path / "KNOWLEDGE_MAP.md").read_text(encoding="utf-8")
    assert "# " in text


def test_main_empty_docs(tmp_path, monkeypatch):
    monkeypatch.setattr(mod, "DOCS", tmp_path)
    monkeypatch.setattr(mod, "ROOT", tmp_path)
    mod.main()
    assert (tmp_path / "KNOWLEDGE_MAP.md").exists()


def test_main_knowledge_map_starts_with_heading(tmp_path, monkeypatch):
    monkeypatch.setattr(mod, "DOCS", tmp_path)
    monkeypatch.setattr(mod, "ROOT", tmp_path)
    mod.main()
    text = (tmp_path / "KNOWLEDGE_MAP.md").read_text(encoding="utf-8")
    assert text.strip().startswith("#")
