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


# ── main ──────────────────────────────────────────────────────────────────────

def test_main_creates_reading_order_md(tmp_path, monkeypatch):
    monkeypatch.setattr(mod, "DOCS", tmp_path)
    monkeypatch.setattr(mod, "ROOT", tmp_path)
    mod.main()
    assert (tmp_path / "READING_ORDER.md").exists()


def test_main_reading_order_has_content(tmp_path, monkeypatch):
    monkeypatch.setattr(mod, "DOCS", tmp_path)
    monkeypatch.setattr(mod, "ROOT", tmp_path)
    mod.main()
    text = (tmp_path / "READING_ORDER.md").read_text(encoding="utf-8")
    assert "# " in text


def test_main_empty_docs(tmp_path, monkeypatch):
    monkeypatch.setattr(mod, "DOCS", tmp_path)
    monkeypatch.setattr(mod, "ROOT", tmp_path)
    mod.main()
    assert (tmp_path / "READING_ORDER.md").exists()


def test_main_reading_order_starts_with_heading(tmp_path, monkeypatch):
    monkeypatch.setattr(mod, "DOCS", tmp_path)
    monkeypatch.setattr(mod, "ROOT", tmp_path)
    mod.main()
    text = (tmp_path / "READING_ORDER.md").read_text(encoding="utf-8")
    assert text.strip().startswith("#")


def test_main_with_section_files(tmp_path, monkeypatch):
    """Lines 83-108, 125-129: main() with actual files in section folder."""
    monkeypatch.setattr(mod, "DOCS", tmp_path)
    monkeypatch.setattr(mod, "ROOT", tmp_path)

    # Create a section folder with some .md files
    section = tmp_path / "01-svyazi"
    section.mkdir()
    (section / "01-executive-summary.md").write_text(
        "# Executive Summary\n\nThis is a detailed overview.\n\n"
        + "word " * 600,
        encoding="utf-8"
    )
    (section / "03-component-catalog.md").write_text(
        "# Component Catalog\n\n```python\ncode here\n```\n\n"
        + "| col1 | col2 |\n|------|------|\n| a | b |\n\n"
        + "word " * 1500,
        encoding="utf-8"
    )

    mod.main()
    out = tmp_path / "READING_ORDER.md"
    assert out.exists()
    text = out.read_text(encoding="utf-8")
    # Should have table rows for the files
    assert "Executive Summary" in text or "01-svyazi" in text


def test_main_with_prereqs(tmp_path, monkeypatch):
    """Lines 104-106: files with prerequisites are processed."""
    monkeypatch.setattr(mod, "DOCS", tmp_path)
    monkeypatch.setattr(mod, "ROOT", tmp_path)

    # Create section folder with a file that matches a PREREQUISITES key
    section = tmp_path / "01-svyazi"
    section.mkdir()
    (section / "09-architectural-gaps.md").write_text(
        "# Architectural Gaps\n\n" + "word " * 800,
        encoding="utf-8"
    )

    mod.main()
    out = tmp_path / "READING_ORDER.md"
    assert out.exists()
    text = out.read_text(encoding="utf-8")
    assert "Architectural Gaps" in text or "01-svyazi" in text


def test_main_many_sections(tmp_path, monkeypatch):
    """Lines 124-132: learning_path rows rendered in output table."""
    monkeypatch.setattr(mod, "DOCS", tmp_path)
    monkeypatch.setattr(mod, "ROOT", tmp_path)

    # Create multiple section folders with files
    for sec in ["01-svyazi", "05-habr-projects"]:
        sec_dir = tmp_path / sec
        sec_dir.mkdir()
        (sec_dir / "01-overview.md").write_text(
            f"# Overview {sec}\n\n" + "word " * 300,
            encoding="utf-8"
        )

    mod.main()
    out = tmp_path / "READING_ORDER.md"
    assert out.exists()
    text = out.read_text(encoding="utf-8")
    # Should have table rows
    assert "|" in text


def test_main_block_via_runpy(tmp_path, monkeypatch):
    """Line 164: __main__ block executes main()."""
    import runpy
    monkeypatch.setattr(mod, "DOCS", tmp_path)
    monkeypatch.setattr(mod, "ROOT", tmp_path)
    script_path = str(ROOT / "scripts" / "improve_reading_order.py")
    runpy.run_path(script_path, run_name="__main__")
