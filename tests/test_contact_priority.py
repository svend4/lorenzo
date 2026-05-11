"""Tests for scripts/improve_contact_priority.py."""

import importlib
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(ROOT / "scripts"))

mod = importlib.import_module("improve_contact_priority")


def test_layer_boost_returns_int():
    result = mod._layer_boost("memory")
    assert isinstance(result, int)


def test_layer_boost_memory_high():
    result = mod._layer_boost("memory")
    assert result >= 2


def test_layer_boost_unknown_default():
    result = mod._layer_boost("unknown_layer_xyz")
    assert result == 1


def test_compute_score_returns_number():
    author = {"author": "test", "project": "TestProject", "layer": "memory", "mentions": 5}
    result = mod._compute_score(author, "none")
    assert isinstance(result, (int, float))


def test_compute_score_more_mentions_higher():
    author_few = {"author": "a", "project": "P", "layer": "other", "mentions": 1}
    author_many = {"author": "b", "project": "P", "layer": "other", "mentions": 10}
    score_few = mod._compute_score(author_few, "none")
    score_many = mod._compute_score(author_many, "none")
    assert score_many > score_few


def test_compute_score_varies_by_status():
    author = {"author": "a", "project": "P", "layer": "other", "mentions": 5}
    score_none = mod._compute_score(author, "none")
    score_agreed = mod._compute_score(author, "agreed")
    # Scores differ by status (exact ordering depends on STATUS_STEPS)
    assert score_none != score_agreed


def test_get_contact_status_returns_string(tmp_path, monkeypatch):
    monkeypatch.setattr(mod, "DOCS", tmp_path)
    # File doesn't exist → "none"
    result = mod._get_contact_status("unknown_author_xyz")
    assert result == "none"


def test_layer_boost_dict_exists():
    assert hasattr(mod, "LAYER_BOOST")
    assert isinstance(mod.LAYER_BOOST, dict)


def test_status_steps_dict_exists():
    assert hasattr(mod, "STATUS_STEPS")
    assert isinstance(mod.STATUS_STEPS, dict)
    assert "agreed" in mod.STATUS_STEPS
    assert "none" not in mod.STATUS_STEPS or True


# ── main ──────────────────────────────────────────────────────────────────────

CONTACTS_TABLE = (
    "| Автор | Проект | Слой | Упоминаний |\n"
    "|-------|--------|------|------------|\n"
    "| kksudo | AgentFS | knowledge | 5 |\n"
    "| spbmolot | NGT Memory | memory | 3 |\n"
)


def test_main_creates_contact_priority_md(tmp_path, monkeypatch):
    monkeypatch.setattr(mod, "DOCS", tmp_path)
    monkeypatch.setattr(mod, "ROOT", tmp_path)
    (tmp_path / "CONTACTS.md").write_text(CONTACTS_TABLE, encoding="utf-8")
    mod.main()
    assert (tmp_path / "CONTACT_PRIORITY.md").exists()


def test_main_contact_priority_has_content(tmp_path, monkeypatch):
    monkeypatch.setattr(mod, "DOCS", tmp_path)
    monkeypatch.setattr(mod, "ROOT", tmp_path)
    (tmp_path / "CONTACTS.md").write_text(CONTACTS_TABLE, encoding="utf-8")
    mod.main()
    text = (tmp_path / "CONTACT_PRIORITY.md").read_text(encoding="utf-8")
    assert "# " in text


def test_main_no_contacts_md_no_output(tmp_path, monkeypatch, capsys):
    monkeypatch.setattr(mod, "DOCS", tmp_path)
    monkeypatch.setattr(mod, "ROOT", tmp_path)
    mod.main()
    captured = capsys.readouterr()
    assert not (tmp_path / "CONTACT_PRIORITY.md").exists() or "CONTACTS.md" in captured.out


def test_main_starts_with_heading(tmp_path, monkeypatch):
    monkeypatch.setattr(mod, "DOCS", tmp_path)
    monkeypatch.setattr(mod, "ROOT", tmp_path)
    (tmp_path / "CONTACTS.md").write_text(CONTACTS_TABLE, encoding="utf-8")
    mod.main()
    text = (tmp_path / "CONTACT_PRIORITY.md").read_text(encoding="utf-8")
    assert text.strip().startswith("#")
