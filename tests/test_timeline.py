"""
Тесты для scripts/improve_timeline.py.

Покрытие:
  - strip_links()     — удаление markdown-ссылок, оставляя текст
  - extract_dates()   — извлечение дат и временных маркеров из текста
"""

import importlib
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(ROOT / "scripts"))

mod = importlib.import_module("improve_timeline")


# ── strip_links ───────────────────────────────────────────────────────────────

def test_strip_links_returns_string():
    result = mod.strip_links("some text")
    assert isinstance(result, str)


def test_strip_links_removes_md_link():
    result = mod.strip_links("See [AgentFS](docs/agentfs.md) for details.")
    assert "(" not in result
    assert "AgentFS" in result


def test_strip_links_keeps_link_text():
    result = mod.strip_links("[AgentFS](docs/agentfs.md)")
    assert "AgentFS" in result


def test_strip_links_removes_url():
    result = mod.strip_links("[Click here](https://example.com)")
    assert "https" not in result
    assert "Click here" in result


def test_strip_links_no_links():
    result = mod.strip_links("plain text without links")
    assert result == "plain text without links"


def test_strip_links_multiple_links():
    result = mod.strip_links("[A](a.md) and [B](b.md)")
    assert "A" in result
    assert "B" in result
    assert "(" not in result


def test_strip_links_empty():
    result = mod.strip_links("")
    assert result == ""


# ── extract_dates ─────────────────────────────────────────────────────────────

def _make_file(tmp_path, name="test.md"):
    f = tmp_path / name
    f.write_text("", encoding="utf-8")
    return f


def test_extract_dates_returns_list(tmp_path, monkeypatch):
    monkeypatch.setattr(mod, "DOCS", tmp_path)
    f = _make_file(tmp_path)
    result = mod.extract_dates("some plain text", f)
    assert isinstance(result, list)


def test_extract_dates_empty_text(tmp_path, monkeypatch):
    monkeypatch.setattr(mod, "DOCS", tmp_path)
    f = _make_file(tmp_path)
    result = mod.extract_dates("", f)
    assert result == []


def test_extract_dates_finds_iso_date(tmp_path, monkeypatch):
    monkeypatch.setattr(mod, "DOCS", tmp_path)
    f = _make_file(tmp_path)
    result = mod.extract_dates("Запуск запланирован на 2025-06-15 после тестирования.", f)
    assert len(result) > 0
    matches = [e["match"] for e in result]
    assert any("2025" in m for m in matches)


def test_extract_dates_finds_year(tmp_path, monkeypatch):
    monkeypatch.setattr(mod, "DOCS", tmp_path)
    f = _make_file(tmp_path)
    result = mod.extract_dates("В 2026 году планируется выпуск системы.", f)
    matches = [e["match"] for e in result]
    assert any("2026" in m for m in matches)


def test_extract_dates_finds_quarter(tmp_path, monkeypatch):
    monkeypatch.setattr(mod, "DOCS", tmp_path)
    f = _make_file(tmp_path)
    result = mod.extract_dates("Релиз запланирован на Q3 2025.", f)
    matches = [e["match"] for e in result]
    assert any("Q3" in m for m in matches)


def test_extract_dates_entry_has_required_keys(tmp_path, monkeypatch):
    monkeypatch.setattr(mod, "DOCS", tmp_path)
    f = _make_file(tmp_path)
    result = mod.extract_dates("Запланировано на 2025-03-01 начало проекта.", f)
    if result:
        for entry in result:
            assert "match" in entry
            assert "kind" in entry
            assert "context" in entry
            assert "file" in entry


def test_extract_dates_context_not_too_long(tmp_path, monkeypatch):
    monkeypatch.setattr(mod, "DOCS", tmp_path)
    f = _make_file(tmp_path)
    text = "A" * 200 + " 2025-06-15 " + "B" * 200
    result = mod.extract_dates(text, f)
    for entry in result:
        assert len(entry["context"]) <= 150


def test_extract_dates_file_relative_path(tmp_path, monkeypatch):
    monkeypatch.setattr(mod, "DOCS", tmp_path)
    subdir = tmp_path / "sub"
    subdir.mkdir()
    f = subdir / "test.md"
    f.write_text("", encoding="utf-8")
    result = mod.extract_dates("В 2025 году появится новая система.", f)
    for entry in result:
        assert "sub" in entry["file"] or "test" in entry["file"]


def test_extract_dates_strips_newlines_from_context(tmp_path, monkeypatch):
    monkeypatch.setattr(mod, "DOCS", tmp_path)
    f = _make_file(tmp_path)
    text = "Начало\nпроекта\n2025-01-01\nпосле\nтестирования"
    result = mod.extract_dates(text, f)
    for entry in result:
        assert "\n" not in entry["context"]
