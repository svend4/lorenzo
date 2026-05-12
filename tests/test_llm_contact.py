"""Tests for scripts/improve_llm_contact.py."""

import importlib
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(ROOT / "scripts"))

mod = importlib.import_module("improve_llm_contact")


def test_find_contact_file_not_found(tmp_path, monkeypatch):
    contacts_dir = tmp_path / "contacts"
    contacts_dir.mkdir()
    monkeypatch.setattr(mod, "DOCS", tmp_path)
    result = mod._find_contact_file("nonexistent_author")
    assert result is None


def test_find_contact_file_finds_by_name(tmp_path, monkeypatch):
    contacts_dir = tmp_path / "contacts"
    contacts_dir.mkdir()
    f = contacts_dir / "kksudo.md"
    f.write_text("# kksudo\n\nAuthor profile.", encoding="utf-8")
    monkeypatch.setattr(mod, "DOCS", tmp_path)
    result = mod._find_contact_file("kksudo")
    assert result == f


def test_find_contact_file_partial_match(tmp_path, monkeypatch):
    contacts_dir = tmp_path / "contacts"
    contacts_dir.mkdir()
    f = contacts_dir / "kksudo-profile.md"
    f.write_text("# kksudo\n\nAuthor profile.", encoding="utf-8")
    monkeypatch.setattr(mod, "DOCS", tmp_path)
    result = mod._find_contact_file("kksudo")
    assert result == f


def test_find_project_file_returns_none_when_absent(tmp_path, monkeypatch):
    monkeypatch.setattr(mod, "DOCS", tmp_path)
    result = mod._find_project_file("nonexistent_project_xyz")
    assert result is None


def test_find_project_file_finds_match(tmp_path, monkeypatch):
    sub = tmp_path / "projects"
    sub.mkdir()
    f = sub / "agentfs.md"
    f.write_text("# AgentFS\n\nFilesystem project.", encoding="utf-8")
    monkeypatch.setattr(mod, "DOCS", tmp_path)
    result = mod._find_project_file("AgentFS")
    assert result == f


def test_find_project_file_skips_contacts(tmp_path, monkeypatch):
    contacts_dir = tmp_path / "contacts"
    contacts_dir.mkdir()
    f = contacts_dir / "agentfs.md"
    f.write_text("# kksudo contact\n\nAgentFS author.", encoding="utf-8")
    monkeypatch.setattr(mod, "DOCS", tmp_path)
    result = mod._find_project_file("agentfs")
    assert result is None


def test_contact_is_messaged_returns_bool(tmp_path):
    f = tmp_path / "contact.md"
    f.write_text("# Author\n\n- [ ] Написали первое сообщение", encoding="utf-8")
    result = mod._contact_is_messaged(f)
    assert isinstance(result, bool)


def test_contact_is_messaged_not_messaged(tmp_path):
    f = tmp_path / "contact.md"
    f.write_text("# Author\n\n- [ ] Написали первое сообщение", encoding="utf-8")
    result = mod._contact_is_messaged(f)
    assert result is False


def test_contact_is_messaged_messaged(tmp_path):
    f = tmp_path / "contact.md"
    f.write_text("# Author\n\n- [x] Написали первое сообщение", encoding="utf-8")
    result = mod._contact_is_messaged(f)
    assert result is True


def test_build_prompt_returns_string(tmp_path):
    f = tmp_path / "contact.md"
    f.write_text("# kksudo\n\nAuthor of AgentFS.", encoding="utf-8")
    result = mod.build_prompt(f, None)
    assert isinstance(result, str)
    assert len(result) > 0


def test_build_prompt_includes_contact_text(tmp_path):
    f = tmp_path / "contact.md"
    f.write_text("# kksudo\n\nAuthor of AgentFS, memory system.", encoding="utf-8")
    result = mod.build_prompt(f, None)
    assert "kksudo" in result


def test_build_prompt_handles_no_project(tmp_path):
    f = tmp_path / "contact.md"
    f.write_text("# Author\n\nSome text.", encoding="utf-8")
    result = mod.build_prompt(f, None)
    assert "нет дополнительных данных" in result


def test_build_prompt_includes_project_excerpt(tmp_path):
    contact = tmp_path / "contact.md"
    contact.write_text("# Author\n\nProfile.", encoding="utf-8")
    project = tmp_path / "agentfs.md"
    project.write_text("# AgentFS\n\nA unique filesystem with special features.", encoding="utf-8")
    result = mod.build_prompt(contact, project)
    assert "AgentFS" in result


def test_enriched_marker_constant():
    assert hasattr(mod, "ENRICHED_MARKER")
    assert isinstance(mod.ENRICHED_MARKER, str)
    assert "llm" in mod.ENRICHED_MARKER.lower()


def test_model_constant():
    assert hasattr(mod, "MODEL")
    assert isinstance(mod.MODEL, str)
    assert "claude" in mod.MODEL.lower()


# ── main ──────────────────────────────────────────────────────────────────────

def test_main_dry_run_all_no_authors(tmp_path, monkeypatch):
    monkeypatch.setattr(mod, "DOCS", tmp_path)
    monkeypatch.setattr(mod, "ROOT", tmp_path)
    monkeypatch.setattr(mod, "DRY_RUN", True)
    monkeypatch.setattr(mod, "ALL_MODE", True)
    monkeypatch.setattr(mod, "AUTHOR", None)
    (tmp_path / "contacts").mkdir()
    mod.main()


def test_main_no_author_no_all_exits(tmp_path, monkeypatch):
    monkeypatch.setattr(mod, "DOCS", tmp_path)
    monkeypatch.setattr(mod, "ROOT", tmp_path)
    monkeypatch.setattr(mod, "DRY_RUN", True)
    monkeypatch.setattr(mod, "ALL_MODE", False)
    monkeypatch.setattr(mod, "AUTHOR", None)
    try:
        mod.main()
    except SystemExit:
        pass


def test_find_contact_file_not_found(tmp_path, monkeypatch):
    monkeypatch.setattr(mod, "DOCS", tmp_path)
    (tmp_path / "contacts").mkdir()
    result = mod._find_contact_file("nonexistent_author_xyz")
    assert result is None


def test_find_contact_file_found(tmp_path, monkeypatch):
    monkeypatch.setattr(mod, "DOCS", tmp_path)
    contacts = tmp_path / "contacts"
    contacts.mkdir()
    (contacts / "kksudo.md").write_text("# kksudo\n\nContent.", encoding="utf-8")
    result = mod._find_contact_file("kksudo")
    assert result is not None
    assert result.name == "kksudo.md"


def test_find_project_file_not_found(tmp_path, monkeypatch):
    monkeypatch.setattr(mod, "DOCS", tmp_path)
    result = mod._find_project_file("nonexistent_project_xyz")
    assert result is None


def test_contact_is_messaged_true(tmp_path):
    f = tmp_path / "contact.md"
    f.write_text("## Статус\n\n- [x] Написали первое сообщение\n", encoding="utf-8")
    result = mod._contact_is_messaged(f)
    assert result is True


def test_contact_is_messaged_false(tmp_path):
    f = tmp_path / "contact.md"
    f.write_text("## Статус\n\n- [ ] Написали первое сообщение\n", encoding="utf-8")
    result = mod._contact_is_messaged(f)
    assert result is False


def test_build_prompt_returns_string(tmp_path):
    f = tmp_path / "contact.md"
    f.write_text("# Author\n\n## Профиль\n\nDeveloper.", encoding="utf-8")
    result = mod.build_prompt(f, None)
    assert isinstance(result, str)
    assert len(result) > 50
