"""
Тесты для scripts/improve_backlinks.py.

Покрытие:
  - extract_links()  — извлечение внутренних md-ссылок
"""

import importlib
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(ROOT / "scripts"))

mod = importlib.import_module("improve_backlinks")


# ── extract_links ─────────────────────────────────────────────────────────────

def test_extract_links_returns_set(tmp_path, monkeypatch):
    monkeypatch.setattr(mod, "ROOT", tmp_path)
    f = tmp_path / "source.md"
    f.write_text("# Title\n", encoding="utf-8")
    result = mod.extract_links("plain text", f)
    assert isinstance(result, set)


def test_extract_links_empty_text(tmp_path, monkeypatch):
    monkeypatch.setattr(mod, "ROOT", tmp_path)
    f = tmp_path / "source.md"
    f.write_text("# Title\n", encoding="utf-8")
    result = mod.extract_links("", f)
    assert result == set()


def test_extract_links_skips_http(tmp_path, monkeypatch):
    monkeypatch.setattr(mod, "ROOT", tmp_path)
    f = tmp_path / "source.md"
    f.write_text("# Title\n", encoding="utf-8")
    result = mod.extract_links("[Link](https://example.com)", f)
    assert len(result) == 0


def test_extract_links_skips_anchor(tmp_path, monkeypatch):
    monkeypatch.setattr(mod, "ROOT", tmp_path)
    f = tmp_path / "source.md"
    f.write_text("# Title\n", encoding="utf-8")
    result = mod.extract_links("[Section](#heading)", f)
    assert len(result) == 0


def test_extract_links_finds_local_file(tmp_path, monkeypatch):
    monkeypatch.setattr(mod, "ROOT", tmp_path)
    source = tmp_path / "source.md"
    target = tmp_path / "target.md"
    target.write_text("# Target\n", encoding="utf-8")
    source.write_text("# Source\n", encoding="utf-8")
    result = mod.extract_links("[Link](target.md)", source)
    assert len(result) > 0


def test_extract_links_relative_path(tmp_path, monkeypatch):
    monkeypatch.setattr(mod, "ROOT", tmp_path)
    sub = tmp_path / "sub"
    sub.mkdir()
    source = sub / "source.md"
    target = tmp_path / "target.md"
    target.write_text("# Target\n", encoding="utf-8")
    source.write_text("# Source\n", encoding="utf-8")
    result = mod.extract_links("[Link](../target.md)", source)
    assert len(result) > 0


def test_extract_links_missing_target(tmp_path, monkeypatch):
    monkeypatch.setattr(mod, "ROOT", tmp_path)
    source = tmp_path / "source.md"
    source.write_text("# Source\n", encoding="utf-8")
    result = mod.extract_links("[Link](nonexistent.md)", source)
    assert len(result) == 0


# ── main ──────────────────────────────────────────────────────────────────────

def test_main_creates_backlinks_md(tmp_path, monkeypatch):
    monkeypatch.setattr(mod, "DOCS", tmp_path)
    monkeypatch.setattr(mod, "ROOT", tmp_path)
    monkeypatch.setattr(sys, "argv", ["prog"])
    (tmp_path / "doc1.md").write_text("# Doc1\n\nContent.", encoding="utf-8")
    (tmp_path / "doc2.md").write_text("# Doc2\n\n[Link](doc1.md)", encoding="utf-8")
    mod.main()
    assert (tmp_path / "BACKLINKS.md").exists()


def test_main_backlinks_md_has_content(tmp_path, monkeypatch):
    monkeypatch.setattr(mod, "DOCS", tmp_path)
    monkeypatch.setattr(mod, "ROOT", tmp_path)
    monkeypatch.setattr(sys, "argv", ["prog"])
    (tmp_path / "doc.md").write_text("# Doc\n\nContent.", encoding="utf-8")
    mod.main()
    text = (tmp_path / "BACKLINKS.md").read_text(encoding="utf-8")
    assert "Индекс обратных ссылок" in text


def test_main_dry_run_no_output(tmp_path, monkeypatch):
    monkeypatch.setattr(mod, "DOCS", tmp_path)
    monkeypatch.setattr(mod, "ROOT", tmp_path)
    monkeypatch.setattr(sys, "argv", ["prog", "--dry-run"])
    (tmp_path / "doc.md").write_text("# Doc\n\nContent.", encoding="utf-8")
    mod.main()
    assert not (tmp_path / "BACKLINKS.md").exists()


def test_main_empty_docs(tmp_path, monkeypatch):
    monkeypatch.setattr(mod, "DOCS", tmp_path)
    monkeypatch.setattr(mod, "ROOT", tmp_path)
    monkeypatch.setattr(sys, "argv", ["prog"])
    mod.main()
    assert (tmp_path / "BACKLINKS.md").exists()


def test_extract_links_long_href_skipped(tmp_path, monkeypatch):
    """Line 27: href > 300 chars → skipped."""
    monkeypatch.setattr(mod, "ROOT", tmp_path)
    source = tmp_path / "source.md"
    source.write_text("# Source\n", encoding="utf-8")
    long_href = "a" * 301 + ".md"
    result = mod.extract_links(f"[Link]({long_href})", source)
    assert len(result) == 0


def test_extract_links_oserror(tmp_path, monkeypatch):
    """Lines 32-33: OSError in path resolution → silently skipped."""
    from pathlib import Path as _Path
    monkeypatch.setattr(mod, "ROOT", tmp_path)
    source = tmp_path / "source.md"
    source.write_text("# Source\n", encoding="utf-8")
    original_resolve = _Path.resolve
    def fake_resolve(self):
        raise OSError("path too long")
    monkeypatch.setattr(_Path, "resolve", fake_resolve)
    result = mod.extract_links("[Link](target.md)", source)
    assert isinstance(result, set)


def test_main_skips_skip_files(tmp_path, monkeypatch):
    """Line 51: SKIP files are not processed."""
    monkeypatch.setattr(mod, "DOCS", tmp_path)
    monkeypatch.setattr(mod, "ROOT", tmp_path)
    monkeypatch.setattr(sys, "argv", ["prog"])
    # Create a SKIP file — it should not be processed for link extraction
    (tmp_path / "BACKLINKS.md").write_text("# Backlinks\n\n[link](target.md).", encoding="utf-8")
    target = tmp_path / "target.md"
    target.write_text("# Target\n", encoding="utf-8")
    mod.main()
    # BACKLINKS.md should be regenerated without referencing itself as a source
    content = (tmp_path / "BACKLINKS.md").read_text(encoding="utf-8")
    assert "Индекс обратных ссылок" in content


def test_main_src_list_truncated(tmp_path, monkeypatch, capsys):
    """Line 76: if len(srcs) > 4 → +N suffix in table."""
    monkeypatch.setattr(mod, "DOCS", tmp_path)
    monkeypatch.setattr(mod, "ROOT", tmp_path)
    monkeypatch.setattr(sys, "argv", ["prog"])
    target = tmp_path / "target.md"
    target.write_text("# Target\n\nContent.", encoding="utf-8")
    # Create 5 source files linking to target
    for i in range(5):
        (tmp_path / f"src{i}.md").write_text(f"# Src{i}\n\n[link](target.md)", encoding="utf-8")
    mod.main()
    content = (tmp_path / "BACKLINKS.md").read_text(encoding="utf-8")
    assert "+1" in content  # 5 sources → 4 shown + "+1"


def test_main_adds_backlinks_block_to_file(tmp_path, monkeypatch):
    """Lines 108-127: files with 3+ incoming links get a backlinks block appended."""
    monkeypatch.setattr(mod, "DOCS", tmp_path)
    monkeypatch.setattr(mod, "ROOT", tmp_path)
    monkeypatch.setattr(sys, "argv", ["prog"])
    target = tmp_path / "target.md"
    target.write_text("# Target\n\nContent.", encoding="utf-8")
    for i in range(3):
        (tmp_path / f"src{i}.md").write_text(f"# Src{i}\n\n[link](target.md)", encoding="utf-8")
    mod.main()
    content = target.read_text(encoding="utf-8")
    assert mod.MARKER in content or "Кто ссылается" in content


def test_main_dry_run_adds_no_block(tmp_path, monkeypatch, capsys):
    """Lines 123-124: dry-run does not write backlink blocks."""
    monkeypatch.setattr(mod, "DOCS", tmp_path)
    monkeypatch.setattr(mod, "ROOT", tmp_path)
    monkeypatch.setattr(sys, "argv", ["prog", "--dry-run"])
    target = tmp_path / "target.md"
    target.write_text("# Target\n\nContent.", encoding="utf-8")
    for i in range(3):
        (tmp_path / f"src{i}.md").write_text(f"# Src{i}\n\n[link](target.md)", encoding="utf-8")
    mod.main()
    content = target.read_text(encoding="utf-8")
    assert mod.MARKER not in content
    out = capsys.readouterr().out
    assert "dry-run" in out.lower() or "dry" in out.lower()


def test_main_skips_file_with_existing_marker(tmp_path, monkeypatch):
    """Line 112-113: file already has MARKER → skip adding block."""
    monkeypatch.setattr(mod, "DOCS", tmp_path)
    monkeypatch.setattr(mod, "ROOT", tmp_path)
    monkeypatch.setattr(sys, "argv", ["prog"])
    target = tmp_path / "target.md"
    target.write_text(f"# Target\n\nContent.\n{mod.MARKER}\n", encoding="utf-8")
    for i in range(3):
        (tmp_path / f"src{i}.md").write_text(f"# Src{i}\n\n[link](target.md)", encoding="utf-8")
    mod.main()
    content = target.read_text(encoding="utf-8")
    assert content.count(mod.MARKER) == 1  # not duplicated


def test_main_skips_skip_named_target(tmp_path, monkeypatch):
    """Line 110: target in backward map whose name is in SKIP → skip."""
    monkeypatch.setattr(mod, "DOCS", tmp_path)
    monkeypatch.setattr(mod, "ROOT", tmp_path)
    monkeypatch.setattr(sys, "argv", ["prog"])
    # Pre-create BACKLINKS.md so extract_links can resolve it
    backlinks_file = tmp_path / "BACKLINKS.md"
    backlinks_file.write_text("# Backlinks\n", encoding="utf-8")
    # 3 files linking to BACKLINKS.md (which is in SKIP)
    for i in range(3):
        (tmp_path / f"src{i}.md").write_text(
            "# Src\n\n[link](BACKLINKS.md)", encoding="utf-8"
        )
    mod.main()
    # BACKLINKS.md should be regenerated (not have a backlinks block added)
    content = backlinks_file.read_text(encoding="utf-8")
    assert mod.MARKER not in content


def test_main_many_sources_shows_ellipsis(tmp_path, monkeypatch):
    """Line 121: more than 8 sources → '...ещё N' appended to block."""
    monkeypatch.setattr(mod, "DOCS", tmp_path)
    monkeypatch.setattr(mod, "ROOT", tmp_path)
    monkeypatch.setattr(sys, "argv", ["prog"])
    target = tmp_path / "target.md"
    target.write_text("# Target\n\nContent.", encoding="utf-8")
    for i in range(9):
        (tmp_path / f"src{i}.md").write_text(f"# Src{i}\n\n[link](target.md)", encoding="utf-8")
    mod.main()
    content = target.read_text(encoding="utf-8")
    assert "ещё 1" in content  # 9 sources → 8 shown + "ещё 1"
