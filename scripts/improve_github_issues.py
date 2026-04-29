"""
improve_github_issues.py — создаёт GitHub Issues из ACTION_ITEMS.md и TODO-блоков.

Без GitHub API: генерирует docs/GITHUB_ISSUES.md с готовым списком задач
в формате, пригодном для ручного или API-создания.

Опционально: если установлен gh CLI и задан --create, создаёт Issues через gh.

Создаёт docs/GITHUB_ISSUES.md.
Запуск:
    python scripts/improve_github_issues.py
    python scripts/improve_github_issues.py --create   # требует gh CLI
    python scripts/improve_github_issues.py --dry-run
    python scripts/improve_github_issues.py --label docs,automation
"""
import re
import shutil
import subprocess
import sys
from pathlib import Path
from datetime import date

ROOT = Path(__file__).parent.parent
DOCS = ROOT / "docs"
TODAY = date.today().isoformat()

CREATE = "--create" in sys.argv
DRY_RUN = "--dry-run" in sys.argv

DEFAULT_LABELS = ["docs", "automation"]
if "--label" in sys.argv:
    idx = sys.argv.index("--label")
    if idx + 1 < len(sys.argv):
        DEFAULT_LABELS = sys.argv[idx + 1].split(',')

SKIP_FILES = {"GITHUB_ISSUES.md", "SEARCH.md"}

# Паттерны для поиска action items
TODO_PATTERNS = [
    # - [ ] Task description
    re.compile(r'^[-*]\s+\[\s*\]\s+(.{10,200})$', re.MULTILINE),
    # TODO: description
    re.compile(r'\bTODO[:\s]+(.{10,150})', re.MULTILINE),
    # FIXME: description
    re.compile(r'\bFIXME[:\s]+(.{10,150})', re.MULTILINE),
    # ❌ description (failed check items)
    re.compile(r'^[-*]\s+❌\s+(.{5,150})$', re.MULTILINE),
]

# Приоритетные файлы
PRIORITY_FILES = [
    "ACTION_ITEMS.md", "DECISIONS.md", "HEALTH.md", "STALENESS.md",
    "COVERAGE.md", "CONTENT_GAPS.md",
]


def _extract_issues(path: Path) -> list[dict]:
    try:
        text = path.read_text(encoding="utf-8")
    except Exception:
        return []

    issues = []
    seen = set()

    # Определяем текущий раздел для метки
    current_section = ""
    for line in text.split('\n'):
        m = re.match(r'^#{1,3}\s+(.+)$', line)
        if m:
            current_section = m.group(1).strip()

    for pat in TODO_PATTERNS:
        for m in pat.finditer(text):
            title = m.group(1).strip()
            # Убираем markdown-разметку
            title = re.sub(r'[`*_]', '', title)
            title = re.sub(r'\s+', ' ', title).strip()
            if len(title) < 10:
                continue
            key = title.lower()[:60]
            if key in seen:
                continue
            seen.add(key)
            issues.append({
                "title": title[:100],
                "source": str(path.relative_to(ROOT)),
                "section": current_section,
                "labels": DEFAULT_LABELS.copy(),
            })

    return issues


def _create_gh_issue(issue: dict) -> bool:
    if not shutil.which("gh"):
        print("  ❌ gh CLI не найден: brew install gh  или  apt install gh")
        return False

    labels_arg = ",".join(issue["labels"])
    body = f"Источник: `{issue['source']}`\nРаздел: {issue['section']}\n\nСоздано автоматически: {TODAY}"

    cmd = [
        "gh", "issue", "create",
        "--title", issue["title"],
        "--body", body,
        "--label", labels_arg,
    ]
    result = subprocess.run(cmd, cwd=ROOT, capture_output=True, text=True)
    if result.returncode == 0:
        print(f"  ✅ Issue создан: {result.stdout.strip()}")
        return True
    else:
        print(f"  ❌ ошибка: {result.stderr[:100]}")
        return False


def main() -> None:
    print("📋 improve_github_issues.py — генерация GitHub Issues")
    if CREATE:
        print("   Режим: создание через gh CLI")
    elif DRY_RUN:
        print("   Режим: dry-run")

    # Сначала приоритетные файлы, потом остальные
    all_files = []
    for name in PRIORITY_FILES:
        p = DOCS / name
        if p.exists():
            all_files.append(p)
    for f in sorted(DOCS.rglob("*.md")):
        if f.name not in SKIP_FILES and f not in all_files:
            all_files.append(f)

    all_issues: list[dict] = []
    for f in all_files:
        issues = _extract_issues(f)
        all_issues.extend(issues)

    print(f"   Найдено задач: {len(all_issues)}\n")

    if CREATE and not DRY_RUN:
        created = 0
        for issue in all_issues[:20]:  # лимит 20 за раз
            if _create_gh_issue(issue):
                created += 1
        print(f"\n  Создано: {created}/{min(len(all_issues), 20)} Issues")
        return

    # Генерируем отчёт
    lines = [
        "# GitHub Issues — список задач\n",
        f"_Обновлено: {TODAY}_\n",
        f"Найдено задач: **{len(all_issues)}**\n",
        "> Создайте Issues вручную или запустите с `--create` (требует gh CLI)\n",
    ]

    # Группировка по источнику
    by_source: dict[str, list[dict]] = {}
    for issue in all_issues:
        src = issue["source"]
        by_source.setdefault(src, []).append(issue)

    for src, issues in sorted(by_source.items()):
        lines.append(f"\n## `{src}` ({len(issues)} задач)\n")
        for issue in issues:
            labels = ', '.join(f'`{l}`' for l in issue["labels"])
            lines.append(f"- [ ] **{issue['title']}**  _{labels}_")

    lines += [
        "\n## Создание через gh CLI\n",
        "```bash",
        "# Установка gh CLI",
        "brew install gh  # macOS",
        "# sudo apt install gh  # Ubuntu",
        "",
        "# Создание Issues",
        "python scripts/improve_github_issues.py --create --label docs,automation",
        "```\n",
    ]

    out = DOCS / "GITHUB_ISSUES.md"
    out.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(f"  wrote: {out.relative_to(ROOT)}")
    print(f"  источников: {len(by_source)}")


if __name__ == "__main__":
    main()
