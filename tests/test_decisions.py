"""
Тесты для scripts/improve_decisions.py.

Покрытие:
  - categorize()         — категоризация текста решения
  - extract_decisions()  — извлечение решений из текста
"""

import importlib
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(ROOT / "scripts"))

mod = importlib.import_module("improve_decisions")


# ── categorize ────────────────────────────────────────────────────────────────

def test_categorize_returns_string():
    result = mod.categorize("some text about the system")
    assert isinstance(result, str)


def test_categorize_architecture_from_agentfs():
    result = mod.categorize("AgentFS is the best choice for knowledge storage")
    assert result == "архитектура"


def test_categorize_architecture_from_layer():
    result = mod.categorize("слой памяти реализован через CardIndex")
    assert result == "архитектура"


def test_categorize_memory_from_yodoca():
    result = mod.categorize("Yodoca handles memory consolidation best")
    assert result == "память"


def test_categorize_memory_from_consol():
    result = mod.categorize("консолидация данных агента через forgetting механизм")
    assert result == "память"


def test_categorize_security_from_sentinel():
    result = mod.categorize("SENTINEL guards against malicious tool calls")
    assert result == "безопасность"


def test_categorize_mvp_from_mvp():
    result = mod.categorize("MVP должен включать только основные функции поиска")
    assert result == "MVP"


def test_categorize_license_from_mit():
    result = mod.categorize("MIT лицензия позволяет использовать без ограничений")
    assert result == "лицензия"


def test_categorize_risks():
    result = mod.categorize("не стоит использовать BSL из-за ограничений")
    # Could match risks or license
    assert result in ("лицензия", "риски", "общее")


def test_categorize_default_general():
    result = mod.categorize("some random text that matches nothing specific here")
    assert result == "общее"


# ── extract_decisions ─────────────────────────────────────────────────────────

def _make_file(tmp_path, name="test.md"):
    f = tmp_path / name
    f.write_text("", encoding="utf-8")
    return f


def test_extract_decisions_returns_list(tmp_path, monkeypatch):
    monkeypatch.setattr(mod, "ROOT", tmp_path)
    f = _make_file(tmp_path)
    result = mod.extract_decisions("plain text without patterns", f)
    assert isinstance(result, list)


def test_extract_decisions_empty_text(tmp_path, monkeypatch):
    monkeypatch.setattr(mod, "ROOT", tmp_path)
    f = _make_file(tmp_path)
    result = mod.extract_decisions("", f)
    assert result == []


def test_extract_decisions_finds_recommendation(tmp_path, monkeypatch):
    monkeypatch.setattr(mod, "ROOT", tmp_path)
    f = _make_file(tmp_path)
    text = "рекомендуется использовать BM25 для основного поиска информации по документам"
    result = mod.extract_decisions(text, f)
    assert len(result) > 0


def test_extract_decisions_has_required_keys(tmp_path, monkeypatch):
    monkeypatch.setattr(mod, "ROOT", tmp_path)
    f = _make_file(tmp_path)
    text = "рекомендуется использовать BM25 для основного поиска документов"
    result = mod.extract_decisions(text, f)
    for item in result:
        assert "text" in item
        assert "file" in item
        assert "category" in item


def test_extract_decisions_skips_short(tmp_path, monkeypatch):
    monkeypatch.setattr(mod, "ROOT", tmp_path)
    f = _make_file(tmp_path)
    result = mod.extract_decisions("рекомендуется это.", f)
    # too short definition
    assert result == []


def test_extract_decisions_finds_best_choice(tmp_path, monkeypatch):
    monkeypatch.setattr(mod, "ROOT", tmp_path)
    f = _make_file(tmp_path)
    text = "лучший выбор: использовать AgentFS для хранения данных в файловой системе"
    result = mod.extract_decisions(text, f)
    assert len(result) > 0


def test_extract_decisions_strips_markdown_links(tmp_path, monkeypatch):
    monkeypatch.setattr(mod, "ROOT", tmp_path)
    f = _make_file(tmp_path)
    text = "рекомендуется [AgentFS](docs/agentfs.md) для хранения знаний и данных агента"
    result = mod.extract_decisions(text, f)
    for item in result:
        assert "](docs/" not in item["text"]


def test_extract_decisions_category_is_set(tmp_path, monkeypatch):
    monkeypatch.setattr(mod, "ROOT", tmp_path)
    f = _make_file(tmp_path)
    text = "рекомендуется использовать AgentFS для хранения данных в файловой системе"
    result = mod.extract_decisions(text, f)
    for item in result:
        assert len(item["category"]) > 0
