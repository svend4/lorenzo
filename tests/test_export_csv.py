"""
Тесты для scripts/improve_export_csv.py.

Покрытие:
  - get_title()     — H1-заголовок или имя файла
  - get_tags()      — тег из <!-- tags: ... -->
  - get_summary()   — первая строка блока <!-- summary -->
  - get_projects()  — упомянутые проекты из PROJECTS
  - has_risk()      — наличие слов риска
  - has_action()    — наличие слов действия
  - get_section()   — раздел из пути файла
"""

import importlib
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(ROOT / "scripts"))

mod = importlib.import_module("improve_export_csv")

# ── get_title ─────────────────────────────────────────────────────────────────

def test_get_title_from_h1():
    text = "# Yodoca — система памяти\n\nСодержимое файла."
    result = mod.get_title(text, Path("yodoca.md"))
    assert result == "Yodoca — система памяти"


def test_get_title_fallback_to_filename():
    text = "Нет заголовка h1 в этом тексте."
    result = mod.get_title(text, Path("agentfs.md"))
    assert result == "agentfs"


def test_get_title_truncates_at_80():
    long_title = "# " + "A" * 100
    result = mod.get_title(long_title, Path("x.md"))
    assert len(result) <= 80


def test_get_title_strips_whitespace():
    text = "#   Заголовок с пробелами   \n\nТекст."
    result = mod.get_title(text, Path("x.md"))
    assert result == "Заголовок с пробелами"


def test_get_title_returns_string():
    result = mod.get_title("no heading", Path("file.md"))
    assert isinstance(result, str)


def test_get_title_ignores_h2():
    text = "## Это H2, не H1\n\nТекст."
    result = mod.get_title(text, Path("doc.md"))
    assert result == "doc"  # fallback

# ── get_tags ──────────────────────────────────────────────────────────────────

def test_get_tags_found():
    text = "<!-- tags: memory, agent, mcp -->\n# Doc"
    result = mod.get_tags(text)
    assert "memory" in result
    assert "agent" in result


def test_get_tags_empty_when_absent():
    text = "# Doc\n\nNo tags here."
    result = mod.get_tags(text)
    assert result == ""


def test_get_tags_returns_string():
    result = mod.get_tags("some text")
    assert isinstance(result, str)


def test_get_tags_strips_whitespace():
    text = "<!--  tags:  memory, agent  -->"
    result = mod.get_tags(text)
    assert result == result.strip()

# ── get_summary ───────────────────────────────────────────────────────────────

def test_get_summary_found():
    text = "<!-- summary -->\n> Краткое описание проекта Yodoca.\n\n# Title"
    result = mod.get_summary(text)
    assert "Yodoca" in result


def test_get_summary_empty_when_absent():
    text = "# Title\n\nNo summary block here."
    result = mod.get_summary(text)
    assert result == ""


def test_get_summary_truncates_at_200():
    long_text = "<!-- summary -->\n> " + "X" * 300 + "\n# Title"
    result = mod.get_summary(long_text)
    assert len(result) <= 200


def test_get_summary_returns_string():
    result = mod.get_summary("no summary")
    assert isinstance(result, str)

# ── get_projects ──────────────────────────────────────────────────────────────

def test_get_projects_finds_known_projects():
    text = "Проекты Yodoca и AgentFS используются в Svyazi."
    result = mod.get_projects(text)
    assert "Yodoca" in result
    assert "AgentFS" in result


def test_get_projects_empty_when_none_mentioned():
    text = "Никаких известных проектов здесь нет."
    result = mod.get_projects(text)
    assert result == ""


def test_get_projects_case_insensitive():
    text = "YODOCA и agentfs упоминаются в тексте."
    result = mod.get_projects(text)
    assert "Yodoca" in result


def test_get_projects_separator():
    text = "Используются Yodoca и AgentFS и Rufler."
    result = mod.get_projects(text)
    assert "; " in result  # projects joined by "; "


def test_get_projects_returns_string():
    result = mod.get_projects("random text")
    assert isinstance(result, str)

# ── has_risk ──────────────────────────────────────────────────────────────────

def test_has_risk_да():
    text = "Существуют серьёзные риски при интеграции."
    assert mod.has_risk(text) == "да"


def test_has_risk_нет():
    text = "Всё работает отлично, проблем нет."
    assert mod.has_risk(text) == "нет"


def test_has_risk_english_keyword():
    text = "There is a potential risk in the architecture."
    assert mod.has_risk(text) == "да"


def test_has_risk_returns_string():
    result = mod.has_risk("some text")
    assert isinstance(result, str)
    assert result in ("да", "нет")

# ── has_action ────────────────────────────────────────────────────────────────

def test_has_action_да():
    text = "Следующий шаг: написать авторам проектов."
    assert mod.has_action(text) == "да"


def test_has_action_нет():
    text = "Это просто описание без призывов к действию."
    assert mod.has_action(text) == "нет"


def test_has_action_mvp_keyword():
    text = "MVP должен быть готов к июню 2026."
    assert mod.has_action(text) == "да"


def test_has_action_returns_string():
    result = mod.has_action("text")
    assert isinstance(result, str)
    assert result in ("да", "нет")

# ── get_section ───────────────────────────────────────────────────────────────

def test_get_section_first_part(monkeypatch, tmp_path):
    monkeypatch.setattr(mod, "DOCS", tmp_path)
    path = tmp_path / "01-svyazi" / "component.md"
    result = mod.get_section(path)
    assert result == "01-svyazi"


def test_get_section_nested(monkeypatch, tmp_path):
    monkeypatch.setattr(mod, "DOCS", tmp_path)
    path = tmp_path / "05-habr-projects" / "memory" / "yodoca.md"
    result = mod.get_section(path)
    assert result == "05-habr-projects"


def test_get_section_root_file(monkeypatch, tmp_path):
    monkeypatch.setattr(mod, "DOCS", tmp_path)
    path = tmp_path / "HEALTH.md"
    result = mod.get_section(path)
    assert result == "HEALTH.md"


def test_get_section_returns_string(monkeypatch, tmp_path):
    monkeypatch.setattr(mod, "DOCS", tmp_path)
    path = tmp_path / "some" / "file.md"
    result = mod.get_section(path)
    assert isinstance(result, str)


# ── main ──────────────────────────────────────────────────────────────────────

def test_main_creates_export_csv(tmp_path, monkeypatch):
    monkeypatch.setattr(mod, "DOCS", tmp_path)
    monkeypatch.setattr(mod, "ROOT", tmp_path)
    mod.main()
    assert (tmp_path / "export.csv").exists()


def test_main_export_csv_has_content(tmp_path, monkeypatch):
    monkeypatch.setattr(mod, "DOCS", tmp_path)
    monkeypatch.setattr(mod, "ROOT", tmp_path)
    (tmp_path / "doc.md").write_text("# AgentFS\n\nContent here.", encoding="utf-8")
    mod.main()
    text = (tmp_path / "export.csv").read_text(encoding="utf-8")
    assert len(text) > 0


def test_main_empty_docs(tmp_path, monkeypatch):
    monkeypatch.setattr(mod, "DOCS", tmp_path)
    monkeypatch.setattr(mod, "ROOT", tmp_path)
    mod.main()
    assert (tmp_path / "export.csv").exists()
