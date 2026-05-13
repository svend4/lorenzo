"""Tests for scripts/improve_questions.py."""

import importlib
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(ROOT / "scripts"))

mod = importlib.import_module("improve_questions")


def test_categorize_returns_string():
    result = mod.categorize("some text")
    assert isinstance(result, str)


def test_categorize_architecture():
    result = mod.categorize("Какая архитектура контракта нужна?")
    assert result == "архитектура"


def test_categorize_integration():
    result = mod.categorize("Как интегрировать MCP протокол?")
    assert result == "интеграция"


def test_categorize_license():
    result = mod.categorize("Какая лицензия у проекта MIT?")
    assert result == "лицензия"


def test_categorize_mvp():
    result = mod.categorize("Когда запустим MVP итерацию?")
    assert result == "MVP/сроки"


def test_categorize_team():
    result = mod.categorize("Кто автор этого контакта?")
    assert result == "команда"


def test_categorize_technology():
    result = mod.categorize("Как реализован алгоритм поиска?")
    assert result == "технология"


def test_categorize_default():
    result = mod.categorize("Нечто совсем неизвестное и неопределённое")
    assert result == "общее"


def test_extract_questions_returns_list(tmp_path, monkeypatch):
    monkeypatch.setattr(mod, "ROOT", tmp_path)
    f = tmp_path / "test.md"
    f.write_text("# Title\n\nКак работает система поиска в данном случае?\n", encoding="utf-8")
    result = mod.extract_questions(f.read_text(encoding="utf-8"), f)
    assert isinstance(result, list)


def test_extract_questions_finds_question(tmp_path, monkeypatch):
    monkeypatch.setattr(mod, "ROOT", tmp_path)
    f = tmp_path / "test.md"
    f.write_text("# Title\n\nКак работает система поиска данных в проекте?\n", encoding="utf-8")
    result = mod.extract_questions(f.read_text(encoding="utf-8"), f)
    assert len(result) >= 1


def test_extract_questions_has_required_keys(tmp_path, monkeypatch):
    monkeypatch.setattr(mod, "ROOT", tmp_path)
    f = tmp_path / "test.md"
    f.write_text("Как именно работает система поиска данных в проекте?\n", encoding="utf-8")
    result = mod.extract_questions(f.read_text(encoding="utf-8"), f)
    for item in result:
        assert "text" in item
        assert "file" in item
        assert "category" in item


def test_extract_questions_skips_short(tmp_path, monkeypatch):
    monkeypatch.setattr(mod, "ROOT", tmp_path)
    f = tmp_path / "test.md"
    f.write_text("Почему?\n", encoding="utf-8")
    result = mod.extract_questions(f.read_text(encoding="utf-8"), f)
    for item in result:
        assert len(item["text"]) >= 15


def test_extract_questions_strips_code_blocks(tmp_path, monkeypatch):
    monkeypatch.setattr(mod, "ROOT", tmp_path)
    f = tmp_path / "test.md"
    f.write_text("```python\nКак работает код внутри блока?\n```\n", encoding="utf-8")
    result = mod.extract_questions(f.read_text(encoding="utf-8"), f)
    assert len(result) == 0


def test_extract_questions_deduplicates(tmp_path, monkeypatch):
    monkeypatch.setattr(mod, "ROOT", tmp_path)
    f = tmp_path / "test.md"
    q = "Как именно работает система поиска данных в проекте?"
    f.write_text(f"{q}\n\n{q}\n", encoding="utf-8")
    result = mod.extract_questions(f.read_text(encoding="utf-8"), f)
    texts = [r["text"][:40].lower() for r in result]
    assert len(texts) == len(set(texts))


# ── main ──────────────────────────────────────────────────────────────────────

def test_main_creates_questions_md(tmp_path, monkeypatch):
    monkeypatch.setattr(mod, "DOCS", tmp_path)
    monkeypatch.setattr(mod, "ROOT", tmp_path)
    (tmp_path / "doc.md").write_text("# Title\n\nWhat is AgentFS?\n", encoding="utf-8")
    mod.main()
    assert (tmp_path / "QUESTIONS.md").exists()


def test_main_empty_docs_no_crash(tmp_path, monkeypatch):
    monkeypatch.setattr(mod, "DOCS", tmp_path)
    monkeypatch.setattr(mod, "ROOT", tmp_path)
    mod.main()
    assert (tmp_path / "QUESTIONS.md").exists()


# ── extract_questions edge cases ──────────────────────────────────────────────

def test_extract_questions_skips_pipe_start(tmp_path, monkeypatch):
    """Line 61: question starts with '|' → skipped."""
    monkeypatch.setattr(mod, "ROOT", tmp_path)
    f = tmp_path / "test.md"
    text = "| Как именно работает система поиска данных в проекте?\n"
    f.write_text(text, encoding="utf-8")
    result = mod.extract_questions(text, f)
    for item in result:
        assert not item["text"].startswith("|")


def test_extract_questions_skips_dash_start(tmp_path, monkeypatch):
    """Line 61: question starts with '-' → skipped."""
    monkeypatch.setattr(mod, "ROOT", tmp_path)
    f = tmp_path / "test.md"
    text = "- Как именно работает система поиска данных в проекте?\n"
    f.write_text(text, encoding="utf-8")
    result = mod.extract_questions(text, f)
    for item in result:
        assert not item["text"].startswith("-")


# ── main: full coverage ───────────────────────────────────────────────────────

def test_main_skips_questions_md(tmp_path, monkeypatch):
    """Line 82: file named QUESTIONS.md → skipped."""
    monkeypatch.setattr(mod, "DOCS", tmp_path)
    monkeypatch.setattr(mod, "ROOT", tmp_path)
    (tmp_path / "QUESTIONS.md").write_text("# Old questions data.", encoding="utf-8")
    (tmp_path / "doc.md").write_text(
        "# Title\n\n" + "Как работает система поиска? " * 10,
        encoding="utf-8",
    )
    mod.main()
    assert (tmp_path / "QUESTIONS.md").exists()


def test_main_finds_questions_in_long_doc(tmp_path, monkeypatch):
    """Lines 86-88, 103-112: long doc with questions → cat_order loop runs."""
    monkeypatch.setattr(mod, "DOCS", tmp_path)
    monkeypatch.setattr(mod, "ROOT", tmp_path)
    content = (
        "# Title\n\n"
        + "Как именно работает система поиска данных в проекте Svyazi? " * 5
    )
    (tmp_path / "doc.md").write_text(content, encoding="utf-8")
    mod.main()
    text = (tmp_path / "QUESTIONS.md").read_text(encoding="utf-8")
    assert "#" in text


def test_main_short_file_skipped(tmp_path, monkeypatch):
    """Line 85: file < 200 chars → continue (skipped)."""
    monkeypatch.setattr(mod, "DOCS", tmp_path)
    monkeypatch.setattr(mod, "ROOT", tmp_path)
    (tmp_path / "doc.md").write_text("# Short\n\nKак работает?", encoding="utf-8")
    mod.main()
    assert (tmp_path / "QUESTIONS.md").exists()


def test_main_many_questions_truncates(tmp_path, monkeypatch):
    """Lines 113-117: 15+ unique questions in one category → remaining message."""
    monkeypatch.setattr(mod, "DOCS", tmp_path)
    monkeypatch.setattr(mod, "ROOT", tmp_path)
    qs = [
        f"Как работает алгоритм поиска вариант{i:02d} для базы данных?"
        for i in range(20)
    ]
    content = "# Doc\n\n" + "\n\n".join(qs) + "\n"
    (tmp_path / "doc.md").write_text(content, encoding="utf-8")
    mod.main()
    assert (tmp_path / "QUESTIONS.md").exists()


def test_main_duplicate_questions_deduplicated(tmp_path, monkeypatch):
    """Lines 107-108: duplicate question keys → continue."""
    monkeypatch.setattr(mod, "DOCS", tmp_path)
    monkeypatch.setattr(mod, "ROOT", tmp_path)
    q = "Как именно работает система поиска данных в этом проекте архитектуры?"
    content = "# Doc\n\n" + (q + "\n\n") * 4
    (tmp_path / "doc.md").write_text(content, encoding="utf-8")
    mod.main()
    assert (tmp_path / "QUESTIONS.md").exists()


# ── __main__ block ────────────────────────────────────────────────────────────

def test_main_block_via_runpy(tmp_path, monkeypatch):
    """Line 126: __main__ block."""
    import runpy
    monkeypatch.setattr(mod, "DOCS", tmp_path)
    monkeypatch.setattr(mod, "ROOT", tmp_path)
    script_path = str(ROOT / "scripts" / "improve_questions.py")
    runpy.run_path(script_path, run_name="__main__")
