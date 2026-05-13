"""
Тесты для scripts/improve_heatmap.py.

Покрытие:
  - density()    — плотность тем в тексте (на 1000 слов)
  - heat_char()  — ASCII-символ тепловой карты по значению
"""

import importlib
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(ROOT / "scripts"))

mod = importlib.import_module("improve_heatmap")


# ── density ───────────────────────────────────────────────────────────────────

def test_density_returns_float():
    result = mod.density("agent memory system", ["agent", "memory"])
    assert isinstance(result, float)


def test_density_zero_for_no_match():
    result = mod.density("plain text here", ["xyz123", "nonexistent"])
    assert result == 0.0


def test_density_positive_for_match():
    result = mod.density("agent agent agent memory", ["agent"])
    assert result > 0.0


def test_density_per_thousand_words():
    # 1 keyword in 1000 words = density of 1.0
    text = "agent " + "word " * 999
    result = mod.density(text, ["agent"])
    assert abs(result - 1.0) < 0.1


def test_density_empty_text():
    result = mod.density("", ["agent"])
    assert result == 0.0


def test_density_multiple_keywords():
    result = mod.density("agent memory memory security", ["agent", "memory"])
    assert result > 0.0


def test_density_higher_for_more_occurrences():
    low = mod.density("agent word word word word", ["agent"])
    high = mod.density("agent agent agent word word", ["agent"])
    assert high > low


# ── heat_char ─────────────────────────────────────────────────────────────────

def test_heat_char_returns_string():
    result = mod.heat_char(5.0, 10.0)
    assert isinstance(result, str)


def test_heat_char_empty_for_zero_max():
    result = mod.heat_char(5.0, 0.0)
    assert result == "░░"


def test_heat_char_empty_for_zero_val():
    result = mod.heat_char(0.0, 10.0)
    assert result == "░░"


def test_heat_char_full_for_high_ratio():
    result = mod.heat_char(9.0, 10.0)  # ratio = 0.9 >= 0.8
    assert result == "██"


def test_heat_char_dark_for_above_60():
    result = mod.heat_char(7.0, 10.0)  # ratio = 0.7
    assert result == "▓▓"


def test_heat_char_medium_for_above_40():
    result = mod.heat_char(5.0, 10.0)  # ratio = 0.5
    assert result == "▒▒"


def test_heat_char_light_for_above_20():
    result = mod.heat_char(3.0, 10.0)  # ratio = 0.3
    assert result == "░░"


def test_heat_char_max_equals_value():
    result = mod.heat_char(10.0, 10.0)  # ratio = 1.0 >= 0.8
    assert result == "██"


# ── main ──────────────────────────────────────────────────────────────────────

def _setup_heatmap(tmp_path, monkeypatch):
    """Create a minimal section so heatmap doesn't fail on empty max()."""
    sec = tmp_path / "test-section"
    sec.mkdir(exist_ok=True)
    (sec / "doc.md").write_text("# AgentFS\n\nагент память svyazi memory.", encoding="utf-8")
    monkeypatch.setattr(mod, "DOCS", tmp_path)
    monkeypatch.setattr(mod, "ROOT", tmp_path)
    monkeypatch.setattr(mod, "SECTIONS", ["test-section"])


def test_main_creates_heatmap_md(tmp_path, monkeypatch):
    _setup_heatmap(tmp_path, monkeypatch)
    mod.main()
    assert (tmp_path / "HEATMAP.md").exists()


def test_main_heatmap_has_content(tmp_path, monkeypatch):
    _setup_heatmap(tmp_path, monkeypatch)
    mod.main()
    text = (tmp_path / "HEATMAP.md").read_text(encoding="utf-8")
    assert "# " in text


def test_main_heatmap_starts_with_heading(tmp_path, monkeypatch):
    _setup_heatmap(tmp_path, monkeypatch)
    mod.main()
    text = (tmp_path / "HEATMAP.md").read_text(encoding="utf-8")
    assert text.strip().startswith("#")


def test_main_heatmap_with_section(tmp_path, monkeypatch):
    _setup_heatmap(tmp_path, monkeypatch)
    mod.main()
    assert (tmp_path / "HEATMAP.md").exists()
