"""
Тесты для scripts/improve_kpi.py.

Покрытие:
  - strip_links()   — удаление markdown-ссылок
  - extract_kpis()  — извлечение числовых KPI из текста
"""

import importlib
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(ROOT / "scripts"))

mod = importlib.import_module("improve_kpi")


# ── strip_links ───────────────────────────────────────────────────────────────

def test_strip_links_returns_string():
    result = mod.strip_links("some text here")
    assert isinstance(result, str)


def test_strip_links_removes_markdown_links():
    result = mod.strip_links("See [AgentFS](docs/agentfs.md) for details.")
    assert "docs/agentfs.md" not in result
    assert "AgentFS" in result


def test_strip_links_empty():
    result = mod.strip_links("")
    assert result == ""


def test_strip_links_no_links():
    result = mod.strip_links("plain text without links")
    assert result == "plain text without links"


def test_strip_links_multiple():
    result = mod.strip_links("[A](a.md) and [B](b.md)")
    assert "A" in result
    assert "B" in result
    assert "(" not in result


# ── extract_kpis ──────────────────────────────────────────────────────────────

def _make_file(tmp_path, name="test.md"):
    f = tmp_path / name
    f.write_text("", encoding="utf-8")
    return f


def test_extract_kpis_returns_list(tmp_path, monkeypatch):
    monkeypatch.setattr(mod, "DOCS", tmp_path)
    f = _make_file(tmp_path)
    result = mod.extract_kpis("plain text", f)
    assert isinstance(result, list)


def test_extract_kpis_empty_text(tmp_path, monkeypatch):
    monkeypatch.setattr(mod, "DOCS", tmp_path)
    f = _make_file(tmp_path)
    result = mod.extract_kpis("", f)
    assert result == []


def test_extract_kpis_finds_count(tmp_path, monkeypatch):
    monkeypatch.setattr(mod, "DOCS", tmp_path)
    f = _make_file(tmp_path)
    result = mod.extract_kpis("436 вакансий в базе данных системы", f)
    assert len(result) > 0
    categories = [item["category"] for item in result]
    assert "Количество" in categories


def test_extract_kpis_finds_percentage(tmp_path, monkeypatch):
    monkeypatch.setattr(mod, "DOCS", tmp_path)
    f = _make_file(tmp_path)
    result = mod.extract_kpis("87% покрытие тестами в системе поиска", f)
    if result:
        categories = [item["category"] for item in result]
        assert "Проценты" in categories


def test_extract_kpis_finds_version(tmp_path, monkeypatch):
    monkeypatch.setattr(mod, "DOCS", tmp_path)
    f = _make_file(tmp_path)
    result = mod.extract_kpis("версия 2.0 системы будет выпущена на следующей неделе", f)
    if result:
        categories = [item["category"] for item in result]
        assert "Версия" in categories


def test_extract_kpis_has_required_keys(tmp_path, monkeypatch):
    monkeypatch.setattr(mod, "DOCS", tmp_path)
    f = _make_file(tmp_path)
    result = mod.extract_kpis("436 вакансий в базе данных системы поиска знаний", f)
    for item in result:
        assert "category" in item
        assert "value" in item
        assert "context" in item
        assert "file" in item


def test_extract_kpis_deduplicates(tmp_path, monkeypatch):
    monkeypatch.setattr(mod, "DOCS", tmp_path)
    f = _make_file(tmp_path)
    result = mod.extract_kpis("436 вакансий и 436 вакансий здесь", f)
    # Should deduplicate by (category, value)
    seen = set()
    for item in result:
        key = (item["category"], item["value"].lower()[:20])
        assert key not in seen
        seen.add(key)


def test_extract_kpis_strips_code_blocks(tmp_path, monkeypatch):
    monkeypatch.setattr(mod, "DOCS", tmp_path)
    f = _make_file(tmp_path)
    result = mod.extract_kpis("```\n436 вакансий внутри блока кода\n```\n", f)
    # Code blocks should be stripped
    assert len(result) == 0


# ── main ──────────────────────────────────────────────────────────────────────

def test_main_creates_kpi_md(tmp_path, monkeypatch):
    monkeypatch.setattr(mod, "DOCS", tmp_path)
    monkeypatch.setattr(mod, "ROOT", tmp_path)
    mod.main()
    assert (tmp_path / "KPI.md").exists()


def test_main_kpi_has_content(tmp_path, monkeypatch):
    monkeypatch.setattr(mod, "DOCS", tmp_path)
    monkeypatch.setattr(mod, "ROOT", tmp_path)
    (tmp_path / "doc.md").write_text("# Title\n\n436 вакансий в 12 кластерах.", encoding="utf-8")
    mod.main()
    text = (tmp_path / "KPI.md").read_text(encoding="utf-8")
    assert "# " in text


def test_main_empty_docs(tmp_path, monkeypatch):
    monkeypatch.setattr(mod, "DOCS", tmp_path)
    monkeypatch.setattr(mod, "ROOT", tmp_path)
    mod.main()
    assert (tmp_path / "KPI.md").exists()


def test_main_kpi_starts_with_heading(tmp_path, monkeypatch):
    monkeypatch.setattr(mod, "DOCS", tmp_path)
    monkeypatch.setattr(mod, "ROOT", tmp_path)
    mod.main()
    text = (tmp_path / "KPI.md").read_text(encoding="utf-8")
    assert text.strip().startswith("#")
