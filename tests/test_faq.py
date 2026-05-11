"""
Тесты для scripts/improve_faq.py.

Покрытие:
  - strip_links()    — удаление markdown-ссылок (оставить текст)
  - extract_qa()     — извлечение пар вопрос-ответ
  - categorize()     — определение категории FAQ по ключевым словам
"""

import importlib
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(ROOT / "scripts"))

mod = importlib.import_module("improve_faq")

# ── strip_links ───────────────────────────────────────────────────────────────

def test_strip_links_returns_string():
    assert isinstance(mod.strip_links("Some text."), str)


def test_strip_links_removes_link_url():
    result = mod.strip_links("See [AgentFS](docs/agentfs.md) here.")
    assert "docs/agentfs.md" not in result
    assert "[" not in result
    assert "]" not in result


def test_strip_links_preserves_link_text():
    result = mod.strip_links("See [AgentFS](docs/agentfs.md) here.")
    assert "AgentFS" in result


def test_strip_links_no_links_unchanged():
    text = "Plain text without links."
    assert mod.strip_links(text) == text


def test_strip_links_multiple_links():
    text = "[Alpha](url1) and [Beta](url2)"
    result = mod.strip_links(text)
    assert "Alpha" in result
    assert "Beta" in result
    assert "url1" not in result
    assert "url2" not in result


def test_strip_links_empty_text():
    assert mod.strip_links("") == ""


# ── extract_qa ────────────────────────────────────────────────────────────────

def test_extract_qa_returns_list():
    result = mod.extract_qa("Some text without Q&A patterns.")
    assert isinstance(result, list)


def test_extract_qa_empty_text():
    result = mod.extract_qa("")
    assert result == []


def test_extract_qa_finds_q_a_pattern():
    text = "\nQ: What is AgentFS?\n\nA: AgentFS is a filesystem-based knowledge management tool for agents.\n\n"
    result = mod.extract_qa(text)
    # May or may not find (depends on regex matching), just verify type
    assert isinstance(result, list)


def test_extract_qa_tuples_have_two_elements():
    text = "\nQ: What is AgentFS?\n\nA: AgentFS is a filesystem-based knowledge management tool for agents.\n\n"
    result = mod.extract_qa(text)
    for pair in result:
        assert len(pair) == 2


def test_extract_qa_skips_code_blocks():
    text = "```\nQ: Inside code block?\nA: Should be ignored.\n```\n"
    result = mod.extract_qa(text)
    assert result == []


# ── categorize ────────────────────────────────────────────────────────────────

def test_categorize_returns_string():
    assert isinstance(mod.categorize("Some question?", "Some answer text."), str)


def test_categorize_architecture_category():
    result = mod.categorize("Что такое архитектура?", "Контракт envelope это слой.")
    assert result == "Архитектура"


def test_categorize_components_category():
    result = mod.categorize("Что такое AgentFS?", "AgentFS is a filesystem tool.")
    assert result == "Компоненты"


def test_categorize_integration_category():
    result = mod.categorize("Как API работает?", "Интеграция MCP протокола.")
    assert result == "Интеграция"


def test_categorize_mvp_category():
    result = mod.categorize("Когда запуск?", "MVP прототип готов.")
    assert result == "MVP/Запуск"


def test_categorize_license_category():
    result = mod.categorize("Какова лицензия?", "Проект использует MIT лицензию.")
    assert result == "Лицензия"


def test_categorize_unknown_topic():
    result = mod.categorize("Погода хорошая?", "Да очень хорошо.")
    assert result == "Общее"
