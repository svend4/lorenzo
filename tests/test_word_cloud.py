"""
Тесты для scripts/improve_word_cloud.py.

Покрытие:
  - font_size()    — линейное масштабирование размера шрифта
  - place_words()  — спиральное размещение слов
  - make_svg()     — генерация SVG-разметки
"""

import importlib
import sys
from pathlib import Path

ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(ROOT / "scripts"))

mod = importlib.import_module("improve_word_cloud")

# ── font_size ─────────────────────────────────────────────────────────────────

def test_font_size_returns_int():
    result = mod.font_size(5, 1, 10)
    assert isinstance(result, int)


def test_font_size_min_count_returns_min_fs():
    result = mod.font_size(1, 1, 10, min_fs=11, max_fs=52)
    assert result == 11


def test_font_size_max_count_returns_max_fs():
    result = mod.font_size(10, 1, 10, min_fs=11, max_fs=52)
    assert result == 52


def test_font_size_equal_min_max_returns_midpoint():
    result = mod.font_size(5, 5, 5, min_fs=11, max_fs=52)
    assert result == (11 + 52) // 2


def test_font_size_mid_count_is_between():
    result = mod.font_size(5, 1, 10, min_fs=11, max_fs=52)
    assert 11 <= result <= 52


def test_font_size_monotone():
    low  = mod.font_size(2, 1, 10, min_fs=11, max_fs=52)
    mid  = mod.font_size(5, 1, 10, min_fs=11, max_fs=52)
    high = mod.font_size(9, 1, 10, min_fs=11, max_fs=52)
    assert low <= mid <= high


def test_font_size_default_params():
    result = mod.font_size(5, 1, 10)
    assert isinstance(result, int)
    assert 11 <= result <= 52


def test_font_size_at_boundary_min():
    result = mod.font_size(0, 0, 100, min_fs=10, max_fs=50)
    assert result == 10


def test_font_size_at_boundary_max():
    result = mod.font_size(100, 0, 100, min_fs=10, max_fs=50)
    assert result == 50


# ── place_words ───────────────────────────────────────────────────────────────

def _sample_words():
    return [
        ("агент", 50, 36),
        ("память", 45, 33),
        ("граф", 40, 30),
        ("yaml", 35, 27),
        ("mcp", 30, 24),
    ]


def test_place_words_returns_list():
    result = mod.place_words(_sample_words(), 800, 400)
    assert isinstance(result, list)


def test_place_words_returns_dicts():
    result = mod.place_words(_sample_words(), 800, 400)
    assert all(isinstance(p, dict) for p in result)


def test_place_words_has_required_keys():
    result = mod.place_words(_sample_words(), 800, 400)
    for p in result:
        assert "word" in p
        assert "x" in p
        assert "y" in p
        assert "fs" in p
        assert "color" in p


def test_place_words_count_matches_input():
    words = _sample_words()
    result = mod.place_words(words, 800, 400)
    assert len(result) == len(words)


def test_place_words_word_names_preserved():
    words = _sample_words()
    result = mod.place_words(words, 800, 400)
    placed_words = {p["word"] for p in result}
    input_words = {w[0] for w in words}
    assert placed_words == input_words


def test_place_words_colors_from_palette():
    result = mod.place_words(_sample_words(), 800, 400)
    for p in result:
        assert p["color"] in mod.COLORS


def test_place_words_empty_input():
    result = mod.place_words([], 800, 400)
    assert result == []


def test_place_words_single_word():
    result = mod.place_words([("агент", 10, 24)], 800, 400)
    assert len(result) == 1
    assert result[0]["word"] == "агент"


def test_place_words_deterministic_with_seed():
    words = _sample_words()
    r1 = mod.place_words(words, 800, 400)
    r2 = mod.place_words(words, 800, 400)
    assert [p["x"] for p in r1] == [p["x"] for p in r2]


# ── make_svg ──────────────────────────────────────────────────────────────────

def _sample_placed():
    return [
        {"word": "агент", "x": 400, "y": 200, "fs": 36, "w": 80, "h": 44, "color": "#2563eb"},
        {"word": "память", "x": 250, "y": 150, "fs": 28, "w": 70, "h": 34, "color": "#16a34a"},
    ]


def test_make_svg_returns_string():
    result = mod.make_svg(_sample_placed(), 800, 400)
    assert isinstance(result, str)


def test_make_svg_starts_with_svg_tag():
    result = mod.make_svg(_sample_placed(), 800, 400)
    assert result.startswith("<svg")


def test_make_svg_ends_with_closing_svg():
    result = mod.make_svg(_sample_placed(), 800, 400)
    assert result.rstrip().endswith("</svg>")


def test_make_svg_contains_width():
    result = mod.make_svg(_sample_placed(), 800, 400)
    assert 'width="800"' in result


def test_make_svg_contains_height():
    result = mod.make_svg(_sample_placed(), 800, 400)
    assert 'height="400"' in result


def test_make_svg_contains_text_elements():
    result = mod.make_svg(_sample_placed(), 800, 400)
    assert "<text" in result


def test_make_svg_contains_all_words():
    placed = _sample_placed()
    result = mod.make_svg(placed, 800, 400)
    for p in placed:
        assert p["word"] in result


def test_make_svg_contains_colors():
    placed = _sample_placed()
    result = mod.make_svg(placed, 800, 400)
    assert "#2563eb" in result
    assert "#16a34a" in result


def test_make_svg_contains_background_rect():
    result = mod.make_svg(_sample_placed(), 800, 400)
    assert "<rect" in result


def test_make_svg_empty_placed():
    result = mod.make_svg([], 800, 400)
    assert result.startswith("<svg")
    assert result.rstrip().endswith("</svg>")
    assert "<text" not in result


def test_make_svg_valid_xmlns():
    result = mod.make_svg(_sample_placed(), 800, 400)
    assert 'xmlns="http://www.w3.org/2000/svg"' in result
