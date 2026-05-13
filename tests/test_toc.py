"""
Тесты для scripts/improve_toc.py.

Покрытие:
  - make_anchor() — якорная ссылка из заголовка
  - build_toc()   — список ссылок на H2/H3 заголовки
  - add_toc()     — вставка TOC в файл
"""

import importlib
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(ROOT / "scripts"))

mod = importlib.import_module("improve_toc")

# ── make_anchor ───────────────────────────────────────────────────────────────

def test_make_anchor_returns_string():
    assert isinstance(mod.make_anchor("My Title"), str)


def test_make_anchor_lowercases():
    assert mod.make_anchor("My Title") == "my-title"


def test_make_anchor_replaces_spaces():
    assert mod.make_anchor("hello world") == "hello-world"


def test_make_anchor_removes_special_chars():
    result = mod.make_anchor("Title: With Colons!")
    assert ":" not in result
    assert "!" not in result


def test_make_anchor_preserves_cyrillic():
    result = mod.make_anchor("Привет мир")
    assert "привет" in result
    assert "мир" in result


def test_make_anchor_multiple_spaces():
    result = mod.make_anchor("Too   Many   Spaces")
    assert "--" not in result


# ── build_toc ─────────────────────────────────────────────────────────────────

def test_build_toc_returns_string():
    text = "# Title\n\n## Section One\n\nContent.\n\n## Section Two\n"
    result = mod.build_toc(text)
    assert isinstance(result, str)


def test_build_toc_includes_h2():
    text = "# Title\n\n## My Section\n\nContent.\n"
    result = mod.build_toc(text)
    assert "My Section" in result


def test_build_toc_includes_h3():
    text = "## H2\n\n### H3 subsection\n\n"
    result = mod.build_toc(text)
    assert "H3 subsection" in result


def test_build_toc_h3_indented():
    text = "## H2\n\n### H3\n"
    result = mod.build_toc(text)
    lines = result.splitlines()
    h3_line = [l for l in lines if "H3" in l][0]
    assert h3_line.startswith("  ")


def test_build_toc_empty_when_no_h2():
    text = "# Title\n\nJust text, no sections.\n"
    result = mod.build_toc(text)
    assert result == ""


def test_build_toc_link_format():
    text = "## My Section\n\nContent.\n"
    result = mod.build_toc(text)
    assert "[My Section]" in result
    assert "(#" in result


def test_build_toc_excludes_h1():
    text = "# Title\n\n## Section\n"
    result = mod.build_toc(text)
    lines = result.splitlines()
    # No H1 should appear
    assert not any("Title" in l for l in lines)


# ── add_toc ───────────────────────────────────────────────────────────────────

def test_add_toc_returns_bool(tmp_path):
    f = tmp_path / "doc.md"
    f.write_text("# Title\n\n" + "word " * 600 + "\n\n## Section A\n\n## Section B\n\n## Section C\n", encoding="utf-8")
    result = mod.add_toc(f)
    assert isinstance(result, bool)


def test_add_toc_adds_marker(tmp_path):
    f = tmp_path / "doc.md"
    f.write_text("# Title\n\n" + "word " * 600 + "\n\n## Alpha\n\n## Beta\n\n## Gamma\n", encoding="utf-8")
    mod.add_toc(f)
    content = f.read_text(encoding="utf-8")
    assert mod.TOC_MARKER in content


def test_add_toc_skips_short_files(tmp_path):
    f = tmp_path / "short.md"
    f.write_text("# Title\n\n## Short\n\nFew words.\n", encoding="utf-8")
    result = mod.add_toc(f)
    assert result is False


def test_add_toc_idempotent(tmp_path):
    f = tmp_path / "doc.md"
    content = "# Title\n\n" + "word " * 600 + "\n\n## A\n\n## B\n\n## C\n"
    f.write_text(content, encoding="utf-8")
    first = mod.add_toc(f)
    second = mod.add_toc(f)
    assert first is True
    assert second is False  # Already has marker


# ── main ──────────────────────────────────────────────────────────────────────

def test_main_adds_toc_to_docs(tmp_path, monkeypatch):
    monkeypatch.setattr(mod, "DOCS", tmp_path)
    monkeypatch.setattr(mod, "ROOT", tmp_path)
    monkeypatch.setattr(mod, "MIN_WORDS", 5)
    sections = "\n\n".join(f"## Section {i}\n\nContent here." for i in range(5))
    content = f"# Title\n\n{sections}\n"
    (tmp_path / "doc.md").write_text(content, encoding="utf-8")
    mod.main()
    text = (tmp_path / "doc.md").read_text(encoding="utf-8")
    assert "<!-- toc -->" in text


def test_main_empty_docs_no_crash(tmp_path, monkeypatch):
    monkeypatch.setattr(mod, "DOCS", tmp_path)
    monkeypatch.setattr(mod, "ROOT", tmp_path)
    mod.main()
