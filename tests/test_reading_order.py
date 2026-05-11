"""
Тесты для scripts/improve_reading_order.py.

Покрытие:
  - file_priority()      — приоритет файла по имени
  - estimate_difficulty() — сложность документа
"""

import importlib
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(ROOT / "scripts"))

mod = importlib.import_module("improve_reading_order")


# ── file_priority ─────────────────────────────────────────────────────────────

def test_file_priority_returns_int(tmp_path):
    f = tmp_path / "01-executive-summary.md"
    result = mod.file_priority(f)
    assert isinstance(result, int)


def test_file_priority_executive_summary_is_1(tmp_path):
    f = tmp_path / "01-executive-summary.md"
    result = mod.file_priority(f)
    assert result == 1


def test_file_priority_readme_is_1(tmp_path):
    f = tmp_path / "readme.md"
    result = mod.file_priority(f)
    assert result == 1


def test_file_priority_roadmap_is_8(tmp_path):
    f = tmp_path / "12-roadmap.md"
    result = mod.file_priority(f)
    assert result == 8


def test_file_priority_unknown_uses_number(tmp_path):
    f = tmp_path / "07-something.md"
    result = mod.file_priority(f)
    assert result == 7


def test_file_priority_no_number_fallback(tmp_path):
    f = tmp_path / "no-prefix-file.md"
    result = mod.file_priority(f)
    assert result == 50


def test_file_priority_mvp_is_7(tmp_path):
    f = tmp_path / "mvp-planning.md"
    result = mod.file_priority(f)
    assert result == 7


# ── estimate_difficulty ───────────────────────────────────────────────────────

def test_estimate_difficulty_returns_int():
    result = mod.estimate_difficulty(100, False, False)
    assert isinstance(result, int)


def test_estimate_difficulty_min_1():
    result = mod.estimate_difficulty(0, False, False)
    assert result >= 1


def test_estimate_difficulty_max_3():
    result = mod.estimate_difficulty(10000, True, True)
    assert result <= 3


def test_estimate_difficulty_short_easy():
    result = mod.estimate_difficulty(100, False, False)
    assert result == 1


def test_estimate_difficulty_medium():
    result = mod.estimate_difficulty(1500, False, False)
    # 1000+ words = +1 score
    assert result >= 1


def test_estimate_difficulty_long_hard():
    result = mod.estimate_difficulty(4000, True, True)
    assert result >= 2


def test_estimate_difficulty_code_increases():
    without = mod.estimate_difficulty(500, False, False)
    with_code = mod.estimate_difficulty(500, True, False)
    assert with_code >= without


def test_estimate_difficulty_table_increases():
    without = mod.estimate_difficulty(500, False, False)
    with_table = mod.estimate_difficulty(500, False, True)
    assert with_table >= without
