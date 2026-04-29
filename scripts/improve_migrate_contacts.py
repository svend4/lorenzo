"""
improve_migrate_contacts.py — миграция docs/contacts/*.md на frontmatter contact-outreach.

Парсит существующие контакты (без frontmatter) и добавляет YAML-frontmatter
с извлечёнными полями: author, projects, статус, платформа.

Использование:
    python scripts/improve_migrate_contacts.py --dry-run
    python scripts/improve_migrate_contacts.py --apply
"""
import re
import sys
from datetime import date
from pathlib import Path

ROOT = Path(__file__).parent.parent
CONTACTS = ROOT / "docs" / "contacts"

CHECKBOXES = {
    "studied": r"\[x\].*Изучили профиль",
    "messaged": r"\[x\].*Написали первое сообщение",
    "replied": r"\[x\].*Получили ответ",
    "agreed": r"\[x\].*Договорились",
}


def detect_status(text: str) -> str:
    """Определяет последний достигнутый статус по чекбоксам."""
    last = "not_started"
    for status_key in ["studied", "messaged", "replied", "agreed"]:
        if re.search(CHECKBOXES[status_key], text, re.IGNORECASE):
            last = status_key
    return last


def extract_author(file_path: Path, text: str) -> str:
    """Имя автора: из заголовка # Контакт: <author> / ... либо из имени файла."""
    m = re.search(r'^#\s+(?:Контакт:\s+)?([^/\n]+?)(?:\s*/|\s*$)', text, re.MULTILINE)
    if m:
        return m.group(1).strip()
    return file_path.stem


def extract_projects(text: str) -> list[str]:
    """Список проектов: из строки **Проекты:** ... или из заголовка."""
    m = re.search(r'\*\*Проекты:\*\*\s*(.+)', text)
    if m:
        raw = m.group(1).strip()
        return [p.strip() for p in raw.split(',') if p.strip()]
    # Из заголовка "Контакт: Author / proj1, proj2"
    m = re.search(r'^#\s+Контакт:\s+[^/]+/\s*(.+)$', text, re.MULTILINE)
    if m:
        return [p.strip() for p in m.group(1).split(',') if p.strip()]
    return []


def detect_platform(text: str) -> str:
    """Платформа: ищем github.com / habr.com / t.me."""
    if "github.com" in text or "@" in text and "github" in text.lower():
        return "GitHub"
    if "habr.com" in text:
        return "Habr"
    if "t.me/" in text or "telegram" in text.lower():
        return "Telegram"
    return "Habr"  # default для Lorenzo


def extract_handle(text: str) -> str:
    """@handle из ссылки или текста."""
    m = re.search(r'@([\w-]+)', text)
    return f"@{m.group(1)}" if m else ""


def has_frontmatter(text: str) -> bool:
    return text.startswith('---\n') and '\n---\n' in text[3:]


def build_frontmatter(file_path: Path, text: str) -> str:
    author = extract_author(file_path, text)
    projects = extract_projects(text)
    status = detect_status(text)
    platform = detect_platform(text)
    handle = extract_handle(text)

    projects_yaml = "[" + ", ".join(f'"{p}"' for p in projects) + "]" if projects else "[]"
    handle_yaml = f'"{handle}"' if handle else 'null'

    fm = [
        '---',
        'template: contact-outreach',
        'version: "1.0"',
        f'author: "{author}"',
        f'author_handle: {handle_yaml}',
        f'projects: {projects_yaml}',
        f'platform: {platform}',
        f'status: {status}',
        'priority: 3',
        f'created: {date.today().isoformat()}',
        'last_contact: null',
        'tags: [контакты, команда]',
        '---',
        '',
    ]
    return '\n'.join(fm)


def ensure_required_sections(text: str) -> str:
    """Добавляет отсутствующие required-секции с плейсхолдерами."""
    required = ["Профиль", "Статус связи", "Первое сообщение"]
    for section in required:
        if not re.search(rf'^##\s+{re.escape(section)}', text, re.MULTILINE):
            # Добавляем секцию перед первым ---  или в конец
            placeholder = f"\n## {section}\n\n_Добавлено автоматически при миграции, заполните данные._\n"
            footer_match = re.search(r'\n---\n_Создано', text)
            if footer_match:
                pos = footer_match.start()
                text = text[:pos] + placeholder + text[pos:]
            else:
                text += placeholder
    return text


def main():
    args = sys.argv[1:]
    apply = '--apply' in args

    if not CONTACTS.exists():
        print(f"❌ {CONTACTS} не найден")
        return 1

    files = sorted(f for f in CONTACTS.glob('*.md') if f.name != 'README.md')
    migrated = 0
    skipped = 0

    for f in files:
        text = f.read_text(encoding='utf-8')

        if has_frontmatter(text):
            skipped += 1
            print(f"  [skip] {f.name} — уже с frontmatter")
            continue

        fm = build_frontmatter(f, text)
        new_text = ensure_required_sections(text)
        new_text = fm + new_text

        if not apply:
            print(f"  [dry] {f.name}: добавим frontmatter (author={extract_author(f, text)!r}, status={detect_status(text)})")
        else:
            f.write_text(new_text, encoding='utf-8')
            print(f"  [migrated] {f.name}")
        migrated += 1

    print(f"\nИтого: {migrated} мигрировано, {skipped} пропущено")
    if not apply and migrated:
        print("→ Запустите с --apply чтобы применить.")
    return 0


if __name__ == '__main__':
    sys.exit(main())
