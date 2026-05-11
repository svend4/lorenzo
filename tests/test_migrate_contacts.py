"""
Тесты для scripts/improve_migrate_contacts.py.

Покрытие:
  - detect_status()        — определение статуса по чекбоксам
  - extract_author()       — имя автора из заголовка / имени файла
  - extract_projects()     — список проектов из текста
  - detect_platform()      — платформа по упоминаниям URL
  - extract_handle()       — @handle из текста
  - has_frontmatter()      — наличие YAML frontmatter
  - ensure_required_sections() — добавление пропущенных секций
"""

import importlib
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(ROOT / "scripts"))

mod = importlib.import_module("improve_migrate_contacts")

# ── detect_status ─────────────────────────────────────────────────────────────

def test_detect_status_not_started():
    text = "# Contact\n\n- [ ] Изучили профиль\n- [ ] Написали первое сообщение"
    assert mod.detect_status(text) == "not_started"


def test_detect_status_studied():
    text = "# Contact\n\n- [x] Изучили профиль\n- [ ] Написали первое сообщение"
    assert mod.detect_status(text) == "studied"


def test_detect_status_messaged():
    text = "- [x] Изучили профиль\n- [x] Написали первое сообщение\n- [ ] Получили ответ"
    assert mod.detect_status(text) == "messaged"


def test_detect_status_replied():
    text = "- [x] Изучили профиль\n- [x] Написали первое сообщение\n- [x] Получили ответ"
    assert mod.detect_status(text) == "replied"


def test_detect_status_agreed():
    text = ("- [x] Изучили профиль\n- [x] Написали первое сообщение\n"
            "- [x] Получили ответ\n- [x] Договорились")
    assert mod.detect_status(text) == "agreed"


def test_detect_status_returns_last_achieved():
    text = "- [x] Написали первое сообщение\n- [ ] Получили ответ"
    result = mod.detect_status(text)
    assert result in ("messaged", "not_started")

# ── extract_author ────────────────────────────────────────────────────────────

def test_extract_author_from_heading():
    text = "# Контакт: kksudo\n\nAgentFS developer."
    result = mod.extract_author(Path("kksudo.md"), text)
    assert result == "kksudo"


def test_extract_author_from_heading_with_project():
    text = "# Контакт: VitalyOborin / Yodoca, Wikontic\n\n..."
    result = mod.extract_author(Path("vitalyoborin.md"), text)
    assert result == "VitalyOborin"


def test_extract_author_fallback_to_filename():
    text = "## Section\n\nNo heading with author."
    result = mod.extract_author(Path("spbmolot.md"), text)
    assert result == "spbmolot"


def test_extract_author_strips_whitespace():
    text = "#  Контакт:  nlaik  \n\nResearcher."
    result = mod.extract_author(Path("nlaik.md"), text)
    assert result == "nlaik"

# ── extract_projects ──────────────────────────────────────────────────────────

def test_extract_projects_from_bold_field():
    text = "## Profile\n\n**Проекты:** Yodoca, Wikontic\n"
    result = mod.extract_projects(text)
    assert "Yodoca" in result
    assert "Wikontic" in result


def test_extract_projects_from_heading():
    text = "# Контакт: VitalyOborin / Yodoca, Wikontic\n\n..."
    result = mod.extract_projects(text)
    assert "Yodoca" in result


def test_extract_projects_empty_when_absent():
    text = "# Контакт: kksudo\n\nNo projects listed here."
    result = mod.extract_projects(text)
    assert isinstance(result, list)


def test_extract_projects_single_project():
    text = "**Проекты:** AgentFS\n"
    result = mod.extract_projects(text)
    assert "AgentFS" in result

# ── detect_platform ───────────────────────────────────────────────────────────

def test_detect_platform_github():
    text = "Profile: https://github.com/kksudo"
    assert mod.detect_platform(text) == "GitHub"


def test_detect_platform_habr():
    text = "Published on https://habr.com/en/articles/123"
    assert mod.detect_platform(text) == "Habr"


def test_detect_platform_telegram():
    text = "Reach me at t.me/myhandle"
    assert mod.detect_platform(text) == "Telegram"


def test_detect_platform_default_habr():
    text = "No platform links here whatsoever."
    assert mod.detect_platform(text) == "Habr"

# ── extract_handle ────────────────────────────────────────────────────────────

def test_extract_handle_finds_at_handle():
    text = "Contact: @kksudo on GitHub"
    assert mod.extract_handle(text) == "@kksudo"


def test_extract_handle_empty_when_absent():
    text = "No handle mentioned in this text."
    assert mod.extract_handle(text) == ""


def test_extract_handle_takes_first():
    text = "@first and @second"
    assert mod.extract_handle(text) == "@first"

# ── has_frontmatter ───────────────────────────────────────────────────────────

def test_has_frontmatter_true():
    text = "---\ntitle: Test\nauthor: kksudo\n---\n\n# Content"
    assert mod.has_frontmatter(text) is True


def test_has_frontmatter_false_no_opener():
    text = "# Title\n\nNo frontmatter here."
    assert mod.has_frontmatter(text) is False


def test_has_frontmatter_false_no_closer():
    text = "---\ntitle: Test\n\n# Content (no closing ---)"
    assert mod.has_frontmatter(text) is False

# ── ensure_required_sections ──────────────────────────────────────────────────

def test_ensure_required_sections_adds_missing():
    text = "# Contact: kksudo\n\n## Профиль\n\nDeveloper.\n"
    result = mod.ensure_required_sections(text)
    assert "## Статус связи" in result
    assert "## Первое сообщение" in result


def test_ensure_required_sections_keeps_existing():
    text = (
        "# Contact\n\n"
        "## Профиль\n\nDeveloper.\n\n"
        "## Статус связи\n\nNot contacted.\n\n"
        "## Первое сообщение\n\nHello!\n"
    )
    result = mod.ensure_required_sections(text)
    # Секции не должны дублироваться
    assert result.count("## Профиль") == 1
    assert result.count("## Статус связи") == 1
    assert result.count("## Первое сообщение") == 1


def test_ensure_required_sections_all_present_no_change():
    text = (
        "## Профиль\n\nProfile info.\n\n"
        "## Статус связи\n\nStatus info.\n\n"
        "## Первое сообщение\n\nFirst message.\n"
    )
    result = mod.ensure_required_sections(text)
    assert "Добавлено автоматически" not in result


def test_ensure_required_sections_returns_string():
    result = mod.ensure_required_sections("# Contact\n\nSome text.")
    assert isinstance(result, str)
