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


# ── _load_full_questions ──────────────────────────────────────────────────────

def test_load_full_questions_with_script(tmp_path, monkeypatch):
    scripts_dir = tmp_path / "scripts"
    scripts_dir.mkdir()
    (scripts_dir / "improve_contacts.py").write_text(
        'FIRST_QUESTIONS = {"kksudo": "Планируете ли поддержку MCP?"}\n',
        encoding="utf-8",
    )
    monkeypatch.setattr(mod, "ROOT", tmp_path)
    result = mod._load_full_questions()
    assert "kksudo" in result


def test_load_full_questions_invalid_script(tmp_path, monkeypatch):
    scripts_dir = tmp_path / "scripts"
    scripts_dir.mkdir()
    (scripts_dir / "improve_contacts.py").write_text(
        "raise RuntimeError('bad script')\n",
        encoding="utf-8",
    )
    monkeypatch.setattr(mod, "ROOT", tmp_path)
    result = mod._load_full_questions()
    assert isinstance(result, dict)


# ── parse_contacts with proper format ─────────────────────────────────────────

def test_parse_contacts_proper_format(tmp_path, monkeypatch):
    (tmp_path / "CONTACTS.md").write_text(
        "| **kksudo** | AgentFS | knowledge/filesystem | 87 | Планируете MCP? |\n"
        "| Автор | Проект | Слой | Упомин | Вопрос |\n",
        encoding="utf-8",
    )
    monkeypatch.setattr(mod, "DOCS", tmp_path)
    monkeypatch.setattr(mod, "ROOT", tmp_path)
    result = mod.parse_contacts()
    assert len(result) >= 1
    assert result[0]["author"] == "kksudo"
    assert result[0]["mentions"] == 87


def test_parse_contacts_em_dash_question(tmp_path, monkeypatch):
    (tmp_path / "CONTACTS.md").write_text(
        "| **kksudo** | AgentFS | knowledge | 87 | — |\n",
        encoding="utf-8",
    )
    monkeypatch.setattr(mod, "DOCS", tmp_path)
    monkeypatch.setattr(mod, "ROOT", tmp_path)
    result = mod.parse_contacts()
    if result:
        assert result[0]["question"] == ""


# ── generate_contacts (DRY_RUN=False) ─────────────────────────────────────────

def test_generate_contacts_creates_file(tmp_path, monkeypatch):
    monkeypatch.setattr(mod, "DOCS", tmp_path)
    monkeypatch.setattr(mod, "ROOT", tmp_path)
    monkeypatch.setattr(mod, "DRY_RUN", False)
    monkeypatch.setattr(mod, "TODAY", "2026-05-12")
    authors = [{"author": "kksudo", "project": "AgentFS", "layer": "knowledge",
                "mentions": 87, "question": "Планируете MCP?"}]
    result = mod.generate_contacts(authors)
    assert result >= 1
    assert (tmp_path / "contacts" / "kksudo.md").exists()


def test_generate_contacts_skips_existing(tmp_path, monkeypatch):
    monkeypatch.setattr(mod, "DOCS", tmp_path)
    monkeypatch.setattr(mod, "ROOT", tmp_path)
    monkeypatch.setattr(mod, "DRY_RUN", False)
    monkeypatch.setattr(mod, "TODAY", "2026-05-12")
    contacts_dir = tmp_path / "contacts"
    contacts_dir.mkdir()
    (contacts_dir / "kksudo.md").write_text("# existing", encoding="utf-8")
    authors = [{"author": "kksudo", "project": "AgentFS", "layer": "knowledge",
                "mentions": 87, "question": "Test?"}]
    result = mod.generate_contacts(authors)
    assert result == 0  # skipped existing


# ── enrich_project_file ────────────────────────────────────────────────────────

def test_enrich_project_file_adds_status(tmp_path, monkeypatch):
    monkeypatch.setattr(mod, "ROOT", tmp_path)
    monkeypatch.setattr(mod, "DOCS", tmp_path)
    monkeypatch.setattr(mod, "DRY_RUN", False)
    monkeypatch.setattr(mod, "TODAY", "2026-05-12")
    md_file = tmp_path / "agentfs.md"
    md_file.write_text("# AgentFS\n\nContent about agent file system.", encoding="utf-8")
    result = mod.enrich_project_file(md_file, {}, {}, [])
    assert result is True
    text = md_file.read_text(encoding="utf-8")
    assert "autofill-status" in text


def test_enrich_project_file_skips_already_enriched(tmp_path, monkeypatch):
    monkeypatch.setattr(mod, "ROOT", tmp_path)
    monkeypatch.setattr(mod, "DOCS", tmp_path)
    monkeypatch.setattr(mod, "DRY_RUN", False)
    md_file = tmp_path / "already.md"
    md_file.write_text("# Doc\n\n<!-- autofill-status -->\ncontent", encoding="utf-8")
    result = mod.enrich_project_file(md_file, {}, {}, [])
    assert result is False


def test_enrich_project_file_dry_run(tmp_path, monkeypatch):
    monkeypatch.setattr(mod, "ROOT", tmp_path)
    monkeypatch.setattr(mod, "DOCS", tmp_path)
    monkeypatch.setattr(mod, "DRY_RUN", True)
    monkeypatch.setattr(mod, "TODAY", "2026-05-12")
    md_file = tmp_path / "agent.md"
    md_file.write_text("# AgentFS\n\nContent.", encoding="utf-8")
    result = mod.enrich_project_file(md_file, {}, {}, [])
    assert result is True
    text = md_file.read_text(encoding="utf-8")
    assert "autofill-status" not in text  # not written in dry_run


def test_enrich_project_file_with_contact(tmp_path, monkeypatch):
    monkeypatch.setattr(mod, "ROOT", tmp_path)
    monkeypatch.setattr(mod, "DOCS", tmp_path)
    monkeypatch.setattr(mod, "DRY_RUN", False)
    monkeypatch.setattr(mod, "TODAY", "2026-05-12")
    md_file = tmp_path / "agentfs.md"
    md_file.write_text("# AgentFS\n\nContent.", encoding="utf-8")
    authors = [{"author": "kksudo", "project": "AgentFS", "layer": "knowledge",
                "mentions": 87, "question": "Test?"}]
    result = mod.enrich_project_file(md_file, {}, {"AgentFS": 87}, authors)
    assert result is True


# ── enrich_project_files ──────────────────────────────────────────────────────

def test_enrich_project_files_with_files(tmp_path, monkeypatch):
    monkeypatch.setattr(mod, "DOCS", tmp_path)
    monkeypatch.setattr(mod, "ROOT", tmp_path)
    monkeypatch.setattr(mod, "DRY_RUN", False)
    monkeypatch.setattr(mod, "TODAY", "2026-05-12")
    habr_dir = tmp_path / "05-habr-projects"
    habr_dir.mkdir()
    (habr_dir / "project.md").write_text("# TestProject\n\nContent.", encoding="utf-8")
    result = mod.enrich_project_files({}, {}, [])
    assert result >= 1


# ── main() with real data ──────────────────────────────────────────────────────

def test_main_non_dry_run_with_contacts(tmp_path, monkeypatch):
    monkeypatch.setattr(mod, "DOCS", tmp_path)
    monkeypatch.setattr(mod, "ROOT", tmp_path)
    monkeypatch.setattr(mod, "DRY_RUN", False)
    monkeypatch.setattr(mod, "TODAY", "2026-05-12")
    (tmp_path / "CONTACTS.md").write_text(
        "| **kksudo** | AgentFS | knowledge | 87 | Test question? |\n",
        encoding="utf-8",
    )
    habr_dir = tmp_path / "05-habr-projects"
    habr_dir.mkdir()
    (habr_dir / "agentfs.md").write_text("# AgentFS\n\nContent.", encoding="utf-8")
    mod.main()
    assert (tmp_path / "contacts").exists()


def test_main_all_already_processed(tmp_path, monkeypatch, capsys):
    monkeypatch.setattr(mod, "DOCS", tmp_path)
    monkeypatch.setattr(mod, "ROOT", tmp_path)
    monkeypatch.setattr(mod, "DRY_RUN", False)
    monkeypatch.setattr(mod, "TODAY", "2026-05-12")
    mod.main()
    out = capsys.readouterr().out
    assert "обработаны" in out or "Готово" in out


def test_generate_contacts_dry_run_print(tmp_path, monkeypatch, capsys):
    """Line 232: dry-run print in generate_contacts when file doesn't exist."""
    monkeypatch.setattr(mod, "DOCS", tmp_path)
    monkeypatch.setattr(mod, "ROOT", tmp_path)
    monkeypatch.setattr(mod, "DRY_RUN", True)
    monkeypatch.setattr(mod, "TODAY", "2026-05-12")
    authors = [{"author": "kksudo", "project": "AgentFS", "layer": "knowledge",
                "mentions": 87, "question": "Test?"}]
    result = mod.generate_contacts(authors)
    assert result == 1
    out = capsys.readouterr().out
    assert "dry" in out or "kksudo" in out


def test_enrich_project_file_no_header(tmp_path, monkeypatch):
    """Line 320: else branch when no H1 header found in file."""
    monkeypatch.setattr(mod, "ROOT", tmp_path)
    monkeypatch.setattr(mod, "DOCS", tmp_path)
    monkeypatch.setattr(mod, "DRY_RUN", False)
    monkeypatch.setattr(mod, "TODAY", "2026-05-12")
    md_file = tmp_path / "noheader.md"
    md_file.write_text("Just some content without a heading.", encoding="utf-8")
    result = mod.enrich_project_file(md_file, {}, {}, [])
    assert result is True


def test_enrich_project_files_skips_readme(tmp_path, monkeypatch):
    """Line 344: continue when file is README.md."""
    monkeypatch.setattr(mod, "DOCS", tmp_path)
    monkeypatch.setattr(mod, "ROOT", tmp_path)
    monkeypatch.setattr(mod, "DRY_RUN", False)
    monkeypatch.setattr(mod, "TODAY", "2026-05-12")
    habr_dir = tmp_path / "05-habr-projects"
    habr_dir.mkdir()
    (habr_dir / "README.md").write_text("# README\n\nIndex.", encoding="utf-8")
    (habr_dir / "project.md").write_text("# TestProject\n\nContent.", encoding="utf-8")
    result = mod.enrich_project_files({}, {}, [])
    assert result == 1  # only project.md, not README.md
