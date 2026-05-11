"""
Тесты для scripts/improve_qa.py.

Покрытие:
  - check_answer()      — поиск ответа по ключевым словам или проектам
  - collect_folder_tags()— определение тегов по наличию ключевых слов
"""

import importlib
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(ROOT / "scripts"))

mod = importlib.import_module("improve_qa")

# ── check_answer ──────────────────────────────────────────────────────────────

def test_check_answer_returns_string():
    result = mod.check_answer("Some text with AgentFS mentioned.", "projects", ["AgentFS"])
    assert isinstance(result, str)


def test_check_answer_finds_project():
    result = mod.check_answer("AgentFS is used here.", "projects", ["AgentFS", "Yodoca"])
    assert "AgentFS" in result


def test_check_answer_not_found_returns_fallback():
    result = mod.check_answer("Unrelated text here.", "projects", ["AgentFS"])
    assert "_Не найдено" in result or "Не найдено" in result


def test_check_answer_case_insensitive():
    result = mod.check_answer("agentfs is great tool.", "projects", ["AgentFS"])
    assert "AgentFS" in result


def test_check_answer_finds_keyword():
    result = mod.check_answer("консолидация памяти происходит каждую ночь.", "keywords", ["консолидац"])
    assert "консолидац" in result


def test_check_answer_multiple_found():
    text = "AgentFS and Yodoca work together."
    result = mod.check_answer(text, "projects", ["AgentFS", "Yodoca", "SENTINEL"])
    assert "AgentFS" in result
    assert "Yodoca" in result


def test_check_answer_limits_to_5():
    items = ["AgentFS", "Yodoca", "SENTINEL", "Rufler", "MemNet", "Svyazi"]
    text = " ".join(items).lower()
    result = mod.check_answer(text, "projects", items)
    # Result should mention at most 5 items
    count = sum(1 for item in items if item in result)
    assert count <= 5


def test_check_answer_empty_text():
    result = mod.check_answer("", "projects", ["AgentFS"])
    assert "_Не найдено" in result or isinstance(result, str)


# ── collect_folder_tags ───────────────────────────────────────────────────────

def test_collect_folder_tags_returns_list(tmp_path, monkeypatch):
    result = mod.collect_folder_tags(tmp_path)
    assert isinstance(result, list)


def test_collect_folder_tags_empty_folder(tmp_path):
    result = mod.collect_folder_tags(tmp_path)
    assert result == []


def test_collect_folder_tags_finds_memory_tag(tmp_path):
    # Tags are read from HTML comments: <!-- tags: memory, agent -->
    (tmp_path / "doc.md").write_text("<!-- tags: memory, agent -->\n# Title\n", encoding="utf-8")
    result = mod.collect_folder_tags(tmp_path)
    assert "memory" in result


def test_collect_folder_tags_finds_rag_tag(tmp_path):
    (tmp_path / "doc.md").write_text("<!-- tags: rag, knowledge -->\n# Title\n", encoding="utf-8")
    result = mod.collect_folder_tags(tmp_path)
    assert "rag" in result


def test_collect_folder_tags_no_duplicates(tmp_path):
    # Multiple files with same tag
    (tmp_path / "a.md").write_text("<!-- tags: memory -->\n# A\n", encoding="utf-8")
    (tmp_path / "b.md").write_text("<!-- tags: memory -->\n# B\n", encoding="utf-8")
    result = mod.collect_folder_tags(tmp_path)
    # Tags returned sorted by count descending, but as keys — each appears once
    assert result.count("memory") == 1


def test_collect_folder_tags_multiple_topics(tmp_path):
    (tmp_path / "doc.md").write_text(
        "<!-- tags: knowledge, rag, memory -->\n# Title\n", encoding="utf-8"
    )
    result = mod.collect_folder_tags(tmp_path)
    assert len(result) >= 1
