"""
Тесты для scripts/improve_broken_links.py.

Покрытие:
  - anchor_from_heading() — GitHub-style якорь из заголовка
  - build_anchor_map()    — словарь file → set of valid anchors
  - check_links()         — проверка ссылок в файле
"""

import importlib
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(ROOT / "scripts"))

mod = importlib.import_module("improve_broken_links")

# ── anchor_from_heading ───────────────────────────────────────────────────────

def test_anchor_from_heading_returns_string():
    result = mod.anchor_from_heading("My Heading")
    assert isinstance(result, str)


def test_anchor_from_heading_starts_with_hash():
    result = mod.anchor_from_heading("My Heading")
    assert result.startswith("#")


def test_anchor_from_heading_lowercases():
    result = mod.anchor_from_heading("My Heading")
    assert result == result.lower()


def test_anchor_from_heading_replaces_spaces_with_dashes():
    result = mod.anchor_from_heading("My Section Title")
    assert result == "#my-section-title"


def test_anchor_from_heading_removes_special_chars():
    result = mod.anchor_from_heading("Title: With Special Chars!")
    assert ":" not in result
    assert "!" not in result


def test_anchor_from_heading_simple():
    result = mod.anchor_from_heading("hello world")
    assert result == "#hello-world"


def test_anchor_from_heading_preserves_hyphens():
    result = mod.anchor_from_heading("my-already-hyphenated")
    assert result == "#my-already-hyphenated"


def test_anchor_from_heading_cyrillic():
    result = mod.anchor_from_heading("Архитектура системы")
    assert result.startswith("#")
    # Letters preserved, spaces → dashes
    assert " " not in result[1:]


# ── build_anchor_map ──────────────────────────────────────────────────────────

def test_build_anchor_map_returns_dict(tmp_path, monkeypatch):
    monkeypatch.setattr(mod, "DOCS", tmp_path)
    monkeypatch.setattr(mod, "SECTION", "")
    result = mod.build_anchor_map()
    assert isinstance(result, dict)


def test_build_anchor_map_empty_docs(tmp_path, monkeypatch):
    monkeypatch.setattr(mod, "DOCS", tmp_path)
    monkeypatch.setattr(mod, "SECTION", "")
    result = mod.build_anchor_map()
    assert result == {}


def test_build_anchor_map_finds_headings(tmp_path, monkeypatch):
    monkeypatch.setattr(mod, "DOCS", tmp_path)
    monkeypatch.setattr(mod, "SECTION", "")
    f = tmp_path / "doc.md"
    f.write_text("# Title\n\n## My Section\n\n### Subsection\n", encoding="utf-8")
    result = mod.build_anchor_map()
    assert str(f) in result
    anchors = result[str(f)]
    assert "#my-section" in anchors


def test_build_anchor_map_values_are_sets(tmp_path, monkeypatch):
    monkeypatch.setattr(mod, "DOCS", tmp_path)
    monkeypatch.setattr(mod, "SECTION", "")
    f = tmp_path / "doc.md"
    f.write_text("# Title\n## Section\n", encoding="utf-8")
    result = mod.build_anchor_map()
    assert isinstance(result[str(f)], set)


# ── check_links ───────────────────────────────────────────────────────────────

def test_check_links_returns_tuple(tmp_path, monkeypatch):
    monkeypatch.setattr(mod, "DOCS", tmp_path)
    monkeypatch.setattr(mod, "ROOT", tmp_path)
    f = tmp_path / "source.md"
    f.write_text("# Title\n\nNo links here.", encoding="utf-8")
    result = mod.check_links(f, {})
    assert isinstance(result, tuple)
    assert len(result) == 2


def test_check_links_no_links_no_errors(tmp_path, monkeypatch):
    monkeypatch.setattr(mod, "DOCS", tmp_path)
    monkeypatch.setattr(mod, "ROOT", tmp_path)
    f = tmp_path / "source.md"
    f.write_text("# Title\n\nNo links here.", encoding="utf-8")
    broken, ok = mod.check_links(f, {})
    assert broken == []


def test_check_links_valid_link_no_error(tmp_path, monkeypatch):
    monkeypatch.setattr(mod, "DOCS", tmp_path)
    monkeypatch.setattr(mod, "ROOT", tmp_path)
    target = tmp_path / "target.md"
    target.write_text("# Target", encoding="utf-8")
    source = tmp_path / "source.md"
    source.write_text("See [Target](target.md) here.", encoding="utf-8")
    anchor_map = {str(target): set()}
    broken, ok = mod.check_links(source, anchor_map)
    assert broken == []


def test_check_links_missing_file_detected(tmp_path, monkeypatch):
    monkeypatch.setattr(mod, "DOCS", tmp_path)
    monkeypatch.setattr(mod, "ROOT", tmp_path)
    source = tmp_path / "source.md"
    source.write_text("See [Missing](nonexistent.md) here.", encoding="utf-8")
    broken, ok = mod.check_links(source, {})
    assert len(broken) >= 1


def test_check_links_http_links_skipped(tmp_path, monkeypatch):
    monkeypatch.setattr(mod, "DOCS", tmp_path)
    monkeypatch.setattr(mod, "ROOT", tmp_path)
    source = tmp_path / "source.md"
    source.write_text("See [External](https://example.com) here.", encoding="utf-8")
    broken, ok = mod.check_links(source, {})
    assert broken == []


# ── main ──────────────────────────────────────────────────────────────────────

def test_main_creates_broken_links_md(tmp_path, monkeypatch):
    monkeypatch.setattr(mod, "DOCS", tmp_path)
    monkeypatch.setattr(mod, "ROOT", tmp_path)
    monkeypatch.setattr(mod, "SECTION", "")
    monkeypatch.setattr(mod, "FIX", False)
    monkeypatch.setattr(mod, "DRY_RUN", False)
    mod.main()
    assert (tmp_path / "BROKEN_LINKS.md").exists()


def test_main_broken_links_has_content(tmp_path, monkeypatch):
    monkeypatch.setattr(mod, "DOCS", tmp_path)
    monkeypatch.setattr(mod, "ROOT", tmp_path)
    monkeypatch.setattr(mod, "SECTION", "")
    monkeypatch.setattr(mod, "FIX", False)
    monkeypatch.setattr(mod, "DRY_RUN", False)
    (tmp_path / "doc.md").write_text(
        "# Title\n\nSee [internal](other.md) here.", encoding="utf-8"
    )
    mod.main()
    text = (tmp_path / "BROKEN_LINKS.md").read_text(encoding="utf-8")
    assert "# " in text


def test_main_empty_docs(tmp_path, monkeypatch):
    monkeypatch.setattr(mod, "DOCS", tmp_path)
    monkeypatch.setattr(mod, "ROOT", tmp_path)
    monkeypatch.setattr(mod, "SECTION", "")
    monkeypatch.setattr(mod, "FIX", False)
    monkeypatch.setattr(mod, "DRY_RUN", False)
    mod.main()
    assert (tmp_path / "BROKEN_LINKS.md").exists()


def test_main_broken_links_starts_with_heading(tmp_path, monkeypatch):
    monkeypatch.setattr(mod, "DOCS", tmp_path)
    monkeypatch.setattr(mod, "ROOT", tmp_path)
    monkeypatch.setattr(mod, "SECTION", "")
    monkeypatch.setattr(mod, "FIX", False)
    monkeypatch.setattr(mod, "DRY_RUN", False)
    mod.main()
    text = (tmp_path / "BROKEN_LINKS.md").read_text(encoding="utf-8")
    assert text.strip().startswith("#")


def test_find_closest_file_found(tmp_path, monkeypatch):
    monkeypatch.setattr(mod, "DOCS", tmp_path)
    (tmp_path / "target.md").write_text("# Target\n\nContent.", encoding="utf-8")
    result = mod._find_closest_file("target.md")
    assert result is not None
    assert result.name == "target.md"


def test_find_closest_file_not_found(tmp_path, monkeypatch):
    monkeypatch.setattr(mod, "DOCS", tmp_path)
    result = mod._find_closest_file("nonexistent.md")
    assert result is None


def test_try_fix_link_with_anchor(tmp_path, monkeypatch):
    monkeypatch.setattr(mod, "DOCS", tmp_path)
    (tmp_path / "real.md").write_text("# Real\n\nContent.", encoding="utf-8")
    src = tmp_path / "source.md"
    result = mod._try_fix_link(src, "real.md#section")
    # Either returns a fix or None — just should not crash
    assert result is None or isinstance(result, str)


def test_fix_broken_links_empty_list(tmp_path, monkeypatch):
    monkeypatch.setattr(mod, "ROOT", tmp_path)
    f = tmp_path / "doc.md"
    f.write_text("# Title\n\nContent.", encoding="utf-8")
    result = mod.fix_broken_links(f, [])
    assert result == 0


def test_fix_broken_links_dry_run(tmp_path, monkeypatch):
    monkeypatch.setattr(mod, "ROOT", tmp_path)
    monkeypatch.setattr(mod, "DRY_RUN", True)
    monkeypatch.setattr(mod, "DOCS", tmp_path)
    f = tmp_path / "source.md"
    f.write_text("# Title\n\nSee [link](missing.md).", encoding="utf-8")
    broken = [{"file": "source.md", "text": "link", "target": "missing.md",
               "issue": "файл не существует"}]
    result = mod.fix_broken_links(f, broken)
    assert isinstance(result, int)


def test_check_links_external_link_not_broken(tmp_path, monkeypatch):
    monkeypatch.setattr(mod, "ROOT", tmp_path)
    f = tmp_path / "doc.md"
    f.write_text("# Title\n\nSee [link](https://example.com).", encoding="utf-8")
    broken, errors = mod.check_links(f, {})
    assert all(b["target"] != "https://example.com" for b in broken)


def test_check_links_broken_internal(tmp_path, monkeypatch):
    monkeypatch.setattr(mod, "ROOT", tmp_path)
    f = tmp_path / "doc.md"
    f.write_text("# Title\n\nSee [link](missing.md).", encoding="utf-8")
    broken, errors = mod.check_links(f, {})
    assert len(broken) > 0
    assert broken[0]["issue"] == "файл не существует"


def test_build_anchor_map_with_file(tmp_path, monkeypatch):
    monkeypatch.setattr(mod, "DOCS", tmp_path)
    monkeypatch.setattr(mod, "SECTION", "")
    f = tmp_path / "doc.md"
    f.write_text("# Title\n\n## Section One\n\n## Section One\n", encoding="utf-8")
    result = mod.build_anchor_map()
    assert str(f) in result
    anchors = result[str(f)]
    assert any("section-one" in a for a in anchors)


def test_safe_exists_returns_false_for_missing():
    result = mod._safe_exists(Path("/nonexistent/path/that/does/not/exist.md"))
    assert result is False
