"""Тесты language detection, i18n, readability."""
import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).parent.parent))

from docstoolkit.lang import (
    detect_language, language_stats,
    t, set_locale, get_locale, available_locales,
    readability_score, syllables_estimate,
)
from docstoolkit.lang.i18n import register_messages


# Detection

def test_detect_english():
    assert detect_language("This is purely English text") == "en"


def test_detect_russian():
    assert detect_language("Это только русский текст") == "ru"


def test_detect_mixed():
    text = "Это текст с английскими словами like memory и storage layer"
    assert detect_language(text) == "mixed"


def test_detect_unknown_short():
    assert detect_language("ab") == "unknown"


def test_language_stats():
    stats = language_stats("Hello мир")
    assert stats["en_chars"] == 5
    assert stats["ru_chars"] == 3
    assert stats["total"] == 8
    assert stats["en_ratio"] == pytest.approx(5/8)


# i18n

def test_t_english():
    assert t("validation.missing_field", locale="en", field="title") == \
           "Missing required field: title"


def test_t_russian():
    assert t("validation.missing_field", locale="ru", field="title") == \
           "Отсутствует обязательное поле: title"


def test_t_unknown_locale_fallbacks_to_english():
    assert t("validation.missing_field", locale="fr", field="x") == \
           "Missing required field: x"


def test_t_unknown_key_returns_key():
    assert t("nonexistent.key") == "nonexistent.key"


def test_set_get_locale():
    set_locale("ru")
    assert get_locale() == "ru"
    set_locale("en")
    assert get_locale() == "en"


def test_set_locale_unknown_fallbacks():
    set_locale("xyz")
    assert get_locale() == "en"


def test_available_locales():
    locs = available_locales()
    assert "en" in locs
    assert "ru" in locs


def test_register_messages_extension():
    register_messages("en", {"plugin.test": "Plugin works"})
    assert t("plugin.test", locale="en") == "Plugin works"


# Readability

def test_syllables_en():
    assert syllables_estimate("hello", "en") == 2
    assert syllables_estimate("a", "en") == 1


def test_syllables_ru():
    assert syllables_estimate("память", "ru") == 2
    assert syllables_estimate("исследование", "ru") == 5


def test_readability_en_simple():
    text = "The cat sat. The dog ran. It is fun."
    result = readability_score(text, lang="en")
    assert result["lang"] == "en"
    assert result["words"] >= 9
    assert result["sentences"] == 3
    assert result["score"] > 80  # очень простой текст


def test_readability_ru_complex():
    text = ("Архитектурное проектирование распределённых систем "
            "требует тщательного рассмотрения многочисленных факторов производительности.")
    result = readability_score(text, lang="ru")
    assert result["lang"] == "ru"
    assert result["score"] < 60  # сложный академический текст


def test_readability_auto_detect_ru():
    text = "Это простой русский текст. Несколько коротких предложений."
    result = readability_score(text)
    assert result["lang"] == "ru"


def test_readability_empty():
    result = readability_score("", lang="en")
    assert result["score"] == 0
    assert result["words"] == 0
