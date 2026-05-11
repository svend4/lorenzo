"""Tests for scripts/part5_mhtml_engine.py."""

import importlib
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(ROOT / "scripts"))

mod = importlib.import_module("part5_mhtml_engine")


# ── split_by_keyword_sections ─────────────────────────────────────────────────

def test_split_by_keyword_sections_returns_dict():
    text = "Introduction text. Research & ML is important."
    result = mod.split_by_keyword_sections(text, ["Research & ML"])
    assert isinstance(result, dict)


def test_split_by_keyword_sections_finds_keyword():
    text = "Intro. Research & ML is key topic. More content."
    result = mod.split_by_keyword_sections(text, ["Research & ML"])
    assert "Research & ML" in result


def test_split_by_keyword_sections_case_insensitive():
    text = "Intro. RESEARCH & ML here. More."
    result = mod.split_by_keyword_sections(text, ["research & ml"])
    assert "research & ml" in result


def test_split_by_keyword_sections_empty_keywords():
    text = "Some content here."
    result = mod.split_by_keyword_sections(text, [])
    assert result == {}


def test_split_by_keyword_sections_missing_keyword():
    text = "Only unrelated content."
    result = mod.split_by_keyword_sections(text, ["Nonexistent Keyword XYZ"])
    assert "Nonexistent Keyword XYZ" not in result


def test_split_by_keyword_sections_multiple_keywords():
    text = "Intro. Security important. Finance also. Trust & Safety last."
    result = mod.split_by_keyword_sections(text, ["Security", "Finance", "Trust & Safety"])
    assert len(result) >= 2


def test_split_by_keyword_sections_section_text():
    text = "Intro. Keyword ABC here. Some long text after it. Next Keyword DEF here."
    result = mod.split_by_keyword_sections(text, ["Keyword ABC", "Keyword DEF"])
    assert "Keyword ABC" in result
    body = result["Keyword ABC"]
    assert "Keyword ABC" in body


def test_split_by_keyword_sections_last_keyword_to_end():
    text = "Intro. LastKeyword here. This text goes to end."
    result = mod.split_by_keyword_sections(text, ["LastKeyword"])
    body = result["LastKeyword"]
    assert "This text goes to end." in body


# ── write_mhtml_section ───────────────────────────────────────────────────────

def test_write_mhtml_section_creates_file(tmp_path, monkeypatch):
    import part1_utils
    monkeypatch.setattr(part1_utils, "ROOT", tmp_path)

    dest = tmp_path / "section.md"
    mod.write_mhtml_section("Content text.", dest, "My Title")
    assert dest.exists()


def test_write_mhtml_section_includes_title(tmp_path, monkeypatch):
    import part1_utils
    monkeypatch.setattr(part1_utils, "ROOT", tmp_path)

    dest = tmp_path / "section.md"
    mod.write_mhtml_section("Content text.", dest, "My Title")
    text = dest.read_text(encoding="utf-8")
    assert "# My Title" in text


def test_write_mhtml_section_includes_content(tmp_path, monkeypatch):
    import part1_utils
    monkeypatch.setattr(part1_utils, "ROOT", tmp_path)

    dest = tmp_path / "section.md"
    mod.write_mhtml_section("The actual content here.", dest, "Title")
    text = dest.read_text(encoding="utf-8")
    assert "The actual content here." in text
