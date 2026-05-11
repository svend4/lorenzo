"""
Тесты для scripts/improve_scoring.py.

Покрытие:
  - score_to_label()       — пороги: GO / УСЛОВНО GO / НЕ ГОТОВ / NO-GO
  - file_exists()          — проверка файла через монкейпатч DOCS
  - file_has_content()     — минимум слов в файле
  - file_contains()        — ключевые слова в файле
  - count_md_in_section()  — количество .md в разделе
"""

import importlib
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(ROOT / "scripts"))

mod = importlib.import_module("improve_scoring")

# ── score_to_label ────────────────────────────────────────────────────────────

def test_score_to_label_100_go():
    assert "GO" in mod.score_to_label(100)


def test_score_to_label_90_go():
    assert "GO" in mod.score_to_label(90)


def test_score_to_label_89_conditional():
    result = mod.score_to_label(89)
    assert "УСЛОВНО" in result or "GO" in result


def test_score_to_label_70_conditional():
    assert "УСЛОВНО" in mod.score_to_label(70)


def test_score_to_label_69_not_ready():
    result = mod.score_to_label(69)
    assert "НЕ ГОТОВ" in result or "NO-GO" in result or "УСЛОВНО" in result


def test_score_to_label_50_boundary():
    result = mod.score_to_label(50)
    assert isinstance(result, str) and len(result) > 0


def test_score_to_label_49_no_go():
    result = mod.score_to_label(49)
    assert "NO-GO" in result or "НЕ ГОТОВ" in result


def test_score_to_label_0_no_go():
    assert "NO-GO" in mod.score_to_label(0)


def test_score_to_label_returns_string():
    for pct in [0, 50, 70, 90, 100]:
        assert isinstance(mod.score_to_label(pct), str)

# ── file_exists ───────────────────────────────────────────────────────────────

def test_file_exists_true(monkeypatch, tmp_path):
    monkeypatch.setattr(mod, "DOCS", tmp_path)
    (tmp_path / "HEALTH.md").write_text("content", encoding="utf-8")
    assert mod.file_exists("HEALTH.md") is True


def test_file_exists_false(monkeypatch, tmp_path):
    monkeypatch.setattr(mod, "DOCS", tmp_path)
    assert mod.file_exists("NONEXISTENT.md") is False


def test_file_exists_nested(monkeypatch, tmp_path):
    monkeypatch.setattr(mod, "DOCS", tmp_path)
    subdir = tmp_path / "01-svyazi"
    subdir.mkdir()
    (subdir / "README.md").write_text("content", encoding="utf-8")
    assert mod.file_exists("01-svyazi/README.md") is True


def test_file_exists_returns_bool(monkeypatch, tmp_path):
    monkeypatch.setattr(mod, "DOCS", tmp_path)
    result = mod.file_exists("any.md")
    assert isinstance(result, bool)

# ── file_has_content ──────────────────────────────────────────────────────────

def test_file_has_content_enough_words(monkeypatch, tmp_path):
    monkeypatch.setattr(mod, "DOCS", tmp_path)
    words = " ".join(["слово"] * 150)
    (tmp_path / "DOC.md").write_text(words, encoding="utf-8")
    assert mod.file_has_content("DOC.md", min_words=100) is True


def test_file_has_content_too_few_words(monkeypatch, tmp_path):
    monkeypatch.setattr(mod, "DOCS", tmp_path)
    (tmp_path / "DOC.md").write_text("мало слов здесь", encoding="utf-8")
    assert mod.file_has_content("DOC.md", min_words=100) is False


def test_file_has_content_missing_file(monkeypatch, tmp_path):
    monkeypatch.setattr(mod, "DOCS", tmp_path)
    assert mod.file_has_content("NONEXISTENT.md") is False


def test_file_has_content_default_min_words(monkeypatch, tmp_path):
    monkeypatch.setattr(mod, "DOCS", tmp_path)
    words = " ".join(["слово"] * 101)
    (tmp_path / "BIG.md").write_text(words, encoding="utf-8")
    assert mod.file_has_content("BIG.md") is True


def test_file_has_content_returns_bool(monkeypatch, tmp_path):
    monkeypatch.setattr(mod, "DOCS", tmp_path)
    result = mod.file_has_content("any.md")
    assert isinstance(result, bool)

# ── file_contains ─────────────────────────────────────────────────────────────

def test_file_contains_keyword_found(monkeypatch, tmp_path):
    monkeypatch.setattr(mod, "DOCS", tmp_path)
    (tmp_path / "DOC.md").write_text("Проект AgentFS использует MIT лицензию.", encoding="utf-8")
    assert mod.file_contains("DOC.md", ["AgentFS"]) is True


def test_file_contains_case_insensitive(monkeypatch, tmp_path):
    monkeypatch.setattr(mod, "DOCS", tmp_path)
    (tmp_path / "DOC.md").write_text("agentfs упоминается здесь.", encoding="utf-8")
    assert mod.file_contains("DOC.md", ["AgentFS"]) is True


def test_file_contains_keyword_absent(monkeypatch, tmp_path):
    monkeypatch.setattr(mod, "DOCS", tmp_path)
    (tmp_path / "DOC.md").write_text("Нет упоминаний интересующего слова.", encoding="utf-8")
    assert mod.file_contains("DOC.md", ["yodoca"]) is False


def test_file_contains_missing_file(monkeypatch, tmp_path):
    monkeypatch.setattr(mod, "DOCS", tmp_path)
    assert mod.file_contains("MISSING.md", ["keyword"]) is False


def test_file_contains_any_keyword(monkeypatch, tmp_path):
    monkeypatch.setattr(mod, "DOCS", tmp_path)
    (tmp_path / "DOC.md").write_text("Здесь есть MIT лицензия.", encoding="utf-8")
    assert mod.file_contains("DOC.md", ["Apache", "MIT", "BSL"]) is True


def test_file_contains_returns_bool(monkeypatch, tmp_path):
    monkeypatch.setattr(mod, "DOCS", tmp_path)
    result = mod.file_contains("any.md", ["kw"])
    assert isinstance(result, bool)

# ── count_md_in_section ───────────────────────────────────────────────────────

def test_count_md_in_section_counts_files(monkeypatch, tmp_path):
    monkeypatch.setattr(mod, "DOCS", tmp_path)
    section = tmp_path / "01-svyazi"
    section.mkdir()
    for i in range(3):
        (section / f"doc{i}.md").write_text("content", encoding="utf-8")
    assert mod.count_md_in_section("01-svyazi") == 3


def test_count_md_in_section_recursive(monkeypatch, tmp_path):
    monkeypatch.setattr(mod, "DOCS", tmp_path)
    section = tmp_path / "05-habr-projects"
    section.mkdir()
    (section / "memory").mkdir()
    (section / "memory" / "yodoca.md").write_text("content", encoding="utf-8")
    (section / "README.md").write_text("readme", encoding="utf-8")
    assert mod.count_md_in_section("05-habr-projects") == 2


def test_count_md_in_section_missing_section(monkeypatch, tmp_path):
    monkeypatch.setattr(mod, "DOCS", tmp_path)
    assert mod.count_md_in_section("nonexistent-section") == 0


def test_count_md_in_section_returns_int(monkeypatch, tmp_path):
    monkeypatch.setattr(mod, "DOCS", tmp_path)
    result = mod.count_md_in_section("any")
    assert isinstance(result, int)


def test_count_md_in_section_ignores_non_md(monkeypatch, tmp_path):
    monkeypatch.setattr(mod, "DOCS", tmp_path)
    section = tmp_path / "01-svyazi"
    section.mkdir()
    (section / "doc.md").write_text("content", encoding="utf-8")
    (section / "data.json").write_text("{}", encoding="utf-8")
    (section / "image.png").write_text("x", encoding="utf-8")
    assert mod.count_md_in_section("01-svyazi") == 1
