"""
Тесты для scripts/improve_action_items.py.

Покрытие:
  - extract_items()  — извлечение задач, рисков, решений из текста
"""

import importlib
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(ROOT / "scripts"))

mod = importlib.import_module("improve_action_items")


def _make_file(tmp_path, name="test.md"):
    f = tmp_path / name
    f.write_text("", encoding="utf-8")
    return f


# ── extract_items ─────────────────────────────────────────────────────────────

def test_extract_items_returns_list(tmp_path, monkeypatch):
    monkeypatch.setattr(mod, "ROOT", tmp_path)
    f = _make_file(tmp_path)
    result = mod.extract_items("plain text without any patterns", f)
    assert isinstance(result, list)


def test_extract_items_empty_text(tmp_path, monkeypatch):
    monkeypatch.setattr(mod, "ROOT", tmp_path)
    f = _make_file(tmp_path)
    result = mod.extract_items("", f)
    assert result == []


def test_extract_items_finds_todo(tmp_path, monkeypatch):
    monkeypatch.setattr(mod, "ROOT", tmp_path)
    f = _make_file(tmp_path)
    result = mod.extract_items("TODO: add authentication to the API gateway system", f)
    assert len(result) > 0
    kinds = [item["kind"] for item in result]
    assert "todo" in kinds


def test_extract_items_finds_risk(tmp_path, monkeypatch):
    monkeypatch.setattr(mod, "ROOT", tmp_path)
    f = _make_file(tmp_path)
    result = mod.extract_items("риск: потеря данных при обновлении индексного файла системы", f)
    assert len(result) > 0
    kinds = [item["kind"] for item in result]
    assert "risk" in kinds


def test_extract_items_finds_decision(tmp_path, monkeypatch):
    monkeypatch.setattr(mod, "ROOT", tmp_path)
    f = _make_file(tmp_path)
    result = mod.extract_items("рекомендуется использовать BM25 для основного поиска информации", f)
    assert len(result) > 0
    kinds = [item["kind"] for item in result]
    assert "decision" in kinds


def test_extract_items_has_required_keys(tmp_path, monkeypatch):
    monkeypatch.setattr(mod, "ROOT", tmp_path)
    f = _make_file(tmp_path)
    result = mod.extract_items("TODO: add search functionality to the API gateway system", f)
    for item in result:
        assert "kind" in item
        assert "text" in item
        assert "file" in item


def test_extract_items_skips_short_values(tmp_path, monkeypatch):
    monkeypatch.setattr(mod, "ROOT", tmp_path)
    f = _make_file(tmp_path)
    result = mod.extract_items("TODO: short", f)
    assert len(result) == 0


def test_extract_items_strips_markdown_links(tmp_path, monkeypatch):
    monkeypatch.setattr(mod, "ROOT", tmp_path)
    f = _make_file(tmp_path)
    result = mod.extract_items(
        "TODO: add [AgentFS](docs/agentfs.md) integration to the gateway system",
        f
    )
    for item in result:
        assert "(" not in item["text"] or ")" not in item["text"] or "[" not in item["text"]


def test_extract_items_truncates_text(tmp_path, monkeypatch):
    monkeypatch.setattr(mod, "ROOT", tmp_path)
    f = _make_file(tmp_path)
    long_text = "TODO: " + "x" * 300
    result = mod.extract_items(long_text, f)
    for item in result:
        assert len(item["text"]) <= 200


def test_extract_items_fixme_is_todo(tmp_path, monkeypatch):
    monkeypatch.setattr(mod, "ROOT", tmp_path)
    f = _make_file(tmp_path)
    result = mod.extract_items("FIXME: resolve the broken authentication in gateway system", f)
    kinds = [item["kind"] for item in result]
    assert "todo" in kinds


def test_extract_items_next_step(tmp_path, monkeypatch):
    monkeypatch.setattr(mod, "ROOT", tmp_path)
    f = _make_file(tmp_path)
    result = mod.extract_items(
        "следующий шаг: реализовать гибридный поиск по всем документам базы знаний",
        f
    )
    kinds = [item["kind"] for item in result]
    assert "next_step" in kinds
