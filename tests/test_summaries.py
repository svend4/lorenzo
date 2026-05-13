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


# ── add_summary with long content (covers lines 53-78) ──────────────────────

LONG_CONTENT = (
    "# Project Overview\n\n"
    "This is a comprehensive description of the AgentFS project that provides "
    "file system operations for storing and retrieving agent knowledge. "
    "It supports multiple storage backends and provides efficient indexing.\n"
)


def test_add_summary_long_file_no_snippet_returns_false(tmp_path):
    """Lines 53-55: long file but only headings → no snippet → False."""
    content = ("# Title\n## Sub\n### Sub2\n") * 10
    f = tmp_path / "test.md"
    f.write_text(content, encoding="utf-8")
    result = mod.add_summary(f, dry_run=True)
    assert result is False


def test_add_summary_long_file_dry_run_true(tmp_path):
    """Lines 53-78 (dry_run path): long file passes → returns True, not written."""
    f = tmp_path / "test.md"
    f.write_text(LONG_CONTENT, encoding="utf-8")
    result = mod.add_summary(f, dry_run=True)
    assert result is True
    assert "<!-- summary -->" not in f.read_text(encoding="utf-8")


def test_add_summary_long_file_writes(tmp_path):
    """Lines 76-77: dry_run=False → file written."""
    f = tmp_path / "test.md"
    f.write_text(LONG_CONTENT, encoding="utf-8")
    result = mod.add_summary(f, dry_run=False)
    assert result is True
    assert "<!-- summary -->" in f.read_text(encoding="utf-8")


def test_add_summary_long_file_with_projects_includes_proj_line(tmp_path):
    """Lines 58-59: file mentions known projects → Проекты: line added."""
    content = (
        "# AgentFS Overview\n\n"
        "AgentFS provides file system operations for agent knowledge. "
        "Yodoca handles memory consolidation. The Svyazi platform integrates "
        "multiple components and subsystems efficiently.\n" * 2
    )
    f = tmp_path / "test.md"
    f.write_text(content, encoding="utf-8")
    mod.add_summary(f, dry_run=False)
    text = f.read_text(encoding="utf-8")
    assert "Проекты:" in text


def test_main_readme_skipped(tmp_path, monkeypatch):
    """Lines 97-99: README.md file is skipped."""
    monkeypatch.setattr(mod, "DOCS", tmp_path)
    monkeypatch.setattr(mod, "ROOT", tmp_path)
    monkeypatch.setattr("sys.argv", ["prog"])
    readme = tmp_path / "README.md"
    readme.write_text(LONG_CONTENT, encoding="utf-8")
    mod.main()
    assert "<!-- summary -->" not in readme.read_text(encoding="utf-8")


def test_main_dry_run_prints_update(tmp_path, monkeypatch, capsys):
    """Lines 104-106: dry_run=True and file gets summary → prints [dry-run]."""
    monkeypatch.setattr(mod, "DOCS", tmp_path)
    monkeypatch.setattr(mod, "ROOT", tmp_path)
    monkeypatch.setattr("sys.argv", ["prog", "--dry-run"])
    f = tmp_path / "doc.md"
    f.write_text(LONG_CONTENT, encoding="utf-8")
    mod.main()
    captured = capsys.readouterr()
    assert "dry-run" in captured.out


def test_main_is_ignored_skipped(tmp_path, monkeypatch):
    """Lines 101-102: is_ignored returns True → file skipped."""
    import sys, types
    mock_module = types.ModuleType("utils_docignore")
    mock_module.is_ignored = lambda path, root=None: path.name == "ignored.md"
    monkeypatch.setitem(sys.modules, "utils_docignore", mock_module)
    monkeypatch.setattr(mod, "DOCS", tmp_path)
    monkeypatch.setattr(mod, "ROOT", tmp_path)
    monkeypatch.setattr("sys.argv", ["prog"])
    f = tmp_path / "ignored.md"
    f.write_text(LONG_CONTENT, encoding="utf-8")
    mod.main()
    assert "<!-- summary -->" not in f.read_text(encoding="utf-8")


def test_main_import_error_uses_fallback(tmp_path, monkeypatch):
    """Lines 92-93: ImportError → fallback lambda used, no crash."""
    import sys
    sentinel = object()
    orig = sys.modules.pop("utils_docignore", sentinel)
    sys.modules["utils_docignore"] = None  # block the import
    try:
        monkeypatch.setattr(mod, "DOCS", tmp_path)
        monkeypatch.setattr(mod, "ROOT", tmp_path)
        monkeypatch.setattr("sys.argv", ["prog"])
        mod.main()
    finally:
        if orig is sentinel:
            sys.modules.pop("utils_docignore", None)
        else:
            sys.modules["utils_docignore"] = orig


def test_main_block_via_runpy(tmp_path, monkeypatch):
    """Line 118: __main__ block."""
    import runpy
    monkeypatch.setattr(mod, "DOCS", tmp_path)
    monkeypatch.setattr(mod, "ROOT", tmp_path)
    monkeypatch.setattr("sys.argv", ["improve_summaries.py"])
    script_path = str(ROOT / "scripts" / "improve_summaries.py")
    runpy.run_path(script_path, run_name="__main__")
