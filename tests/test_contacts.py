"""
Тесты для scripts/improve_contacts.py.

Покрытие:
  - extract_contacts()     — извлечение контактов из текста
  - find_author_mentions() — поиск упоминаний известных авторов
"""

import importlib
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(ROOT / "scripts"))

mod = importlib.import_module("improve_contacts")


# ── extract_contacts ──────────────────────────────────────────────────────────

def test_extract_contacts_returns_dict():
    result = mod.extract_contacts("plain text")
    assert isinstance(result, dict)


def test_extract_contacts_empty():
    result = mod.extract_contacts("")
    assert isinstance(result, dict)


def test_extract_contacts_finds_email():
    result = mod.extract_contacts("Contact: user@example.com for details.")
    assert "email" in result
    assert "user@example.com" in result["email"]


def test_extract_contacts_finds_github():
    result = mod.extract_contacts("See github.com/kksudo/agentfs for code.")
    assert "github" in result
    assert len(result["github"]) > 0


def test_extract_contacts_finds_telegram():
    result = mod.extract_contacts("Message me at t.me/username for help.")
    assert "telegram" in result


def test_extract_contacts_finds_habr():
    result = mod.extract_contacts("Check habr.com/ru/users/kksudo for articles.")
    assert "habr" in result


def test_extract_contacts_multiple_types():
    text = "Email: user@test.com. GitHub: github.com/user/repo"
    result = mod.extract_contacts(text)
    assert len(result) >= 1


def test_extract_contacts_no_duplicates():
    text = "user@example.com and user@example.com again."
    result = mod.extract_contacts(text)
    if "email" in result:
        # Should be a set, no duplicates
        assert len(result["email"]) == 1


# ── find_author_mentions ──────────────────────────────────────────────────────

def test_find_author_mentions_returns_list():
    result = mod.find_author_mentions("plain text")
    assert isinstance(result, list)


def test_find_author_mentions_empty():
    result = mod.find_author_mentions("")
    assert result == []


def test_find_author_mentions_finds_kksudo():
    result = mod.find_author_mentions("Project by kksudo on AgentFS.")
    assert "kksudo" in result


def test_find_author_mentions_finds_vitaly():
    result = mod.find_author_mentions("VitalyOborin created Yodoca memory system.")
    assert "VitalyOborin" in result


def test_find_author_mentions_case_insensitive():
    result = mod.find_author_mentions("KKSUDO is the author of AgentFS.")
    assert "kksudo" in result


def test_find_author_mentions_unknown_author():
    result = mod.find_author_mentions("Someone unknown wrote this text.")
    assert len(result) == 0


def test_find_author_mentions_multiple():
    result = mod.find_author_mentions(
        "kksudo created AgentFS and VitalyOborin created Yodoca."
    )
    assert "kksudo" in result
    assert "VitalyOborin" in result


# ── main ──────────────────────────────────────────────────────────────────────

def test_main_creates_contacts_md(tmp_path, monkeypatch):
    monkeypatch.setattr(mod, "DOCS", tmp_path)
    monkeypatch.setattr(mod, "ROOT", tmp_path)
    mod.main()
    assert (tmp_path / "CONTACTS.md").exists()


def test_main_contacts_has_content(tmp_path, monkeypatch):
    monkeypatch.setattr(mod, "DOCS", tmp_path)
    monkeypatch.setattr(mod, "ROOT", tmp_path)
    (tmp_path / "doc.md").write_text(
        "# AgentFS\n\nkksudo: https://github.com/kksudo/agentfs", encoding="utf-8"
    )
    mod.main()
    text = (tmp_path / "CONTACTS.md").read_text(encoding="utf-8")
    assert "# " in text


def test_main_empty_docs(tmp_path, monkeypatch):
    monkeypatch.setattr(mod, "DOCS", tmp_path)
    monkeypatch.setattr(mod, "ROOT", tmp_path)
    mod.main()
    assert (tmp_path / "CONTACTS.md").exists()


def test_main_contacts_starts_with_heading(tmp_path, monkeypatch):
    monkeypatch.setattr(mod, "DOCS", tmp_path)
    monkeypatch.setattr(mod, "ROOT", tmp_path)
    mod.main()
    text = (tmp_path / "CONTACTS.md").read_text(encoding="utf-8")
    assert text.strip().startswith("#")
