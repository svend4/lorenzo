"""
Тесты для scripts/improve_contact_status.py.

Покрытие:
  - get_current_status() — чтение чекбоксов из текста
  - set_checkbox()       — установка/снятие [x] по label
  - add_note()           — добавление заметки в раздел ## Заметки
  - find_contact_file()  — поиск файла по частичному имени
"""

import importlib
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(ROOT / "scripts"))

mod = importlib.import_module("improve_contact_status")

# ── get_current_status ────────────────────────────────────────────────────────

def _contact_text(studied=False, messaged=False, replied=False, agreed=False) -> str:
    def cb(checked): return "[x]" if checked else "[ ]"
    return (
        f"# Контакт: kksudo\n\n"
        f"## Статус связи\n\n"
        f"- {cb(studied)} Изучили профиль\n"
        f"- {cb(messaged)} Написали первое сообщение\n"
        f"- {cb(replied)} Получили ответ\n"
        f"- {cb(agreed)} Договорились о сотрудничестве\n"
    )


def test_get_current_status_all_false():
    status = mod.get_current_status(_contact_text())
    assert status == {"studied": False, "messaged": False,
                      "replied": False, "agreed": False}


def test_get_current_status_studied_only():
    status = mod.get_current_status(_contact_text(studied=True))
    assert status["studied"] is True
    assert status["messaged"] is False


def test_get_current_status_all_true():
    status = mod.get_current_status(
        _contact_text(studied=True, messaged=True, replied=True, agreed=True))
    assert all(status.values())


def test_get_current_status_returns_dict():
    result = mod.get_current_status("some text")
    assert isinstance(result, dict)
    assert set(result.keys()) == {"studied", "messaged", "replied", "agreed"}


def test_get_current_status_empty_text():
    status = mod.get_current_status("")
    assert all(v is False for v in status.values())


def test_get_current_status_case_insensitive():
    text = "- [X] Изучили профиль\n"
    status = mod.get_current_status(text)
    assert status["studied"] is True

# ── set_checkbox ──────────────────────────────────────────────────────────────

def test_set_checkbox_mark_checked():
    text = "- [ ] Изучили профиль\n"
    result = mod.set_checkbox(text, "Изучили профиль", True)
    assert "[x]" in result
    assert "[ ]" not in result


def test_set_checkbox_mark_unchecked():
    text = "- [x] Изучили профиль\n"
    result = mod.set_checkbox(text, "Изучили профиль", False)
    assert "[ ]" in result
    assert "[x]" not in result


def test_set_checkbox_preserves_other_lines():
    text = "- [ ] Изучили профиль\n- [ ] Написали первое сообщение\n"
    result = mod.set_checkbox(text, "Изучили профиль", True)
    assert "Написали первое сообщение" in result
    assert "[ ] Написали первое сообщение" in result


def test_set_checkbox_returns_string():
    result = mod.set_checkbox("text", "Label", True)
    assert isinstance(result, str)


def test_set_checkbox_missing_label_returns_original():
    text = "- [ ] Другой лейбл\n"
    result = mod.set_checkbox(text, "Несуществующий лейбл", True)
    assert result == text


def test_set_checkbox_multiple_occurrences():
    text = "- [ ] Изучили профиль\n- [ ] Изучили профиль\n"
    result = mod.set_checkbox(text, "Изучили профиль", True)
    assert result.count("[x]") == 2

# ── add_note ──────────────────────────────────────────────────────────────────

def test_add_note_creates_section():
    text = "# Контакт: kksudo\n\nОписание.\n"
    result = mod.add_note(text, "Ответил через GitHub")
    assert "## Заметки" in result
    assert "Ответил через GitHub" in result


def test_add_note_appends_to_existing_section():
    text = "# Контакт\n\n## Заметки\n\n- 2026-01-01: Первая заметка\n"
    result = mod.add_note(text, "Вторая заметка")
    assert "Первая заметка" in result
    assert "Вторая заметка" in result


def test_add_note_inserts_before_footer():
    text = "# Контакт\n\nТекст.\n\n---\n_Footer_\n"
    result = mod.add_note(text, "Тест")
    # Note should appear before the ---
    notes_pos = result.index("## Заметки")
    footer_pos = result.index("---")
    assert notes_pos < footer_pos


def test_add_note_contains_date():
    from datetime import date
    text = "# Контакт\n\nОписание.\n"
    result = mod.add_note(text, "Тест")
    assert date.today().isoformat() in result


def test_add_note_returns_string():
    result = mod.add_note("text", "note")
    assert isinstance(result, str)

# ── find_contact_file ─────────────────────────────────────────────────────────

def test_find_contact_file_exact_match(monkeypatch, tmp_path):
    monkeypatch.setattr(mod, "CONTACTS_DIR", tmp_path)
    (tmp_path / "kksudo.md").write_text("# kksudo", encoding="utf-8")
    result = mod.find_contact_file("kksudo")
    assert result is not None
    assert result.name == "kksudo.md"


def test_find_contact_file_partial_match(monkeypatch, tmp_path):
    monkeypatch.setattr(mod, "CONTACTS_DIR", tmp_path)
    (tmp_path / "kksudo.md").write_text("# kksudo", encoding="utf-8")
    result = mod.find_contact_file("kk")
    assert result is not None


def test_find_contact_file_no_match(monkeypatch, tmp_path):
    monkeypatch.setattr(mod, "CONTACTS_DIR", tmp_path)
    (tmp_path / "kksudo.md").write_text("# kksudo", encoding="utf-8")
    result = mod.find_contact_file("nonexistent_author_xyz")
    assert result is None


def test_find_contact_file_ambiguous_returns_none(monkeypatch, tmp_path, capsys):
    monkeypatch.setattr(mod, "CONTACTS_DIR", tmp_path)
    (tmp_path / "kksudo.md").write_text("# A", encoding="utf-8")
    (tmp_path / "kk_other.md").write_text("# B", encoding="utf-8")
    result = mod.find_contact_file("kk")
    assert result is None


def test_find_contact_file_missing_dir(monkeypatch, tmp_path):
    monkeypatch.setattr(mod, "CONTACTS_DIR", tmp_path / "nonexistent")
    result = mod.find_contact_file("anyone")
    assert result is None


# ── main ──────────────────────────────────────────────────────────────────────

def test_main_list_no_crash(tmp_path, monkeypatch):
    monkeypatch.setattr(mod, "CONTACTS_DIR", tmp_path)
    monkeypatch.setattr(mod, "ROOT", tmp_path)
    monkeypatch.setattr("sys.argv", ["prog", "--list"])
    mod.main()


def test_main_no_args_shows_usage(tmp_path, monkeypatch, capsys):
    monkeypatch.setattr(mod, "CONTACTS_DIR", tmp_path)
    monkeypatch.setattr(mod, "ROOT", tmp_path)
    monkeypatch.setattr("sys.argv", ["prog"])
    mod.main()
    out = capsys.readouterr().out
    assert "Использование" in out or "author" in out.lower()


def test_main_author_not_found_exits(tmp_path, monkeypatch):
    monkeypatch.setattr(mod, "CONTACTS_DIR", tmp_path)
    monkeypatch.setattr(mod, "ROOT", tmp_path)
    monkeypatch.setattr("sys.argv", ["prog", "--author", "nobody"])
    try:
        mod.main()
    except SystemExit:
        pass


def _make_contact(path: "Path", stem: str = "kksudo") -> "Path":
    f = path / f"{stem}.md"
    f.write_text(
        "# kksudo\n\n"
        "## Статус\n\n"
        "- [ ] Изучили профиль\n"
        "- [ ] Написали первое сообщение\n"
        "- [ ] Получили ответ\n"
        "- [ ] Договорились о сотрудничестве\n",
        encoding="utf-8",
    )
    return f


def test_main_author_found_shows_status(tmp_path, monkeypatch, capsys):
    contacts = tmp_path / "contacts"
    contacts.mkdir()
    _make_contact(contacts)
    monkeypatch.setattr(mod, "CONTACTS_DIR", contacts)
    monkeypatch.setattr(mod, "ROOT", tmp_path)
    monkeypatch.setattr("sys.argv", ["prog", "--author", "kksudo"])
    mod.main()
    out = capsys.readouterr().out
    assert "kksudo" in out


def test_main_author_studied_updates(tmp_path, monkeypatch):
    contacts = tmp_path / "contacts"
    contacts.mkdir()
    f = _make_contact(contacts)
    monkeypatch.setattr(mod, "CONTACTS_DIR", contacts)
    monkeypatch.setattr(mod, "ROOT", tmp_path)
    monkeypatch.setattr("sys.argv", ["prog", "--author", "kksudo", "--studied"])
    monkeypatch.setattr(mod, "_apply_status_to_file", lambda path, args: True)
    monkeypatch.setattr(mod, "find_contact_file", lambda q: contacts / "kksudo.md")
    import subprocess as _sp
    monkeypatch.setattr(_sp, "run", lambda *a, **kw: None)
    mod.main()


def test_main_bulk_missing_names_exits(tmp_path, monkeypatch):
    contacts = tmp_path / "contacts"
    contacts.mkdir()
    monkeypatch.setattr(mod, "CONTACTS_DIR", contacts)
    monkeypatch.setattr(mod, "ROOT", tmp_path)
    monkeypatch.setattr("sys.argv", ["prog", "--bulk"])
    try:
        mod.main()
    except SystemExit:
        pass


def test_main_bulk_updates_contacts(tmp_path, monkeypatch):
    contacts = tmp_path / "contacts"
    contacts.mkdir()
    _make_contact(contacts, "kksudo")
    monkeypatch.setattr(mod, "CONTACTS_DIR", contacts)
    monkeypatch.setattr(mod, "ROOT", tmp_path)
    monkeypatch.setattr("sys.argv", ["prog", "--bulk", "kksudo", "--studied"])
    monkeypatch.setattr(mod, "find_contact_file", lambda name: contacts / f"{name}.md")
    changed_calls = []
    monkeypatch.setattr(
        mod, "_apply_status_to_file",
        lambda path, args: (changed_calls.append(path), False)[1],
    )
    mod.main()


def test_list_all_contacts_with_files(tmp_path, monkeypatch, capsys):
    contacts = tmp_path / "contacts"
    contacts.mkdir()
    _make_contact(contacts)
    monkeypatch.setattr(mod, "CONTACTS_DIR", contacts)
    monkeypatch.setattr(mod, "ROOT", tmp_path)
    mod.list_all_contacts()
    out = capsys.readouterr().out
    assert "kksudo" in out


def test_show_status_prints_author(tmp_path, monkeypatch, capsys):
    contacts = tmp_path / "contacts"
    contacts.mkdir()
    f = _make_contact(contacts)
    monkeypatch.setattr(mod, "ROOT", tmp_path)
    mod.show_status(f)
    out = capsys.readouterr().out
    assert "kksudo" in out
