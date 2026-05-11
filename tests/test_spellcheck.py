"""
Тесты для scripts/improve_spellcheck.py.

Покрытие:
  - check_file_known()  — поиск известных опечаток
  - fix_known_typos()   — замена опечаток в тексте файла
"""

import importlib
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(ROOT / "scripts"))

mod = importlib.import_module("improve_spellcheck")

# ── check_file_known ──────────────────────────────────────────────────────────

def test_check_file_known_returns_list(tmp_path):
    f = tmp_path / "doc.md"
    f.write_text("# Title\n\nClean text without any typos.", encoding="utf-8")
    result = mod.check_file_known(f)
    assert isinstance(result, list)


def test_check_file_known_finds_typo(tmp_path):
    f = tmp_path / "doc.md"
    f.write_text("# Title\n\nThis is архтектура система.", encoding="utf-8")
    result = mod.check_file_known(f)
    assert len(result) >= 1
    typos = [r[0] for r in result]
    assert "архтектура" in typos


def test_check_file_known_finds_correction(tmp_path):
    f = tmp_path / "doc.md"
    f.write_text("# Title\n\nThis is архтектура система.", encoding="utf-8")
    result = mod.check_file_known(f)
    for typo, fix in result:
        if typo == "архтектура":
            assert fix == "архитектура"


def test_check_file_known_no_typos(tmp_path):
    f = tmp_path / "doc.md"
    f.write_text("# Title\n\nArchitecture is clean text with no known typos here.", encoding="utf-8")
    result = mod.check_file_known(f)
    # These known typos should not appear
    assert result == []


def test_check_file_known_deduplicates(tmp_path):
    f = tmp_path / "doc.md"
    f.write_text("архтектура архтектура архтектура", encoding="utf-8")
    result = mod.check_file_known(f)
    typos = [r[0] for r in result]
    assert typos.count("архтектура") == 1


def test_check_file_known_english_typo(tmp_path):
    f = tmp_path / "doc.md"
    f.write_text("# Title\n\nThis is antrhropic API usage.", encoding="utf-8")
    result = mod.check_file_known(f)
    typos = [r[0] for r in result]
    assert "antrhropic" in typos


def test_check_file_known_skips_code_blocks(tmp_path):
    f = tmp_path / "doc.md"
    # Known typo inside code block should be skipped
    f.write_text("# Title\n\n```\nархтектура\n```\n\nClean text.", encoding="utf-8")
    result = mod.check_file_known(f)
    assert result == []


# ── fix_known_typos ───────────────────────────────────────────────────────────

def test_fix_known_typos_returns_int(tmp_path):
    f = tmp_path / "doc.md"
    f.write_text("# Title\n\nСмотри архтектура системы.", encoding="utf-8")
    result = mod.fix_known_typos(f)
    assert isinstance(result, int)


def test_fix_known_typos_fixes_known_typo(tmp_path):
    f = tmp_path / "doc.md"
    f.write_text("# Title\n\nСмотри архтектура системы.", encoding="utf-8")
    mod.fix_known_typos(f)
    content = f.read_text(encoding="utf-8")
    assert "архитектура" in content
    assert "архтектура" not in content


def test_fix_known_typos_returns_count(tmp_path):
    f = tmp_path / "doc.md"
    f.write_text("архтектура архтектура текст", encoding="utf-8")
    count = mod.fix_known_typos(f)
    assert count >= 1


def test_fix_known_typos_no_typos_returns_zero(tmp_path):
    f = tmp_path / "doc.md"
    f.write_text("# Title\n\nClean text with no typos at all.", encoding="utf-8")
    count = mod.fix_known_typos(f)
    assert count == 0


def test_fix_known_typos_preserves_other_content(tmp_path):
    f = tmp_path / "doc.md"
    original = "# Important Title\n\nархтектура системы\n\n## Keep This Section\n"
    f.write_text(original, encoding="utf-8")
    mod.fix_known_typos(f)
    content = f.read_text(encoding="utf-8")
    assert "Important Title" in content
    assert "Keep This Section" in content


# ── main ──────────────────────────────────────────────────────────────────────

def test_main_dry_run_no_crash(tmp_path, monkeypatch):
    monkeypatch.setattr(mod, "DOCS", tmp_path)
    monkeypatch.setattr(mod, "ROOT", tmp_path)
    monkeypatch.setattr(mod, "SECTION_FILTER", None)
    monkeypatch.setattr(mod, "FIX", False)
    (tmp_path / "doc.md").write_text("# Title\n\nContent.", encoding="utf-8")
    mod.main()


def test_main_creates_spellcheck_md(tmp_path, monkeypatch):
    monkeypatch.setattr(mod, "DOCS", tmp_path)
    monkeypatch.setattr(mod, "ROOT", tmp_path)
    monkeypatch.setattr(mod, "SECTION_FILTER", None)
    monkeypatch.setattr(mod, "FIX", False)
    (tmp_path / "doc.md").write_text("# Title\n\nContent.", encoding="utf-8")
    mod.main()
    assert (tmp_path / "SPELLCHECK.md").exists()
