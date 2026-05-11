"""Tests for scripts/mcp_contacts_server.py."""

import importlib
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(ROOT / "scripts"))

mod = importlib.import_module("mcp_contacts_server")


# ── CONTACT_CHECKBOXES ────────────────────────────────────────────────────────

def test_contact_checkboxes_is_dict():
    assert isinstance(mod.CONTACT_CHECKBOXES, dict)
    assert len(mod.CONTACT_CHECKBOXES) > 0


def test_contact_checkboxes_has_studied():
    assert "studied" in mod.CONTACT_CHECKBOXES


def test_contact_checkboxes_has_messaged():
    assert "messaged" in mod.CONTACT_CHECKBOXES


def test_contact_checkboxes_values_are_strings():
    for key, val in mod.CONTACT_CHECKBOXES.items():
        assert isinstance(val, str)


# ── _find_contact_file ────────────────────────────────────────────────────────

def test_find_contact_file_no_dir(tmp_path, monkeypatch):
    monkeypatch.setattr(mod, "DOCS", tmp_path)
    # contacts dir does not exist
    result = mod._find_contact_file("kksudo")
    assert result is None


def test_find_contact_file_finds_file(tmp_path, monkeypatch):
    monkeypatch.setattr(mod, "DOCS", tmp_path)
    contacts = tmp_path / "contacts"
    contacts.mkdir()
    (contacts / "kksudo.md").write_text("# kksudo\n", encoding="utf-8")
    result = mod._find_contact_file("kksudo")
    assert result is not None
    assert result.name == "kksudo.md"


def test_find_contact_file_partial_match(tmp_path, monkeypatch):
    monkeypatch.setattr(mod, "DOCS", tmp_path)
    contacts = tmp_path / "contacts"
    contacts.mkdir()
    (contacts / "vitalyoborin.md").write_text("# VitalyOborin\n", encoding="utf-8")
    result = mod._find_contact_file("vitaly")
    assert result is not None


def test_find_contact_file_not_found(tmp_path, monkeypatch):
    monkeypatch.setattr(mod, "DOCS", tmp_path)
    contacts = tmp_path / "contacts"
    contacts.mkdir()
    (contacts / "kksudo.md").write_text("# kksudo\n", encoding="utf-8")
    result = mod._find_contact_file("nonexistent_person_xyz")
    assert result is None


# ── tool_get_contacts ─────────────────────────────────────────────────────────

def test_tool_get_contacts_no_contacts_md(tmp_path, monkeypatch):
    monkeypatch.setattr(mod, "DOCS", tmp_path)
    monkeypatch.setattr(mod, "read_doc", lambda filename: "")
    result = mod.tool_get_contacts("AgentFS")
    assert isinstance(result, str)
    assert "CONTACTS.md" in result or "не найден" in result.lower()


def test_tool_get_contacts_returns_string(tmp_path, monkeypatch):
    monkeypatch.setattr(mod, "DOCS", tmp_path)
    monkeypatch.setattr(mod, "read_doc",
                        lambda filename: "## AgentFS\n\nkksudo — AgentFS author")
    result = mod.tool_get_contacts("AgentFS")
    assert isinstance(result, str)


# ── tool_list_contacts ────────────────────────────────────────────────────────

def test_tool_list_contacts_no_dir(tmp_path, monkeypatch):
    monkeypatch.setattr(mod, "DOCS", tmp_path)
    result = mod.tool_list_contacts()
    assert isinstance(result, str)
    assert "contacts" in result.lower() or "не найден" in result.lower()


def test_tool_list_contacts_with_files(tmp_path, monkeypatch):
    monkeypatch.setattr(mod, "DOCS", tmp_path)
    contacts = tmp_path / "contacts"
    contacts.mkdir()
    (contacts / "kksudo.md").write_text(
        "# kksudo\n\n- [ ] Изучили профиль\n- [ ] Написали первое сообщение\n",
        encoding="utf-8"
    )
    result = mod.tool_list_contacts()
    assert isinstance(result, str)
    assert "kksudo" in result


# ── tool_get_contact ──────────────────────────────────────────────────────────

def test_tool_get_contact_not_found(tmp_path, monkeypatch):
    monkeypatch.setattr(mod, "DOCS", tmp_path)
    contacts = tmp_path / "contacts"
    contacts.mkdir()
    result = mod.tool_get_contact("nonexistent")
    assert isinstance(result, str)
    assert "не найден" in result.lower() or "❌" in result


def test_tool_get_contact_found(tmp_path, monkeypatch):
    monkeypatch.setattr(mod, "DOCS", tmp_path)
    contacts = tmp_path / "contacts"
    contacts.mkdir()
    (contacts / "kksudo.md").write_text("# kksudo profile\n\nAuthor info.", encoding="utf-8")
    result = mod.tool_get_contact("kksudo")
    assert isinstance(result, str)
    assert "kksudo" in result


# ── dispatch ──────────────────────────────────────────────────────────────────

def test_dispatch_get_contacts(tmp_path, monkeypatch):
    monkeypatch.setattr(mod, "DOCS", tmp_path)
    monkeypatch.setattr(mod, "read_doc", lambda filename: "")
    result = mod.dispatch("get_contacts", {"project": "AgentFS"})
    assert isinstance(result, str)


def test_dispatch_list_contacts(tmp_path, monkeypatch):
    monkeypatch.setattr(mod, "DOCS", tmp_path)
    (tmp_path / "contacts").mkdir()
    result = mod.dispatch("list_contacts", {})
    assert isinstance(result, str)


def test_dispatch_unknown_tool():
    result = mod.dispatch("unknown_xyz", {})
    assert "unknown_xyz" in result or "Неизвестный" in result
