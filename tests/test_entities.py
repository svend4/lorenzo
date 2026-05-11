"""
Тесты для scripts/improve_entities.py.

Покрытие:
  - find_github_urls() — извлечение GitHub URL из текста
  - count_entity()     — подсчёт упоминаний сущности в тексте
  - build_counts()     — сводная таблица упоминаний по всем текстам
  - table()            — форматирование строк Markdown-таблицы
"""

import importlib
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(ROOT / "scripts"))

mod = importlib.import_module("improve_entities")

# ── find_github_urls ──────────────────────────────────────────────────────────

def test_find_github_urls_returns_list():
    result = mod.find_github_urls("Some text here.")
    assert isinstance(result, list)


def test_find_github_urls_finds_basic_url():
    text = "See https://github.com/user/repo for details."
    result = mod.find_github_urls(text)
    assert "https://github.com/user/repo" in result


def test_find_github_urls_deduplicates():
    text = "https://github.com/user/repo and https://github.com/user/repo again"
    result = mod.find_github_urls(text)
    assert result.count("https://github.com/user/repo") == 1


def test_find_github_urls_empty_text():
    assert mod.find_github_urls("") == []


def test_find_github_urls_no_github():
    text = "See https://example.com or https://gitlab.com/user/repo"
    result = mod.find_github_urls(text)
    assert result == []


def test_find_github_urls_multiple_repos():
    text = ("Check https://github.com/alpha/alpha-repo and "
            "https://github.com/beta/beta-repo here.")
    result = mod.find_github_urls(text)
    assert len(result) == 2


# ── count_entity ──────────────────────────────────────────────────────────────

def test_count_entity_returns_int():
    result = mod.count_entity("AgentFS is great. AgentFS is here.", "AgentFS")
    assert isinstance(result, int)


def test_count_entity_counts_correctly():
    text = "AgentFS is great. AgentFS is here. AgentFS once more."
    result = mod.count_entity(text, "AgentFS")
    assert result == 3


def test_count_entity_case_insensitive():
    text = "AgentFS and agentfs and AGENTFS"
    result = mod.count_entity(text, "AgentFS")
    assert result == 3


def test_count_entity_zero_when_not_found():
    result = mod.count_entity("Hello world", "AgentFS")
    assert result == 0


def test_count_entity_empty_text():
    result = mod.count_entity("", "AgentFS")
    assert result == 0


def test_count_entity_single_occurrence():
    result = mod.count_entity("I use AgentFS for knowledge.", "AgentFS")
    assert result == 1


# ── build_counts ──────────────────────────────────────────────────────────────

def test_build_counts_returns_list():
    texts = {"file1.md": "AgentFS is great."}
    result = mod.build_counts(["AgentFS"], texts)
    assert isinstance(result, list)


def test_build_counts_tuple_structure():
    texts = {"file1.md": "AgentFS is used here."}
    result = mod.build_counts(["AgentFS"], texts)
    assert len(result) == 1
    ent, total, files = result[0]
    assert ent == "AgentFS"
    assert isinstance(total, int)
    assert isinstance(files, int)


def test_build_counts_correct_totals():
    texts = {
        "a.md": "AgentFS AgentFS here",
        "b.md": "AgentFS once",
    }
    result = mod.build_counts(["AgentFS"], texts)
    _, total, file_count = result[0]
    assert total == 3
    assert file_count == 2


def test_build_counts_skips_zero_mentions():
    texts = {"file.md": "No matches here at all."}
    result = mod.build_counts(["AgentFS"], texts)
    assert result == []


def test_build_counts_sorted_by_total_descending():
    texts = {"f.md": "AgentFS AgentFS AgentFS Yodoca"}
    result = mod.build_counts(["AgentFS", "Yodoca"], texts)
    totals = [r[1] for r in result]
    assert totals == sorted(totals, reverse=True)


def test_build_counts_empty_entity_list():
    texts = {"f.md": "Some text."}
    result = mod.build_counts([], texts)
    assert result == []


def test_build_counts_empty_texts():
    result = mod.build_counts(["AgentFS"], {})
    assert result == []


