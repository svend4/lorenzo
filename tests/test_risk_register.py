"""
Тесты для scripts/improve_risk_register.py.

Покрытие:
  - risk_score()    — произведение вероятности и влияния
  - risk_level()    — текстовый уровень риска по score
  - make_matrix()   — 5×5 матрица рисков
"""

import importlib
import sys
from pathlib import Path

ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(ROOT / "scripts"))

mod = importlib.import_module("improve_risk_register")

# ── risk_score ────────────────────────────────────────────────────────────────

def test_risk_score_returns_int():
    assert isinstance(mod.risk_score(3, 4), int)


def test_risk_score_product():
    assert mod.risk_score(3, 4) == 12


def test_risk_score_ones():
    assert mod.risk_score(1, 1) == 1


def test_risk_score_max():
    assert mod.risk_score(5, 5) == 25


def test_risk_score_zero_prob():
    assert mod.risk_score(0, 5) == 0


def test_risk_score_zero_impact():
    assert mod.risk_score(4, 0) == 0


def test_risk_score_symmetric():
    assert mod.risk_score(3, 4) == mod.risk_score(4, 3)


# ── risk_level ────────────────────────────────────────────────────────────────

def test_risk_level_returns_string():
    assert isinstance(mod.risk_level(10), str)


def test_risk_level_critical_at_16():
    result = mod.risk_level(16)
    assert "КРИТИЧЕСКИЙ" in result


def test_risk_level_critical_at_25():
    result = mod.risk_level(25)
    assert "КРИТИЧЕСКИЙ" in result


def test_risk_level_high_at_9():
    result = mod.risk_level(9)
    assert "ВЫСОКИЙ" in result


def test_risk_level_high_at_15():
    result = mod.risk_level(15)
    assert "ВЫСОКИЙ" in result


def test_risk_level_medium_at_4():
    result = mod.risk_level(4)
    assert "СРЕДНИЙ" in result


def test_risk_level_medium_at_8():
    result = mod.risk_level(8)
    assert "СРЕДНИЙ" in result


def test_risk_level_low_at_1():
    result = mod.risk_level(1)
    assert "НИЗКИЙ" in result


def test_risk_level_low_at_3():
    result = mod.risk_level(3)
    assert "НИЗКИЙ" in result


def test_risk_level_boundary_16_is_critical():
    assert "КРИТИЧЕСКИЙ" in mod.risk_level(16)


def test_risk_level_boundary_15_is_high():
    assert "ВЫСОКИЙ" in mod.risk_level(15)


def test_risk_level_boundary_9_is_high():
    assert "ВЫСОКИЙ" in mod.risk_level(9)


def test_risk_level_boundary_8_is_medium():
    assert "СРЕДНИЙ" in mod.risk_level(8)


def test_risk_level_boundary_4_is_medium():
    assert "СРЕДНИЙ" in mod.risk_level(4)


def test_risk_level_boundary_3_is_low():
    assert "НИЗКИЙ" in mod.risk_level(3)


# ── make_matrix ───────────────────────────────────────────────────────────────

def test_make_matrix_returns_list():
    result = mod.make_matrix()
    assert isinstance(result, list)


def test_make_matrix_non_empty():
    result = mod.make_matrix()
    assert len(result) > 0


def test_make_matrix_starts_with_code_fence():
    result = mod.make_matrix()
    assert result[0] == "```"


def test_make_matrix_ends_with_code_fence():
    result = mod.make_matrix()
    assert result[-1] == "```"


def test_make_matrix_has_5_data_rows():
    result = mod.make_matrix()
    # header line + 5 impact rows inside code fence
    inner = result[1:-1]  # exclude ``` fences
    data_rows = [r for r in inner if "|" in r]
    assert len(data_rows) == 5


def test_make_matrix_contains_critical():
    result = mod.make_matrix()
    text = "\n".join(result)
    assert "КРИТ" in text


def test_make_matrix_contains_high():
    result = mod.make_matrix()
    text = "\n".join(result)
    assert "ВЫСК" in text


def test_make_matrix_contains_medium():
    result = mod.make_matrix()
    text = "\n".join(result)
    assert "СРЕД" in text


def test_make_matrix_contains_low():
    result = mod.make_matrix()
    text = "\n".join(result)
    assert "НИЗК" in text


def test_make_matrix_top_right_is_critical():
    # Impact 5, Probability 5 → score 25 → КРИТИЧЕСКИЙ
    result = mod.make_matrix()
    # First data row is impact=5 (highest)
    data_rows = [r for r in result if "|" in r]
    top_row = data_rows[0]
    assert "КРИТ" in top_row


def test_make_matrix_bottom_left_is_low():
    # Impact 1, Probability 1 → score 1 → НИЗКИЙ
    result = mod.make_matrix()
    data_rows = [r for r in result if "|" in r]
    bottom_row = data_rows[-1]
    assert "НИЗК" in bottom_row
