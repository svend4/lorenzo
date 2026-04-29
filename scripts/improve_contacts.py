"""
improve_contacts.py — извлекает email, Telegram, GitHub, Habr-ники
из всех docs/ и создаёт docs/CONTACTS.md.
Запуск: python scripts/improve_contacts.py
"""
import re
from pathlib import Path
from collections import defaultdict

ROOT = Path(__file__).parent.parent
DOCS = ROOT / "docs"

# Паттерны для контактов
PATTERNS = {
    "email":    r'\b[a-zA-Z0-9._%+\-]+@[a-zA-Z0-9.\-]+\.[a-zA-Z]{2,}\b',
    "telegram": r'(?:t\.me|telegram\.me|@)[/]?([a-zA-Z0-9_]{4,})',
    "github":   r'github\.com/([a-zA-Z0-9\-]+(?:/[a-zA-Z0-9\-_.]+)?)',
    "habr":     r'habr\.com/(?:ru/)?(?:users?|company)/([a-zA-Z0-9_\-]+)',
    "habr_user": r'\bhttps?://habr\.com/[^\s\)"\']+',
}

# Известные авторы с их проектами
KNOWN_AUTHORS = {
    "andrey_chuyan":  {"проект": "Svyazi", "слой": "ingestion/CardIndex"},
    "VitalyOborin":   {"проект": "Yodoca", "слой": "memory"},
    "kksudo":         {"проект": "AgentFS", "слой": "knowledge/filesystem"},
    "spbmolot":       {"проект": "NGT Memory", "слой": "memory"},
    "AnastasiyaW":    {"проект": "knowledge-space, mclaude", "слой": "knowledge/orchestration"},
    "Sonia_Black":    {"проект": "knowledge-space", "слой": "knowledge"},
    "lee-to":         {"проект": "AI Factory", "слой": "orchestration"},
    "Cutcode":        {"проект": "AIF Handoff", "слой": "orchestration"},
    "zodigancode":    {"проект": "Rufler", "слой": "orchestration"},
    "tagir_analyzes": {"проект": "Legal RAG", "слой": "rag"},
    "VladSpace":      {"проект": "Graph RAG", "слой": "rag"},
    "Antipozitive":   {"проект": "MemNet", "слой": "memory"},
    "nlaik":          {"проект": "LiteParse / research-docs", "слой": "rag"},
    "Dmitriila":      {"проект": "SENTINEL", "слой": "security"},
    "MiXaiLL76":      {"проект": "Auto AI Router", "слой": "security"},
}

# Лучшие первые вопросы для каждого автора
FIRST_QUESTIONS = {
    "andrey_chuyan":  "Стоит ли расширять CardIndex до person/project/episode/evidence "
                      "или лучше держать разные индексы?",
    "VitalyOborin":   "Что сильнее влияет на качество памяти: "
                      "отдельный consolidator, decay или строгая типизация записей?",
    "kksudo":         "Что лучше класть в .agentos, а что выносить "
                      "в machine-only state вне vault conventions?",
    "spbmolot":       "Где проходит практическая граница между полезной ассоциацией "
                      "и ложной ко-активацией тем для community discovery?",
    "AnastasiyaW":    "Держать operational benchmark/gotcha cards в одной базе "
                      "с reference cards или отдельным слоем?",
}


def extract_contacts(text: str) -> dict[str, set[str]]:
    """Находит все контакты в тексте."""
    result: dict[str, set[str]] = defaultdict(set)
    for kind, pattern in PATTERNS.items():
        for m in re.finditer(pattern, text, re.IGNORECASE):
            val = m.group(0).strip()
            if len(val) > 3:
                result[kind].add(val)
    return result


def find_author_mentions(text: str) -> list[str]:
    """Находит упоминания известных авторов."""
    found = []
    low = text.lower()
    for author in KNOWN_AUTHORS:
        if author.lower() in low:
            found.append(author)
    return found


def main():
    print("Извлечение контактов из docs/...")

    all_contacts: dict[str, dict[str, set]] = defaultdict(lambda: defaultdict(set))
    author_files: dict[str, list[str]] = defaultdict(list)

    for f in DOCS.rglob("*.md"):
        text = f.read_text(encoding="utf-8")
        contacts = extract_contacts(text)
        rel = str(f.relative_to(ROOT))

        for kind, values in contacts.items():
            for v in values:
                all_contacts[kind][v].add(rel)

        for author in find_author_mentions(text):
            author_files[author].append(rel)

    # Строим CONTACTS.md
    lines = [
        "# Контакты и авторы\n",
        "## Ключевые авторы проектов\n",
        "| Автор | Проект | Слой | Упомянут в файлах | Первый вопрос |",
        "|-------|--------|------|-------------------|---------------|",
    ]

    for author, info in sorted(KNOWN_AUTHORS.items()):
        count = len(author_files.get(author, []))
        question = FIRST_QUESTIONS.get(author, "—")
        lines.append(
            f"| **{author}** | {info['проект']} | {info['слой']} "
            f"| {count} | {question} |"
        )

    # GitHub ссылки
    if all_contacts["github"]:
        lines.append("\n## GitHub репозитории\n")
        lines.append("| Репозиторий | Упоминается в файлах |")
        lines.append("|-------------|---------------------|")
        for repo, files in sorted(all_contacts["github"].items()):
            if "svg" in repo or "badge" in repo:
                continue
            count = len(files)
            if count >= 2:
                lines.append(f"| `github.com/{repo}` | {count} |")

    # Habr профили
    if all_contacts["habr"]:
        lines.append("\n## Хабр профили\n")
        lines.append("| Профиль | Файлов |")
        lines.append("|---------|--------|")
        for profile, files in sorted(all_contacts["habr"].items()):
            lines.append(f"| `habr.com/.../{profile}` | {len(files)} |")

    # Email
    emails = {e for e in all_contacts["email"]
               if not e.endswith((".png", ".svg", ".jpg"))
               and "example" not in e}
    if emails:
        lines.append("\n## Email адреса\n")
        for email in sorted(emails)[:20]:
            lines.append(f"- `{email}`")

    # Шаблон первого сообщения
    lines += [
        "\n## Шаблон первого сообщения\n",
        "```",
        "Здравствуйте!",
        "Я собираю прототип Svyazi 2.0 — локальной community intelligence platform.",
        "В вашем проекте [ПРОЕКТ] меня особенно интересует слой [СЛОЙ].",
        "",
        "Один конкретный вопрос: [ВОПРОС]",
        "",
        "Если интересно — пришлю одностраничную схему интеграции.",
        "Если нет — спасибо за публикацию, она уже повлияла на архитектуру.",
        "```",
    ]

    out = DOCS / "CONTACTS.md"
    out.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(f"  wrote: {out.relative_to(ROOT)}")
    print(f"  авторов: {len(KNOWN_AUTHORS)}, GitHub репо: {len(all_contacts['github'])}")


if __name__ == "__main__":
    main()
