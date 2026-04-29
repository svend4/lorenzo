"""
improve_autofill.py — заполняет шаблоны данными из уже сгенерированных скриптов.
Нулевая стоимость ($0), детерминировано.

Требует предварительного запуска:
    improve_contacts.py, improve_tags.py, improve_similar.py, improve_entities.py

Создаёт:
    docs/contacts/  — заполненные contact-outreach.md для каждого автора (15 файлов)

Обновляет:
    docs/05-habr-projects/**/*.md  — добавляет блок ## Статус с тегами/упоминаниями/контактом
    docs/04-ai-collaborations/**/*.md — аналогично

Запуск:
    python scripts/improve_autofill.py
    python scripts/improve_autofill.py --dry-run
"""
import re
import sys
from pathlib import Path
from datetime import date

DRY_RUN = "--dry-run" in sys.argv
ROOT = Path(__file__).parent.parent
DOCS = ROOT / "docs"
TMPL = DOCS / "templates"
TODAY = date.today().isoformat()

# ---------------------------------------------------------------------------
# Парсеры данных из уже сгенерированных файлов
# ---------------------------------------------------------------------------

def parse_contacts() -> list[dict]:
    """Читает таблицу авторов из CONTACTS.md."""
    path = DOCS / "CONTACTS.md"
    if not path.exists():
        print("  ⚠️  CONTACTS.md не найден — запустите improve_contacts.py")
        return []

    text = path.read_text(encoding="utf-8")
    # Ищем строки таблицы: | **Author** | Project | Layer | N | Question |
    rows = []
    for line in text.splitlines():
        m = re.match(
            r'\|\s*\*{0,2}(\w+)\*{0,2}\s*\|'   # Автор
            r'\s*([^|]+)\|'                      # Проект
            r'\s*([^|]+)\|'                      # Слой
            r'\s*(\d+)\s*\|'                     # Упоминаний
            r'\s*(.*?)\s*\|',                    # Вопрос
            line,
        )
        if m and m.group(1).lower() not in ("автор", "---"):
            rows.append({
                "author":    m.group(1).strip(),
                "project":   m.group(2).strip(),
                "layer":     m.group(3).strip(),
                "mentions":  int(m.group(4)),
                "question":  m.group(5).strip() if m.group(5).strip() != "—" else "",
            })
    return rows


def parse_entity_mentions() -> dict[str, int]:
    """Читает счётчик упоминаний проектов из ENTITIES.md."""
    path = DOCS / "ENTITIES.md"
    if not path.exists():
        return {}

    text = path.read_text(encoding="utf-8")
    result: dict[str, int] = {}
    for line in text.splitlines():
        # | **Проект** | 229 | 45 |
        m = re.match(r'\|\s*\*{0,2}([^|*]+?)\*{0,2}\s*\|\s*(\d+)\s*\|\s*(\d+)', line)
        if m:
            result[m.group(1).strip()] = int(m.group(2))
    return result


def parse_tags_per_file() -> dict[str, list[str]]:
    """Читает теги для каждого файла из TAGS.md."""
    path = DOCS / "TAGS.md"
    if not path.exists():
        return {}

    text = path.read_text(encoding="utf-8")
    tags_map: dict[str, list[str]] = {}

    # Структура TAGS.md: ## #tag (N файлов) \n - `path`
    current_tag = ""
    for line in text.splitlines():
        tag_m = re.match(r'##\s*#(\w+)', line)
        if tag_m:
            current_tag = tag_m.group(1)
            continue
        file_m = re.match(r'\s*-\s*`(docs/[^`]+)`', line)
        if file_m and current_tag:
            rel = file_m.group(1)
            tags_map.setdefault(rel, []).append(current_tag)

    return tags_map


def parse_similar_per_file() -> dict[str, list[tuple[str, float]]]:
    """Читает похожие документы из SIMILAR.md."""
    path = DOCS / "SIMILAR.md"
    if not path.exists():
        return {}

    text = path.read_text(encoding="utf-8")
    result: dict[str, list[tuple[str, float]]] = {}

    # Строки таблицы: | 0.667 | `file_a` | `file_b` |
    for line in text.splitlines():
        m = re.match(r'\|\s*([\d.]+)\s*\|\s*`([^`]+)`\s*\|\s*`([^`]+)`', line)
        if m:
            score = float(m.group(1))
            a, b = m.group(2), m.group(3)
            result.setdefault(a, []).append((b, score))
            result.setdefault(b, []).append((a, score))

    return result


# ---------------------------------------------------------------------------
# Генерация contact-outreach.md для каждого автора
# ---------------------------------------------------------------------------

CONTACT_TEMPLATE = """\
# Контакт: {author} / {project}

<!-- summary: Шаблон для связи с автором {project} -->
<!-- tags: контакты, команда -->

## Профиль

| Параметр | Значение |
|----------|---------|
| Ник | **{author}** |
| GitHub | [@{author}](https://github.com/{author}) |
| Проекты | {project} |
| Слой в Svyazi | {layer} |
| Упомянут в документах | {mentions} файлах |
| Платформа | Habr / GitHub |

## Статус связи

- [ ] Изучили профиль
- [ ] Написали первое сообщение
- [ ] Получили ответ
- [ ] Договорились о сотрудничестве

## Первое сообщение

```
Здравствуйте, {author}!

Я изучаю {project} — он отлично вписывается в Svyazi 2.0,
которую я собираю как локальную community intelligence platform.

{project} закрывает слой «{layer}» в архитектуре.{question_block}

Было бы интересно пообщаться — как лучше связаться?
```

## Открытые вопросы

{questions_section}
---
_Создано автоматически: {today}_
"""


def make_contact_file(author: dict) -> str:
    q = author["question"]
    question_block = f"\n\nОдин конкретный вопрос: {q}" if q else ""
    questions_section = f"1. {q}\n2. [Вопрос 2]\n" if q else "1. [Вопрос 1]\n2. [Вопрос 2]\n"

    return CONTACT_TEMPLATE.format(
        author=author["author"],
        project=author["project"],
        layer=author["layer"],
        mentions=author["mentions"],
        question_block=question_block,
        questions_section=questions_section,
        today=TODAY,
    )


def generate_contacts(authors: list[dict]) -> int:
    out_dir = DOCS / "contacts"
    if not DRY_RUN:
        out_dir.mkdir(exist_ok=True)

    created = 0
    for a in authors:
        slug = re.sub(r'[^a-z0-9]', '-', a["author"].lower())
        out_path = out_dir / f"{slug}.md"

        if out_path.exists():
            continue  # не перезаписываем уже заполненные

        content = make_contact_file(a)
        if DRY_RUN:
            print(f"  [dry] создаст {out_path.relative_to(ROOT)}")
        else:
            out_path.write_text(content, encoding="utf-8")
            print(f"  ✅ {out_path.relative_to(ROOT)}")
        created += 1

    return created


# ---------------------------------------------------------------------------
# Добавление блока ## Статус в проектные файлы
# ---------------------------------------------------------------------------

STATUS_MARKER = "<!-- autofill-status -->"

STATUS_TEMPLATE = """\
<!-- autofill-status -->
## Статус

| Параметр | Значение |
|----------|---------|
| Теги | {tags} |
| Упоминаний в репо | {mentions} |
| Слой | {layer} |
| Контакт | {contact_link} |
| Статус связи | не писали |

_Обновлено: {today}_
"""


def find_contact_for_project(project_name: str, authors: list[dict]) -> dict | None:
    """Ищет автора, чей проект содержит project_name."""
    name_lower = project_name.lower()
    for a in authors:
        if name_lower in a["project"].lower():
            return a
    return None


def enrich_project_file(
    md_path: Path,
    tags_map: dict[str, list[str]],
    mentions_map: dict[str, int],
    authors: list[dict],
) -> bool:
    """Добавляет блок ## Статус в файл проекта, если его ещё нет."""
    text = md_path.read_text(encoding="utf-8")
    if STATUS_MARKER in text:
        return False  # уже обработан

    rel_path = str(md_path.relative_to(ROOT)).replace("\\", "/")
    file_tags = tags_map.get(rel_path, [])
    if not file_tags:
        # Пробуем короткий путь (docs/...)
        short = "docs/" + str(md_path.relative_to(DOCS)).replace("\\", "/")
        file_tags = tags_map.get(short, [])

    # Определяем название проекта из заголовка файла
    title_m = re.search(r'^#\s+(.+)', text, re.MULTILINE)
    project_name = title_m.group(1).split("[")[0].split(":")[0].strip() if title_m else md_path.stem

    mentions = mentions_map.get(project_name, 0)
    contact = find_contact_for_project(project_name, authors)

    layer = contact["layer"] if contact else "—"
    if contact:
        slug = re.sub(r'[^a-z0-9]', '-', contact["author"].lower())
        contact_link = f"[@{contact['author']}](docs/contacts/{slug}.md)"
    else:
        contact_link = "—"

    status_block = STATUS_TEMPLATE.format(
        tags=", ".join(f"`{t}`" for t in file_tags) if file_tags else "—",
        mentions=mentions if mentions else "—",
        layer=layer,
        contact_link=contact_link,
        today=TODAY,
    )

    # Вставляем после первого заголовка (и summary-блока если есть)
    insert_after = re.search(r'((?:<!-- summary -->.*?---\s*\n)|(?:^#[^#].*?\n))', text, re.DOTALL)
    if insert_after:
        pos = insert_after.end()
        new_text = text[:pos] + "\n" + status_block + "\n" + text[pos:]
    else:
        new_text = status_block + "\n" + text

    if DRY_RUN:
        print(f"  [dry] обновит {rel_path}")
        return True

    md_path.write_text(new_text, encoding="utf-8")
    print(f"  ✅ {rel_path}")
    return True


def enrich_project_files(
    tags_map: dict[str, list[str]],
    mentions_map: dict[str, int],
    authors: list[dict],
) -> int:
    target_sections = [
        DOCS / "05-habr-projects",
        DOCS / "04-ai-collaborations",
    ]
    updated = 0
    for section in target_sections:
        for md in sorted(section.rglob("*.md")):
            if md.name in ("README.md", "QA.md"):
                continue
            if enrich_project_file(md, tags_map, mentions_map, authors):
                updated += 1
    return updated


# ---------------------------------------------------------------------------
# Точка входа
# ---------------------------------------------------------------------------

def main():
    print("📋 improve_autofill.py — заполнение шаблонов данными")
    if DRY_RUN:
        print("   Режим: dry-run (ничего не записывает)\n")

    print("🔍 Читаем данные из уже сгенерированных файлов...")
    authors  = parse_contacts()
    mentions = parse_entity_mentions()
    tags     = parse_tags_per_file()
    similar  = parse_similar_per_file()

    print(f"   Авторов из CONTACTS.md: {len(authors)}")
    print(f"   Проектов из ENTITIES.md: {len(mentions)}")
    print(f"   Файлов с тегами: {len(tags)}")
    print()

    print("📬 Генерируем contact-outreach.md для каждого автора...")
    n_contacts = generate_contacts(authors)
    print(f"   Создано: {n_contacts} файлов в docs/contacts/\n")

    print("📄 Добавляем блок ## Статус в проектные файлы...")
    n_enriched = enrich_project_files(tags, mentions, authors)
    print(f"   Обновлено: {n_enriched} файлов\n")

    total = n_contacts + n_enriched
    if total == 0:
        print("ℹ️  Все файлы уже обработаны — повторный запуск не нужен.")
    else:
        print(f"✅ Готово: {total} файлов обработано.")
        if not DRY_RUN:
            print("   Следующий шаг: просмотри docs/contacts/ и заполни первые сообщения.")


if __name__ == "__main__":
    main()
