"""
improve_digest_auto.py — автодайджест изменений за N дней.

Анализирует git-лог и содержимое изменённых файлов:
  1. Какие файлы добавлены / изменены / удалены за период
  2. Ключевые слова из изменений (TF-IDF на diff)
  3. Статистика: сколько слов добавлено/удалено
  4. Самые активные секции
  5. Новые концепты (слова, появившиеся впервые)

Запуск:
    python scripts/improve_digest_auto.py            # за 7 дней
    python scripts/improve_digest_auto.py --days 30  # за месяц
    python scripts/improve_digest_auto.py --since 2026-04-01
    python scripts/improve_digest_auto.py --format text  # терминал
"""
import re
import subprocess
import sys
from collections import Counter, defaultdict
from pathlib import Path
from datetime import date, timedelta

ROOT = Path(__file__).parent.parent
DOCS = ROOT / "docs"
TODAY = date.today().isoformat()

DAYS = 7
FORMAT = "md"
SINCE = None

if "--days" in sys.argv:
    idx = sys.argv.index("--days")
    if idx + 1 < len(sys.argv):
        DAYS = int(sys.argv[idx + 1])

if "--since" in sys.argv:
    idx = sys.argv.index("--since")
    if idx + 1 < len(sys.argv):
        SINCE = sys.argv[idx + 1]

if "--format" in sys.argv:
    idx = sys.argv.index("--format")
    if idx + 1 < len(sys.argv):
        FORMAT = sys.argv[idx + 1]

if SINCE is None:
    since_date = date.today() - timedelta(days=DAYS)
    SINCE = since_date.isoformat()

STOPWORDS = {
    "и", "в", "не", "на", "с", "по", "к", "из", "за", "для", "это",
    "как", "но", "или", "что", "был", "его", "её", "их", "мы", "вы",
    "при", "от", "до", "об", "так", "все", "они", "же", "том",
    "the", "a", "an", "is", "of", "in", "on", "to", "for", "with",
    "by", "and", "not", "it", "we", "are", "this", "that", "be",
    "docs", "summary", "tags", "true", "false", "null",
}

SECTION_LABELS = {
    "01-svyazi":               "Svyazi 2.0",
    "02-anthropic-vacancies":  "Anthropic",
    "03-technology-combinations": "Технологии",
    "04-ai-collaborations":    "AI-ансамбли",
    "05-habr-projects":        "Хабр-проекты",
    "contacts":                "Контакты",
    "templates":               "Шаблоны",
    "scripts":                 "Скрипты",
}


def _git(cmd: list[str]) -> str:
    try:
        result = subprocess.run(
            ["git"] + cmd, capture_output=True, text=True,
            cwd=ROOT, timeout=30
        )
        return result.stdout.strip()
    except Exception:
        return ""


def _get_commits(since: str) -> list[dict]:
    out = _git(["log", f"--since={since}", "--format=%H|%ae|%s|%ad", "--date=short"])
    commits = []
    for line in out.splitlines():
        parts = line.split("|", 3)
        if len(parts) == 4:
            commits.append({
                "hash": parts[0][:8],
                "author": parts[1],
                "subject": parts[2],
                "date": parts[3],
            })
    return commits


def _get_changed_files(since: str) -> dict[str, list[str]]:
    """Возвращает {статус: [файлы]}."""
    out = _git(["diff", "--name-status", f"--since={since}",
                f"HEAD@{{'{since}'}}", "HEAD"])
    if not out:
        out = _git(["log", f"--since={since}", "--name-status",
                    "--format=", "--diff-filter=ADM"])
    changes: dict[str, list[str]] = defaultdict(list)
    for line in out.splitlines():
        line = line.strip()
        if not line or line.startswith("commit"):
            continue
        parts = line.split("\t")
        if len(parts) >= 2:
            status = parts[0][0]  # A / M / D / R
            fname = parts[-1]
            if fname.endswith(".md") or fname.endswith(".py"):
                changes[status].append(fname)
    return dict(changes)


def _get_diff_text(since: str) -> str:
    """Получить текст всех изменений (diff)."""
    out = _git(["diff", f"HEAD@{{'{since}'}}", "HEAD", "--", "docs/"])
    if not out:
        # fallback: recent commits diff
        commits = _get_commits(since)
        if len(commits) >= 2:
            oldest = commits[-1]["hash"]
            out = _git(["diff", oldest + "^", "HEAD", "--", "docs/"])
    return out


def _tokenize_diff(diff: str) -> tuple[Counter, Counter]:
    """Возвращает (added_tokens, removed_tokens)."""
    added: list[str] = []
    removed: list[str] = []
    for line in diff.splitlines():
        if line.startswith("+") and not line.startswith("+++"):
            tokens = re.findall(r'[а-яёa-z]{4,}', line[1:].lower())
            added.extend(t for t in tokens if t not in STOPWORDS)
        elif line.startswith("-") and not line.startswith("---"):
            tokens = re.findall(r'[а-яёa-z]{4,}', line[1:].lower())
            removed.extend(t for t in tokens if t not in STOPWORDS)
    return Counter(added), Counter(removed)


def _section_of(path: str) -> str:
    parts = path.split("/")
    if len(parts) >= 2 and parts[0] == "docs":
        return parts[1]
    if len(parts) >= 1 and parts[0] == "scripts":
        return "scripts"
    return "root"


def _commit_stats(since: str) -> dict:
    """Статистика коммитов за период."""
    commits = _get_commits(since)
    authors: Counter = Counter()
    by_date: Counter = Counter()
    for c in commits:
        authors[c["author"]] += 1
        by_date[c["date"]] += 1
    return {
        "total": len(commits),
        "commits": commits[:10],
        "authors": authors.most_common(5),
        "by_date": dict(sorted(by_date.items())),
    }


def _file_stats_from_log(since: str) -> dict:
    """Файлы изменённые за период через git log."""
    out = _git(["log", f"--since={since}", "--name-only", "--format=", "--diff-filter=ADM"])
    added_files: list[str] = []
    modified_files: list[str] = []

    # Используем --diff-filter отдельно
    added_out = _git(["log", f"--since={since}", "--name-only", "--format=", "--diff-filter=A"])
    for line in added_out.splitlines():
        line = line.strip()
        if line.endswith((".md", ".py", ".json")):
            added_files.append(line)

    mod_out = _git(["log", f"--since={since}", "--name-only", "--format=", "--diff-filter=M"])
    seen: set[str] = set(added_files)
    for line in mod_out.splitlines():
        line = line.strip()
        if line.endswith((".md", ".py")) and line not in seen:
            modified_files.append(line)
            seen.add(line)

    # По секциям
    by_section: Counter = Counter()
    for f in added_files + modified_files:
        by_section[_section_of(f)] += 1

    return {
        "added": added_files[:20],
        "modified": modified_files[:20],
        "by_section": by_section.most_common(8),
        "total_changed": len(added_files) + len(modified_files),
    }


def main() -> None:
    print(f"📰 improve_digest_auto.py — дайджест изменений")
    print(f"   С: {SINCE} по {TODAY} ({DAYS} дн.) | Формат: {FORMAT}\n")

    commit_stats = _commit_stats(SINCE)
    file_stats = _file_stats_from_log(SINCE)

    print(f"   Коммитов: {commit_stats['total']}")
    print(f"   Файлов изменено: {file_stats['total_changed']}")

    # Diff-анализ ключевых слов
    print("   Анализирую diff...", end=" ", flush=True)
    diff_text = _get_diff_text(SINCE)
    added_tokens, removed_tokens = _tokenize_diff(diff_text)
    new_concepts = [t for t in added_tokens if t not in removed_tokens
                    and added_tokens[t] >= 3][:15]
    top_added = added_tokens.most_common(15)
    print(f"+{sum(added_tokens.values())} слов, -{sum(removed_tokens.values())} слов")

    if FORMAT == "text":
        print(f"\n  📋 Дайджест с {SINCE}:")
        print(f"  Коммитов: {commit_stats['total']}")
        for c in commit_stats["commits"][:5]:
            print(f"    [{c['date']}] {c['subject'][:60]}")
        print(f"\n  Новых файлов: {len(file_stats['added'])}")
        for f in file_stats["added"][:5]:
            print(f"    + {f}")
        print(f"\n  Ключевые новые слова: {', '.join(w for w, _ in top_added[:8])}")
        return

    # Markdown
    lines = [
        "# Автодайджест изменений\n",
        f"_Период: {SINCE} — {TODAY} ({DAYS} дней)_\n",
        "---\n",
        "## Сводка\n",
        "| Метрика | Значение |",
        "|---------|----------|",
        f"| Коммитов | **{commit_stats['total']}** |",
        f"| Новых файлов | **{len(file_stats['added'])}** |",
        f"| Изменённых файлов | **{len(file_stats['modified'])}** |",
        f"| Слов добавлено | **+{sum(added_tokens.values()):,}** |",
        f"| Слов удалено | **−{sum(removed_tokens.values()):,}** |",
    ]

    if file_stats["by_section"]:
        lines += ["\n## Активность по секциям\n",
                  "| Секция | Изменений |",
                  "|--------|-----------|"]
        for sec, cnt in file_stats["by_section"]:
            label = SECTION_LABELS.get(sec, sec)
            bar = "▓" * min(cnt, 20)
            lines.append(f"| `{label}` | {bar} {cnt} |")

    if commit_stats["commits"]:
        lines += ["\n## Последние коммиты\n"]
        for c in commit_stats["commits"]:
            lines.append(f"- `{c['date']}` [{c['hash']}] {c['subject'][:70]}")

    if file_stats["added"]:
        lines += ["\n## Новые файлы\n"]
        for f in file_stats["added"][:15]:
            sec = _section_of(f)
            label = SECTION_LABELS.get(sec, sec)
            fname = f.split("/")[-1]
            lines.append(f"- [`{fname}`]({f}) — `{label}`")

    if file_stats["modified"]:
        lines += ["\n## Изменённые файлы\n"]
        for f in file_stats["modified"][:15]:
            fname = f.split("/")[-1]
            lines.append(f"- [`{fname}`]({f})")

    if top_added:
        lines += ["\n## Ключевые слова изменений\n",
                  "| Слово | Добавлено | Удалено |",
                  "|-------|-----------|---------|"]
        for word, cnt in top_added:
            rem = removed_tokens.get(word, 0)
            delta = f"+{cnt}" if cnt > rem else f"−{rem - cnt}"
            lines.append(f"| `{word}` | +{cnt} | −{rem} |")

    if new_concepts:
        lines += ["\n## Новые концепты\n",
                  f"_Слова появившиеся в этом периоде (≥3 раза):_\n"]
        lines.append(", ".join(f"`{w}`" for w in new_concepts))

    lines += [f"\n---\n_Дайджест сгенерирован автоматически: {TODAY}_\n"]

    out = DOCS / "DIGEST_AUTO.md"
    out.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(f"  wrote: {out.relative_to(ROOT)}")

    if new_concepts:
        print(f"  Новые концепты: {', '.join(new_concepts[:5])}")


if __name__ == "__main__":
    main()
