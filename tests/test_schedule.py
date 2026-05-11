"""
Тесты для scripts/improve_schedule.py.

Покрытие:
  - gantt_bar()  — ASCII Gantt-бар по кварталам
"""

import importlib
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(ROOT / "scripts"))

mod = importlib.import_module("improve_schedule")


# ── gantt_bar ─────────────────────────────────────────────────────────────────

def test_gantt_bar_returns_string():
    result = mod.gantt_bar(0, 2)
    assert isinstance(result, str)


def test_gantt_bar_correct_length():
    result = mod.gantt_bar(0, 2, total_q=8)
    assert len(result) == 8


def test_gantt_bar_empty_start():
    result = mod.gantt_bar(0, 0, total_q=8)
    assert result == "░" * 8


def test_gantt_bar_full():
    result = mod.gantt_bar(0, 8, total_q=8)
    assert result == "█" * 8


def test_gantt_bar_offset():
    result = mod.gantt_bar(2, 3, total_q=8)
    # First 2 chars = empty, next 3 = filled, rest = empty
    assert result[:2] == "░░"
    assert result[2:5] == "███"
    assert result[5:] == "░░░"


def test_gantt_bar_clamps_at_total():
    result = mod.gantt_bar(6, 5, total_q=8)
    # start=6 + duration=5 would exceed 8, so fill to 8
    assert len(result) == 8
    assert result[:6] == "░░░░░░"


def test_gantt_bar_single_quarter():
    result = mod.gantt_bar(3, 1, total_q=8)
    assert result[3] == "█"
    assert result[:3] == "░░░"
    assert result[4:] == "░░░░"


# ── main ──────────────────────────────────────────────────────────────────────

def test_main_creates_schedule_md(tmp_path, monkeypatch):
    monkeypatch.setattr(mod, "DOCS", tmp_path)
    monkeypatch.setattr(mod, "ROOT", tmp_path)
    (tmp_path / "doc.md").write_text("# Title\n\nQ1 2025 task planning.", encoding="utf-8")
    mod.main()
    assert (tmp_path / "SCHEDULE.md").exists()


def test_main_schedule_has_content(tmp_path, monkeypatch):
    monkeypatch.setattr(mod, "DOCS", tmp_path)
    monkeypatch.setattr(mod, "ROOT", tmp_path)
    (tmp_path / "doc.md").write_text("# Title\n\nQ1 2025 task planning.", encoding="utf-8")
    mod.main()
    text = (tmp_path / "SCHEDULE.md").read_text(encoding="utf-8")
    assert "# " in text


def test_main_empty_docs(tmp_path, monkeypatch):
    monkeypatch.setattr(mod, "DOCS", tmp_path)
    monkeypatch.setattr(mod, "ROOT", tmp_path)
    mod.main()
    assert (tmp_path / "SCHEDULE.md").exists()


def test_main_schedule_has_milestones(tmp_path, monkeypatch):
    monkeypatch.setattr(mod, "DOCS", tmp_path)
    monkeypatch.setattr(mod, "ROOT", tmp_path)
    mod.main()
    text = (tmp_path / "SCHEDULE.md").read_text(encoding="utf-8")
    assert "Milestone" in text or "Статус" in text or "%" in text or "Веха" in text
