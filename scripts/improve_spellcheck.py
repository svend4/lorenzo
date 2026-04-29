"""
improve_spellcheck.py — проверка орфографии в docs/.
Без внешних зависимостей: использует встроенный словарь частых опечаток
и опциональный pyspellchecker если установлен.

Создаёт docs/SPELLCHECK.md — список подозрительных слов по файлам.
Запуск:
    python scripts/improve_spellcheck.py
    python scripts/improve_spellcheck.py --fix   # авто-замена по известным парам
    python scripts/improve_spellcheck.py --section 05-habr-projects
"""
import re
import sys
from collections import defaultdict
from pathlib import Path
from datetime import date

ROOT = Path(__file__).parent.parent
DOCS = ROOT / "docs"
TODAY = date.today().isoformat()
FIX  = "--fix" in sys.argv
DRY  = "--dry-run" in sys.argv

SECTION_FILTER = None
if "--section" in sys.argv:
    idx = sys.argv.index("--section")
    if idx + 1 < len(sys.argv):
        SECTION_FILTER = DOCS / sys.argv[idx + 1]

SKIP_FILES = {"SEARCH.md", "BROKEN_LINKS.md", "SPELLCHECK.md"}

# Известные опечатки/исправления (ru + en терминология проекта)
KNOWN_FIXES: dict[str, str] = {
    "связяи": "связи",    "свезяи": "связи",   "связи2": "Svyazi 2.0",
    "архтектура": "архитектура", "арихтектура": "архитектура",
    "интергация": "интеграция",  "интергации": "интеграции",
    "репозитроий": "репозиторий","репозиторйи": "репозиторий",
    "докуемнт": "документ",  "документвация": "документация",
    "иснтрумент": "инструмент", "инстурмент": "инструмент",
    "конфигруация": "конфигурация",
    "вописание": "описание",  "опсиание": "описание",
    "реализция": "реализация", "реалзиация": "реализация",
    "проверяет": "проверяет",  "провеяет": "проверяет",
    "antrhropic": "Anthropic", "antrhopic": "Anthropic",
    "cluade": "Claude",  "clauide": "Claude",
    "knowlegde": "knowledge", "knoweldge": "knowledge",
    "retreival": "retrieval",  "retireval": "retrieval",
    "embedings": "embeddings", "embeddigns": "embeddings",
    "orchesrtation": "orchestration",
}

# Технические слова — не считать опечатками
WHITELIST = {
    "svyazi", "yodoca", "agentfs", "habr", "llm", "rag", "mcp", "api",
    "github", "markdown", "yaml", "json", "toc", "kv", "db", "ui", "ux",
    "mvp", "oss", "sdk", "cli", "ide", "ci", "cd", "pr", "url", "html",
    "css", "js", "ts", "py", "md", "csv", "utf", "bm25", "tfidf",
    "anthropic", "claude", "haiku", "sonnet", "opus",
    "ngt", "agentfs", "kksudo", "spbmolot", "vitalyoborin",
}


def _extract_words(text: str) -> list[str]:
    """Извлекает слова из текста (без кода и ссылок)."""
    # Убираем code-блоки, HTML-комментарии, URL
    clean = re.sub(r'```.*?```', ' ', text, flags=re.DOTALL)
    clean = re.sub(r'`[^`]+`', ' ', clean)
    clean = re.sub(r'<!--.*?-->', ' ', clean, flags=re.DOTALL)
    clean = re.sub(r'https?://\S+', ' ', clean)
    # Только слова
    return re.findall(r'\b[а-яёa-z]{4,}\b', clean.lower())


def check_file_known(path: Path) -> list[tuple[str, str]]:
    """Находит известные опечатки в файле. Возвращает [(опечатка, исправление)]."""
    text = path.read_text(encoding="utf-8")
    words = _extract_words(text)
    found = []
    seen = set()
    for w in words:
        if w in KNOWN_FIXES and w not in seen:
            found.append((w, KNOWN_FIXES[w]))
            seen.add(w)
    return found


def check_file_pyspell(path: Path, spell) -> list[str]:
    """Использует pyspellchecker для проверки (если доступен)."""
    text = path.read_text(encoding="utf-8")
    words = _extract_words(text)
    ru_words = [w for w in words if re.match(r'[а-яё]+', w) and w not in WHITELIST]
    unknown = spell.unknown(set(ru_words))
    # Фильтруем слова из белого списка и очень короткие
    return [w for w in sorted(unknown) if w not in WHITELIST and len(w) > 4]


def fix_known_typos(path: Path) -> int:
    """Исправляет известные опечатки в файле."""
    text = path.read_text(encoding="utf-8")
    changes = 0
    for typo, correct in KNOWN_FIXES.items():
        if typo in text.lower():
            # Заменяем с сохранением регистра первой буквы
            pattern = re.compile(re.escape(typo), re.IGNORECASE)
            def _replace(m):
                orig = m.group(0)
                if orig[0].isupper():
                    return correct.capitalize()
                return correct
            new_text = pattern.sub(_replace, text)
            if new_text != text:
                text = new_text
                changes += 1
    if changes and not DRY:
        path.write_text(text, encoding="utf-8")
    elif changes and DRY:
        print(f"  [dry] {path.relative_to(ROOT)}: {changes} исправлений")
    return changes


def main() -> None:
    print("📝 improve_spellcheck.py — проверка орфографии")

    # Пробуем загрузить pyspellchecker
    spell = None
    try:
        from spellchecker import SpellChecker
        spell = SpellChecker(language="ru")
        print("   pyspellchecker: доступен (расширенная проверка)")
    except ImportError:
        print("   pyspellchecker: не установлен (только известные опечатки)")
        print("   pip install pyspellchecker для расширенной проверки")

    target = SECTION_FILTER or DOCS
    files = [f for f in target.rglob("*.md") if f.name not in SKIP_FILES]
    print(f"   Файлов для проверки: {len(files)}\n")

    results: dict[str, dict] = {}
    total_fixed = 0

    for f in sorted(files):
        known = check_file_known(f)
        pyspell_words: list[str] = []
        if spell:
            pyspell_words = check_file_pyspell(f, spell)

        if known or pyspell_words:
            results[str(f.relative_to(ROOT))] = {
                "known": known,
                "pyspell": pyspell_words[:10],  # топ-10
            }

        if FIX and known:
            fixed = fix_known_typos(f)
            total_fixed += fixed

    if FIX:
        print(f"  Исправлено: {total_fixed} замен в файлах")

    lines = [
        "# Отчёт орфографии\n",
        f"_Обновлено: {TODAY}_\n",
        f"Файлов с проблемами: **{len(results)}**\n",
    ]

    if results:
        lines += ["## Найденные проблемы\n"]
        for fpath, data in sorted(results.items()):
            lines.append(f"### `{fpath}`\n")
            if data["known"]:
                for typo, fix in data["known"]:
                    lines.append(f"- ❌ `{typo}` → `{fix}`")
            if data["pyspell"]:
                lines.append(f"- ⚠️  Подозрительные слова: {', '.join(f'`{w}`' for w in data['pyspell'])}")
            lines.append("")

    lines += [
        "## Авто-исправление\n",
        "```bash",
        "python scripts/improve_spellcheck.py --fix",
        "python scripts/improve_spellcheck.py --fix --dry-run  # посмотреть перед записью",
        "```\n",
        f"Известных пар опечатка→исправление: **{len(KNOWN_FIXES)}**",
    ]

    out = DOCS / "SPELLCHECK.md"
    out.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(f"  wrote: {out.relative_to(ROOT)}")
    print(f"  файлов с проблемами: {len(results)}")


if __name__ == "__main__":
    main()
