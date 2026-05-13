"""Tests for scripts/improve_llm_enrich.py."""

import importlib
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(ROOT / "scripts"))

mod = importlib.import_module("improve_llm_enrich")


def test_extract_facts_returns_dict(tmp_path, monkeypatch):
    monkeypatch.setattr(mod, "ROOT", tmp_path)
    f = tmp_path / "project.md"
    f.write_text("# My Project\n\nSome content about the project.", encoding="utf-8")
    result = mod.extract_facts(f)
    assert isinstance(result, dict)


def test_extract_facts_has_title(tmp_path, monkeypatch):
    monkeypatch.setattr(mod, "ROOT", tmp_path)
    f = tmp_path / "project.md"
    f.write_text("# My Project Title\n\nContent.", encoding="utf-8")
    result = mod.extract_facts(f)
    assert "title" in result
    assert result["title"] == "My Project Title"


def test_extract_facts_title_fallback_to_stem(tmp_path, monkeypatch):
    monkeypatch.setattr(mod, "ROOT", tmp_path)
    f = tmp_path / "my-project.md"
    f.write_text("No heading here.\n\nContent.", encoding="utf-8")
    result = mod.extract_facts(f)
    assert result["title"] == "my-project"


def test_extract_facts_has_tags(tmp_path, monkeypatch):
    monkeypatch.setattr(mod, "ROOT", tmp_path)
    f = tmp_path / "project.md"
    f.write_text("# Project\n\n<!-- tags: memory, agent, rag -->\n\nContent.", encoding="utf-8")
    result = mod.extract_facts(f)
    assert "tags" in result
    assert isinstance(result["tags"], list)
    assert "memory" in result["tags"]
    assert "agent" in result["tags"]


def test_extract_facts_empty_tags(tmp_path, monkeypatch):
    monkeypatch.setattr(mod, "ROOT", tmp_path)
    f = tmp_path / "project.md"
    f.write_text("# Project\n\nContent without tags.", encoding="utf-8")
    result = mod.extract_facts(f)
    assert result["tags"] == []


def test_extract_facts_has_summary(tmp_path, monkeypatch):
    monkeypatch.setattr(mod, "ROOT", tmp_path)
    f = tmp_path / "project.md"
    f.write_text("# Project\n\n<!-- summary -->\n> This is the summary text.\n\nContent.", encoding="utf-8")
    result = mod.extract_facts(f)
    assert "summary" in result
    assert "summary text" in result["summary"]


def test_extract_facts_empty_summary(tmp_path, monkeypatch):
    monkeypatch.setattr(mod, "ROOT", tmp_path)
    f = tmp_path / "project.md"
    f.write_text("# Project\n\nContent without summary.", encoding="utf-8")
    result = mod.extract_facts(f)
    assert result["summary"] == ""


def test_extract_facts_has_projects(tmp_path, monkeypatch):
    monkeypatch.setattr(mod, "ROOT", tmp_path)
    f = tmp_path / "project.md"
    f.write_text("# Project\n\n**Проекты:** AgentFS, NGT Memory, Yodoca\n\nContent.", encoding="utf-8")
    result = mod.extract_facts(f)
    assert "projects" in result
    assert "AgentFS" in result["projects"]


def test_extract_facts_has_chunks(tmp_path, monkeypatch):
    monkeypatch.setattr(mod, "ROOT", tmp_path)
    f = tmp_path / "project.md"
    f.write_text("# Project\n\nContent.\n\n## Section\n\nMore content.", encoding="utf-8")
    result = mod.extract_facts(f)
    assert "chunks" in result
    assert isinstance(result["chunks"], list)


def test_extract_facts_has_tokens(tmp_path, monkeypatch):
    monkeypatch.setattr(mod, "ROOT", tmp_path)
    f = tmp_path / "project.md"
    f.write_text("# Project\n\nContent.", encoding="utf-8")
    result = mod.extract_facts(f)
    assert "tokens" in result
    assert isinstance(result["tokens"], int)


def test_extract_facts_has_path(tmp_path, monkeypatch):
    monkeypatch.setattr(mod, "ROOT", tmp_path)
    f = tmp_path / "project.md"
    f.write_text("# Project\n\nContent.", encoding="utf-8")
    result = mod.extract_facts(f)
    assert "path" in result
    assert "project.md" in result["path"]


def test_enrich_prompt_constant():
    assert hasattr(mod, "ENRICH_PROMPT")
    assert isinstance(mod.ENRICH_PROMPT, str)
    assert "{title}" in mod.ENRICH_PROMPT


def test_dry_run_attribute():
    assert hasattr(mod, "DRY_RUN")
    assert isinstance(mod.DRY_RUN, bool)


def test_sections_constant():
    assert hasattr(mod, "SECTIONS")
    assert isinstance(mod.SECTIONS, list)
    assert "05-habr-projects" in mod.SECTIONS


def test_out_dir_attribute():
    assert hasattr(mod, "OUT_DIR")
    assert isinstance(mod.OUT_DIR, Path)


# ── main ──────────────────────────────────────────────────────────────────────

def test_main_dry_run_no_crash(tmp_path, monkeypatch):
    monkeypatch.setattr(mod, "DOCS", tmp_path)
    monkeypatch.setattr(mod, "ROOT", tmp_path)
    monkeypatch.setattr(mod, "DRY_RUN", True)
    monkeypatch.setattr(mod, "SECTIONS", [])
    monkeypatch.setattr(mod, "SECTION_FILTER", None)
    monkeypatch.setattr(mod, "FILE_FILTER", None)
    monkeypatch.setattr(mod, "FORCE", False)
    mod.main()


def test_main_dry_run_with_file(tmp_path, monkeypatch):
    doc = tmp_path / "doc.md"
    doc.write_text("# AgentFS\n\nContent.", encoding="utf-8")
    monkeypatch.setattr(mod, "DOCS", tmp_path)
    monkeypatch.setattr(mod, "ROOT", tmp_path)
    monkeypatch.setattr(mod, "DRY_RUN", True)
    monkeypatch.setattr(mod, "SECTIONS", [])
    monkeypatch.setattr(mod, "SECTION_FILTER", None)
    monkeypatch.setattr(mod, "FILE_FILTER", doc)
    monkeypatch.setattr(mod, "FORCE", False)
    mod.main()


def test_main_dry_run_empty_sections(tmp_path, monkeypatch):
    monkeypatch.setattr(mod, "DOCS", tmp_path)
    monkeypatch.setattr(mod, "ROOT", tmp_path)
    monkeypatch.setattr(mod, "DRY_RUN", True)
    monkeypatch.setattr(mod, "SECTIONS", ["nonexistent-section"])
    monkeypatch.setattr(mod, "SECTION_FILTER", None)
    monkeypatch.setattr(mod, "FILE_FILTER", None)
    monkeypatch.setattr(mod, "FORCE", False)
    mod.main()


def test_extract_facts_returns_dict(tmp_path, monkeypatch):
    monkeypatch.setattr(mod, "ROOT", tmp_path)
    f = tmp_path / "agentfs.md"
    f.write_text("# AgentFS\n\n<!-- tags: memory, agent -->\n\nContent.", encoding="utf-8")
    result = mod.extract_facts(f)
    assert isinstance(result, dict)
    assert "title" in result
    assert "tags" in result
    assert result["title"] == "AgentFS"


def test_extract_facts_finds_tags(tmp_path, monkeypatch):
    monkeypatch.setattr(mod, "ROOT", tmp_path)
    f = tmp_path / "doc.md"
    f.write_text("# Title\n\n<!-- tags: memory, search -->\n\nContent.", encoding="utf-8")
    result = mod.extract_facts(f)
    assert "memory" in result["tags"]
    assert "search" in result["tags"]


def test_build_enriched_returns_string(tmp_path, monkeypatch):
    monkeypatch.setattr(mod, "ROOT", tmp_path)
    facts = {
        "title": "AgentFS", "tags": ["memory"], "summary": "Agent filesystem.",
        "projects": "Yodoca", "path": "docs/agentfs.md",
        "chunks": [], "tokens": 100,
    }
    result = mod.build_enriched(facts, "## Content\n\nSome enriched content.")
    assert isinstance(result, str)
    assert "AgentFS" in result


# ── arg parsing ───────────────────────────────────────────────────────────────

def test_model_eq_arg_parsing():
    """Line 45: --model=VALUE sets DEFAULT_MODEL."""
    orig_argv = sys.argv[:]
    try:
        sys.argv = ["prog", "--model=claude-opus-4-7"]
        importlib.reload(mod)
        assert mod.DEFAULT_MODEL == "claude-opus-4-7"
    finally:
        sys.argv = orig_argv
        importlib.reload(mod)


def test_model_space_arg_parsing():
    """Lines 47-49: --model VALUE sets DEFAULT_MODEL."""
    orig_argv = sys.argv[:]
    try:
        sys.argv = ["prog", "--model", "claude-haiku-4-5-20251001"]
        importlib.reload(mod)
        assert mod.DEFAULT_MODEL == "claude-haiku-4-5-20251001"
    finally:
        sys.argv = orig_argv
        importlib.reload(mod)


def test_section_arg_parsing():
    """Lines 53-55: --section NAME sets SECTION_FILTER."""
    orig_argv = sys.argv[:]
    try:
        sys.argv = ["prog", "--section", "05-habr-projects"]
        importlib.reload(mod)
        assert mod.SECTION_FILTER == "05-habr-projects"
    finally:
        sys.argv = orig_argv
        importlib.reload(mod)


def test_file_arg_parsing():
    """Lines 60-63: --file PATH sets FILE_FILTER."""
    orig_argv = sys.argv[:]
    try:
        sys.argv = ["prog", "--file", "docs/05-habr-projects/memory/yodoca.md"]
        importlib.reload(mod)
        assert mod.FILE_FILTER is not None
    finally:
        sys.argv = orig_argv
        importlib.reload(mod)


# ── enrich_with_llm ───────────────────────────────────────────────────────────

def test_enrich_with_llm_single_chunk():
    """Lines 149-170: enrich_with_llm calls client and returns string."""
    class MockContent:
        text = "## Что это\n\nEnriched content here."
    class MockResp:
        content = [MockContent()]
    class MockMessages:
        def create(self, **kwargs):
            return MockResp()
    class MockClient:
        messages = MockMessages()

    facts = {
        "title": "AgentFS",
        "tags": ["memory", "agent"],
        "summary": "Agent filesystem.",
        "projects": "Yodoca",
        "chunks": ["This is the main content of the project."],
        "tokens": 10,
        "path": "docs/agentfs.md",
    }
    result = mod.enrich_with_llm(facts, MockClient(), "claude-haiku-4-5-20251001")
    assert isinstance(result, str)
    assert "Enriched content" in result


def test_enrich_with_llm_no_tags():
    """Line 154: tags_first = 'core' when no tags."""
    class MockContent:
        text = "Enriched."
    class MockResp:
        content = [MockContent()]
    class MockMessages:
        def create(self, **kwargs):
            return MockResp()
    class MockClient:
        messages = MockMessages()

    facts = {
        "title": "Project",
        "tags": [],
        "summary": "",
        "projects": "",
        "chunks": ["chunk one", "chunk two", "chunk three", "chunk four"],
        "tokens": 40,
        "path": "docs/project.md",
    }
    result = mod.enrich_with_llm(facts, MockClient(), "claude-haiku-4-5-20251001")
    assert isinstance(result, str)


# ── main: edge cases ──────────────────────────────────────────────────────────

def test_main_dry_run_with_force_flag(tmp_path, monkeypatch):
    """Line 221: FORCE=True prints force message."""
    monkeypatch.setattr(mod, "DOCS", tmp_path)
    monkeypatch.setattr(mod, "ROOT", tmp_path)
    monkeypatch.setattr(mod, "DRY_RUN", True)
    monkeypatch.setattr(mod, "SECTIONS", [])
    monkeypatch.setattr(mod, "SECTION_FILTER", None)
    monkeypatch.setattr(mod, "FILE_FILTER", None)
    monkeypatch.setattr(mod, "FORCE", True)
    mod.main()


def test_main_file_filter_missing(tmp_path, monkeypatch):
    """Lines 229-230: FILE_FILTER doesn't exist → sys.exit(1)."""
    monkeypatch.setattr(mod, "DOCS", tmp_path)
    monkeypatch.setattr(mod, "ROOT", tmp_path)
    monkeypatch.setattr(mod, "DRY_RUN", False)
    monkeypatch.setattr(mod, "SECTIONS", [])
    monkeypatch.setattr(mod, "SECTION_FILTER", None)
    monkeypatch.setattr(mod, "FILE_FILTER", tmp_path / "nonexistent.md")
    monkeypatch.setattr(mod, "FORCE", False)

    class MockAnthropicModule:
        def Anthropic(self):
            return object()
    monkeypatch.setitem(sys.modules, "anthropic", MockAnthropicModule())
    with pytest.raises(SystemExit):
        mod.main()


def test_main_dry_run_with_section(tmp_path, monkeypatch):
    """Lines 239-242: section loop with rglob, skips README.md and QA.md."""
    sec = tmp_path / "05-habr-projects"
    sec.mkdir()
    (sec / "doc.md").write_text("# Project\n\nContent.", encoding="utf-8")
    (sec / "README.md").write_text("# README\n\nIndex.", encoding="utf-8")
    (sec / "QA.md").write_text("# QA\n\nQuestions.", encoding="utf-8")
    monkeypatch.setattr(mod, "DOCS", tmp_path)
    monkeypatch.setattr(mod, "ROOT", tmp_path)
    monkeypatch.setattr(mod, "DRY_RUN", True)
    monkeypatch.setattr(mod, "SECTIONS", ["05-habr-projects"])
    monkeypatch.setattr(mod, "SECTION_FILTER", None)
    monkeypatch.setattr(mod, "FILE_FILTER", None)
    monkeypatch.setattr(mod, "FORCE", False)
    mod.main()


def test_main_apply_with_mock_anthropic(tmp_path, monkeypatch):
    """Lines 260-296: non-dry-run uses mock anthropic to enrich files."""
    sec = tmp_path / "05-habr-projects"
    sec.mkdir()
    (sec / "doc.md").write_text("# Project\n\nContent here.", encoding="utf-8")
    monkeypatch.setattr(mod, "DOCS", tmp_path)
    monkeypatch.setattr(mod, "ROOT", tmp_path)
    monkeypatch.setattr(mod, "DRY_RUN", False)
    monkeypatch.setattr(mod, "SECTIONS", ["05-habr-projects"])
    monkeypatch.setattr(mod, "SECTION_FILTER", None)
    monkeypatch.setattr(mod, "FILE_FILTER", None)
    monkeypatch.setattr(mod, "FORCE", False)
    monkeypatch.setattr(mod, "OUT_DIR", tmp_path / "enriched")

    class MockContent:
        text = "## Что это\n\nEnriched."
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
    mod.main()
    assert (tmp_path / "enriched").exists()


def test_main_apply_already_enriched_no_force(tmp_path, monkeypatch):
    """Line 278-279: out_path exists and not FORCE → skip."""
    sec = tmp_path / "05-habr-projects"
    sec.mkdir()
    (sec / "doc.md").write_text("# Project\n\nContent.", encoding="utf-8")
    out_sec = tmp_path / "enriched" / "05-habr-projects"
    out_sec.mkdir(parents=True)
    (out_sec / "doc-enriched.md").write_text("already enriched", encoding="utf-8")
    monkeypatch.setattr(mod, "DOCS", tmp_path)
    monkeypatch.setattr(mod, "ROOT", tmp_path)
    monkeypatch.setattr(mod, "DRY_RUN", False)
    monkeypatch.setattr(mod, "SECTIONS", ["05-habr-projects"])
    monkeypatch.setattr(mod, "SECTION_FILTER", None)
    monkeypatch.setattr(mod, "FILE_FILTER", None)
    monkeypatch.setattr(mod, "FORCE", False)
    monkeypatch.setattr(mod, "OUT_DIR", tmp_path / "enriched")

    class MockAnthropicModule:
        def Anthropic(self):
            class Inst:
                class messages:
                    @staticmethod
                    def create(**kwargs):
                        raise AssertionError("should not be called")
            return Inst()

    monkeypatch.setitem(sys.modules, "anthropic", MockAnthropicModule())
    mod.main()  # should skip without calling LLM


def test_main_apply_exception_caught(tmp_path, monkeypatch):
    """Lines 291-293: exception in enrich loop → errors += 1, no crash."""
    sec = tmp_path / "05-habr-projects"
    sec.mkdir()
    (sec / "doc.md").write_text("# Project\n\nContent.", encoding="utf-8")
    monkeypatch.setattr(mod, "DOCS", tmp_path)
    monkeypatch.setattr(mod, "ROOT", tmp_path)
    monkeypatch.setattr(mod, "DRY_RUN", False)
    monkeypatch.setattr(mod, "SECTIONS", ["05-habr-projects"])
    monkeypatch.setattr(mod, "SECTION_FILTER", None)
    monkeypatch.setattr(mod, "FILE_FILTER", None)
    monkeypatch.setattr(mod, "FORCE", False)
    monkeypatch.setattr(mod, "OUT_DIR", tmp_path / "enriched")

    class MockMessages:
        def create(self, **kwargs):
            raise RuntimeError("API error")
    class MockAnthropicInstance:
        messages = MockMessages()
    class MockAnthropicModule:
        def Anthropic(self):
            return MockAnthropicInstance()

    monkeypatch.setitem(sys.modules, "anthropic", MockAnthropicModule())
    mod.main()  # should not crash


def test_main_apply_anthropic_not_installed(tmp_path, monkeypatch):
    """Lines 262-264: anthropic not importable → sys.exit(1)."""
    sec = tmp_path / "05-habr-projects"
    sec.mkdir()
    (sec / "doc.md").write_text("# Project\n\nContent.", encoding="utf-8")
    monkeypatch.setattr(mod, "DOCS", tmp_path)
    monkeypatch.setattr(mod, "ROOT", tmp_path)
    monkeypatch.setattr(mod, "DRY_RUN", False)
    monkeypatch.setattr(mod, "SECTIONS", ["05-habr-projects"])
    monkeypatch.setattr(mod, "SECTION_FILTER", None)
    monkeypatch.setattr(mod, "FILE_FILTER", None)
    monkeypatch.setattr(mod, "FORCE", False)
    saved = sys.modules.pop("anthropic", None)
    try:
        with pytest.raises(SystemExit):
            mod.main()
    finally:
        if saved is not None:
            sys.modules["anthropic"] = saved


# ── __main__ block ────────────────────────────────────────────────────────────

def test_main_block_via_runpy(tmp_path, monkeypatch):
    """Line 300: __main__ block."""
    import runpy
    orig_argv = sys.argv[:]
    try:
        sys.argv = ["prog", "--dry-run"]
        monkeypatch.setattr(mod, "DOCS", tmp_path)
        monkeypatch.setattr(mod, "ROOT", tmp_path)
        script_path = str(ROOT / "scripts" / "improve_llm_enrich.py")
        runpy.run_path(script_path, run_name="__main__")
    finally:
        sys.argv = orig_argv
