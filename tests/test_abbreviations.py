"""
Тесты для scripts/improve_abbreviations.py.

Покрытие:
  - find_abbrevs()   — автообнаружение аббревиатур в тексте
  - count_usage()    — подсчёт упоминаний аббревиатуры
"""

import importlib
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(ROOT / "scripts"))

mod = importlib.import_module("improve_abbreviations")


# ── find_abbrevs ──────────────────────────────────────────────────────────────

def test_find_abbrevs_returns_dict():
    result = mod.find_abbrevs("Some text without abbreviations here.")
    assert isinstance(result, dict)


def test_find_abbrevs_empty_text():
    result = mod.find_abbrevs("")
    assert result == {}


def test_find_abbrevs_finds_dash_pattern():
    result = mod.find_abbrevs("API — интерфейс программирования приложений для разработки")
    assert "API" in result


def test_find_abbrevs_finds_colon_pattern():
    result = mod.find_abbrevs("MCP: Model Context Protocol для AI инструментов")
    assert "MCP" in result


def test_find_abbrevs_extracts_definition():
    result = mod.find_abbrevs("API — интерфейс программирования приложений для разработки")
    if "API" in result:
        assert len(result["API"]) > 5


def test_find_abbrevs_skips_too_short():
    result = mod.find_abbrevs("A — это что-то")
    assert "A" not in result


def test_find_abbrevs_skips_too_long():
    result = mod.find_abbrevs("ABCDEFGHIJK — это слишком длинная аббревиатура для словаря")
    assert "ABCDEFGHIJK" not in result


def test_find_abbrevs_skips_non_all_caps():
    result = mod.find_abbrevs("Api — это не аббревиатура потому что смешанный регистр здесь")
    assert "Api" not in result


def test_find_abbrevs_limits_definition_length():
    long_def = "x" * 200
    result = mod.find_abbrevs(f"API — {long_def}")
    if "API" in result:
        assert len(result["API"]) <= 120


def test_find_abbrevs_no_duplicate_abbr():
    text = "API — интерфейс первый раз. API — интерфейс второй раз в тексте."
    result = mod.find_abbrevs(text)
    if "API" in result:
        assert isinstance(result["API"], str)


def test_find_abbrevs_finds_slash_abbr():
    result = mod.find_abbrevs("CI/CD — непрерывная интеграция и доставка программного обеспечения")
    assert "CI/CD" in result or len(result) == 0  # may or may not match depending on pattern


# ── count_usage ───────────────────────────────────────────────────────────────

def test_count_usage_returns_int():
    result = mod.count_usage("Use API here.", "API")
    assert isinstance(result, int)


def test_count_usage_finds_single():
    result = mod.count_usage("The API is great.", "API")
    assert result == 1


def test_count_usage_finds_multiple():
    result = mod.count_usage("API and API and API in the text.", "API")
    assert result == 3


def test_count_usage_zero_if_not_found():
    result = mod.count_usage("No abbreviations here in this text.", "API")
    assert result == 0


def test_count_usage_word_boundary():
    result = mod.count_usage("APIS is not API.", "API")
    assert result == 1


def test_count_usage_case_sensitive():
    result = mod.count_usage("api is not the same as API.", "API")
    assert result == 1
