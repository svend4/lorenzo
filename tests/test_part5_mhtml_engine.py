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


# ── extract_and_split ─────────────────────────────────────────────────────────

def test_extract_and_split_no_text_returns_early(tmp_path, monkeypatch, capsys):
    """Line 48-50: parse_mhtml returns empty string → early return with warning."""
    import part1_utils
    monkeypatch.setattr(part1_utils, "ROOT", tmp_path)
    monkeypatch.setattr(mod, "parse_mhtml", lambda p: "")
    mhtml = tmp_path / "fake.mhtml"
    mhtml.write_text("dummy", encoding="utf-8")
    mod.extract_and_split(mhtml, {}, tmp_path / "out")
    out = capsys.readouterr().out
    assert "WARNING" in out or "no text" in out.lower()


def test_extract_and_split_with_h2_sections(tmp_path, monkeypatch):
    """Lines 55-66: many H2 sections → writes files based on H2 headings."""
    import part1_utils
    monkeypatch.setattr(part1_utils, "ROOT", tmp_path)
    # Fake text with many H2 headings so len(h2_sections) > 3
    fake_text = "\n".join([
        f"## Section {i}\n\nContent for section {i}.\n"
        for i in range(5)
    ])
    monkeypatch.setattr(mod, "parse_mhtml", lambda p: fake_text)
    out_dir = tmp_path / "out"
    out_dir.mkdir()
    mhtml = tmp_path / "fake.mhtml"
    mhtml.write_text("dummy", encoding="utf-8")
    mod.extract_and_split(mhtml, {}, out_dir)
    # Should have created some .md files
    md_files = list(out_dir.glob("*.md"))
    assert len(md_files) > 0


def test_extract_and_split_with_no_title_h2(tmp_path, monkeypatch, capsys):
    """Lines 58-60: H2 section with empty title → fname = 00-intro.md."""
    import part1_utils, part2_split_md
    monkeypatch.setattr(part1_utils, "ROOT", tmp_path)
    # Split_by_h2 returns a list where first element has empty title
    fake_sections = [("", "Intro body content.")] + [
        (f"Section {i}", f"Body {i}") for i in range(4)
    ]
    monkeypatch.setattr(mod, "split_by_h2", lambda text: fake_sections)
    monkeypatch.setattr(mod, "parse_mhtml", lambda p: "fake text")
    out_dir = tmp_path / "out"
    out_dir.mkdir()
    mhtml = tmp_path / "fake.mhtml"
    mhtml.write_text("dummy", encoding="utf-8")
    mod.extract_and_split(mhtml, {}, out_dir)
    assert (out_dir / "00-intro.md").exists()


def test_extract_and_split_keyword_sections(tmp_path, monkeypatch):
    """Lines 68-76: few H2 sections → falls back to keyword splitting."""
    import part1_utils
    monkeypatch.setattr(part1_utils, "ROOT", tmp_path)
    # Only 1 H2 section so len <= 3 → keyword path
    monkeypatch.setattr(mod, "split_by_h2", lambda text: [("Only", "one section")])
    fake_text = "Research content here. Finance content here."
    monkeypatch.setattr(mod, "parse_mhtml", lambda p: fake_text)
    sections_map = {
        "Research": ("research.md", "Research Section"),
        "Finance": ("finance.md", "Finance Section"),
    }
    out_dir = tmp_path / "out"
    out_dir.mkdir()
    mhtml = tmp_path / "fake.mhtml"
    mhtml.write_text("dummy", encoding="utf-8")
    mod.extract_and_split(mhtml, sections_map, out_dir)
    # At least one file should be written
    md_files = list(out_dir.glob("*.md"))
    assert len(md_files) > 0


def test_extract_and_split_skips_existing_files(tmp_path, monkeypatch):
    """Line 65: dest.exists() check — if file already exists, skip it."""
    import part1_utils
    monkeypatch.setattr(part1_utils, "ROOT", tmp_path)
    fake_sections = [(f"Section {i}", f"Body {i}") for i in range(5)]
    monkeypatch.setattr(mod, "split_by_h2", lambda text: fake_sections)
    monkeypatch.setattr(mod, "parse_mhtml", lambda p: "fake text")
    out_dir = tmp_path / "out"
    out_dir.mkdir()
    # Pre-create one of the expected output files
    (out_dir / "00-Section 0.md").write_text("# Pre-existing", encoding="utf-8")
    mhtml = tmp_path / "fake.mhtml"
    mhtml.write_text("dummy", encoding="utf-8")
    mod.extract_and_split(mhtml, {}, out_dir)
    content = (out_dir / "00-Section 0.md").read_text(encoding="utf-8")
    assert content == "# Pre-existing"
