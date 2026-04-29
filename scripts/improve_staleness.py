"""
improve_staleness.py — находит документы которые давно не обновлялись или неполные.

Проверяет:
  - Файлы без изменений в git > N дней (по умолчанию 30)
  - Файлы без summary-комментария
  - Файлы без тегов
  - Файлы короче 100 слов (заготовки)

Создаёт docs/STALENESS.md.
Запуск: python scripts/improve_staleness.py
        python scripts/improve_staleness.py --days 60   # другой порог
        python scripts/improve_staleness.py --no-git    # без git-дат (только контент)
"""
import re
import subprocess
import sys
from pathlib import Path
from datetime import date, datetime

ROOT = Path(__file__).parent.parent
DOCS = ROOT / "docs"
TODAY = date.today()

STALE_DAYS = 30
for arg in sys.argv:
    if arg.startswith("--days="):
        STALE_DAYS = int(arg.split("=", 1)[1])
if "--days" in sys.argv:
    idx = sys.argv.index("--days")
    if idx + 1 < len(sys.argv):
        STALE_DAYS = int(sys.argv[idx + 1])

USE_GIT = "--no-git" not in sys.argv

SKIP_FILES = {"SEARCH.md", "DUPLICATES.md", "STALENESS.md", "COVERAGE.md",
              "CONTACT_PRIORITY.md", "search_index.json"}


def _git_last_modified(path: Path) -> date | None:
    """Возвращает дату последнего коммита затронувшего файл."""
    if not USE_GIT:
        return None
    result = subprocess.run(
        ["git", "log", "-1", "--format=%ci", "--", str(path.relative_to(ROOT))],
        cwd=ROOT, capture_output=True, text=True
    )
    line = result.stdout.strip()
    if not line:
        return None
    try:
        return datetime.fromisoformat(line[:10]).date()
    except ValueError:
        return None


def _has_summary(text: str) -> bool:
    return bool(re.search(r'<!--\s*summary[:\s]', text))


def _has_tags(text: str) -> bool:
    return bool(re.search(r'<!--\s*tags:', text))


def _word_count(text: str) -> int:
    clean = re.sub(r'<!--.*?-->', '', text, flags=re.DOTALL)
    clean = re.sub(r'[#*`\[\]|>]', ' ', clean)
    return len(clean.split())


def analyze_docs() -> list[dict]:
    results = []
    for f in sorted(DOCS.rglob("*.md")):
        if f.name in SKIP_FILES:
            continue
        text = f.read_text(encoding="utf-8")
        words = _word_count(text)
        last_mod = _git_last_modified(f)
        days_old = (TODAY - last_mod).days if last_mod else None

        issues = []
        if not _has_summary(text):
            issues.append("нет summary")
        if not _has_tags(text):
            issues.append("нет тегов")
        if words < 100:
            issues.append(f"короткий ({words} слов)")
        if days_old is not None and days_old > STALE_DAYS:
            issues.append(f"устарел ({days_old}д)")

        if issues:
            results.append({
                "path": f.relative_to(ROOT),
                "words": words,
                "last_mod": str(last_mod) if last_mod else "—",
                "days_old": days_old,
                "issues": issues,
            })
    return results


def main() -> None:
    print(f"🕰  improve_staleness.py — поиск устаревших документов (порог: {STALE_DAYS}д)")

    docs = analyze_docs()
    docs_sorted = sorted(docs, key=lambda d: -(d["days_old"] or 0))

    # Разбиваем по типу проблемы
    stale   = [d for d in docs_sorted if any("устарел" in i for i in d["issues"])]
    no_meta = [d for d in docs_sorted if any("нет summary" in i or "нет тегов" in i
                                              for i in d["issues"]) and d not in stale]
    short   = [d for d in docs_sorted if any("короткий" in i for i in d["issues"])
               and d not in stale and d not in no_meta]

    lines = [
        "# Отчёт об устаревших документах\n",
        f"_Порог: {STALE_DAYS} дней. Обновлено: {TODAY}_\n",
        f"Найдено проблем: **{len(docs)}** файлов\n",
    ]

    if stale:
        lines += [f"## Устаревшие (> {STALE_DAYS}д без изменений) — {len(stale)} файлов\n",
                  "| Файл | Последнее изменение | Дней | Проблемы |",
                  "|------|--------------------|----|---------|"]
        for d in stale[:30]:
            issues_str = ", ".join(d["issues"])
            lines.append(f"| `{d['path']}` | {d['last_mod']} | {d['days_old']} | {issues_str} |")
        lines.append("")

    if no_meta:
        lines += [f"## Без метаданных (нет summary или тегов) — {len(no_meta)} файлов\n",
                  "| Файл | Слов | Проблемы |",
                  "|------|------|---------|"]
        for d in no_meta[:20]:
            lines.append(f"| `{d['path']}` | {d['words']} | {', '.join(d['issues'])} |")
        lines.append("")

    if short:
        lines += [f"## Короткие (< 100 слов, заготовки) — {len(short)} файлов\n",
                  "| Файл | Слов |",
                  "|------|------|"]
        for d in short[:20]:
            lines.append(f"| `{d['path']}` | {d['words']} |")
        lines.append("")

    lines += [
        "## Рекомендуемые действия\n",
        "```bash",
        "# Добавить summary и теги к файлам без метаданных",
        "python scripts/improve_summaries.py",
        "python scripts/improve_tags.py",
        "",
        "# Обогатить короткие файлы через LLM",
        "python scripts/improve_llm_enrich.py --section 05-habr-projects",
        "```",
    ]

    out = DOCS / "STALENESS.md"
    out.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(f"  wrote: {out.relative_to(ROOT)}")
    print(f"  устаревших: {len(stale)}, без метаданных: {len(no_meta)}, коротких: {len(short)}")


if __name__ == "__main__":
    main()
