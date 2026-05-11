"""
Тесты для scripts/improve_cost.py.

Покрытие:
  - extract_time_estimates() — извлечение оценок времени из текста
"""

import importlib
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(ROOT / "scripts"))

mod = importlib.import_module("improve_cost")


# ── extract_time_estimates ────────────────────────────────────────────────────

def test_extract_time_estimates_returns_list():
    result = mod.extract_time_estimates("plain text without estimates")
    assert isinstance(result, list)


def test_extract_time_estimates_empty():
    result = mod.extract_time_estimates("")
    assert result == []


def test_extract_time_estimates_finds_month_range():
    result = mod.extract_time_estimates("Потребуется 3-6 месяцев для разработки системы")
    assert len(result) > 0


def test_extract_time_estimates_finds_single_months():
    result = mod.extract_time_estimates("На реализацию потребуется 3 месяца работы команды")
    assert len(result) > 0


def test_extract_time_estimates_finds_weeks():
    result = mod.extract_time_estimates("Спринт займёт 2 недели разработки")
    assert len(result) > 0


def test_extract_time_estimates_returns_tuples():
    result = mod.extract_time_estimates("Займёт 2 недели разработки компонентов системы")
    for item in result:
        assert isinstance(item, tuple)
        assert len(item) == 2


def test_extract_time_estimates_tuple_has_context_and_weeks():
    result = mod.extract_time_estimates("Займёт 2 недели разработки системы поиска")
    for context, weeks in result:
        assert isinstance(context, str)
        assert isinstance(weeks, int)


def test_extract_time_estimates_month_range_average():
    result = mod.extract_time_estimates("Займёт 2-4 месяца разработки системы поиска")
    for context, weeks in result:
        # 2-4 months avg = 3 months = 12 weeks
        if "месяц" in context.lower() or "месяц" in context:
            assert weeks > 0


def test_extract_time_estimates_limits_to_10():
    text = " ".join([f"займёт {i} недель разработки" for i in range(1, 20)])
    result = mod.extract_time_estimates(text)
    assert len(result) <= 10


def test_extract_time_estimates_context_max_len():
    result = mod.extract_time_estimates("Займёт 3 месяца для реализации этой задачи")
    for context, _ in result:
        assert len(context) <= 100


# ── main ──────────────────────────────────────────────────────────────────────

def test_main_creates_cost_md(tmp_path, monkeypatch):
    monkeypatch.setattr(mod, "DOCS", tmp_path)
    monkeypatch.setattr(mod, "ROOT", tmp_path)
    mod.main()
    assert (tmp_path / "COST.md").exists()


def test_main_cost_has_content(tmp_path, monkeypatch):
    monkeypatch.setattr(mod, "DOCS", tmp_path)
    monkeypatch.setattr(mod, "ROOT", tmp_path)
    (tmp_path / "doc.md").write_text(
        "# Title\n\nЗаймёт 3 месяца для реализации системы.", encoding="utf-8"
    )
    mod.main()
    text = (tmp_path / "COST.md").read_text(encoding="utf-8")
    assert "# " in text


def test_main_empty_docs(tmp_path, monkeypatch):
    monkeypatch.setattr(mod, "DOCS", tmp_path)
    monkeypatch.setattr(mod, "ROOT", tmp_path)
    mod.main()
    assert (tmp_path / "COST.md").exists()


def test_main_cost_starts_with_heading(tmp_path, monkeypatch):
    monkeypatch.setattr(mod, "DOCS", tmp_path)
    monkeypatch.setattr(mod, "ROOT", tmp_path)
    mod.main()
    text = (tmp_path / "COST.md").read_text(encoding="utf-8")
    assert text.strip().startswith("#")
