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


# ── arg parsing ───────────────────────────────────────────────────────────────

def test_author_arg_parsing():
    """Lines 32-34: --author NAME sets AUTHOR."""
    orig_argv = sys.argv[:]
    try:
        sys.argv = ["prog", "--author", "kksudo"]
        importlib.reload(mod)
        assert mod.AUTHOR == "kksudo"
    finally:
        sys.argv = orig_argv
        importlib.reload(mod)


# ── _get_all_authors_no_reply ─────────────────────────────────────────────────

def test_get_all_authors_no_reply_empty(tmp_path, monkeypatch):
    """Lines 172-175: contacts dir empty → empty list."""
    monkeypatch.setattr(mod, "DOCS", tmp_path)
    contacts = tmp_path / "contacts"
    contacts.mkdir()
    result = mod._get_all_authors_no_reply()
    assert result == []


def test_get_all_authors_no_reply_finds_unmessaged(tmp_path, monkeypatch):
    """Lines 172-175: unmessaged author found."""
    monkeypatch.setattr(mod, "DOCS", tmp_path)
    contacts = tmp_path / "contacts"
    contacts.mkdir()
    (contacts / "author1.md").write_text(
        "# Author1\n\n- [ ] Написали первое сообщение\n", encoding="utf-8"
    )
    result = mod._get_all_authors_no_reply()
    assert len(result) == 1


# ── enrich_contact ────────────────────────────────────────────────────────────

def test_enrich_contact_dry_run(tmp_path, monkeypatch):
    """Lines 128-131: DRY_RUN=True → just prints, returns True."""
    monkeypatch.setattr(mod, "DOCS", tmp_path)
    monkeypatch.setattr(mod, "DRY_RUN", True)
    contacts = tmp_path / "contacts"
    contacts.mkdir()
    f = contacts / "author.md"
    f.write_text("# Author\n\nContent here.", encoding="utf-8")
    result = mod.enrich_contact(f, None)
    assert result is True


def test_enrich_contact_with_mock_client(tmp_path, monkeypatch):
    """Lines 133-165: non-dry-run enrich_contact with mock API client."""
    monkeypatch.setattr(mod, "DOCS", tmp_path)
    monkeypatch.setattr(mod, "DRY_RUN", False)
    contacts = tmp_path / "contacts"
    contacts.mkdir()
    f = contacts / "author.md"
    f.write_text("# Author\n\nContent here.", encoding="utf-8")

    class MockContent:
        text = "Improved message text here."
    class MockResp:
        content = [MockContent()]
    class MockMessages:
        def create(self, **kwargs):
            return MockResp()
    class MockClient:
        messages = MockMessages()

    result = mod.enrich_contact(f, MockClient())
    assert result is True


def test_enrich_contact_updates_existing_marker(tmp_path, monkeypatch):
    """Lines 147-153: file already has ENRICHED_MARKER → update existing block."""
    monkeypatch.setattr(mod, "DOCS", tmp_path)
    monkeypatch.setattr(mod, "DRY_RUN", False)
    contacts = tmp_path / "contacts"
    contacts.mkdir()
    f = contacts / "author.md"
    marker = mod.ENRICHED_MARKER
    f.write_text(
        f"# Author\n\n{marker}\n## Old Block (LLM, 2025-01-01)\n\n```\nOld message.\n```\n\n## Other\n\nContent.\n",
        encoding="utf-8",
    )

    class MockContent:
        text = "New improved message."
    class MockResp:
        content = [MockContent()]
    class MockMessages:
        def create(self, **kwargs):
            return MockResp()
    class MockClient:
        messages = MockMessages()

    mod.enrich_contact(f, MockClient())
    content = f.read_text(encoding="utf-8")
    assert "New improved message" in content


def test_enrich_contact_inserts_after_first_message(tmp_path, monkeypatch):
    """Lines 157-159: insert_after 'Первое сообщение' code block found."""
    monkeypatch.setattr(mod, "DOCS", tmp_path)
    monkeypatch.setattr(mod, "DRY_RUN", False)
    contacts = tmp_path / "contacts"
    contacts.mkdir()
    f = contacts / "author.md"
    f.write_text(
        "# Author\n\n## Первое сообщение\n\nHello world.\n```\ndraft\n```\n\nAfterward.\n",
        encoding="utf-8",
    )

    class MockContent:
        text = "Better message."
    class MockResp:
        content = [MockContent()]
    class MockMessages:
        def create(self, **kwargs):
            return MockResp()
    class MockClient:
        messages = MockMessages()

    mod.enrich_contact(f, MockClient())
    content = f.read_text(encoding="utf-8")
    assert "Better message" in content


# ── main ──────────────────────────────────────────────────────────────────────

def test_main_author_not_found_exits(tmp_path, monkeypatch):
    """Lines 188-191: AUTHOR set but contact not found → sys.exit(1)."""
    monkeypatch.setattr(mod, "DOCS", tmp_path)
    monkeypatch.setattr(mod, "ROOT", tmp_path)
    monkeypatch.setattr(mod, "DRY_RUN", True)
    monkeypatch.setattr(mod, "ALL_MODE", False)
    monkeypatch.setattr(mod, "AUTHOR", "nonexistent_author_xyz")
    (tmp_path / "contacts").mkdir()
    with pytest.raises(SystemExit):
        mod.main()


def test_main_author_found_sets_targets(tmp_path, monkeypatch):
    """Line 192: AUTHOR set and found → targets = [path]."""
    contacts = tmp_path / "contacts"
    contacts.mkdir()
    (contacts / "kksudo.md").write_text("# kksudo\n\nContent.", encoding="utf-8")
    monkeypatch.setattr(mod, "DOCS", tmp_path)
    monkeypatch.setattr(mod, "ROOT", tmp_path)
    monkeypatch.setattr(mod, "DRY_RUN", True)
    monkeypatch.setattr(mod, "ALL_MODE", False)
    monkeypatch.setattr(mod, "AUTHOR", "kksudo")
    mod.main()  # DRY_RUN → should not crash


def test_main_dry_run_with_author_targets(tmp_path, monkeypatch):
    """Lines 203-204: DRY_RUN=True with valid targets → prints plan."""
    monkeypatch.setattr(mod, "DOCS", tmp_path)
    monkeypatch.setattr(mod, "ROOT", tmp_path)
    monkeypatch.setattr(mod, "DRY_RUN", True)
    monkeypatch.setattr(mod, "ALL_MODE", True)
    monkeypatch.setattr(mod, "AUTHOR", None)
    contacts = tmp_path / "contacts"
    contacts.mkdir()
    (contacts / "author1.md").write_text(
        "# Author1\n\n- [ ] Написали первое сообщение\n", encoding="utf-8"
    )
    mod.main()  # should not crash


def test_main_apply_with_mock_anthropic(tmp_path, monkeypatch):
    """Lines 218-225: non-dry-run uses mock anthropic client."""
    monkeypatch.setattr(mod, "DOCS", tmp_path)
    monkeypatch.setattr(mod, "ROOT", tmp_path)
    monkeypatch.setattr(mod, "DRY_RUN", False)
    monkeypatch.setattr(mod, "ALL_MODE", True)
    monkeypatch.setattr(mod, "AUTHOR", None)
    contacts = tmp_path / "contacts"
    contacts.mkdir()
    (contacts / "author1.md").write_text(
        "# Author1\n\n- [ ] Написали первое сообщение\n", encoding="utf-8"
    )

    class MockContent:
        text = "Improved message."
    class MockResp:
        content = [MockContent()]
    class MockMessages:
        def create(self, **kwargs):
            return MockResp()
    class MockAnthropicInstance:
        messages = MockMessages()
    class MockAnthropicModule:
        def Anthropic(self):
            return MockAnthropicInstance()

    monkeypatch.setitem(sys.modules, "anthropic", MockAnthropicModule())
    monkeypatch.setattr(mod, "DRY_RUN", False)
    mod.main()  # should not crash


def test_main_apply_anthropic_not_installed(tmp_path, monkeypatch):
    """Lines 214-216: anthropic not importable → sys.exit(1)."""
    monkeypatch.setattr(mod, "DOCS", tmp_path)
    monkeypatch.setattr(mod, "ROOT", tmp_path)
    monkeypatch.setattr(mod, "DRY_RUN", False)
    monkeypatch.setattr(mod, "ALL_MODE", True)
    monkeypatch.setattr(mod, "AUTHOR", None)
    contacts = tmp_path / "contacts"
    contacts.mkdir()
    (contacts / "author1.md").write_text(
        "# Author1\n\n- [ ] Написали первое сообщение\n", encoding="utf-8"
    )
    saved = sys.modules.pop("anthropic", None)
    try:
        with pytest.raises(SystemExit):
            mod.main()
    finally:
        if saved is not None:
            sys.modules["anthropic"] = saved


def test_main_apply_enrich_exception_handled(tmp_path, monkeypatch):
    """Lines 226-227: enrich_contact raises → exception caught."""
    monkeypatch.setattr(mod, "DOCS", tmp_path)
    monkeypatch.setattr(mod, "ROOT", tmp_path)
    monkeypatch.setattr(mod, "DRY_RUN", False)
    monkeypatch.setattr(mod, "ALL_MODE", True)
    monkeypatch.setattr(mod, "AUTHOR", None)
    contacts = tmp_path / "contacts"
    contacts.mkdir()
    (contacts / "author1.md").write_text(
        "# Author1\n\n- [ ] Написали первое сообщение\n", encoding="utf-8"
    )

    class MockMessages:
        def create(self, **kwargs):
            raise RuntimeError("API error")
    class MockAnthropicInstance:
        messages = MockMessages()
    class MockAnthropicModule:
        def Anthropic(self):
            return MockAnthropicInstance()

    monkeypatch.setitem(sys.modules, "anthropic", MockAnthropicModule())
    mod.main()  # exception caught, should not crash


def test_get_all_authors_skips_readme(tmp_path, monkeypatch):
    """Line 173: README.md in contacts → skip."""
    monkeypatch.setattr(mod, "DOCS", tmp_path)
    contacts = tmp_path / "contacts"
    contacts.mkdir()
    (contacts / "README.md").write_text("# Contacts index.", encoding="utf-8")
    result = mod._get_all_authors_no_reply()
    assert result == []


# ── __main__ block ────────────────────────────────────────────────────────────

def test_main_block_via_runpy(tmp_path, monkeypatch):
    """Line 234: __main__ block."""
    import runpy
    monkeypatch.setattr(mod, "DOCS", tmp_path)
    monkeypatch.setattr(mod, "ROOT", tmp_path)
    monkeypatch.setattr(mod, "DRY_RUN", True)
    monkeypatch.setattr(mod, "ALL_MODE", False)
    monkeypatch.setattr(mod, "AUTHOR", None)
    script_path = str(ROOT / "scripts" / "improve_llm_contact.py")
    try:
        runpy.run_path(script_path, run_name="__main__")
    except SystemExit:
        pass  # exits with code 1 (no --author or --all)
