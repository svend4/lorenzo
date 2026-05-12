"""Tests for scripts/improve_llm_summary.py."""

import importlib
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(ROOT / "scripts"))

mod = importlib.import_module("improve_llm_summary")


def test_map_prompt_constant():
    assert hasattr(mod, "MAP_PROMPT")
    assert isinstance(mod.MAP_PROMPT, str)
    assert "{chunk}" in mod.MAP_PROMPT


def test_reduce_prompt_constant():
    assert hasattr(mod, "REDUCE_PROMPT")
    assert isinstance(mod.REDUCE_PROMPT, str)
    assert "{title}" in mod.REDUCE_PROMPT
    assert "{summaries}" in mod.REDUCE_PROMPT


def test_min_words_constant():
    assert hasattr(mod, "MIN_WORDS")
    assert isinstance(mod.MIN_WORDS, int)
    assert mod.MIN_WORDS > 0


def test_dry_run_attribute():
    assert hasattr(mod, "DRY_RUN")
    assert isinstance(mod.DRY_RUN, bool)


def test_today_attribute():
    assert hasattr(mod, "TODAY")
    assert isinstance(mod.TODAY, str)
    assert len(mod.TODAY) == 10


def test_model_attribute():
    assert hasattr(mod, "MODEL")
    assert isinstance(mod.MODEL, str)
    assert "claude" in mod.MODEL.lower()


def test_docs_path_attribute():
    assert hasattr(mod, "DOCS")
    assert isinstance(mod.DOCS, Path)


def test_map_prompt_has_instructions():
    # Should instruct about summarization
    assert "суммари" in mod.MAP_PROMPT.lower() or "summary" in mod.MAP_PROMPT.lower() or "кратко" in mod.MAP_PROMPT.lower()


def test_reduce_prompt_has_format():
    # Should have format instructions
    assert "Markdown" in mod.REDUCE_PROMPT or "markdown" in mod.REDUCE_PROMPT.lower()


def test_min_words_reasonable():
    # Should be between 100 and 1000
    assert 100 <= mod.MIN_WORDS <= 1000


# ── main ──────────────────────────────────────────────────────────────────────

def test_main_dry_run_no_crash(tmp_path, monkeypatch):
    monkeypatch.setattr(mod, "DOCS", tmp_path)
    monkeypatch.setattr(mod, "ROOT", tmp_path)
    monkeypatch.setattr(mod, "DRY_RUN", True)
    monkeypatch.setattr(mod, "SECTION_FILTER", None)
    monkeypatch.setattr(mod, "DIGEST_PATH", tmp_path / "DIGEST.md")
    mod.main()


def test_main_dry_run_with_file(tmp_path, monkeypatch):
    doc = tmp_path / "doc.md"
    doc.write_text("# AgentFS\n\n" + "Content. " * 30, encoding="utf-8")
    monkeypatch.setattr(mod, "DOCS", tmp_path)
    monkeypatch.setattr(mod, "ROOT", tmp_path)
    monkeypatch.setattr(mod, "DRY_RUN", True)
    monkeypatch.setattr(mod, "SECTION_FILTER", None)
    monkeypatch.setattr(mod, "DIGEST_PATH", tmp_path / "DIGEST.md")
    mod.main()


def test_collect_targets_empty_dir(tmp_path, monkeypatch):
    monkeypatch.setattr(mod, "DOCS", tmp_path)
    monkeypatch.setattr(mod, "FILE_FILTER", None)
    monkeypatch.setattr(mod, "SECTION_FILTER", None)
    result = mod.collect_targets()
    assert isinstance(result, list)


def test_collect_targets_with_file_filter(tmp_path, monkeypatch):
    f = tmp_path / "doc.md"
    f.write_text("# Title\n\n" + "word " * 300, encoding="utf-8")
    monkeypatch.setattr(mod, "DOCS", tmp_path)
    monkeypatch.setattr(mod, "FILE_FILTER", f)
    result = mod.collect_targets()
    assert f in result


def test_collect_targets_file_filter_missing(tmp_path, monkeypatch):
    monkeypatch.setattr(mod, "DOCS", tmp_path)
    monkeypatch.setattr(mod, "FILE_FILTER", tmp_path / "nonexistent.md")
    result = mod.collect_targets()
    assert result == []


def test_load_digest_missing_file(tmp_path, monkeypatch):
    monkeypatch.setattr(mod, "DIGEST_PATH", tmp_path / "nonexistent.md")
    result = mod.load_digest()
    assert result == {}


def test_load_digest_with_existing(tmp_path, monkeypatch):
    digest = tmp_path / "DIGEST.md"
    digest.write_text(
        "## Title\n_Файл: [doc.md](doc.md)_\n\nContent.\n",
        encoding="utf-8"
    )
    monkeypatch.setattr(mod, "DIGEST_PATH", digest)
    result = mod.load_digest()
    assert "doc.md" in result


def test_append_to_digest_creates_file(tmp_path, monkeypatch):
    digest = tmp_path / "DIGEST.md"
    monkeypatch.setattr(mod, "DIGEST_PATH", digest)
    mod.append_to_digest("## New Section\n\nContent.\n")
    assert digest.exists()
    assert "New Section" in digest.read_text(encoding="utf-8")
