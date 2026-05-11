"""Tests for scripts/improve_timeline_events.py."""

import importlib
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(ROOT / "scripts"))

mod = importlib.import_module("improve_timeline_events")


def test_extract_context_returns_string():
    result = mod._extract_context("This is a test sentence about events.")
    assert isinstance(result, str)


def test_extract_context_strips_markdown():
    result = mod._extract_context("**Bold** _italic_ `code` text here")
    assert "**" not in result
    assert "`" not in result


def test_extract_context_replaces_url():
    result = mod._extract_context("See https://example.com for details.")
    assert "https" not in result
    assert "[URL]" in result


def test_extract_context_max_200():
    long_text = "word " * 100
    result = mod._extract_context(long_text)
    assert len(result) <= 200


def test_current_heading_returns_string():
    text = "# Title\n## Section\nsome content"
    result = mod._current_heading(text)
    assert isinstance(result, str)


def test_current_heading_finds_last():
    text = "# Title\n## First\nsome content\n## Last Section\nmore"
    result = mod._current_heading(text)
    assert "Last" in result


def test_current_heading_empty():
    result = mod._current_heading("no headings here")
    assert result == ""


def test_extract_events_returns_list(tmp_path, monkeypatch):
    monkeypatch.setattr(mod, "ROOT", tmp_path)
    f = tmp_path / "test.md"
    f.write_text("# Title\n\nIn 2024 the project was launched.\n", encoding="utf-8")
    result = mod.extract_events(f)
    assert isinstance(result, list)


def test_extract_events_finds_year(tmp_path, monkeypatch):
    monkeypatch.setattr(mod, "ROOT", tmp_path)
    f = tmp_path / "test.md"
    f.write_text("In 2024 the project launched its first release.\n", encoding="utf-8")
    result = mod.extract_events(f)
    found = [e for e in result if "2024" in e.get("date_str", "")]
    assert len(found) >= 1


def test_extract_events_finds_full_date(tmp_path, monkeypatch):
    monkeypatch.setattr(mod, "ROOT", tmp_path)
    f = tmp_path / "test.md"
    f.write_text("Released 2024-03-15 as the stable build.\n", encoding="utf-8")
    result = mod.extract_events(f)
    found = [e for e in result if "2024" in e.get("date_str", "")]
    assert len(found) >= 1


def test_extract_events_has_required_keys(tmp_path, monkeypatch):
    monkeypatch.setattr(mod, "ROOT", tmp_path)
    f = tmp_path / "test.md"
    f.write_text("In 2024 something happened here.\n", encoding="utf-8")
    result = mod.extract_events(f)
    for event in result:
        assert "date_str" in event
        assert "source" in event
        assert "context" in event


def test_extract_events_missing_file(tmp_path, monkeypatch):
    monkeypatch.setattr(mod, "ROOT", tmp_path)
    f = tmp_path / "missing.md"
    result = mod.extract_events(f)
    assert result == []


# ── main ──────────────────────────────────────────────────────────────────────

def test_main_creates_timeline_md(tmp_path, monkeypatch):
    monkeypatch.setattr(mod, "DOCS", tmp_path)
    monkeypatch.setattr(mod, "ROOT", tmp_path)
    monkeypatch.setattr(mod, "SECTION_FILTER", None)
    (tmp_path / "doc.md").write_text("# Title\n\n2026-05-01: Launch event.\n", encoding="utf-8")
    mod.main()
    assert (tmp_path / "TIMELINE.md").exists()


def test_main_empty_docs_no_crash(tmp_path, monkeypatch):
    monkeypatch.setattr(mod, "DOCS", tmp_path)
    monkeypatch.setattr(mod, "ROOT", tmp_path)
    monkeypatch.setattr(mod, "SECTION_FILTER", None)
    mod.main()
    assert (tmp_path / "TIMELINE.md").exists()
