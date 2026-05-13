"""Tests for scripts/improve_export_report.py."""

import importlib
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(ROOT / "scripts"))

mod = importlib.import_module("improve_export_report")


def test_read_md_missing(tmp_path, monkeypatch):
    monkeypatch.setattr(mod, "DOCS", tmp_path)
    result = mod._read_md("missing.md")
    assert result == ""


def test_read_md_existing(tmp_path, monkeypatch):
    monkeypatch.setattr(mod, "DOCS", tmp_path)
    f = tmp_path / "test.md"
    f.write_text("# Title\n\nContent.", encoding="utf-8")
    result = mod._read_md("test.md")
    assert "Title" in result


def test_read_json_missing(tmp_path, monkeypatch):
    monkeypatch.setattr(mod, "DOCS", tmp_path)
    result = mod._read_json("missing.json")
    assert result == {}


def test_read_json_valid(tmp_path, monkeypatch):
    import json
    monkeypatch.setattr(mod, "DOCS", tmp_path)
    f = tmp_path / "data.json"
    f.write_text(json.dumps({"key": "value"}), encoding="utf-8")
    result = mod._read_json("data.json")
    assert result == {"key": "value"}


def test_extract_section_returns_list():
    text = "# Title\n\n## Section A\n\nContent line 1\nContent line 2\n\n## Section B\n\nOther"
    result = mod._extract_section(text, "Section A")
    assert isinstance(result, list)


def test_extract_section_finds_content():
    text = "# Title\n\n## Important Section\n\nFirst line of content\nSecond line\n\n## Next Section\n"
    result = mod._extract_section(text, "Important Section")
    assert any("First line" in r for r in result)


def test_extract_section_missing_heading():
    text = "# Title\n\nContent without the section.\n"
    result = mod._extract_section(text, "Nonexistent Section")
    assert result == []


def test_extract_section_respects_max_lines():
    lines = "\n".join(f"Line {i}" for i in range(50))
    text = f"## Section\n\n{lines}\n"
    result = mod._extract_section(text, "Section", max_lines=5)
    assert len(result) <= 5


def test_extract_table_rows_returns_list():
    text = "## Table Section\n\n| A | B |\n|---|---|\n| 1 | 2 |\n"
    result = mod._extract_table_rows(text, "Table Section")
    assert isinstance(result, list)


def test_extract_table_rows_finds_rows():
    text = "## Authors\n\n| Author | Project |\n|--------|--------|\n| Alice | Project A |\n| Bob | Project B |\n"
    result = mod._extract_table_rows(text, "Authors")
    assert len(result) >= 2  # header + 2 data rows (not separator)


def test_extract_table_rows_skips_separator():
    text = "## Table\n\n| Col |\n|-----|\n| Data |\n"
    result = mod._extract_table_rows(text, "Table")
    # Should not include separator row
    assert not any("---" in row for row in result)


def test_key_decisions_returns_list(tmp_path, monkeypatch):
    monkeypatch.setattr(mod, "DOCS", tmp_path)
    (tmp_path / "DECISIONS.md").write_text(
        "# Decisions\n\n- Use Python 3.11 for the project\n- Choose MIT license\n",
        encoding="utf-8"
    )
    result = mod._key_decisions(n=5)
    assert isinstance(result, list)


def test_key_decisions_finds_items(tmp_path, monkeypatch):
    monkeypatch.setattr(mod, "DOCS", tmp_path)
    (tmp_path / "DECISIONS.md").write_text(
        "# Decisions\n\n- Use Python 3.11 for the project\n- Choose MIT license\n",
        encoding="utf-8"
    )
    result = mod._key_decisions(n=5)
    assert len(result) >= 1


def test_key_decisions_missing_file(tmp_path, monkeypatch):
    monkeypatch.setattr(mod, "DOCS", tmp_path)
    result = mod._key_decisions()
    assert result == []


def test_open_questions_returns_list(tmp_path, monkeypatch):
    monkeypatch.setattr(mod, "DOCS", tmp_path)
    (tmp_path / "QUESTIONS.md").write_text(
        "# Questions\n\n- What is the best memory approach?\n- How to handle concurrency?\n",
        encoding="utf-8"
    )
    result = mod._open_questions(n=5)
    assert isinstance(result, list)


# ── main ──────────────────────────────────────────────────────────────────────

def test_main_creates_report_md(tmp_path, monkeypatch):
    monkeypatch.setattr(mod, "DOCS", tmp_path)
    monkeypatch.setattr(mod, "ROOT", tmp_path)
    (tmp_path / "doc.md").write_text("# AgentFS\n\nContent.", encoding="utf-8")
    mod.main()
    assert (tmp_path / "REPORT.md").exists()


def test_main_report_has_content(tmp_path, monkeypatch):
    monkeypatch.setattr(mod, "DOCS", tmp_path)
    monkeypatch.setattr(mod, "ROOT", tmp_path)
    (tmp_path / "doc.md").write_text("# AgentFS\n\nContent.", encoding="utf-8")
    mod.main()
    text = (tmp_path / "REPORT.md").read_text(encoding="utf-8")
    assert "# " in text


def test_main_empty_docs_no_crash(tmp_path, monkeypatch):
    monkeypatch.setattr(mod, "DOCS", tmp_path)
    monkeypatch.setattr(mod, "ROOT", tmp_path)
    mod.main()
    assert (tmp_path / "REPORT.md").exists()
