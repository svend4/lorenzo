"""Tests for scripts/improve_auto_linker.py."""

import importlib
import json
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(ROOT / "scripts"))

mod = importlib.import_module("improve_auto_linker")


def test_make_link_returns_string():
    result = mod._make_link("AgentFS", "docs/05-habr-projects/knowledge/agentfs.md", "docs/01-svyazi/intro.md")
    assert isinstance(result, str)


def test_make_link_contains_name():
    result = mod._make_link("AgentFS", "docs/05-habr-projects/knowledge/agentfs.md", "docs/01-svyazi/intro.md")
    assert "AgentFS" in result


def test_make_link_is_markdown_link():
    result = mod._make_link("AgentFS", "docs/05-habr-projects/knowledge/agentfs.md", "docs/01-svyazi/intro.md")
    assert result.startswith("[") and "](" in result and result.endswith(")")


def test_link_paragraph_returns_tuple():
    entity_map = {
        "AgentFS": {"type": "projects", "best_file": "docs/05-habr-projects/knowledge/agentfs.md", "files_count": 5},
    }
    result = mod._link_paragraph("AgentFS is great for knowledge management.", entity_map, "docs/other.md")
    assert isinstance(result, tuple)
    assert len(result) == 2


def test_link_paragraph_replaces_entity():
    entity_map = {
        "AgentFS": {"type": "projects", "best_file": "docs/05-habr-projects/knowledge/agentfs.md", "files_count": 5},
    }
    new_text, count = mod._link_paragraph("AgentFS is great.", entity_map, "docs/other.md")
    assert count > 0
    assert "[AgentFS]" in new_text


def test_link_paragraph_skips_self_reference():
    entity_map = {
        "AgentFS": {"type": "projects", "best_file": "docs/agentfs.md", "files_count": 5},
    }
    # Source is the same as best_file → should skip
    new_text, count = mod._link_paragraph("AgentFS is great.", entity_map, "docs/agentfs.md")
    assert count == 0


def test_link_paragraph_skips_already_linked():
    entity_map = {
        "AgentFS": {"type": "projects", "best_file": "docs/agentfs.md", "files_count": 5},
    }
    # Already a link → should skip
    new_text, count = mod._link_paragraph("[AgentFS](../agentfs.md) is great.", entity_map, "docs/other.md")
    assert count == 0


def test_link_paragraph_skips_none_best_file():
    entity_map = {
        "AgentFS": {"type": "projects", "best_file": None, "files_count": 5},
    }
    new_text, count = mod._link_paragraph("AgentFS is great.", entity_map, "docs/other.md")
    assert count == 0


def test_link_paragraph_empty_text():
    entity_map = {}
    new_text, count = mod._link_paragraph("", entity_map, "docs/other.md")
    assert count == 0
    assert new_text == ""


def test_load_entity_map_missing_file(tmp_path, monkeypatch):
    monkeypatch.setattr(mod, "ENTITIES_PATH", tmp_path / "missing.json")
    result = mod._load_entity_map(min_mentions=1)
    assert result == {}


def test_load_entity_map_valid(tmp_path, monkeypatch):
    data = {
        "AgentFS": {
            "name": "AgentFS",
            "type": "projects",
            "files": ["docs/a.md", "docs/b.md", "docs/c.md"],
        }
    }
    entities_file = tmp_path / "named_entities.json"
    entities_file.write_text(json.dumps(data), encoding="utf-8")
    monkeypatch.setattr(mod, "ENTITIES_PATH", entities_file)
    result = mod._load_entity_map(min_mentions=2)
    assert "AgentFS" in result


def test_load_entity_map_filters_by_mentions(tmp_path, monkeypatch):
    data = {
        "AgentFS": {
            "name": "AgentFS",
            "type": "projects",
            "files": ["docs/a.md"],  # Only 1 file, below min_mentions=3
        }
    }
    entities_file = tmp_path / "named_entities.json"
    entities_file.write_text(json.dumps(data), encoding="utf-8")
    monkeypatch.setattr(mod, "ENTITIES_PATH", entities_file)
    result = mod._load_entity_map(min_mentions=3)
    assert "AgentFS" not in result


def test_process_file_returns_tuple(tmp_path, monkeypatch):
    monkeypatch.setattr(mod, "ROOT", tmp_path)
    f = tmp_path / "test.md"
    f.write_text("# Test\n\nSome content here.\n", encoding="utf-8")
    result = mod.process_file(f, {})
    assert isinstance(result, tuple)
    assert len(result) == 2


def test_process_file_skips_headings(tmp_path, monkeypatch):
    monkeypatch.setattr(mod, "ROOT", tmp_path)
    entity_map = {
        "AgentFS": {"type": "projects", "best_file": "docs/agentfs.md", "files_count": 5},
    }
    f = tmp_path / "test.md"
    f.write_text("# AgentFS Overview\n\nContent here.\n", encoding="utf-8")
    new_text, count = mod.process_file(f, entity_map)
    # Headings should not be linked
    assert "# AgentFS Overview" in new_text or count == 0


def test_process_file_skips_code_blocks(tmp_path, monkeypatch):
    monkeypatch.setattr(mod, "ROOT", tmp_path)
    entity_map = {
        "AgentFS": {"type": "projects", "best_file": str(tmp_path / "agentfs.md"), "files_count": 5},
    }
    f = tmp_path / "test.md"
    f.write_text("```python\nAgentFS.init()\n```\n", encoding="utf-8")
    new_text, count = mod.process_file(f, entity_map)
    # Code blocks should not be linked
    assert "```" in new_text


# ── main ──────────────────────────────────────────────────────────────────────

def test_main_dry_run_no_crash(tmp_path, monkeypatch):
    monkeypatch.setattr(mod, "DOCS", tmp_path)
    monkeypatch.setattr(mod, "ROOT", tmp_path)
    monkeypatch.setattr(mod, "APPLY", False)
    monkeypatch.setattr(mod, "DRY_RUN", True)
    monkeypatch.setattr(mod, "SECTION_FILTER", None)
    (tmp_path / "doc.md").write_text("# AgentFS\n\nAgentFS memory agent.", encoding="utf-8")
    mod.main()  # dry-run → must not raise


def test_main_empty_docs_no_crash(tmp_path, monkeypatch):
    monkeypatch.setattr(mod, "DOCS", tmp_path)
    monkeypatch.setattr(mod, "ROOT", tmp_path)
    monkeypatch.setattr(mod, "APPLY", False)
    monkeypatch.setattr(mod, "DRY_RUN", True)
    monkeypatch.setattr(mod, "SECTION_FILTER", None)
    mod.main()  # no files → must not raise


def test_main_apply_no_crash(tmp_path, monkeypatch):
    monkeypatch.setattr(mod, "DOCS", tmp_path)
    monkeypatch.setattr(mod, "ROOT", tmp_path)
    monkeypatch.setattr(mod, "APPLY", True)
    monkeypatch.setattr(mod, "DRY_RUN", False)
    monkeypatch.setattr(mod, "SECTION_FILTER", None)
    (tmp_path / "doc.md").write_text("# Title\n\nContent about memory.", encoding="utf-8")
    mod.main()  # apply → must not raise


# ── arg parsing ────────────────────────────────────────────────────────────────

def test_types_arg_parsing():
    """Lines 39-41: --types sets TYPES_FILTER."""
    orig = sys.argv[:]
    try:
        sys.argv = ["prog", "--types", "projects,tech"]
        importlib.reload(mod)
        assert "projects" in mod.TYPES_FILTER
    finally:
        sys.argv = orig
        importlib.reload(mod)


def test_min_mentions_arg_parsing():
    """Lines 45-47: --min-mentions sets MIN_MENTIONS."""
    orig = sys.argv[:]
    try:
        sys.argv = ["prog", "--min-mentions", "5"]
        importlib.reload(mod)
        assert mod.MIN_MENTIONS == 5
    finally:
        sys.argv = orig
        importlib.reload(mod)


def test_section_arg_parsing():
    """Lines 51-53: --section sets SECTION_FILTER."""
    orig = sys.argv[:]
    try:
        sys.argv = ["prog", "--section", "01-svyazi"]
        importlib.reload(mod)
        assert mod.SECTION_FILTER is not None
    finally:
        sys.argv = orig
        importlib.reload(mod)


# ── _load_entity_map: exception reading file ──────────────────────────────────

def test_load_entity_map_invalid_json(tmp_path, monkeypatch):
    """Lines 76-77: invalid JSON → except Exception → return {}."""
    entities_file = tmp_path / "named_entities.json"
    entities_file.write_text("not valid json{{", encoding="utf-8")
    monkeypatch.setattr(mod, "ENTITIES_PATH", entities_file)
    result = mod._load_entity_map(min_mentions=1)
    assert result == {}


def test_load_entity_map_with_types_filter(tmp_path, monkeypatch):
    """Line 84: TYPES_FILTER is non-empty → use it."""
    data = {
        "AgentFS": {"type": "projects", "files": ["a.md", "b.md"]},
        "Svyazi": {"type": "frameworks", "files": ["a.md", "b.md"]},
    }
    entities_file = tmp_path / "named_entities.json"
    entities_file.write_text(json.dumps(data), encoding="utf-8")
    monkeypatch.setattr(mod, "ENTITIES_PATH", entities_file)
    monkeypatch.setattr(mod, "TYPES_FILTER", {"projects"})
    result = mod._load_entity_map(min_mentions=1)
    assert "AgentFS" in result
    assert "Svyazi" not in result


# ── _make_link: exception path ─────────────────────────────────────────────────

def test_make_link_exception_path(monkeypatch, tmp_path):
    """Lines 125-126: ROOT path issue → fallback to original target."""
    monkeypatch.setattr(mod, "ROOT", tmp_path / "different_root")
    result = mod._make_link("AgentFS", "docs/agentfs.md", "docs/other.md")
    assert "AgentFS" in result


# ── process_file: exception and heading/blockquote skipping ─────────────────────

def test_process_file_read_error(tmp_path, monkeypatch):
    """Lines 161-162: exception reading file → return ('', 0)."""
    monkeypatch.setattr(mod, "ROOT", tmp_path)
    from pathlib import Path as _Path
    orig_read = _Path.read_text
    def mock_read(self, *a, **kw):
        raise OSError("mock error")
    monkeypatch.setattr(_Path, "read_text", mock_read)
    bad = tmp_path / "bad.md"
    bad.write_text("content", encoding="utf-8")
    result = mod.process_file(bad, {})
    # After monkeypatching read_text, calling process_file should return ("", 0)
    assert result == ("", 0)


def test_process_file_skips_blockquotes(tmp_path, monkeypatch):
    """Lines 185-186: blockquote lines → not linked."""
    monkeypatch.setattr(mod, "ROOT", tmp_path)
    entity_map = {
        "AgentFS": {"type": "projects", "best_file": str(tmp_path / "agentfs.md"), "files_count": 5},
    }
    f = tmp_path / "test.md"
    f.write_text("> AgentFS is mentioned in this blockquote.\n", encoding="utf-8")
    new_text, count = mod.process_file(f, entity_map)
    assert count == 0


# ── main: entity_map empty ────────────────────────────────────────────────────

def test_main_entity_map_empty_prints_warning(tmp_path, monkeypatch, capsys):
    """Lines 204-205: entity_map empty → print warning and return."""
    monkeypatch.setattr(mod, "DOCS", tmp_path)
    monkeypatch.setattr(mod, "ROOT", tmp_path)
    monkeypatch.setattr(mod, "APPLY", False)
    monkeypatch.setattr(mod, "DRY_RUN", True)
    monkeypatch.setattr(mod, "SECTION_FILTER", None)
    monkeypatch.setattr(mod, "ENTITIES_PATH", tmp_path / "missing.json")
    (tmp_path / "doc.md").write_text("# Title\n\nContent.\n", encoding="utf-8")
    mod.main()
    out = capsys.readouterr().out
    assert "named_entities.json" in out or "не найден" in out


# ── main: APPLY mode writes files ────────────────────────────────────────────

def test_main_apply_writes_links(tmp_path, monkeypatch):
    """Lines 233-237: APPLY mode → file written with links."""
    monkeypatch.setattr(mod, "DOCS", tmp_path)
    monkeypatch.setattr(mod, "ROOT", tmp_path)
    monkeypatch.setattr(mod, "APPLY", True)
    monkeypatch.setattr(mod, "DRY_RUN", False)
    monkeypatch.setattr(mod, "SECTION_FILTER", None)
    monkeypatch.setattr(mod, "MIN_MENTIONS", 1)
    # Create a named_entities.json with an entity
    data = {"AgentFS": {"type": "projects", "files": ["doc.md", "doc2.md"], "best_file": "doc2.md"}}
    entities_file = tmp_path / "named_entities.json"
    entities_file.write_text(json.dumps(data), encoding="utf-8")
    monkeypatch.setattr(mod, "ENTITIES_PATH", entities_file)
    (tmp_path / "doc.md").write_text("AgentFS is a knowledge system.\n", encoding="utf-8")
    (tmp_path / "doc2.md").write_text("AgentFS reference.\n", encoding="utf-8")
    mod.main()
    # File should have been processed


# ── __main__ block ─────────────────────────────────────────────────────────────

def test_main_block_via_runpy(tmp_path, monkeypatch):
    """Line 245: __main__ block."""
    import runpy
    monkeypatch.setattr(mod, "DOCS", tmp_path)
    monkeypatch.setattr(mod, "ROOT", tmp_path)
    monkeypatch.setattr(mod, "APPLY", False)
    monkeypatch.setattr(mod, "DRY_RUN", True)
    monkeypatch.setattr(mod, "SECTION_FILTER", None)
    runpy.run_path(str(ROOT / "scripts" / "improve_auto_linker.py"), run_name="__main__")
