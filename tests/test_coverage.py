"""
Тесты для scripts/improve_coverage.py.

Покрытие:
  - check_features()  — проверка признаков документа
  - _word_count()     — подсчёт слов без комментариев
"""

import importlib
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(ROOT / "scripts"))

mod = importlib.import_module("improve_coverage")


# ── check_features ────────────────────────────────────────────────────────────

def test_check_features_returns_dict():
    result = mod.check_features("# Title\n\nContent.")
    assert isinstance(result, dict)


def test_check_features_has_all_keys():
    result = mod.check_features("# Title\n\nContent.")
    for key in ("summary", "tags", "toc", "crossrefs", "status", "backlinks"):
        assert key in result


def test_check_features_all_false_empty():
    result = mod.check_features("")
    for val in result.values():
        assert val is False


def test_check_features_detects_summary():
    result = mod.check_features("<!-- summary -->\n> Annotation.\n")
    assert result["summary"] is True


def test_check_features_detects_tags():
    result = mod.check_features("<!-- tags: memory, agent -->\n# Title\n")
    assert result["tags"] is True


def test_check_features_detects_toc():
    result = mod.check_features("## Содержание\n- [Section](#section)\n")
    assert result["toc"] is True


def test_check_features_detects_crossrefs():
    result = mod.check_features("## See also\n- [Related](#related)\n")
    assert result["crossrefs"] is True


def test_check_features_detects_status():
    result = mod.check_features("<!-- autofill-status -->\n")
    assert result["status"] is True


def test_check_features_detects_backlinks():
    result = mod.check_features("## Упоминается в\n- [File](file.md)\n")
    assert result["backlinks"] is True


def test_check_features_no_false_positives():
    result = mod.check_features("# Title\n\nRegular content without markers.\n")
    # None should be detected
    assert not any(result.values())


# ── _word_count ───────────────────────────────────────────────────────────────

def test_word_count_returns_int():
    result = mod._word_count("one two three")
    assert isinstance(result, int)


def test_word_count_counts_words():
    result = mod._word_count("one two three four five")
    assert result >= 4


def test_word_count_empty():
    result = mod._word_count("")
    assert result == 0


def test_word_count_excludes_comments():
    result_clean = mod._word_count("word")
    result_with_comment = mod._word_count("<!-- comment with words --> word")
    assert result_clean == result_with_comment


# ── main ──────────────────────────────────────────────────────────────────────

def test_main_creates_coverage_md(tmp_path, monkeypatch):
    monkeypatch.setattr(mod, "DOCS", tmp_path)
    monkeypatch.setattr(mod, "ROOT", tmp_path)
    monkeypatch.setattr(mod, "TARGET_SECTIONS", ["docs"])
    sec = tmp_path / "docs"
    sec.mkdir()
    (sec / "doc.md").write_text("# Title\n\nContent here.\n", encoding="utf-8")
    mod.main()
    assert (tmp_path / "COVERAGE.md").exists()


def test_main_coverage_has_content(tmp_path, monkeypatch):
    monkeypatch.setattr(mod, "DOCS", tmp_path)
    monkeypatch.setattr(mod, "ROOT", tmp_path)
    monkeypatch.setattr(mod, "TARGET_SECTIONS", ["docs"])
    sec = tmp_path / "docs"
    sec.mkdir()
    (sec / "doc.md").write_text("# Title\n\nContent here.\n", encoding="utf-8")
    mod.main()
    text = (tmp_path / "COVERAGE.md").read_text(encoding="utf-8")
    assert "# " in text


def test_main_empty_sections(tmp_path, monkeypatch):
    monkeypatch.setattr(mod, "DOCS", tmp_path)
    monkeypatch.setattr(mod, "ROOT", tmp_path)
    monkeypatch.setattr(mod, "TARGET_SECTIONS", [])
    mod.main()
    assert (tmp_path / "COVERAGE.md").exists()


def test_main_coverage_starts_with_heading(tmp_path, monkeypatch):
    monkeypatch.setattr(mod, "DOCS", tmp_path)
    monkeypatch.setattr(mod, "ROOT", tmp_path)
    monkeypatch.setattr(mod, "TARGET_SECTIONS", [])
    mod.main()
    text = (tmp_path / "COVERAGE.md").read_text(encoding="utf-8")
    assert text.strip().startswith("#")
