"""
improve_abbreviations.py — словарь аббревиатур и сокращений из docs/.
Ищет: "ABC — это ...", "ABC (от англ. ...)", "ABC: ...", капс-слова.
Создаёт docs/ABBREVIATIONS.md.
Запуск: python scripts/improve_abbreviations.py
"""
import re
from pathlib import Path
from collections import defaultdict, Counter

ROOT = Path(__file__).parent.parent
DOCS = ROOT / "docs"

SKIP = {"ABBREVIATIONS.md", "GLOSSARY.md", "CONCEPTS.md"}

# Известные аббревиатуры (дополнение к автоматически найденным)
KNOWN = {
    "MCP":   "Model Context Protocol — протокол контекста для AI-инструментов",
    "RAG":   "Retrieval-Augmented Generation — генерация с поиском по базе знаний",
    "LLM":   "Large Language Model — большая языковая модель",
    "CRDT":  "Conflict-free Replicated Data Type — структура данных без конфликтов слияния",
    "PII":   "Personally Identifiable Information — персональные данные",
    "MVP":   "Minimum Viable Product — минимально жизнеспособный продукт",
    "OSS":   "Open Source Software — программное обеспечение с открытым кодом",
    "API":   "Application Programming Interface — интерфейс программирования приложений",
    "SDK":   "Software Development Kit — набор инструментов разработчика",
    "CLI":   "Command Line Interface — интерфейс командной строки",
    "CI/CD": "Continuous Integration / Continuous Deployment",
    "TF-IDF":"Term Frequency–Inverse Document Frequency — метрика важности термина",
    "JWT":   "JSON Web Token — токен аутентификации",
    "YAML":  "YAML Ain't Markup Language — формат конфигурационных файлов",
    "BSL":   "Business Source License — бизнес-лицензия с открытым кодом",
    "MIT":   "Massachusetts Institute of Technology License — разрешительная лицензия",
    "SGB":   "Sozialgesetzbuch — Социальный кодекс Германии",
    "P2P":   "Peer-to-Peer — децентрализованная сеть",
    "GDPR":  "General Data Protection Regulation — европейский регламент защиты данных",
    "FAQ":   "Frequently Asked Questions — часто задаваемые вопросы",
    "TODO":  "To Do — задача к выполнению",
    "NLP":   "Natural Language Processing — обработка естественного языка",
}

# Паттерны для автообнаружения
PATTERNS = [
    # "ABC — ..." или "ABC: ..."
    r'\b([A-Z]{2,8}(?:/[A-Z]{1,4})?)\b\s*[—:]\s*([^.\n]{10,150})',
    # "ABC (от англ. Full Name)"
    r'\b([A-Z]{2,8})\b\s*\((?:от\s+англ\.|англ\.?|en:|от\s+)([^)]{5,80})\)',
    # "аббревиатура ABC расшифровывается"
    r'аббревиатур[а-я]+\s+([A-Z]{2,8})\s+(?:расшифровывается|означает)[^.]+\.\s*([^.\n]{5,100})',
]


def find_abbrevs(text: str) -> dict[str, str]:
    result = {}
    for pattern in PATTERNS:
        for m in re.finditer(pattern, text):
            abbr = m.group(1).strip()
            defn = m.group(2).strip()[:120]
            if len(abbr) < 2 or len(abbr) > 8:
                continue
            # Фильтруем числа и случайные заглавные
            if not re.match(r'^[A-Z/\-]{2,8}$', abbr):
                continue
            if abbr not in result:
                result[abbr] = defn
    return result


def count_usage(text: str, abbr: str) -> int:
    return len(re.findall(r'\b' + re.escape(abbr) + r'\b', text))


def main():
    print("Словарь аббревиатур...")

    auto: dict[str, list] = defaultdict(list)
    all_text = ""

    for f in sorted(DOCS.rglob("*.md")):
        if f.name in SKIP:
            continue
        text = f.read_text(encoding="utf-8")
        all_text += text + "\n"
        for abbr, defn in find_abbrevs(text).items():
            auto[abbr].append(defn)

    # Объединяем: известные + автонайденные
    combined: dict[str, str] = {}
    for abbr, defn in KNOWN.items():
        combined[abbr] = defn

    for abbr, defs in auto.items():
        if abbr not in combined and len(defs) >= 1:
            combined[abbr] = defs[0]

    # Считаем использование
    usage: dict[str, int] = {a: count_usage(all_text, a) for a in combined}
    combined_sorted = sorted(combined.items(), key=lambda x: x[0])

    lines = [
        "# Словарь аббревиатур и сокращений\n",
        f"**Найдено:** {len(combined)} аббревиатур "
        f"({len(KNOWN)} известных + {len(combined)-len(KNOWN)} автоматически)\n",
        "| Аббревиатура | Расшифровка | Упоминаний |",
        "|-------------|-------------|------------|",
    ]
    for abbr, defn in combined_sorted:
        cnt = usage.get(abbr, 0)
        mark = " ⭐" if abbr in KNOWN else ""
        lines.append(f"| **{abbr}**{mark} | {defn} | {cnt} |")

    # Топ по частоте
    top = sorted(usage.items(), key=lambda x: -x[1])[:15]
    lines += [
        "\n## Самые часто используемые\n",
        "| Аббревиатура | Упоминаний |",
        "|-------------|------------|",
    ]
    for abbr, cnt in top:
        defn = combined.get(abbr, "—")[:60]
        lines.append(f"| **{abbr}** | {cnt} — _{defn}_ |")

    out = DOCS / "ABBREVIATIONS.md"
    out.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(f"  wrote: {out.relative_to(ROOT)}")
    print(f"  аббревиатур: {len(combined)}")


if __name__ == "__main__":
    main()
