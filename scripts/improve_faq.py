"""
improve_faq.py — строит FAQ из QA-паттернов в документах.
Ищет: "Вопрос/Ответ", "Q:", "A:", "—" после вопроса, секции ## FAQ.
Создаёт docs/FAQ.md.
Запуск: python scripts/improve_faq.py
"""
import re
from pathlib import Path
from collections import defaultdict

ROOT = Path(__file__).parent.parent
DOCS = ROOT / "docs"

SKIP = {"FAQ.md", "QA.md", "QUESTIONS.md"}

CATEGORIES = {
    "Архитектура":   ["контракт", "архитектур", "схема", "envelope", "слой"],
    "Компоненты":    ["cardindex", "agentfs", "yodoca", "ngt", "sentinel", "rufler"],
    "Интеграция":    ["mcp", "api", "интеграц", "совмест", "protocol"],
    "MVP/Запуск":    ["mvp", "запуск", "прототип", "начать", "первый шаг"],
    "Лицензия":      ["лицензи", "mit", "bsl", "apache", "права"],
    "Команда":       ["автор", "контакт", "написать", "команда", "kksudo"],
    "Безопасность":  ["pii", "security", "приватн", "allowlist", "quarantine"],
}

# Паттерны для извлечения пар вопрос-ответ
QA_PATTERNS = [
    # "**Вопрос:** ... **Ответ:** ..."
    r'\*\*(?:Вопрос|Question)[:\s]\*\*\s*(.{10,200}?)\s*\*\*(?:Ответ|Answer)[:\s]\*\*\s*(.{10,400}?)(?=\n\n|\Z|\*\*Вопрос)',
    # "Q: ... A: ..."
    r'(?:^|\n)Q[:\s]+(.{10,200}?)\n+A[:\s]+(.{10,400}?)(?=\n\nQ|\Z)',
    # "## Часто задаваемые вопросы" — секция с парами
    r'#{2,3}\s+(.{10,100}\?)\s*\n+([^#]{20,400}?)(?=\n#{2,3}|\Z)',
    # Вопрос на отдельной строке заканчивается "?"
    r'(?:^|\n)([А-ЯA-Z][^\n]{15,150}\?)\s*\n+([^\n#*]{30,300})',
]

CURATED_FAQ = [
    ("Что такое Svyazi 2.0?",
     "Svyazi 2.0 — это экосистема из 20+ взаимосвязанных OSS-проектов для "
     "построения AI-систем с памятью, оркестрацией агентов и безопасной обработкой данных."),
    ("Какова лицензия проекта?",
     "Компоненты используют разные лицензии: MIT (AgentFS, knowledge-space), "
     "Apache 2.0 (Yodoca), BSL 1.1 (NGT-memory). Проект Lorenzo — MIT."),
    ("С чего начать?",
     "Начните с Executive Summary (docs/01-svyazi/01-executive-summary.md), "
     "затем MVP Planning (07-mvp-planning.md) и Roadmap (12-roadmap.md)."),
    ("Как связаться с авторами компонентов?",
     "Контакты в docs/CONTACTS.md. Авторы: kksudo (Андрей) — AgentFS, "
     "spbmolot (Виталий) — ряд Habr-проектов. Используйте шаблон "
     "docs/templates/contact-outreach.md."),
    ("Что такое MCP?",
     "Model Context Protocol — открытый протокол Anthropic для взаимодействия "
     "LLM с внешними инструментами и данными. Ключевой элемент архитектуры Svyazi."),
    ("Каков статус готовности MVP?",
     "Согласно SCORING.md: 96% (159/164 баллов) — документация и архитектура готовы. "
     "Остаётся: связаться с авторами и реализовать прототип Knowledge OS."),
]


def extract_qa(text: str) -> list[tuple[str, str]]:
    # Убираем code-блоки
    text = re.sub(r'```.*?```', '', text, flags=re.DOTALL)
    pairs = []
    seen: set = set()

    for pattern in QA_PATTERNS:
        for m in re.finditer(pattern, text, re.MULTILINE | re.DOTALL):
            q = re.sub(r'\s+', ' ', m.group(1)).strip()
            a = re.sub(r'\s+', ' ', m.group(2)).strip()
            if len(q) < 10 or len(a) < 20:
                continue
            if not q.endswith("?") and "?" not in q:
                continue
            key = q.lower()[:30]
            if key in seen:
                continue
            seen.add(key)
            pairs.append((q[:200], a[:400]))
    return pairs


def categorize(q: str, a: str) -> str:
    text = (q + " " + a).lower()
    for cat, kws in CATEGORIES.items():
        if any(k in text for k in kws):
            return cat
    return "Общее"


def main():
    print("Строю FAQ...")

    by_cat: dict[str, list] = defaultdict(list)
    total = 0

    # Кураторские вопросы — в начало
    for q, a in CURATED_FAQ:
        cat = categorize(q, a)
        by_cat[cat].append((q, a, "curated"))
        total += 1

    # Автоматические из документов
    for f in sorted(DOCS.rglob("*.md")):
        if f.name in SKIP:
            continue
        text = f.read_text(encoding="utf-8")
        if len(text.split()) < 100:
            continue
        for q, a in extract_qa(text):
            cat = categorize(q, a)
            by_cat[cat].append((q, a, str(f.relative_to(ROOT))))
            total += 1

    cat_order = ["Архитектура", "MVP/Запуск", "Компоненты", "Интеграция",
                 "Безопасность", "Лицензия", "Команда", "Общее"]

    lines = [
        "# Часто задаваемые вопросы (FAQ)\n",
        f"_Извлечено: {total} вопросов и ответов_\n",
    ]

    for cat in cat_order:
        items = by_cat.get(cat, [])
        if not items:
            continue
        lines.append(f"\n## {cat}\n")
        seen: set = set()
        for q, a, source in items:
            key = q.lower()[:35]
            if key in seen:
                continue
            seen.add(key)
            lines.append(f"### {q}\n")
            lines.append(f"{a}\n")
            if source != "curated":
                short = source.split("/")[-1].replace(".md", "")
                lines.append(f"_→ [{short}]({source})_\n")
            if len(seen) >= 8:
                break

    out = DOCS / "FAQ.md"
    out.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(f"  wrote: {out.relative_to(ROOT)}")
    print(f"  вопросов: {total}")


if __name__ == "__main__":
    main()
