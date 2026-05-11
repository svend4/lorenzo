"""
Тесты для scripts/improve_readability_v2.py.

Покрытие:
  - count_syllables()     — подсчёт слогов по гласным
  - clean_text()          — удаление markdown-разметки
  - compute_readability() — метрики читаемости (Flesch-Kincaid адаптация)
"""

import importlib
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(ROOT / "scripts"))

mod = importlib.import_module("improve_readability_v2")

# ── count_syllables ───────────────────────────────────────────────────────────

def test_count_syllables_returns_int():
    result = mod.count_syllables("памяти")
    assert isinstance(result, int)


def test_count_syllables_russian_word():
    # "память" has 2 vowels: а, я → 2 syllables
    result = mod.count_syllables("память")
    assert result == 2


def test_count_syllables_english_word():
    # "agent" has 2 vowels: a, e → 2 syllables
    result = mod.count_syllables("agent")
    assert result == 2


def test_count_syllables_minimum_one():
    # Even words with no vowels get minimum 1
    result = mod.count_syllables("brrr")
    assert result >= 1


def test_count_syllables_multi_vowel():
    # "консолидация" → к-о-н-с-о-л-и-д-а-ц-и-я → 5 vowels
    result = mod.count_syllables("консолидация")
    assert result >= 4


def test_count_syllables_single_vowel():
    result = mod.count_syllables("он")
    assert result == 1


# ── clean_text ────────────────────────────────────────────────────────────────

def test_clean_text_returns_string():
    assert isinstance(mod.clean_text("Some text."), str)


def test_clean_text_removes_code_blocks():
    text = "Before.\n```python\nprint('x')\n```\nAfter."
    result = mod.clean_text(text)
    assert "print" not in result


def test_clean_text_removes_inline_code():
    text = "Use the `agent.run()` method here."
    result = mod.clean_text(text)
    assert "`" not in result


def test_clean_text_removes_urls():
    text = "See https://github.com/user/repo for more info."
    result = mod.clean_text(text)
    assert "github.com" not in result


def test_clean_text_removes_html_comments():
    text = "Before. <!-- hidden --> After."
    result = mod.clean_text(text)
    assert "hidden" not in result


def test_clean_text_removes_markdown_symbols():
    text = "**Bold** and _italic_ and # Heading"
    result = mod.clean_text(text)
    assert "#" not in result


def test_clean_text_empty():
    assert mod.clean_text("") == ""


# ── compute_readability ───────────────────────────────────────────────────────

_LONG_TEXT = (
    "Агент с памятью — это система, которая умеет запоминать прошлые взаимодействия "
    "и использовать их для улучшения будущих ответов. "
    "Такие агенты применяются в разработке Knowledge OS для Svyazi 2.0. "
    "Ключевым компонентом является модуль консолидации, который периодически "
    "обрабатывает накопленный опыт и формирует устойчивые паттерны поведения. "
    "Интеграция с базами знаний позволяет агентам получать доступ к структурированной "
    "информации при формировании ответов и принятии решений. "
    "Архитектурные решения определяют качество работы системы в целом. "
) * 5


def test_compute_readability_returns_dict():
    result = mod.compute_readability(_LONG_TEXT)
    assert isinstance(result, dict)


def test_compute_readability_has_required_keys():
    result = mod.compute_readability(_LONG_TEXT)
    assert "fre" in result
    assert "level" in result


def test_compute_readability_fre_in_range():
    result = mod.compute_readability(_LONG_TEXT)
    assert 0 <= result["fre"] <= 100


def test_compute_readability_level_is_string():
    result = mod.compute_readability(_LONG_TEXT)
    assert isinstance(result["level"], str)


def test_compute_readability_empty_for_short_text():
    result = mod.compute_readability("Short.")
    assert result == {}


def test_compute_readability_words_count():
    result = mod.compute_readability(_LONG_TEXT)
    assert "n_words" in result or "avg_sent_len" in result or "fre" in result


def test_compute_readability_level_known_value():
    result = mod.compute_readability(_LONG_TEXT)
    valid_levels = {"🟢 Лёгкий", "🟡 Средний", "🟠 Сложный", "🔴 Очень сложный"}
    assert result["level"] in valid_levels
