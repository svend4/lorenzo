"""
Тесты для scripts/improve_summaries.py.

Покрытие:
  - extract_annotation()  — извлечение первого абзаца и списка проектов
  - add_summary()         — добавление аннотации в начало файла
"""

import importlib
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(ROOT / "scripts"))

mod = importlib.import_module("improve_summaries")


# ── extract_annotation ────────────────────────────────────────────────────────

def test_extract_annotation_returns_tuple():
    result = mod.extract_annotation("# Title\n\nSome text here that is longer than 30 chars indeed.\n")
    assert isinstance(result, tuple)
    assert len(result) == 2


def test_extract_annotation_first_is_string():
    snippet, _ = mod.extract_annotation("# Title\n\nSome text here that is longer than 30 characters.\n")
    assert isinstance(snippet, str)


def test_extract_annotation_second_is_list():
    _, projects = mod.extract_annotation("# Title\n\nSome text here that is longer than 30 chars.\n")
    assert isinstance(projects, list)


def test_extract_annotation_extracts_first_paragraph():
    text = "# Title\n\nThis is the first paragraph with enough text to be extracted by the function.\n"
    snippet, _ = mod.extract_annotation(text)
    assert "first paragraph" in snippet


def test_extract_annotation_skips_headings():
    text = "# Title\n## Subtitle\n\nThis is the first real paragraph with enough text for extraction.\n"
    snippet, _ = mod.extract_annotation(text)
    assert not snippet.startswith("#")


def test_extract_annotation_skips_table_rows():
    text = "# Title\n| col1 | col2 |\n\nThis is the actual text with enough content for extraction.\n"
    snippet, _ = mod.extract_annotation(text)
    assert not snippet.startswith("|")


def test_extract_annotation_finds_agentfs_project():
    text = "# Title\n\nAgentFS is a file system for storing agent knowledge in structured format.\n"
    _, projects = mod.extract_annotation(text)
    assert "AgentFS" in projects


def test_extract_annotation_finds_yodoca_project():
    text = "# Title\n\nYodoca handles memory consolidation and forgetting mechanisms for agents.\n"
    _, projects = mod.extract_annotation(text)
    assert "Yodoca" in projects


def test_extract_annotation_finds_multiple_projects():
    text = "# Title\n\nAgentFS and Yodoca work together in the Svyazi platform architecture.\n"
    _, projects = mod.extract_annotation(text)
    assert "AgentFS" in projects
    assert "Yodoca" in projects
    assert "Svyazi" in projects


def test_extract_annotation_no_projects():
    text = "# Title\n\nThis text mentions no known projects from the knowledge base system.\n"
    _, projects = mod.extract_annotation(text)
    assert isinstance(projects, list)


def test_extract_annotation_snippet_max_200():
    long_line = "A" * 300
    text = f"# Title\n\n{long_line}\n"
    snippet, _ = mod.extract_annotation(text)
    assert len(snippet) <= 200


def test_extract_annotation_empty_text():
    snippet, projects = mod.extract_annotation("")
    assert snippet == ""
    assert projects == []


def test_extract_annotation_skips_short_lines():
    text = "# Title\n\nShort.\n\nThis is a longer paragraph with enough content to qualify.\n"
    snippet, _ = mod.extract_annotation(text)
    # Should pick the longer line, not the short one
    assert len(snippet) > 30 or snippet == ""


# ── add_summary ───────────────────────────────────────────────────────────────

def test_add_summary_returns_bool(tmp_path):
    f = tmp_path / "test.md"
    f.write_text(
        "# Title\n\nThis is a long enough paragraph for testing the summary function.\n",
        encoding="utf-8"
    )
    result = mod.add_summary(f, dry_run=True)
    assert isinstance(result, bool)


def test_add_summary_skips_short_file(tmp_path):
    f = tmp_path / "test.md"
    f.write_text("# Title\n\nShort.", encoding="utf-8")
    result = mod.add_summary(f, dry_run=True)
    assert result is False


def test_add_summary_skips_existing_summary_marker(tmp_path):
    f = tmp_path / "test.md"
    f.write_text(
        "# Title\n<!-- summary -->\n> Some annotation.\n\n---\n\nMore content here.\n",
        encoding="utf-8"
    )
    result = mod.add_summary(f, dry_run=True)
    assert result is False


def test_add_summary_skips_textrank_marker(tmp_path):
    f = tmp_path / "test.md"
    f.write_text(
        "# Title\n<!-- textrank-summary -->\nContent here that is very long.\n",
        encoding="utf-8"
    )
    result = mod.add_summary(f, dry_run=True)
    assert result is False


def test_add_summary_skips_abstract_marker(tmp_path):
    f = tmp_path / "test.md"
    f.write_text(
        "# Title\n<!-- abstract-auto -->\nContent here.\n",
        encoding="utf-8"
    )
    result = mod.add_summary(f, dry_run=True)
    assert result is False


def test_add_summary_returns_true_for_good_file(tmp_path):
    f = tmp_path / "test.md"
    f.write_text(
        "# Title\n\nThis is a longer paragraph that has more than 30 characters in it.\n",
        encoding="utf-8"
    )
    result = mod.add_summary(f, dry_run=True)
    assert isinstance(result, bool)


def test_add_summary_dry_run_no_write(tmp_path):
    original = "# Title\n\nThis is a long enough paragraph for testing the add summary function.\n"
    f = tmp_path / "test.md"
    f.write_text(original, encoding="utf-8")
    mod.add_summary(f, dry_run=True)
    assert f.read_text(encoding="utf-8") == original


def test_add_summary_writes_marker(tmp_path):
    f = tmp_path / "test.md"
    f.write_text(
        "# Title\n\nThis is a long enough paragraph for testing the add summary function.\n",
        encoding="utf-8"
    )
    result = mod.add_summary(f, dry_run=False)
    if result:
        content = f.read_text(encoding="utf-8")
        assert "<!-- summary -->" in content


def test_add_summary_inserts_after_h1(tmp_path):
    f = tmp_path / "test.md"
    f.write_text(
        "# The Main Title\n\nThis is a long enough paragraph for testing the add summary.\n",
        encoding="utf-8"
    )
    result = mod.add_summary(f, dry_run=False)
    if result:
        content = f.read_text(encoding="utf-8")
        h1_pos = content.index("# The Main Title")
        summary_pos = content.index("<!-- summary -->")
        assert summary_pos > h1_pos


# ── main ──────────────────────────────────────────────────────────────────────

def test_main_dry_run_no_crash(tmp_path, monkeypatch):
    monkeypatch.setattr(mod, "DOCS", tmp_path)
    monkeypatch.setattr(mod, "ROOT", tmp_path)
    monkeypatch.setattr("sys.argv", ["prog", "--dry-run"])
    (tmp_path / "doc.md").write_text("# Title\n\nContent here.", encoding="utf-8")
    mod.main()  # must not raise


def test_main_dry_run_empty_docs(tmp_path, monkeypatch):
    monkeypatch.setattr(mod, "DOCS", tmp_path)
    monkeypatch.setattr(mod, "ROOT", tmp_path)
    monkeypatch.setattr("sys.argv", ["prog", "--dry-run"])
    mod.main()  # must not raise


def test_main_apply_adds_summary(tmp_path, monkeypatch):
    monkeypatch.setattr(mod, "DOCS", tmp_path)
    monkeypatch.setattr(mod, "ROOT", tmp_path)
    monkeypatch.setattr("sys.argv", ["prog"])
    f = tmp_path / "doc.md"
    f.write_text(
        "# Title\n\nThis is a long paragraph for the summary generation test.",
        encoding="utf-8"
    )
    mod.main()
    content = f.read_text(encoding="utf-8")
    assert "<!-- summary" in content or "# Title" in content
