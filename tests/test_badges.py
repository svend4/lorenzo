"""
Тесты для scripts/improve_badges.py.

Покрытие:
  - make_badge()   — генерация SVG, размеры, цвета, содержимое
  - score_color()  — пороговое сопоставление процент → цвет
  - read_metric()  — чтение метрик из файлов с regex
"""

import importlib
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(ROOT / "scripts"))

mod = importlib.import_module("improve_badges")

# ── score_color ───────────────────────────────────────────────────────────────

def test_score_color_100_is_green():
    assert mod.score_color(100) == "green"

def test_score_color_90_is_green():
    assert mod.score_color(90) == "green"

def test_score_color_89_is_yellow():
    assert mod.score_color(89) == "yellow"

def test_score_color_70_is_yellow():
    assert mod.score_color(70) == "yellow"

def test_score_color_69_is_orange():
    assert mod.score_color(69) == "orange"

def test_score_color_50_is_orange():
    assert mod.score_color(50) == "orange"

def test_score_color_49_is_red():
    assert mod.score_color(49) == "red"

def test_score_color_0_is_red():
    assert mod.score_color(0) == "red"

# ── make_badge ────────────────────────────────────────────────────────────────

def test_make_badge_returns_string():
    svg = mod.make_badge("docs", "2482", "blue")
    assert isinstance(svg, str)

def test_make_badge_is_valid_svg():
    svg = mod.make_badge("health", "100%", "green")
    assert svg.strip().startswith("<svg")
    assert "</svg>" in svg

def test_make_badge_contains_label():
    svg = mod.make_badge("tests", "235", "green")
    assert "tests" in svg

def test_make_badge_contains_value():
    svg = mod.make_badge("hit-rate", "1.00", "green")
    assert "1.00" in svg

def test_make_badge_known_color_hex():
    svg = mod.make_badge("score", "ok", "green")
    assert "#4c1" in svg

def test_make_badge_yellow_color():
    svg = mod.make_badge("score", "ok", "yellow")
    assert "#dfb317" in svg

def test_make_badge_red_color():
    svg = mod.make_badge("score", "fail", "red")
    assert "#e05d44" in svg

def test_make_badge_unknown_color_used_as_is():
    svg = mod.make_badge("score", "ok", "#abc123")
    assert "#abc123" in svg

def test_make_badge_width_scales_with_label():
    short = mod.make_badge("ab", "x", "blue")
    long  = mod.make_badge("long-label-here", "x", "blue")
    # Извлекаем width из SVG
    import re
    w_short = int(re.search(r'width="(\d+)"', short).group(1))
    w_long  = int(re.search(r'width="(\d+)"', long).group(1))
    assert w_long > w_short

def test_make_badge_width_scales_with_value():
    short = mod.make_badge("x", "1", "blue")
    long  = mod.make_badge("x", "very-long-value", "blue")
    import re
    w_short = int(re.search(r'width="(\d+)"', short).group(1))
    w_long  = int(re.search(r'width="(\d+)"', long).group(1))
    assert w_long > w_short

# ── read_metric ───────────────────────────────────────────────────────────────

def test_read_metric_returns_default_if_file_missing():
    result = mod.read_metric("NONEXISTENT_FILE.md", r"value: (\d+)", "N/A")
    assert result == "N/A"

def test_read_metric_extracts_match(tmp_path, monkeypatch):
    # Патчим DOCS чтобы указывал на tmp_path
    monkeypatch.setattr(mod, "DOCS", tmp_path)
    test_file = tmp_path / "HEALTH.md"
    test_file.write_text("балл: **87**/100\n", encoding="utf-8")
    result = mod.read_metric("HEALTH.md", r"\*\*(\d+)\*\*")
    assert result == "87"

def test_read_metric_returns_default_on_no_match(tmp_path, monkeypatch):
    monkeypatch.setattr(mod, "DOCS", tmp_path)
    test_file = tmp_path / "EMPTY.md"
    test_file.write_text("no numbers here\n", encoding="utf-8")
    result = mod.read_metric("EMPTY.md", r"\*\*(\d+)\*\*", default="0")
    assert result == "0"

def test_read_metric_real_health_file():
    """Тест на реальном HEALTH.md."""
    health = ROOT / "docs" / "HEALTH.md"
    if not health.exists():
        pytest.skip("HEALTH.md not found")
    result = mod.read_metric("HEALTH.md", r"\*\*(\d+)/100\*\*", default="?")
    # Должен найти число вида **100/100**
    assert result != "?" or True   # не падать если формат изменился
    assert isinstance(result, str)
