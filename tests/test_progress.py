"""
Тесты для scripts/improve_progress.py.

Покрытие:
  - extract_checkitems() — подсчёт [x] и [ ] пунктов
  - categorize()         — определение фазы по ключевым словам
  - progress_bar()       — текстовая полоса прогресса
"""

import importlib
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(ROOT / "scripts"))

mod = importlib.import_module("improve_progress")

# ── extract_checkitems ────────────────────────────────────────────────────────

def test_extract_checkitems_returns_tuple():
    result = mod.extract_checkitems("- [x] Done\n- [ ] Todo\n")
    assert isinstance(result, tuple)
    assert len(result) == 3


def test_extract_checkitems_counts_done():
    text = "- [x] First done\n- [x] Second done\n- [ ] Todo\n"
    done, total, todos = mod.extract_checkitems(text)
    assert done == 2


def test_extract_checkitems_counts_total():
    text = "- [x] Done\n- [ ] Todo1\n- [ ] Todo2\n"
    done, total, todos = mod.extract_checkitems(text)
    assert total == 3


def test_extract_checkitems_returns_todo_list():
    text = "- [x] Done\n- [ ] First todo\n- [ ] Second todo\n"
    done, total, todos = mod.extract_checkitems(text)
    assert isinstance(todos, list)
    assert len(todos) == 2
    assert "First todo" in todos


def test_extract_checkitems_empty_text():
    done, total, todos = mod.extract_checkitems("")
    assert done == 0
    assert total == 0
    assert todos == []


def test_extract_checkitems_no_checkitems():
    text = "# Title\n\nSome text without any checkboxes.\n"
    done, total, todos = mod.extract_checkitems(text)
    assert done == 0
    assert total == 0


def test_extract_checkitems_case_insensitive_done():
    text = "- [X] Done uppercase\n"
    done, total, todos = mod.extract_checkitems(text)
    assert done == 1


def test_extract_checkitems_all_done():
    text = "- [x] A\n- [x] B\n- [x] C\n"
    done, total, todos = mod.extract_checkitems(text)
    assert done == total
    assert todos == []


# ── categorize ────────────────────────────────────────────────────────────────

def test_categorize_returns_string():
    assert isinstance(mod.categorize("Write some code"), str)


def test_categorize_research_phase():
    result = mod.categorize("Провести анализ архитектуры компонентов")
    assert result == "Фаза 1: Исследование"


def test_categorize_contacts_phase():
    result = mod.categorize("Написать авторам проектов")
    assert result == "Фаза 2: Контакты"


def test_categorize_prototype_phase():
    result = mod.categorize("Реализовать MVP прототип")
    assert result == "Фаза 3: Прототип"


def test_categorize_integration_phase():
    result = mod.categorize("Интеграция API компонентов")
    assert result == "Фаза 4: Интеграция"


def test_categorize_launch_phase():
    result = mod.categorize("Запуск production релиз")
    assert result == "Фаза 5: Запуск"


def test_categorize_unknown_returns_general():
    result = mod.categorize("нет ключевых слов совсем тут")
    assert result == "Общее"


# ── progress_bar ──────────────────────────────────────────────────────────────

def test_progress_bar_returns_string():
    result = mod.progress_bar(5, 10)
    assert isinstance(result, str)


def test_progress_bar_zero_total():
    result = mod.progress_bar(0, 0)
    assert isinstance(result, str)
    assert "░" in result


def test_progress_bar_correct_length():
    result = mod.progress_bar(5, 10, width=20)
    # bar + space + percentage text
    bar_part = result.split(" ")[0]
    assert len(bar_part) == 20


def test_progress_bar_full_progress():
    result = mod.progress_bar(10, 10, width=10)
    assert "█" * 10 in result
    assert "100%" in result


def test_progress_bar_zero_done():
    result = mod.progress_bar(0, 10, width=10)
    assert "░" * 10 in result
    assert "0%" in result


def test_progress_bar_half_progress():
    result = mod.progress_bar(5, 10, width=10)
    assert "50%" in result


def test_progress_bar_monotone():
    low  = mod.progress_bar(2, 10, width=20)
    high = mod.progress_bar(8, 10, width=20)
    low_filled  = low.count("█")
    high_filled = high.count("█")
    assert low_filled < high_filled
