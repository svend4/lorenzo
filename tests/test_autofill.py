"""
Тесты для scripts/improve_autofill.py.

Покрытие:
  - parse_entity_mentions()   — счётчик упоминаний из ENTITIES.md
  - parse_tags_per_file()     — теги на файл из TAGS.md
  - parse_similar_per_file()  — похожие документы из SIMILAR.md
  - make_contact_file()       — генерация contact-outreach.md
  - find_contact_for_project() — поиск контакта по имени проекта
"""

import importlib
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(ROOT / "scripts"))

mod = importlib.import_module("improve_autofill")

# ── parse_entity_mentions ─────────────────────────────────────────────────────

def test_parse_entity_mentions_returns_dict():
    result = mod.parse_entity_mentions()
    assert isinstance(result, dict)


def test_parse_entity_mentions_positive_counts():
    result = mod.parse_entity_mentions()
    if result:
        for val in result.values():
            assert isinstance(val, int)
            assert val >= 0


def test_parse_entity_mentions_known_project(monkeypatch, tmp_path):
    fake_entities = tmp_path / "ENTITIES.md"
    fake_entities.write_text(
        "| **Svyazi** | 229 | 45 |\n"
        "| **AgentFS** | 87 | 12 |\n",
        encoding="utf-8",
    )
    monkeypatch.setattr(mod, "DOCS", tmp_path)
    result = mod.parse_entity_mentions()
    assert "Svyazi" in result
    assert result["Svyazi"] == 229
    assert result["AgentFS"] == 87

# ── parse_tags_per_file ───────────────────────────────────────────────────────

def test_parse_tags_per_file_returns_dict():
    result = mod.parse_tags_per_file()
    assert isinstance(result, dict)


def test_parse_tags_per_file_values_are_lists():
    result = mod.parse_tags_per_file()
    for val in result.values():
        assert isinstance(val, list)


def test_parse_tags_per_file_parses_correctly(monkeypatch, tmp_path):
    fake_tags = tmp_path / "TAGS.md"
    fake_tags.write_text(
        "## #memory\n\n- `docs/05-habr-projects/memory/yodoca.md`\n"
        "- `docs/05-habr-projects/memory/ngt-memory.md`\n\n"
        "## #agent\n\n- `docs/05-habr-projects/memory/yodoca.md`\n",
        encoding="utf-8",
    )
    monkeypatch.setattr(mod, "DOCS", tmp_path)
    result = mod.parse_tags_per_file()
    yodoca_key = "docs/05-habr-projects/memory/yodoca.md"
    assert yodoca_key in result
    assert "memory" in result[yodoca_key]
    assert "agent" in result[yodoca_key]

# ── parse_similar_per_file ────────────────────────────────────────────────────

def test_parse_similar_per_file_returns_dict():
    result = mod.parse_similar_per_file()
    assert isinstance(result, dict)


def test_parse_similar_per_file_values_are_lists():
    result = mod.parse_similar_per_file()
    for val in result.values():
        assert isinstance(val, list)
        for item in val:
            assert len(item) == 2   # (path, score)
            assert isinstance(item[1], float)


def test_parse_similar_per_file_symmetric(monkeypatch, tmp_path):
    fake_similar = tmp_path / "SIMILAR.md"
    fake_similar.write_text(
        "| 0.750 | `docs/a.md` | `docs/b.md` |\n"
        "| 0.500 | `docs/a.md` | `docs/c.md` |\n",
        encoding="utf-8",
    )
    monkeypatch.setattr(mod, "DOCS", tmp_path)
    result = mod.parse_similar_per_file()
    assert "docs/a.md" in result
    assert "docs/b.md" in result   # симметрично
    paths_for_a = [p for p, _ in result["docs/a.md"]]
    assert "docs/b.md" in paths_for_a

# ── make_contact_file ─────────────────────────────────────────────────────────

def _sample_author(**kwargs):
    defaults = {
        "author": "kksudo",
        "project": "AgentFS",
        "layer": "knowledge/filesystem",
        "mentions": 87,
        "question": "Планируется ли поддержка MCP?",
    }
    defaults.update(kwargs)
    return defaults


def test_make_contact_file_returns_string():
    result = mod.make_contact_file(_sample_author())
    assert isinstance(result, str)


def test_make_contact_file_contains_author():
    result = mod.make_contact_file(_sample_author())
    assert "kksudo" in result


def test_make_contact_file_contains_project():
    result = mod.make_contact_file(_sample_author())
    assert "AgentFS" in result


def test_make_contact_file_contains_required_sections():
    result = mod.make_contact_file(_sample_author())
    assert "## Профиль" in result
    assert "## Статус связи" in result
    assert "## Первое сообщение" in result


def test_make_contact_file_contains_question():
    result = mod.make_contact_file(_sample_author(question="Как использовать?"))
    assert "Как использовать?" in result


def test_make_contact_file_no_question_block():
    result = mod.make_contact_file(_sample_author(question=""))
    assert isinstance(result, str)
    assert "AgentFS" in result

# ── find_contact_for_project ──────────────────────────────────────────────────

def test_find_contact_for_project_finds_exact():
    authors = [
        {"author": "kksudo",    "project": "AgentFS", "layer": "x", "mentions": 1, "question": ""},
        {"author": "spbmolot",  "project": "NGT Memory", "layer": "y", "mentions": 2, "question": ""},
    ]
    result = mod.find_contact_for_project("AgentFS", authors)
    assert result is not None
    assert result["author"] == "kksudo"


def test_find_contact_for_project_case_insensitive():
    authors = [{"author": "kksudo", "project": "AgentFS", "layer": "x", "mentions": 1, "question": ""}]
    result = mod.find_contact_for_project("agentfs", authors)
    assert result is not None


def test_find_contact_for_project_returns_none_if_missing():
    authors = [{"author": "kksudo", "project": "AgentFS", "layer": "x", "mentions": 1, "question": ""}]
    result = mod.find_contact_for_project("NonExistentProject", authors)
    assert result is None


def test_find_contact_for_project_empty_list():
    assert mod.find_contact_for_project("AgentFS", []) is None


# ── main ──────────────────────────────────────────────────────────────────────

def test_main_dry_run_no_crash(tmp_path, monkeypatch):
    monkeypatch.setattr(mod, "DOCS", tmp_path)
    monkeypatch.setattr(mod, "ROOT", tmp_path)
    monkeypatch.setattr(mod, "DRY_RUN", True)
    mod.main()  # empty CONTACTS.md / ENTITIES.md → must not raise


def test_main_with_contacts_md(tmp_path, monkeypatch):
    monkeypatch.setattr(mod, "DOCS", tmp_path)
    monkeypatch.setattr(mod, "ROOT", tmp_path)
    monkeypatch.setattr(mod, "DRY_RUN", True)
    (tmp_path / "CONTACTS.md").write_text(
        "| Автор | Проект | Слой | Файл |\n"
        "|-------|--------|------|------|\n"
        "| kksudo | AgentFS | knowledge | docs/agentfs.md |\n",
        encoding="utf-8"
    )
    mod.main()  # must not raise


def test_main_empty_docs_no_crash(tmp_path, monkeypatch):
    monkeypatch.setattr(mod, "DOCS", tmp_path)
    monkeypatch.setattr(mod, "ROOT", tmp_path)
    monkeypatch.setattr(mod, "DRY_RUN", True)
    mod.main()  # must not raise
