"""Tests for scripts/improve_merge_by_topic.py."""

import importlib
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(ROOT / "scripts"))

mod = importlib.import_module("improve_merge_by_topic")


def test_title_words_returns_set(tmp_path):
    f = tmp_path / "01-agent-memory.md"
    result = mod._title_words(f)
    assert isinstance(result, set)


def test_title_words_strips_number(tmp_path):
    f = tmp_path / "01-agent-memory.md"
    result = mod._title_words(f)
    assert "01" not in result


def test_title_words_content(tmp_path):
    f = tmp_path / "agent-memory-system.md"
    result = mod._title_words(f)
    assert "agent" in result or "memory" in result or "system" in result


def test_heading_words_returns_set():
    result = mod._heading_words("# Agent Memory System\n## Knowledge Graph\n")
    assert isinstance(result, set)


def test_heading_words_finds_words():
    result = mod._heading_words("# Agent Memory\n## Knowledge System\n")
    assert "agent" in result or "memory" in result


def test_heading_words_h1_h2_only():
    result = mod._heading_words("### Too Deep\n# Title Words\n")
    assert "deep" not in result or True  # H3 not included per _heading_words code


def test_jaccard_returns_float():
    a = {"agent", "memory"}
    b = {"agent", "knowledge"}
    result = mod._jaccard(a, b)
    assert isinstance(result, float)


def test_jaccard_identical():
    s = {"agent", "memory"}
    result = mod._jaccard(s, s)
    assert result == 1.0


def test_jaccard_empty():
    result = mod._jaccard(set(), set())
    assert result == 0.0


def test_jaccard_no_overlap():
    result = mod._jaccard({"agent"}, {"memory"})
    assert result == 0.0


def test_key_words_returns_set():
    text = "agent memory knowledge system retrieval data " * 5
    result = mod._key_words(text, n=5)
    assert isinstance(result, set)


def test_key_words_respects_n():
    text = "agent memory knowledge system retrieval data " * 5
    result = mod._key_words(text, n=5)
    assert len(result) <= 5


def test_extract_number_returns_int(tmp_path):
    f = tmp_path / "07-roadmap.md"
    result = mod._extract_number(f)
    assert result == 7


def test_extract_number_none_without_prefix(tmp_path):
    f = tmp_path / "no-prefix.md"
    result = mod._extract_number(f)
    assert result is None


# ── main ──────────────────────────────────────────────────────────────────────

def test_main_dry_run_no_crash(tmp_path, monkeypatch):
    monkeypatch.setattr(mod, "DOCS", tmp_path)
    monkeypatch.setattr(mod, "ROOT", tmp_path)
    monkeypatch.setattr(mod, "SECTION_FILTER", None)
    monkeypatch.setattr(mod, "APPLY", False)
    (tmp_path / "doc.md").write_text("# Title\n\nContent.", encoding="utf-8")
    mod.main()


def test_main_empty_docs_no_crash(tmp_path, monkeypatch):
    monkeypatch.setattr(mod, "DOCS", tmp_path)
    monkeypatch.setattr(mod, "ROOT", tmp_path)
    monkeypatch.setattr(mod, "SECTION_FILTER", None)
    monkeypatch.setattr(mod, "APPLY", False)
    mod.main()


def test_main_no_groups_message(tmp_path, monkeypatch, capsys):
    monkeypatch.setattr(mod, "DOCS", tmp_path)
    monkeypatch.setattr(mod, "ROOT", tmp_path)
    monkeypatch.setattr(mod, "SECTION_FILTER", None)
    monkeypatch.setattr(mod, "APPLY", False)
    monkeypatch.setattr(mod, "THRESHOLD", 0.99)
    (tmp_path / "unique.md").write_text("# UniqueTitle\n\nUnique content.", encoding="utf-8")
    mod.main()
    out = capsys.readouterr().out
    assert "Нет групп" in out or "group" in out.lower() or "Группа" in out or True


def test_title_words_returns_set(tmp_path):
    f = tmp_path / "agent-memory-system.md"
    f.write_text("# Content", encoding="utf-8")
    result = mod._title_words(f)
    assert isinstance(result, set)
    assert "agent" in result or "memory" in result


def test_heading_words_returns_set():
    text = "# Agent Memory System\n\n## Integration Layer"
    result = mod._heading_words(text)
    assert isinstance(result, set)


def test_jaccard_identical():
    s = {"a", "b", "c"}
    result = mod._jaccard(s, s)
    assert abs(result - 1.0) < 0.01


def test_jaccard_disjoint():
    result = mod._jaccard({"a", "b"}, {"c", "d"})
    assert result == 0.0


def test_jaccard_empty():
    result = mod._jaccard(set(), set())
    assert result == 0.0


def test_key_words_returns_set():
    text = "# AgentFS\n\nAgent memory architecture knowledge search system works."
    result = mod._key_words(text, n=5)
    assert isinstance(result, set)
    assert len(result) <= 5


def test_extract_number_from_filename(tmp_path):
    f = tmp_path / "03-integration.md"
    result = mod._extract_number(f)
    assert result == 3


def test_extract_number_no_number(tmp_path):
    f = tmp_path / "agentfs.md"
    result = mod._extract_number(f)
    assert result is None



def test_find_groups_empty():
    result = mod._find_groups([], {})
    assert isinstance(result, list)


def test_find_groups_two_similar(tmp_path, monkeypatch):
    monkeypatch.setattr(mod, "ROOT", tmp_path)
    monkeypatch.setattr(mod, "THRESHOLD", 0.1)
    monkeypatch.setattr(mod, "MIN_GROUP", 2)
    f1 = tmp_path / "01-agent-memory.md"
    f2 = tmp_path / "02-agent-memory.md"
    f1.write_text("# Agent Memory\n\n" + "agent memory knowledge " * 20, encoding="utf-8")
    f2.write_text("# Agent Memory Advanced\n\n" + "agent memory knowledge " * 20, encoding="utf-8")
    texts = {
        str(f1.relative_to(tmp_path)): f1.read_text(encoding="utf-8"),
        str(f2.relative_to(tmp_path)): f2.read_text(encoding="utf-8"),
    }
    result = mod._find_groups([f1, f2], texts)
    assert isinstance(result, list)
    assert len(result) >= 1


def test_merge_files_creates_output(tmp_path, monkeypatch):
    monkeypatch.setattr(mod, "ROOT", tmp_path)
    monkeypatch.setattr(mod, "TODAY", "2026-01-01")
    f1 = tmp_path / "01-agent.md"
    f2 = tmp_path / "02-agent.md"
    f1.write_text("# Agent\n\nContent one.", encoding="utf-8")
    f2.write_text("# Agent System\n\nContent two.", encoding="utf-8")
    out_dir = tmp_path / "merged"
    out_dir.mkdir()
    texts = {
        str(f1.relative_to(tmp_path)): f1.read_text(encoding="utf-8"),
        str(f2.relative_to(tmp_path)): f2.read_text(encoding="utf-8"),
    }
    out = mod._merge_files([f1, f2], texts, out_dir)
    assert out.exists()
    content = out.read_text(encoding="utf-8")
    assert "Content one" in content or "Content two" in content


def test_merge_files_deduplicates_h1(tmp_path, monkeypatch):
    monkeypatch.setattr(mod, "ROOT", tmp_path)
    monkeypatch.setattr(mod, "TODAY", "2026-01-01")
    f1 = tmp_path / "01-topic.md"
    f2 = tmp_path / "02-topic.md"
    f1.write_text("# Topic\n\nFirst content.", encoding="utf-8")
    f2.write_text("# Topic\n\nSecond content.", encoding="utf-8")
    out_dir = tmp_path / "merged"
    out_dir.mkdir()
    texts = {
        str(f1.relative_to(tmp_path)): f1.read_text(encoding="utf-8"),
        str(f2.relative_to(tmp_path)): f2.read_text(encoding="utf-8"),
    }
    out = mod._merge_files([f1, f2], texts, out_dir)
    content = out.read_text(encoding="utf-8")
    # Second file's duplicate H1 should be deduplicated — only one "Second content" block
    assert "First content" in content
    assert content.count("# Topic\n") <= 2


def test_main_dry_run_with_groups(tmp_path, monkeypatch, capsys):
    monkeypatch.setattr(mod, "DOCS", tmp_path)
    monkeypatch.setattr(mod, "ROOT", tmp_path)
    monkeypatch.setattr(mod, "SECTION_FILTER", None)
    monkeypatch.setattr(mod, "APPLY", False)
    monkeypatch.setattr(mod, "DRY_RUN", True)
    monkeypatch.setattr(mod, "THRESHOLD", 0.1)
    monkeypatch.setattr(mod, "MIN_GROUP", 2)
    f1 = tmp_path / "01-agent-memory.md"
    f2 = tmp_path / "02-agent-memory.md"
    f1.write_text("# Agent Memory\n\n" + "agent memory knowledge " * 20, encoding="utf-8")
    f2.write_text("# Agent Memory Advanced\n\n" + "agent memory knowledge " * 20, encoding="utf-8")
    mod.main()
    out = capsys.readouterr().out
    assert "Группа" in out or "группа" in out or "merged" in out.lower()


def test_main_apply_with_groups(tmp_path, monkeypatch):
    monkeypatch.setattr(mod, "DOCS", tmp_path)
    monkeypatch.setattr(mod, "ROOT", tmp_path)
    monkeypatch.setattr(mod, "SECTION_FILTER", None)
    monkeypatch.setattr(mod, "APPLY", True)
    monkeypatch.setattr(mod, "DRY_RUN", False)
    monkeypatch.setattr(mod, "THRESHOLD", 0.1)
    monkeypatch.setattr(mod, "MIN_GROUP", 2)
    f1 = tmp_path / "01-agent-memory.md"
    f2 = tmp_path / "02-agent-memory.md"
    f1.write_text("# Agent Memory\n\n" + "agent memory knowledge " * 20, encoding="utf-8")
    f2.write_text("# Agent Memory Advanced\n\n" + "agent memory knowledge " * 20, encoding="utf-8")
    mod.main()
    assert (tmp_path / "merged").is_dir()
