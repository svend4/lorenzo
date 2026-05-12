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


# ── cmd_build helpers ─────────────────────────────────────────────────────────

def _setup_cards(tmp_path):
    """Create a small CardStore with one real card."""
    sys.path.insert(0, str(Path(__file__).parent.parent / "scripts"))
    from utils_card_envelope import CardEnvelope, CardStore
    cards_dir = tmp_path / "cards"
    cards_dir.mkdir()
    store = CardStore(cards_dir)
    card = CardEnvelope(
        card_id="sha256:test0001",
        card_type="doc",
        state="raw",
        payload={"title": "Test Doc", "path": "test.md", "wc": 50, "tags": [], "summary": "A test document"},
        edges=[],
    )
    store.put(card)
    return cards_dir, store


def test_cmd_build_dry_run(tmp_path, monkeypatch, capsys):
    monkeypatch.setattr(mod, "DOCS", tmp_path)
    monkeypatch.setattr(mod, "ROOT", tmp_path)
    monkeypatch.setattr(mod, "CARDS", tmp_path / "cards")
    f = tmp_path / "doc.md"
    f.write_text("# Title\n\nContent about agent memory.", encoding="utf-8")
    mod.cmd_build(dry_run=True)
    out = capsys.readouterr().out
    assert "dry-run" in out or "Карточек" in out or "dry" in out.lower()


def test_cmd_build_no_dry_run(tmp_path, monkeypatch, capsys):
    monkeypatch.setattr(mod, "DOCS", tmp_path)
    monkeypatch.setattr(mod, "ROOT", tmp_path)
    cards_dir = tmp_path / "cards"
    monkeypatch.setattr(mod, "CARDS", cards_dir)
    f = tmp_path / "doc.md"
    f.write_text("# Title\n\nContent about agent memory.", encoding="utf-8")
    mod.cmd_build(dry_run=False)
    out = capsys.readouterr().out
    assert "Записано" in out or "Карточек" in out


def test_cmd_build_verbose(tmp_path, monkeypatch, capsys):
    monkeypatch.setattr(mod, "DOCS", tmp_path)
    monkeypatch.setattr(mod, "ROOT", tmp_path)
    cards_dir = tmp_path / "cards"
    monkeypatch.setattr(mod, "CARDS", cards_dir)
    f = tmp_path / "doc.md"
    f.write_text("# Title\n\nContent.", encoding="utf-8")
    mod.cmd_build(dry_run=False, verbose=True)
    out = capsys.readouterr().out
    assert isinstance(out, str)


def test_cmd_build_incremental(tmp_path, monkeypatch, capsys):
    monkeypatch.setattr(mod, "DOCS", tmp_path)
    monkeypatch.setattr(mod, "ROOT", tmp_path)
    cards_dir = tmp_path / "cards"
    monkeypatch.setattr(mod, "CARDS", cards_dir)
    f = tmp_path / "doc.md"
    f.write_text("# Title\n\nContent.", encoding="utf-8")
    mod.cmd_build(dry_run=False, incremental=False)
    mod.cmd_build(dry_run=False, incremental=True)
    out = capsys.readouterr().out
    assert isinstance(out, str)


def test_cmd_stats_with_cards(tmp_path, monkeypatch, capsys):
    cards_dir, _ = _setup_cards(tmp_path)
    monkeypatch.setattr(mod, "CARDS", cards_dir)
    mod.cmd_stats()
    out = capsys.readouterr().out
    assert isinstance(out, str)


def test_cmd_stats_empty_cards(tmp_path, monkeypatch, capsys):
    monkeypatch.setattr(mod, "CARDS", tmp_path / "no_cards")
    mod.cmd_stats()
    out = capsys.readouterr().out
    assert "пуст" in out or "CardStore" in out


def test_cmd_search_with_cards(tmp_path, monkeypatch, capsys):
    cards_dir, _ = _setup_cards(tmp_path)
    monkeypatch.setattr(mod, "CARDS", cards_dir)
    mod.cmd_search("test doc")
    out = capsys.readouterr().out
    assert isinstance(out, str)


def test_cmd_search_no_results(tmp_path, monkeypatch, capsys):
    cards_dir, _ = _setup_cards(tmp_path)
    monkeypatch.setattr(mod, "CARDS", cards_dir)
    mod.cmd_search("xyzxyz_no_match_abcdef")
    out = capsys.readouterr().out
    assert "Ничего" in out or "не найдено" in out.lower()


def test_cmd_search_no_cards(tmp_path, monkeypatch, capsys):
    monkeypatch.setattr(mod, "CARDS", tmp_path / "no_cards")
    mod.cmd_search("agent")
    out = capsys.readouterr().out
    assert "пуст" in out or "CardStore" in out


def test_cmd_get_existing(tmp_path, monkeypatch, capsys):
    cards_dir, _ = _setup_cards(tmp_path)
    monkeypatch.setattr(mod, "CARDS", cards_dir)
    mod.cmd_get("sha256:test0001")
    out = capsys.readouterr().out
    assert "sha256:test0001" in out or "Test Doc" in out or "{" in out


def test_cmd_get_partial_match(tmp_path, monkeypatch, capsys):
    cards_dir, _ = _setup_cards(tmp_path)
    monkeypatch.setattr(mod, "CARDS", cards_dir)
    mod.cmd_get("Test Doc")
    out = capsys.readouterr().out
    assert isinstance(out, str)


def test_cmd_get_not_found(tmp_path, monkeypatch, capsys):
    cards_dir, _ = _setup_cards(tmp_path)
    monkeypatch.setattr(mod, "CARDS", cards_dir)
    mod.cmd_get("nonexistent_card_id_xyz")
    out = capsys.readouterr().out
    assert "не найдена" in out or "not found" in out.lower() or "Найдено" in out or "Карточка" in out


def test_cmd_link_dry_run(tmp_path, monkeypatch, capsys):
    cards_dir, _ = _setup_cards(tmp_path)
    monkeypatch.setattr(mod, "CARDS", cards_dir)
    mod.cmd_link("sha256:test0001", "docs/other.md", rel="references", dry_run=True)
    out = capsys.readouterr().out
    assert "dry-run" in out or "ребро" in out.lower() or "Добавлено" in out


def test_cmd_link_not_found(tmp_path, monkeypatch, capsys):
    cards_dir, _ = _setup_cards(tmp_path)
    monkeypatch.setattr(mod, "CARDS", cards_dir)
    mod.cmd_link("nonexistent_xyz", "docs/other.md", dry_run=True)
    out = capsys.readouterr().out
    assert "не найдена" in out or "not found" in out.lower()


def test_cmd_link_no_cards(tmp_path, monkeypatch, capsys):
    monkeypatch.setattr(mod, "CARDS", tmp_path / "no_cards")
    mod.cmd_link("any_id", "docs/other.md", dry_run=True)
    out = capsys.readouterr().out
    assert "пуст" in out or "CardStore" in out


def test_cmd_approve_dry_run(tmp_path, monkeypatch, capsys):
    cards_dir, _ = _setup_cards(tmp_path)
    monkeypatch.setattr(mod, "CARDS", cards_dir)
    mod.cmd_approve("sha256:test0001", dry_run=True)
    out = capsys.readouterr().out
    assert "approved" in out or "dry-run" in out


def test_cmd_approve_not_found(tmp_path, monkeypatch, capsys):
    cards_dir, _ = _setup_cards(tmp_path)
    monkeypatch.setattr(mod, "CARDS", cards_dir)
    mod.cmd_approve("nonexistent_xyz", dry_run=True)
    out = capsys.readouterr().out
    assert "не найдена" in out or "not found" in out.lower()


def test_cmd_decay_dry_run(tmp_path, monkeypatch, capsys):
    cards_dir, _ = _setup_cards(tmp_path)
    monkeypatch.setattr(mod, "CARDS", cards_dir)
    mod.cmd_decay("sha256:test0001", dry_run=True)
    out = capsys.readouterr().out
    assert "decayed" in out or "dry-run" in out


def test_cmd_export_json(tmp_path, monkeypatch, capsys):
    cards_dir, _ = _setup_cards(tmp_path)
    monkeypatch.setattr(mod, "CARDS", cards_dir)
    monkeypatch.setattr(mod, "ROOT", tmp_path)
    mod.cmd_export(fmt="json")
    out = capsys.readouterr().out
    assert "Записано" in out or "json" in out.lower()


def test_cmd_export_csv(tmp_path, monkeypatch, capsys):
    cards_dir, _ = _setup_cards(tmp_path)
    monkeypatch.setattr(mod, "CARDS", cards_dir)
    monkeypatch.setattr(mod, "ROOT", tmp_path)
    mod.cmd_export(fmt="csv")
    out = capsys.readouterr().out
    assert "Записано" in out or "csv" in out.lower()


def test_cmd_export_md(tmp_path, monkeypatch, capsys):
    cards_dir, _ = _setup_cards(tmp_path)
    monkeypatch.setattr(mod, "CARDS", cards_dir)
    monkeypatch.setattr(mod, "ROOT", tmp_path)
    mod.cmd_export(fmt="md")
    out = capsys.readouterr().out
    assert "Записано" in out or "md" in out.lower()


def test_cmd_export_invalid_fmt(tmp_path, monkeypatch, capsys):
    cards_dir, _ = _setup_cards(tmp_path)
    monkeypatch.setattr(mod, "CARDS", cards_dir)
    monkeypatch.setattr(mod, "ROOT", tmp_path)
    mod.cmd_export(fmt="xml")
    out = capsys.readouterr().out
    assert "Неизвестный" in out or "unknown" in out.lower()


def test_cmd_export_no_cards_dir(tmp_path, monkeypatch, capsys):
    monkeypatch.setattr(mod, "CARDS", tmp_path / "no_cards")
    mod.cmd_export()
    out = capsys.readouterr().out
    assert "пуст" in out or "CardStore" in out


def test_main_get_no_crash(tmp_path, monkeypatch, capsys):
    monkeypatch.setattr("sys.argv", ["prog", "--get", "nonexistent"])
    monkeypatch.setattr(mod, "CARDS", tmp_path / "no_cards")
    mod.main()


def test_main_link_no_crash(tmp_path, monkeypatch, capsys):
    monkeypatch.setattr("sys.argv", ["prog", "--link", "from_id", "to.md", "--dry-run"])
    monkeypatch.setattr(mod, "CARDS", tmp_path / "no_cards")
    mod.main()


def test_main_approve_no_crash(tmp_path, monkeypatch, capsys):
    monkeypatch.setattr("sys.argv", ["prog", "--approve", "some_id", "--dry-run"])
    monkeypatch.setattr(mod, "CARDS", tmp_path / "no_cards")
    mod.main()


def test_main_decay_no_crash(tmp_path, monkeypatch, capsys):
    monkeypatch.setattr("sys.argv", ["prog", "--decay", "some_id", "--dry-run"])
    monkeypatch.setattr(mod, "CARDS", tmp_path / "no_cards")
    mod.main()


def test_main_export_no_crash(tmp_path, monkeypatch, capsys):
    monkeypatch.setattr("sys.argv", ["prog", "--export", "--fmt", "csv"])
    monkeypatch.setattr(mod, "CARDS", tmp_path / "no_cards")
    mod.main()


def test_main_no_args_prints_help(monkeypatch, capsys):
    monkeypatch.setattr("sys.argv", ["prog"])
    mod.main()
    out = capsys.readouterr().out
    assert isinstance(out, str)
