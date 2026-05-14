"""
improve_query_log.py — query analytics for Svyazi 2.0 gateway.

Reads .claude/query_log.jsonl (written by gateway.py on every search request)
and produces docs/QUERY_ANALYTICS.md with:
  - Top queries by frequency
  - Latency distribution (p50 / p95 / p99)
  - Query patterns by hour of day
  - Search source breakdown (ask / search / chat)
  - Zero-result queries (need corpus gaps filled)

Usage:
  python scripts/improve_query_log.py           # generate report
  python scripts/improve_query_log.py --top 20  # top 20 queries
  python scripts/improve_query_log.py --json    # JSON output
  python scripts/improve_query_log.py --tail 50 # last 50 log lines
"""

import json
import math
import sys
from collections import Counter, defaultdict
from datetime import datetime
from pathlib import Path

ROOT      = Path(__file__).parent.parent
LOG_FILE  = ROOT / ".claude" / "query_log.jsonl"
OUT_MD    = ROOT / "docs" / "QUERY_ANALYTICS.md"


# ── Log loading ───────────────────────────────────────────────────────────────

def load_log(max_lines: int = 0) -> list[dict]:
    if not LOG_FILE.exists():
        return []
    entries = []
    lines = LOG_FILE.read_text(encoding="utf-8").splitlines()
    if max_lines:
        lines = lines[-max_lines:]
    for line in lines:
        line = line.strip()
        if not line:
            continue
        try:
            entries.append(json.loads(line))
        except json.JSONDecodeError:
            continue
    return entries


# ── Analytics ─────────────────────────────────────────────────────────────────

def percentile(values: list[float], p: float) -> float:
    if not values:
        return 0.0
    sorted_v = sorted(values)
    idx = int(math.ceil(p / 100 * len(sorted_v))) - 1
    return sorted_v[max(0, idx)]


def analyse(entries: list[dict]) -> dict:
    if not entries:
        return {"count": 0}

    queries       = [e.get("query", "") for e in entries]
    latencies     = [e.get("ms", 0) for e in entries if e.get("ms") is not None]
    sources       = Counter(e.get("source", "unknown") for e in entries)
    zero_results  = [e.get("query", "") for e in entries if e.get("results", 1) == 0]

    # Normalise queries (lowercase, strip punctuation)
    def _norm(q: str) -> str:
        return q.lower().strip(" .?!")

    freq = Counter(_norm(q) for q in queries if q)

    # Hour-of-day pattern
    hour_counts: dict[int, int] = defaultdict(int)
    for e in entries:
        ts = e.get("ts", "")
        try:
            hour = int(ts[11:13])
            hour_counts[hour] += 1
        except (ValueError, IndexError):
            pass

    # Avg results per query
    result_counts = [e.get("results", 0) for e in entries]
    avg_results = sum(result_counts) / max(len(result_counts), 1)

    return {
        "count":        len(entries),
        "unique":       len(freq),
        "top_queries":  freq.most_common(20),
        "zero_results": list(dict.fromkeys(zero_results))[:20],  # dedup
        "sources":      dict(sources),
        "avg_results":  round(avg_results, 1),
        "latency": {
            "p50":  round(percentile(latencies, 50), 1),
            "p95":  round(percentile(latencies, 95), 1),
            "p99":  round(percentile(latencies, 99), 1),
            "avg":  round(sum(latencies) / max(len(latencies), 1), 1),
        },
        "by_hour": dict(sorted(hour_counts.items())),
        "first_ts": entries[0].get("ts", ""),
        "last_ts":  entries[-1].get("ts", ""),
    }


# ── Report ────────────────────────────────────────────────────────────────────

def build_report(stats: dict) -> str:
    date = datetime.now().strftime("%Y-%m-%d")

    if stats.get("count", 0) == 0:
        return (
            f"# Query Analytics — Svyazi 2.0\n\n"
            f"_Сгенерировано: {date}_\n\n"
            "_Лог запросов пуст. Запросы записываются при обращении к gateway.py._\n"
        )

    lines = [
        "# Query Analytics — Svyazi 2.0",
        "",
        f"_Сгенерировано: {date}_",
        f"_Период: {stats['first_ts']} — {stats['last_ts']}_",
        "",
        f"**Всего запросов:** {stats['count']}  "
        f"**Уникальных:** {stats['unique']}  "
        f"**Среднее результатов:** {stats['avg_results']}",
        "",
        "## Латентность",
        "",
        "| p50 | p95 | p99 | avg |",
        "|-----|-----|-----|-----|",
        f"| {stats['latency']['p50']}мс | {stats['latency']['p95']}мс "
        f"| {stats['latency']['p99']}мс | {stats['latency']['avg']}мс |",
        "",
        "## Источники запросов",
        "",
        "| Источник | Запросов |",
        "|---------|---------|",
    ]
    for src, cnt in sorted(stats["sources"].items(), key=lambda x: -x[1]):
        lines.append(f"| `{src}` | {cnt} |")

    lines += [
        "",
        "## Топ запросов",
        "",
        "| # | Запрос | Частота |",
        "|---|--------|---------|",
    ]
    for i, (q, cnt) in enumerate(stats["top_queries"][:20], 1):
        lines.append(f"| {i} | {q[:60]} | {cnt} |")

    if stats.get("zero_results"):
        lines += [
            "",
            "## Запросы без результатов (пробелы в корпусе)",
            "",
        ]
        for q in stats["zero_results"][:10]:
            lines.append(f"- `{q}`")

    if stats.get("by_hour"):
        lines += ["", "## Активность по часам", "", "```"]
        max_cnt = max(stats["by_hour"].values(), default=1)
        for h in range(24):
            cnt   = stats["by_hour"].get(h, 0)
            bar   = "█" * int(cnt / max_cnt * 30)
            lines.append(f"  {h:02d}:00  {bar} {cnt}")
        lines.append("```")

    return "\n".join(lines) + "\n"


# ── Main ──────────────────────────────────────────────────────────────────────

def main() -> int:
    args      = sys.argv[1:]
    top_n     = 20
    json_out  = "--json" in args
    tail      = 0

    i = 0
    while i < len(args):
        if args[i] == "--top" and i + 1 < len(args):
            top_n = int(args[i + 1]); i += 2
        elif args[i] == "--tail" and i + 1 < len(args):
            tail = int(args[i + 1]); i += 2
        else:
            i += 1

    entries = load_log(max_lines=tail)
    stats   = analyse(entries)

    if json_out:
        print(json.dumps(stats, ensure_ascii=False, indent=2))
        return 0

    report = build_report(stats)
    OUT_MD.write_text(report, encoding="utf-8")

    count = stats.get("count", 0)
    if count == 0:
        print("⚠  Лог запросов пуст. Запустите gateway.py и сделайте несколько запросов.")
    else:
        print(f"📊 Query Analytics")
        print(f"   Запросов:  {count}")
        print(f"   Уникальных: {stats['unique']}")
        print(f"   p50 latency: {stats['latency']['p50']}мс")
        print(f"   Нет результатов: {len(stats.get('zero_results', []))}")
        print(f"\n✅ {OUT_MD.relative_to(ROOT)}")

        if stats.get("top_queries"):
            print("\n— Топ запросов —")
            for q, cnt in stats["top_queries"][:10]:
                print(f"  {cnt:3d}×  {q[:60]}")

    return 0


if __name__ == "__main__":
    sys.exit(main())
