"""
improve_digest_weekly.py — еженедельный дайджест Svyazi 2.0.

Объединяет четыре источника данных в один отчёт:
  1. Git активность: коммиты, новые/изменённые файлы, активные секции
  2. Card lifecycle: approved/normalized/raw + изменения за неделю
  3. Hot cards: топ-5 из .claude/hot_cards.json (PageRank + query_freq)
  4. Query analytics: топ запросов к gateway из .claude/query_log.jsonl

Создаёт: docs/DIGEST_WEEKLY.md

Использование:
  python scripts/improve_digest_weekly.py
  python scripts/improve_digest_weekly.py --days 14   # за 2 недели
  python scripts/improve_digest_weekly.py --no-cards  # без hot cards секции
"""

import json
import re
import subprocess
import sys
from collections import Counter, defaultdict
from datetime import datetime, timedelta
from pathlib import Path

ROOT = Path(__file__).parent.parent
DOCS = ROOT / "docs"


# ── Git helpers ───────────────────────────────────────────────────────────────

def _git(*args) -> str:
    result = subprocess.run(
        ["git"] + list(args), cwd=ROOT,
        capture_output=True, text=True
    )
    return result.stdout.strip()


def get_git_activity(days: int = 7) -> dict:
    since = (datetime.now() - timedelta(days=days)).strftime("%Y-%m-%d")
    log   = _git("log", f"--since={since}", "--oneline", "--no-merges")
    commits = [l for l in log.splitlines() if l.strip()]

    diff = _git("diff", f"--name-status",
                f"HEAD~{len(commits)}", "HEAD") if commits else ""
    added: list[str] = []
    modified: list[str] = []
    for line in diff.splitlines():
        parts = line.split("\t", 1)
        if len(parts) == 2:
            status, path = parts
            if status.startswith("A"):
                added.append(path)
            elif status.startswith("M"):
                modified.append(path)

    folder_count: dict[str, int] = defaultdict(int)
    for f in added + modified:
        parts = Path(f).parts
        folder = parts[1] if len(parts) > 2 else parts[0]
        folder_count[str(folder)] += 1

    return {
        "commits":  commits,
        "added":    added,
        "modified": modified,
        "folders":  dict(folder_count),
        "since":    since,
        "days":     days,
    }


# ── Card lifecycle stats ──────────────────────────────────────────────────────

def get_card_stats() -> dict:
    total = approved = normalized = raw = 0
    for md in DOCS.rglob("*.md"):
        if any(p in md.parts for p in ("obsidian",)):
            continue
        try:
            text = md.read_text(encoding="utf-8", errors="ignore")
        except Exception:
            continue
        total += 1
        m = re.search(r"^state:\s*(\S+)", text, re.MULTILINE)
        state = m.group(1).strip("\"'") if m else "raw"
        if state == "approved":
            approved += 1
        elif state == "normalized":
            normalized += 1
        else:
            raw += 1
    return {
        "total":      total,
        "approved":   approved,
        "normalized": normalized,
        "raw":        raw,
        "promote_pct": round(approved / max(total, 1) * 100, 1),
    }


# ── Hot cards ─────────────────────────────────────────────────────────────────

def get_hot_cards(top_k: int = 5) -> list[dict]:
    p = ROOT / ".claude" / "hot_cards.json"
    if not p.exists():
        return []
    try:
        data = json.loads(p.read_text(encoding="utf-8"))
        return data.get("top", [])[:top_k]
    except Exception:
        return []


# ── Query analytics ───────────────────────────────────────────────────────────

def get_query_analytics(days: int = 7, top_k: int = 5) -> dict:
    p = ROOT / ".claude" / "query_log.jsonl"
    if not p.exists():
        return {"count": 0}

    since = datetime.now() - timedelta(days=days)
    entries = []
    for line in p.read_text(encoding="utf-8").splitlines():
        try:
            e = json.loads(line)
            ts = datetime.strptime(e.get("ts", "2000-01-01"), "%Y-%m-%dT%H:%M:%S")
            if ts >= since:
                entries.append(e)
        except (json.JSONDecodeError, ValueError):
            continue

    if not entries:
        return {"count": 0}

    freq = Counter(e.get("query", "").lower().strip() for e in entries)
    latencies = [e.get("ms", 0) for e in entries]
    avg_ms = sum(latencies) / max(len(latencies), 1)

    return {
        "count":       len(entries),
        "unique":      len(freq),
        "top_queries": freq.most_common(top_k),
        "avg_ms":      round(avg_ms, 1),
    }


# ── Word count ────────────────────────────────────────────────────────────────

def word_count() -> int:
    return sum(
        len(f.read_text(encoding="utf-8").split())
        for f in DOCS.rglob("*.md")
    )


# ── Report builder ────────────────────────────────────────────────────────────

def build_report(
    git_data: dict,
    cards: dict,
    hot: list[dict],
    queries: dict,
    days: int,
    include_cards: bool = True,
) -> str:
    date_str   = datetime.now().strftime("%Y-%m-%d")
    total_md   = len(list(DOCS.rglob("*.md")))
    total_wds  = word_count()

    lines = [
        f"# Еженедельный дайджест — {date_str}",
        "",
        f"_Период: последние {days} дней (с {git_data['since']})_",
        "",
        "## Итого",
        "",
        "| Метрика | Значение |",
        "|---------|---------|",
        f"| Коммитов за период | **{len(git_data['commits'])}** |",
        f"| Новых файлов | **{len(git_data['added'])}** |",
        f"| Изменённых файлов | **{len(git_data['modified'])}** |",
        f"| Всего MD файлов | **{total_md}** |",
        f"| Всего слов | **{total_wds:,}** |",
        "",
    ]

    # Card lifecycle
    if include_cards:
        pr = cards["promote_pct"]
        lines += [
            "## Жизненный цикл карточек",
            "",
            "| Статус | Кол-во |",
            "|--------|--------|",
            f"| ✅ approved | **{cards['approved']}** |",
            f"| ⚠️ normalized | {cards['normalized']} |",
            f"| ❌ raw | {cards['raw']} |",
            f"| Promote rate | **{pr}%** |",
            "",
        ]

    # Hot cards
    if hot:
        lines += ["## Горячие карточки (топ-5)", ""]
        for i, d in enumerate(hot[:5], 1):
            title = (d.get("title") or d.get("path", "?"))[:60]
            hot_s = d.get("_hot", 0)
            state = d.get("state", "raw")
            badge = {"approved": "✅", "normalized": "⚠️"}.get(state, "❌")
            lines.append(f"{i}. {badge} **{title}**  `hot={hot_s:.3f}`")
        lines.append("")

    # Query analytics
    if queries.get("count", 0) > 0:
        lines += [
            "## Запросы к gateway",
            "",
            f"**Запросов за период:** {queries['count']}  "
            f"**Уникальных:** {queries['unique']}  "
            f"**Avg latency:** {queries['avg_ms']}мс",
            "",
        ]
        if queries.get("top_queries"):
            lines += ["| Запрос | Частота |", "|--------|---------|"]
            for q, cnt in queries["top_queries"]:
                lines.append(f"| {q[:55]} | {cnt} |")
            lines.append("")

    # Commits
    if git_data["commits"]:
        lines += ["## Коммиты", "", "```"]
        for c in git_data["commits"][:15]:
            lines.append(c)
        lines += ["```", ""]

    # New markdown files
    md_added = [f for f in git_data["added"] if f.endswith(".md")]
    if md_added:
        lines += ["## Новые документы", ""]
        for f in md_added[:20]:
            lines.append(f"- `{f}`")
        lines.append("")

    # Active sections
    if git_data["folders"]:
        lines += [
            "## Активность по разделам",
            "",
            "| Раздел | Изменений |",
            "|--------|----------|",
        ]
        for folder, count in sorted(
            git_data["folders"].items(), key=lambda x: -x[1]
        )[:10]:
            lines.append(f"| `{folder}/` | {count} |")
        lines.append("")

    lines += [
        "---",
        "",
        f"_Сгенерировано: {datetime.now().strftime('%Y-%m-%d %H:%M')}_",
    ]
    return "\n".join(lines) + "\n"


# ── Main ──────────────────────────────────────────────────────────────────────

def main() -> int:
    args         = sys.argv[1:]
    days         = 7
    include_cards = "--no-cards" not in args

    i = 0
    while i < len(args):
        if args[i] == "--days" and i + 1 < len(args):
            days = int(args[i + 1]); i += 2
        else:
            i += 1

    print(f"Еженедельный дайджест (последние {days} дней)…")

    git_data = get_git_activity(days)
    cards    = get_card_stats() if include_cards else {}
    hot      = get_hot_cards(top_k=5)
    queries  = get_query_analytics(days=days)

    report = build_report(git_data, cards, hot, queries, days, include_cards)

    out = DOCS / "DIGEST_WEEKLY.md"
    out.write_text(report, encoding="utf-8")

    print(f"  Коммитов: {len(git_data['commits'])}")
    print(f"  Новых файлов: {len(git_data['added'])}")
    if include_cards:
        print(f"  Approved: {cards['approved']}  normalized: {cards['normalized']}  raw: {cards['raw']}")
    if hot:
        print(f"  Hot cards: {len(hot)} (топ: {(hot[0].get('title') or '?')[:40]})")
    if queries.get("count", 0) > 0:
        print(f"  Запросов: {queries['count']}  avg: {queries['avg_ms']}мс")
    print(f"\n✅ {out.relative_to(ROOT)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
