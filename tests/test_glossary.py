"""
Тесты для scripts/improve_glossary.py.

Покрытие:
  - extract_urls() — извлечение HTTP URL из текста
  - find_mentions() — поиск упоминаний терминов в docs/*.md
"""

import importlib
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(ROOT / "scripts"))

mod = importlib.import_module("improve_glossary")

# ── extract_urls ──────────────────────────────────────────────────────────────

def test_extract_urls_returns_list():
    result = mod.extract_urls("Some text here.")
    assert isinstance(result, list)


def test_extract_urls_finds_http():
    text = "See https://example.com for details."
    result = mod.extract_urls(text)
    assert any("example.com" in u for u in result)


def test_extract_urls_finds_github():
    text = "See https://github.com/user/repo here."
    result = mod.extract_urls(text)
    assert any("github.com/user/repo" in u for u in result)


def test_extract_urls_empty_text():
    assert mod.extract_urls("") == []


def test_extract_urls_no_urls():
    assert mod.extract_urls("Just plain text here.") == []


def test_extract_urls_multiple_urls():
    text = "See https://example.com and https://github.com/user/repo"
    result = mod.extract_urls(text)
    assert len(result) == 2


def test_extract_urls_http_and_https():
    text = "http://old.example.com and https://new.example.com"
    result = mod.extract_urls(text)
    assert len(result) == 2


# ── find_mentions ─────────────────────────────────────────────────────────────

def test_find_mentions_returns_dict(tmp_path, monkeypatch):
    monkeypatch.setattr(mod, "DOCS", tmp_path)
    monkeypatch.setattr(mod, "ROOT", tmp_path.parent)
    result = mod.find_mentions("", ["AgentFS"])
    assert isinstance(result, dict)


def test_find_mentions_empty_docs(tmp_path, monkeypatch):
    monkeypatch.setattr(mod, "DOCS", tmp_path)
    monkeypatch.setattr(mod, "ROOT", tmp_path.parent)
    result = mod.find_mentions("", ["AgentFS"])
    assert "AgentFS" not in result or result["AgentFS"] == []


def test_find_mentions_finds_term(tmp_path, monkeypatch):
    monkeypatch.setattr(mod, "DOCS", tmp_path)
    monkeypatch.setattr(mod, "ROOT", tmp_path.parent)
    f = tmp_path / "doc.md"
    f.write_text("# Title\n\nAgentFS is a great tool.", encoding="utf-8")
    result = mod.find_mentions("", ["AgentFS"])
    assert "AgentFS" in result
    assert len(result["AgentFS"]) == 1


def test_find_mentions_case_insensitive(tmp_path, monkeypatch):
    monkeypatch.setattr(mod, "DOCS", tmp_path)
    monkeypatch.setattr(mod, "ROOT", tmp_path.parent)
    f = tmp_path / "doc.md"
    f.write_text("agentfs is here", encoding="utf-8")
    result = mod.find_mentions("", ["AgentFS"])
    assert "AgentFS" in result
    assert len(result["AgentFS"]) >= 1


def test_find_mentions_missing_term(tmp_path, monkeypatch):
    monkeypatch.setattr(mod, "DOCS", tmp_path)
    monkeypatch.setattr(mod, "ROOT", tmp_path.parent)
    f = tmp_path / "doc.md"
    f.write_text("# Title\n\nNo relevant content here.", encoding="utf-8")
    result = mod.find_mentions("", ["AgentFS"])
    assert result.get("AgentFS", []) == []


def test_find_mentions_multiple_files(tmp_path, monkeypatch):
    monkeypatch.setattr(mod, "DOCS", tmp_path)
    monkeypatch.setattr(mod, "ROOT", tmp_path.parent)
    (tmp_path / "a.md").write_text("AgentFS here", encoding="utf-8")
    (tmp_path / "b.md").write_text("AgentFS there", encoding="utf-8")
    result = mod.find_mentions("", ["AgentFS"])
    assert len(result["AgentFS"]) == 2


# ── main ──────────────────────────────────────────────────────────────────────

def test_make_glossary_creates_file(tmp_path, monkeypatch):
    monkeypatch.setattr(mod, "DOCS", tmp_path)
    monkeypatch.setattr(mod, "ROOT", tmp_path)
    (tmp_path / "doc.md").write_text("# AgentFS\n\nContent.", encoding="utf-8")
    mod.make_glossary()
    assert (tmp_path / "GLOSSARY.md").exists()


def test_make_authors_creates_file(tmp_path, monkeypatch):
    monkeypatch.setattr(mod, "DOCS", tmp_path)
    monkeypatch.setattr(mod, "ROOT", tmp_path)
    (tmp_path / "doc.md").write_text("# AgentFS\n\nContent.", encoding="utf-8")
    mod.make_authors()
    assert (tmp_path / "AUTHORS.md").exists()


def test_make_glossary_has_content(tmp_path, monkeypatch):
    monkeypatch.setattr(mod, "DOCS", tmp_path)
    monkeypatch.setattr(mod, "ROOT", tmp_path)
    (tmp_path / "doc.md").write_text("# AgentFS\n\nContent.", encoding="utf-8")
    mod.make_glossary()
    text = (tmp_path / "GLOSSARY.md").read_text(encoding="utf-8")
    assert "# " in text


def test_make_url_index_creates_file(tmp_path, monkeypatch):
    monkeypatch.setattr(mod, "DOCS", tmp_path)
    monkeypatch.setattr(mod, "ROOT", tmp_path)
    (tmp_path / "doc.md").write_text("# Title\n\nSee https://github.com/user/repo here.", encoding="utf-8")
    mod.make_url_index()
    assert (tmp_path / "LINKS.md").exists()
