"""
Тесты для scripts/improve_card_index.py.

Покрытие:
  - _extract_internal_links() — парсинг внутренних .md ссылок
  - _file_mtime_iso()         — ISO-формат mtime файла
"""

import importlib
import sys
import os
from pathlib import Path

import pytest

ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(ROOT / "scripts"))

mod = importlib.import_module("improve_card_index")

# ── _extract_internal_links ───────────────────────────────────────────────────

def test_extract_internal_links_finds_md_link(tmp_path, monkeypatch):
    # Files must be under ROOT for relative_to(ROOT) to work
    monkeypatch.setattr(mod, "ROOT", tmp_path)
    target = tmp_path / "other.md"
    target.write_text("# Other", encoding="utf-8")
    source = tmp_path / "source.md"
    text = "See [Other Doc](other.md) for details."
    links = mod._extract_internal_links(text, source)
    assert any("other.md" in l for l in links)


def test_extract_internal_links_skips_http():
    source = Path("docs/source.md")
    text = "See [External](https://example.com/page.md) for details."
    links = mod._extract_internal_links(text, source)
    assert links == []


def test_extract_internal_links_skips_anchors(tmp_path, monkeypatch):
    monkeypatch.setattr(mod, "ROOT", tmp_path)
    target = tmp_path / "other.md"
    target.write_text("# Other", encoding="utf-8")
    source = tmp_path / "source.md"
    text = "[Section](other.md#section-title)"
    links = mod._extract_internal_links(text, source)
    # anchor stripped from href before resolve
    assert any("other.md" in l for l in links)


def test_extract_internal_links_empty_text():
    source = Path("docs/source.md")
    links = mod._extract_internal_links("", source)
    assert links == []


def test_extract_internal_links_no_md_links():
    source = Path("docs/source.md")
    text = "No links here. Just plain text."
    links = mod._extract_internal_links(text, source)
    assert links == []


def test_extract_internal_links_returns_list():
    source = Path("docs/source.md")
    result = mod._extract_internal_links("some text", source)
    assert isinstance(result, list)


def test_extract_internal_links_nonexistent_target_excluded(tmp_path):
    source = tmp_path / "source.md"
    text = "[Missing](nonexistent_file.md)"
    links = mod._extract_internal_links(text, source)
    # nonexistent file → not included
    assert links == []


def test_extract_internal_links_multiple_links(tmp_path, monkeypatch):
    monkeypatch.setattr(mod, "ROOT", tmp_path)
    a = tmp_path / "a.md"
    b = tmp_path / "b.md"
    a.write_text("# A", encoding="utf-8")
    b.write_text("# B", encoding="utf-8")
    source = tmp_path / "source.md"
    text = "See [A](a.md) and [B](b.md)."
    links = mod._extract_internal_links(text, source)
    assert len(links) == 2

# ── _file_mtime_iso ───────────────────────────────────────────────────────────

def test_file_mtime_iso_returns_string(tmp_path):
    f = tmp_path / "file.md"
    f.write_text("content", encoding="utf-8")
    result = mod._file_mtime_iso(f)
    assert isinstance(result, str)


def test_file_mtime_iso_format(tmp_path):
    f = tmp_path / "file.md"
    f.write_text("content", encoding="utf-8")
    result = mod._file_mtime_iso(f)
    # Should match YYYY-MM-DDTHH:MM:SS+00:00
    import re
    assert re.match(r'\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}\+00:00', result)


def test_file_mtime_iso_monotone(tmp_path):
    import time
    f = tmp_path / "file.md"
    f.write_text("v1", encoding="utf-8")
    t1 = mod._file_mtime_iso(f)
    time.sleep(0.05)
    f.write_text("v2", encoding="utf-8")
    t2 = mod._file_mtime_iso(f)
    assert t2 >= t1


def test_file_mtime_iso_differs_between_files(tmp_path):
    import time
    f1 = tmp_path / "f1.md"
    f1.write_text("v1", encoding="utf-8")
    time.sleep(0.05)
    f2 = tmp_path / "f2.md"
    f2.write_text("v2", encoding="utf-8")
    assert mod._file_mtime_iso(f1) <= mod._file_mtime_iso(f2)


# ── main ──────────────────────────────────────────────────────────────────────

def test_main_stats_no_crash(tmp_path, monkeypatch):
    monkeypatch.setattr("sys.argv", ["prog", "--stats"])
    monkeypatch.setattr(mod, "CARDS", tmp_path / "cards")
    mod.main()


def test_main_build_dry_run_no_crash(tmp_path, monkeypatch):
    monkeypatch.setattr("sys.argv", ["prog", "--build", "--dry-run"])
    monkeypatch.setattr(mod, "DOCS", tmp_path)
    monkeypatch.setattr(mod, "ROOT", tmp_path)
    monkeypatch.setattr(mod, "CARDS", tmp_path / "cards")
    (tmp_path / "doc.md").write_text("# Title\n\nContent.", encoding="utf-8")
    mod.main()


def test_main_search_no_crash(tmp_path, monkeypatch):
    monkeypatch.setattr("sys.argv", ["prog", "--search", "agent"])
    monkeypatch.setattr(mod, "CARDS", tmp_path / "cards")
    mod.main()
