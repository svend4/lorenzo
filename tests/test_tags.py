"""
Тесты для scripts/improve_tags.py.

Покрытие:
  - detect_tags() — обнаружение тем по ключевым словам
  - tag_file()    — добавление строки тегов в файл
"""

import importlib
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(ROOT / "scripts"))

mod = importlib.import_module("improve_tags")

# ── detect_tags ───────────────────────────────────────────────────────────────

def test_detect_tags_returns_list():
    result = mod.detect_tags("Some text about memory and agents.")
    assert isinstance(result, list)


def test_detect_tags_finds_memory_topic():
    text = "Yodoca handles memory consolidation and forgetting mechanisms."
    result = mod.detect_tags(text)
    assert "memory" in result


def test_detect_tags_finds_rag_topic():
    text = "LiteParse is a RAG system for retrieval."
    result = mod.detect_tags(text)
    assert "rag" in result


def test_detect_tags_finds_security_topic():
    text = "SENTINEL provides PII protection and allowlist filtering."
    result = mod.detect_tags(text)
    assert "security" in result


def test_detect_tags_finds_knowledge_topic():
    text = "AgentFS uses a vault-based knowledge-space for cards."
    result = mod.detect_tags(text)
    assert "knowledge" in result


def test_detect_tags_empty_text():
    result = mod.detect_tags("")
    assert result == []


def test_detect_tags_no_matching_topics():
    result = mod.detect_tags("слово слово слово другое слово")
    assert result == []


def test_detect_tags_case_insensitive():
    text = "YODOCA handles MEMORY consolidation."
    result = mod.detect_tags(text)
    assert "memory" in result


def test_detect_tags_multiple_topics():
    text = "Rufler orchestration system uses YAML for agent swarm configuration."
    result = mod.detect_tags(text)
    assert "orchestration" in result


# ── tag_file ──────────────────────────────────────────────────────────────────

def test_tag_file_returns_list(tmp_path):
    f = tmp_path / "doc.md"
    f.write_text("# Title\n\nYodoca handles memory consolidation.", encoding="utf-8")
    result = mod.tag_file(f)
    assert isinstance(result, list)


_MEMORY_TEXT = ("# Title\n\nYodoca handles memory consolidation and forgetting "
                "mechanisms for episodic agents in the knowledge system.\n")


def test_tag_file_returns_tags_when_found(tmp_path):
    f = tmp_path / "doc.md"
    f.write_text(_MEMORY_TEXT, encoding="utf-8")
    result = mod.tag_file(f)
    assert len(result) > 0


def test_tag_file_writes_tag_line(tmp_path):
    f = tmp_path / "doc.md"
    f.write_text(_MEMORY_TEXT, encoding="utf-8")
    mod.tag_file(f)
    content = f.read_text(encoding="utf-8")
    assert mod.ALREADY_TAGGED in content


def test_tag_file_idempotent(tmp_path):
    f = tmp_path / "doc.md"
    f.write_text(_MEMORY_TEXT, encoding="utf-8")
    first = mod.tag_file(f)
    second = mod.tag_file(f)
    assert second == []  # Already tagged → no-op


def test_tag_file_skips_short_files(tmp_path):
    f = tmp_path / "short.md"
    f.write_text("# Short", encoding="utf-8")
    result = mod.tag_file(f)
    assert result == []


def test_tag_file_empty_when_no_topics(tmp_path):
    f = tmp_path / "doc.md"
    f.write_text("# Title\n\nJust generic text with nothing specific to tag.", encoding="utf-8")
    result = mod.tag_file(f)
    # No tags detected → nothing written, empty result
    assert result == []


# ── main ──────────────────────────────────────────────────────────────────────

def test_main_creates_tags_md(tmp_path, monkeypatch):
    monkeypatch.setattr(mod, "DOCS", tmp_path)
    monkeypatch.setattr(mod, "ROOT", tmp_path)
    (tmp_path / "doc.md").write_text("# Title\n\nContent.", encoding="utf-8")
    mod.main()
    assert (tmp_path / "TAGS.md").exists()


def test_main_empty_docs_no_crash(tmp_path, monkeypatch):
    monkeypatch.setattr(mod, "DOCS", tmp_path)
    monkeypatch.setattr(mod, "ROOT", tmp_path)
    mod.main()
    assert (tmp_path / "TAGS.md").exists()
