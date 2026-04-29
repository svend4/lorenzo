"""
improve_llm_contact.py — генерирует персонализированное первое сообщение автору через LLM.

Читает:
  - docs/contacts/<author>.md — профиль и черновик сообщения
  - docs/05-habr-projects/**/<project>.md — детали проекта
  - docs/CONTACTS.md — слой архитектуры

Создаёт обогащённый вариант первого сообщения с конкретными техническими деталями.

Требует: pip install anthropic
Запуск:
    python scripts/improve_llm_contact.py --author kksudo
    python scripts/improve_llm_contact.py --author kksudo --dry-run
    python scripts/improve_llm_contact.py --all   # все авторы без ответа
"""
import re
import sys
import time
from pathlib import Path
from datetime import date

ROOT = Path(__file__).parent.parent
DOCS = ROOT / "docs"
TODAY = date.today().isoformat()

DRY_RUN = "--dry-run" in sys.argv
ALL_MODE = "--all"     in sys.argv

AUTHOR = None
if "--author" in sys.argv:
    idx = sys.argv.index("--author")
    if idx + 1 < len(sys.argv):
        AUTHOR = sys.argv[idx + 1]

MODEL = "claude-haiku-4-5-20251001"


def _find_contact_file(author_query: str) -> Path | None:
    query = author_query.lower()
    candidates = [f for f in (DOCS / "contacts").glob("*.md")
                  if query in f.stem.lower()]
    if len(candidates) == 1:
        return candidates[0]
    slug = re.sub(r'[^a-z0-9]', '-', query)
    direct = DOCS / "contacts" / f"{slug}.md"
    return direct if direct.exists() else None


def _find_project_file(project_name: str) -> Path | None:
    """Ищет файл проекта по имени."""
    project_lower = project_name.lower().split()[0]  # первое слово
    for f in DOCS.rglob("*.md"):
        if project_lower in f.stem.lower() and "contacts" not in str(f):
            return f
    return None


def _contact_is_messaged(path: Path) -> bool:
    text = path.read_text(encoding="utf-8")
    return bool(re.search(r'\[x\].*Написали первое сообщение', text, re.IGNORECASE))


def build_prompt(contact_path: Path, project_path: Path | None) -> str:
    contact_text = contact_path.read_text(encoding="utf-8")

    project_excerpt = ""
    if project_path and project_path.exists():
        proj_text = project_path.read_text(encoding="utf-8")
        # Берём первые 2000 символов
        clean = re.sub(r'<!--.*?-->', '', proj_text, flags=re.DOTALL)
        project_excerpt = clean[:2000]

    # Извлекаем текущий черновик сообщения из контактного файла
    draft_m = re.search(r'```\n(Здравствуйте.+?)```', contact_text, re.DOTALL)
    current_draft = draft_m.group(1).strip() if draft_m else ""

    # Извлекаем вопрос
    question_m = re.search(r'## Открытые вопросы\n\n(.+?)(?:\n##|\Z)', contact_text, re.DOTALL)
    questions = question_m.group(1).strip() if question_m else ""

    return f"""\
Ты помогаешь написать первое сообщение автору открытого проекта для потенциального сотрудничества.

**Контекст:**
Svyazi 2.0 — локальная community intelligence platform, которая объединяет лучшие OSS-проекты
в единую архитектуру Knowledge OS. Проект автора — важный компонент этой архитектуры.

**Профиль автора (из базы знаний):**
{contact_text[:800]}

**Детали проекта:**
{project_excerpt or "— нет дополнительных данных —"}

**Текущий черновик сообщения:**
{current_draft or "— черновик не найден —"}

**Открытые вопросы:**
{questions or "— нет вопросов —"}

---

Улучши сообщение:
1. Добавь конкретные технические детали из проекта (версия, стек, особенности)
2. Покажи что реально изучил проект (упомяни специфическую особенность)
3. Объясни конкретно как проект закрывает нужный слой в Svyazi 2.0
4. Один конкретный технический вопрос (не общий "как связаться")
5. Объём: 5-8 предложений, деловой но не формальный тон

Выведи ТОЛЬКО текст улучшенного сообщения, без объяснений.
"""


ENRICHED_MARKER = "<!-- llm-contact-draft -->"


def enrich_contact(contact_path: Path, client) -> bool:
    """Генерирует улучшенное сообщение и вставляет в файл."""
    text = contact_path.read_text(encoding="utf-8")

    # Ищем проект автора для дополнительного контекста
    proj_m = re.search(r'\|\s*Проекты\s*\|\s*([^|]+)\|', text)
    project_name = proj_m.group(1).strip() if proj_m else ""
    project_path = _find_project_file(project_name) if project_name else None

    prompt = build_prompt(contact_path, project_path)

    if DRY_RUN:
        tokens = len(prompt.split()) * 1.3
        print(f"  [dry] {contact_path.stem}: ~{tokens:.0f} токенов, проект={project_name or '—'}")
        return True

    resp = client.messages.create(
        model=MODEL,
        max_tokens=500,
        messages=[{"role": "user", "content": prompt}],
    )
    improved_message = resp.content[0].text.strip()

    # Вставляем улучшенное сообщение после блока кода с черновиком
    llm_block = (
        f"\n{ENRICHED_MARKER}\n"
        f"## Улучшенное сообщение (LLM, {TODAY})\n\n"
        f"```\n{improved_message}\n```\n"
    )

    if ENRICHED_MARKER in text:
        # Обновляем существующий блок
        new_text = re.sub(
            rf'{re.escape(ENRICHED_MARKER)}.*?(?=\n##|\Z)',
            llm_block.strip(),
            text, flags=re.DOTALL
        )
    else:
        # Вставляем после блока "## Первое сообщение"
        insert_after = re.search(r'(## Первое сообщение.*?```\n)', text, re.DOTALL)
        if insert_after:
            pos = insert_after.end()
            new_text = text[:pos] + llm_block + text[pos:]
        else:
            new_text = text + llm_block

    contact_path.write_text(new_text, encoding="utf-8")
    print(f"  ✅ {contact_path.stem}: улучшенное сообщение записано")
    return True


def _get_all_authors_no_reply() -> list[Path]:
    contacts_dir = DOCS / "contacts"
    result = []
    for f in sorted(contacts_dir.glob("*.md")):
        if f.name == "README.md":
            continue
        if not _contact_is_messaged(f):
            result.append(f)
    return result


def main() -> None:
    print("✍️  improve_llm_contact.py — генерация персонализированных сообщений")
    print(f"   Модель: {MODEL}")
    if DRY_RUN:
        print("   Режим: dry-run\n")

    targets: list[Path] = []

    if AUTHOR:
        path = _find_contact_file(AUTHOR)
        if not path:
            print(f"❌ Контакт '{AUTHOR}' не найден")
            sys.exit(1)
        targets = [path]
    elif ALL_MODE:
        targets = _get_all_authors_no_reply()
        print(f"   Авторов без ответа: {len(targets)}\n")
    else:
        print("❌ Укажите --author <имя> или --all")
        print("   Пример: python scripts/improve_llm_contact.py --author kksudo")
        sys.exit(1)

    if DRY_RUN:
        for p in targets:
            build_prompt_info = f"{p.stem}"
            print(f"  [dry] обработает: {build_prompt_info}")
        # Оценка стоимости
        n = len(targets)
        est_tokens = n * 800
        cost = est_tokens / 1e6 * 0.25
        print(f"\n  Итого: {n} файлов, ~{est_tokens:,} токенов, ~${cost:.4f}")
        return

    try:
        import anthropic
    except ImportError:
        print("❌ pip install anthropic")
        sys.exit(1)

    client = anthropic.Anthropic()
    ok = 0
    for path in targets:
        print(f"  🔄 {path.stem}...")
        try:
            if enrich_contact(path, client):
                ok += 1
            time.sleep(0.5)
        except Exception as e:
            print(f"  ❌ {path.stem}: {e}")

    print(f"\n✅ Готово: {ok}/{len(targets)} обработано")
    print(f"   Откройте docs/contacts/ и выберите лучший вариант сообщения.")


if __name__ == "__main__":
    main()
