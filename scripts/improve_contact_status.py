"""
improve_contact_status.py — обновляет статус контакта в docs/contacts/<slug>.md.
Удобная альтернатива ручному редактированию файла.

Использование:
    python scripts/improve_contact_status.py --list
    python scripts/improve_contact_status.py --author kksudo --studied
    python scripts/improve_contact_status.py --author kksudo --messaged
    python scripts/improve_contact_status.py --author kksudo --replied
    python scripts/improve_contact_status.py --author kksudo --agreed
    python scripts/improve_contact_status.py --author kksudo --note "Ответил через LinkedIn"

Поддерживает частичное имя: --author kk ищет kksudo если он единственный совпадающий.
"""
import re
import sys
from pathlib import Path
from datetime import date

ROOT = Path(__file__).parent.parent
CONTACTS_DIR = ROOT / "docs" / "contacts"
TODAY = date.today().isoformat()

CHECKBOXES = {
    "studied":  "Изучили профиль",
    "messaged": "Написали первое сообщение",
    "replied":  "Получили ответ",
    "agreed":   "Договорились о сотрудничестве",
}


def find_contact_file(author_query: str) -> Path | None:
    """Ищет файл контакта по неполному имени автора."""
    if not CONTACTS_DIR.exists():
        return None

    query = author_query.lower()
    candidates = [f for f in CONTACTS_DIR.glob("*.md") if query in f.stem.lower()]

    if len(candidates) == 1:
        return candidates[0]
    if len(candidates) > 1:
        names = [f.stem for f in candidates]
        print(f"❓ Несколько совпадений: {', '.join(names)} — уточните имя")
        return None
    return None


def get_current_status(text: str) -> dict[str, bool]:
    """Читает текущий статус чекбоксов из текста файла."""
    status = {}
    for key, label in CHECKBOXES.items():
        checked = bool(re.search(rf'\[x\].*{re.escape(label)}', text, re.IGNORECASE))
        status[key] = checked
    return status


def set_checkbox(text: str, label: str, checked: bool) -> str:
    """Ставит [x] или [ ] для строки с данным label."""
    mark = "[x]" if checked else "[ ]"
    pattern = rf'(\[[ x]\])(\s*{re.escape(label)})'
    replacement = rf'{mark}\2'
    new_text, count = re.subn(pattern, replacement, text, flags=re.IGNORECASE)
    if count == 0:
        print(f"  ⚠️  Строка '{label}' не найдена в файле")
    return new_text


def add_note(text: str, note: str) -> str:
    """Добавляет запись в раздел заметок (создаёт если нет)."""
    note_line = f"- {TODAY}: {note}"

    if "## Заметки" in text:
        return text.replace("## Заметки\n", f"## Заметки\n{note_line}\n")

    # Создаём раздел заметок перед последней строкой
    footer_match = re.search(r'\n---\n', text)
    if footer_match:
        pos = footer_match.start()
        return text[:pos] + f"\n## Заметки\n\n{note_line}\n" + text[pos:]

    return text + f"\n## Заметки\n\n{note_line}\n"


def show_status(path: Path) -> None:
    """Печатает текущий статус контакта."""
    text = path.read_text(encoding="utf-8")
    status = get_current_status(text)

    author = path.stem
    print(f"\n📋 Контакт: {author}")
    print(f"   Файл: {path.relative_to(ROOT)}")
    print()

    marks = {True: "✅", False: "⬜"}
    for key, label in CHECKBOXES.items():
        print(f"   {marks[status[key]]} {label}")

    # Показываем заметки если есть
    if "## Заметки" in text:
        notes_m = re.search(r'## Заметки\n\n(.+?)(?:\n##|\Z)', text, re.DOTALL)
        if notes_m:
            print(f"\n   Заметки:\n{notes_m.group(1).rstrip()}")
    print()


def list_all_contacts() -> None:
    """Показывает сводную таблицу всех контактов."""
    if not CONTACTS_DIR.exists():
        print("❌ docs/contacts/ не найден — запустите improve_autofill.py")
        return

    files = sorted([f for f in CONTACTS_DIR.glob("*.md") if f.name != "README.md"])
    if not files:
        print("❌ Нет файлов в docs/contacts/")
        return

    print(f"\n📋 Контакты ({len(files)} авторов):\n")
    header = f"{'Автор':<20} {'Изучен':<8} {'Написали':<10} {'Ответили':<10} {'Договор':<8}"
    print(header)
    print("-" * len(header))

    for f in files:
        text = f.read_text(encoding="utf-8")
        st = get_current_status(text)
        marks = {True: "✅", False: "⬜"}
        print(f"{f.stem:<20} {marks[st['studied']]:<8} {marks[st['messaged']]:<10} "
              f"{marks[st['replied']]:<10} {marks[st['agreed']]:<8}")

    print()


def main() -> None:
    args = sys.argv[1:]

    if not args or "--list" in args:
        list_all_contacts()
        if "--list" in args:
            return
        print("Использование: python scripts/improve_contact_status.py --author <имя> --<статус>")
        print("Флаги статуса: --studied | --messaged | --replied | --agreed")
        print("Заметка: --note 'текст'")
        return

    if "--author" not in args:
        print("❌ Укажите --author <имя>")
        sys.exit(1)

    idx = args.index("--author")
    if idx + 1 >= len(args):
        print("❌ После --author нужно имя автора")
        sys.exit(1)

    author_query = args[idx + 1]
    path = find_contact_file(author_query)

    if path is None:
        # Попробовать точный совпадение через слаг
        slug = re.sub(r'[^a-z0-9]', '-', author_query.lower())
        direct = CONTACTS_DIR / f"{slug}.md"
        if direct.exists():
            path = direct
        else:
            print(f"❌ Контакт '{author_query}' не найден в {CONTACTS_DIR.relative_to(ROOT)}/")
            print("   Список: python scripts/improve_contact_status.py --list")
            sys.exit(1)

    text = path.read_text(encoding="utf-8")

    changed = False

    # Обновляем статусы
    for key, label in CHECKBOXES.items():
        if f"--{key}" in args:
            old_status = get_current_status(text)
            text = set_checkbox(text, label, True)
            print(f"  ✅ Отмечено: {label}")
            changed = True

    # Добавляем заметку
    if "--note" in args:
        note_idx = args.index("--note")
        if note_idx + 1 < len(args):
            note = args[note_idx + 1]
            text = add_note(text, note)
            print(f"  📝 Заметка добавлена: {note}")
            changed = True

    if changed:
        path.write_text(text, encoding="utf-8")
        print(f"\n✅ {path.relative_to(ROOT)} обновлён")

        # Синхронизируем прогресс автоматически
        import subprocess
        sync_script = ROOT / "scripts" / "improve_progress_sync.py"
        if sync_script.exists():
            subprocess.run([sys.executable, str(sync_script)], cwd=ROOT,
                           capture_output=True)
            print("   PROGRESS.md синхронизирован")
    else:
        # Если флагов статуса нет — показываем текущий статус
        show_status(path)


if __name__ == "__main__":
    main()
