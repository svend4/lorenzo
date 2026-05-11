"""
Тесты для scripts/improve_status_badges.py.

Покрытие:
  - shields_io()        — URL-кодирование для shields.io
  - svg_badge()         — генерация SVG, размеры, содержимое
  - color_for_score()   — пороговые зоны 0–100
  - count_files()       — подсчёт файлов по glob-паттерну
  - count_skills()      — количество .claude/skills/*.md
  - count_templates()   — количество docs/templates/*.md
  - count_scripts()     — количество scripts/improve_*.py
  - get_health_score()  — чтение балла из HEALTH.md
  - validation_status() — валидных / с ошибками из VALIDATION.md
"""

import importlib
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(ROOT / "scripts"))

mod = importlib.import_module("improve_status_badges")

# ── shields_io ────────────────────────────────────────────────────────────────

def test_shields_io_returns_url():
    url = mod.shields_io("docs", "2482", "blue")
    assert url.startswith("https://img.shields.io/badge/")


def test_shields_io_encodes_hyphens():
    url = mod.shields_io("hit-rate", "1.00", "green")
    assert "hit--rate" in url


def test_shields_io_encodes_underscores():
    url = mod.shields_io("test_count", "340", "green")
    assert "test__count" in url


def test_shields_io_encodes_spaces():
    url = mod.shields_io("my label", "value", "blue")
    assert "my_label" in url


def test_shields_io_contains_color():
    url = mod.shields_io("x", "y", "brightgreen")
    assert "brightgreen" in url

# ── svg_badge ─────────────────────────────────────────────────────────────────

def test_svg_badge_is_valid_svg():
    svg = mod.svg_badge("tests", "340", "#4c1")
    assert "<svg" in svg
    assert "</svg>" in svg


def test_svg_badge_contains_label():
    svg = mod.svg_badge("coverage", "100%", "green")
    assert "coverage" in svg


def test_svg_badge_contains_message():
    svg = mod.svg_badge("health", "87", "green")
    assert "87" in svg


def test_svg_badge_width_scales_with_label():
    import re
    short = mod.svg_badge("ab", "1", "blue")
    long  = mod.svg_badge("long-label-here", "1", "blue")
    w_short = int(re.search(r'width="(\d+)"', short).group(1))
    w_long  = int(re.search(r'width="(\d+)"', long).group(1))
    assert w_long > w_short


def test_svg_badge_minimum_width():
    import re
    svg = mod.svg_badge("x", "y", "blue")
    w = int(re.search(r'width="(\d+)"', svg).group(1))
    assert w >= 80   # 40 + 40 minimum

# ── color_for_score ───────────────────────────────────────────────────────────

def test_color_for_score_100_brightgreen():
    assert mod.color_for_score(100) == "brightgreen"

def test_color_for_score_90_brightgreen():
    assert mod.color_for_score(90) == "brightgreen"

def test_color_for_score_89_green():
    assert mod.color_for_score(89) == "green"

def test_color_for_score_75_green():
    assert mod.color_for_score(75) == "green"

def test_color_for_score_74_yellowgreen():
    assert mod.color_for_score(74) == "yellowgreen"

def test_color_for_score_60_yellowgreen():
    assert mod.color_for_score(60) == "yellowgreen"

def test_color_for_score_59_yellow():
    assert mod.color_for_score(59) == "yellow"

def test_color_for_score_40_yellow():
    assert mod.color_for_score(40) == "yellow"

def test_color_for_score_39_orange():
    assert mod.color_for_score(39) == "orange"

def test_color_for_score_20_orange():
    assert mod.color_for_score(20) == "orange"

def test_color_for_score_19_red():
    assert mod.color_for_score(19) == "red"

def test_color_for_score_0_red():
    assert mod.color_for_score(0) == "red"

# ── count_files ───────────────────────────────────────────────────────────────

def test_count_files_returns_int():
    result = mod.count_files("*.md")
    assert isinstance(result, int)


def test_count_files_positive_for_existing():
    result = mod.count_files("*.md")
    assert result > 0


def test_count_files_zero_for_nonexistent_dir(tmp_path):
    result = mod.count_files("*.md", tmp_path / "nonexistent")
    assert result == 0


def test_count_files_zero_for_no_match(tmp_path):
    result = mod.count_files("*.xyz", tmp_path)
    assert result == 0

# ── count_skills ──────────────────────────────────────────────────────────────

def test_count_skills_positive():
    result = mod.count_skills()
    assert result > 0  # у нас 28 скиллов

# ── count_templates ───────────────────────────────────────────────────────────

def test_count_templates_positive():
    result = mod.count_templates()
    assert result > 0  # у нас 22 шаблона

# ── count_scripts ─────────────────────────────────────────────────────────────

def test_count_scripts_ge_150():
    result = mod.count_scripts()
    assert result >= 150  # у нас 165 скриптов

# ── get_health_score ──────────────────────────────────────────────────────────

def test_get_health_score_returns_int_or_none():
    result = mod.get_health_score()
    assert result is None or isinstance(result, int)


def test_get_health_score_in_range():
    result = mod.get_health_score()
    if result is not None:
        assert 0 <= result <= 100


def test_get_health_score_positive():
    result = mod.get_health_score()
    if result is not None:
        assert result > 0  # HEALTH.md существует и > 0

# ── validation_status ─────────────────────────────────────────────────────────

def test_validation_status_returns_tuple():
    result = mod.validation_status()
    assert isinstance(result, tuple)
    assert len(result) == 2


def test_validation_status_non_negative():
    valid, errors = mod.validation_status()
    assert valid >= 0
    assert errors >= 0


def test_validation_status_valid_ge_errors():
    valid, errors = mod.validation_status()
    # У нас 21 валидный и 0 с ошибками
    if valid > 0:
        assert errors == 0
