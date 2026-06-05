"""
improve_feedback_loop.py — close the search-corpus feedback loop.

Reads .claude/query_log.jsonl (written by gateway.py), identifies:
  - Zero-result queries  → hard gaps (no related content at all)
  - Low-result queries   → soft gaps (< 3 results, needs more content)
  - Repeated queries     → high-demand topics (invest in more coverage)

For each gap, finds the best matching existing cards via BM25 and suggests:
  a) Cross-link the gap query to those cards (improve discoverability)
  b) Create a stub card for the topic (content gap)
  c) Merge related partial cards (consolidation)

Outputs:
  docs/FEEDBACK_LOOP.md  — gap analysis report
  .claude/gap_queue.jsonl — machine-readable gap queue for automation

With --apply: creates stub cards in docs/cards/generated/ for hard gaps.

Usage:
  python scripts/improve_feedback_loop.py           # analyse gaps
  python scripts/improve_feedback_loop.py --apply   # create stub cards
  python scripts/improve_feedback_loop.py --days 30 # look back 30 days
  python scripts/improve_feedback_loop.py --json    # JSON output
"""

import json
import math
import re
import sys
from collections import Counter
from datetime import datetime, timedelta
from pathlib import Path

ROOT     = Path(__file__).parent.parent
DOCS     = ROOT / "docs"
LOG_FILE = ROOT / ".claude" / "query_log.jsonl"
OUT_MD   = DOCS / "FEEDBACK_LOOP.md"
OUT_JSON = ROOT / ".claude" / "gap_queue.jsonl"

_STOPWORDS = {
    "и","в","на","что","как","это","для","или","но","по","к","из","а","не",
    "с","о","от","за","до","то","же","при","уже","так","ещё","бы","ли",
    "the","a","an","of","in","to","is","for","with","by","and","or","but",
}


# ── Log loading ───────────────────────────────────────────────────────────────

def load_log(days: int = 7) -> list[dict]:
    if not LOG_FILE.exists():
        return []
    since = datetime.now() - timedelta(days=days)
    entries = []
    for line in LOG_FILE.read_text(encoding="utf-8").splitlines():
        try:
            e = json.loads(line)
            ts = datetime.strptime(e.get("ts", "2000-01-01"), "%Y-%m-%dT%H:%M:%S")
            if ts >= since:
                entries.append(e)
        except (json.JSONDecodeError, ValueError):
            continue
    return entries


# ── Gap detection ─────────────────────────────────────────────────────────────

def detect_gaps(entries: list[dict]) -> dict:
    zero_result  = []
    low_result   = []
    freq         = Counter()

    for e in entries:
        q = e.get("query", "").strip()
        if not q:
            continue
        q_norm = q.lower().strip(" .?!")
        freq[q_norm] += 1
        r = e.get("results", 10)
        if r == 0:
            zero_result.append(q_norm)
        elif r < 3:
            low_result.append(q_norm)

    # Deduplicate while preserving order
    zero_uniq = list(dict.fromkeys(zero_result))
    low_uniq  = list(dict.fromkeys(low_result))

    # High-demand: queries asked 3+ times
    high_demand = [(q, c) for q, c in freq.most_common(20) if c >= 2]

    return {
        "zero_result":  zero_uniq,
        "low_result":   low_uniq,
        "high_demand":  high_demand,
        "total":        len(entries),
        "unique":       len(freq),
    }


# ── BM25 search over index for gap analysis ───────────────────────────────────

_INDEX: list[dict] | None = None


def _load_index() -> list[dict]:
    global _INDEX
    if _INDEX is None:
        p = DOCS / "search_index.json"
        _INDEX = json.loads(p.read_text(encoding="utf-8")) if p.exists() else []
    return _INDEX


def _tok(text: str) -> list[str]:
    return [t for t in re.findall(r"[а-яёa-z0-9]{3,}", text.lower())
            if t not in _STOPWORDS]


def _bm25_top(query: str, top_k: int = 3) -> list[dict]:
    docs   = _load_index()
    tokens = _tok(query)
    if not tokens or not docs:
        return []
    N     = len(docs)
    k1, b = 1.5, 0.75
    df    = Counter()
    for d in docs:
        words = set(_tok((d.get("title") or "") + " " + (d.get("content") or "")))
        df.update(words)
    idf = {t: math.log((N - df.get(t, 0) + 0.5) / (df.get(t, 0) + 0.5) + 1)
           for t in set(tokens)}
    scored = []
    for d in docs:
        words = _tok((d.get("title") or "") + " " + (d.get("content") or ""))
        dl    = max(len(words), 1)
        avgdl = 100  # approximate
        score = sum(
            idf.get(t, 0) * (words.count(t) * (k1 + 1))
            / (words.count(t) + k1 * (1 - b + b * dl / avgdl))
            for t in tokens
        )
        if score > 0:
            scored.append((score, d))
    scored.sort(key=lambda x: x[0], reverse=True)
    return [d for _, d in scored[:top_k]]


# ── Stub card generator ───────────────────────────────────────────────────────

def _create_stub(query: str, related: list[dict]) -> Path:
    """Create a minimal stub card for a gap topic."""
    slug = re.sub(r"[^\w\s-]", "", query.lower()).strip()
    slug = re.sub(r"[\s_]+", "-", slug)[:50]
    out_dir = DOCS / "cards" / "generated"
    out_dir.mkdir(parents=True, exist_ok=True)
    out = out_dir / f"{slug}.md"

    related_links = "\n".join(
        f"- [{d.get('title', d.get('path','?'))[:60]}]({d.get('path', '')})"
        for d in related[:3]
    )

    content = f"""---
state: raw
generated_from: feedback_loop
query: "{query}"
created: {datetime.now().strftime('%Y-%m-%d')}
tags: [gap, generated]
---
# {query.title()}

<!-- summary -->
> Тема требует более подробного освещения. Создано автоматически как заглушка для запроса «{query}».

<!-- tags: gap, generated -->

## Связанные материалы

{related_links or '_Связанных материалов не найдено._'}

## Описание

_TODO: наполнить этот раздел._
"""
    out.write_text(content, encoding="utf-8")
    return out


# ── Report builder ────────────────────────────────────────────────────────────

def build_report(gaps: dict, related_map: dict[str, list[dict]]) -> str:
    date = datetime.now().strftime("%Y-%m-%d")

    if gaps["total"] == 0:
        return (
            f"# Feedback Loop — Svyazi 2.0\n\n_Сгенерировано: {date}_\n\n"
            "_Лог запросов пуст. Запустите gateway.py и сделайте несколько запросов._\n"
        )

    lines = [
        "# Feedback Loop — Svyazi 2.0",
        "",
        f"_Сгенерировано: {date}_",
        "",
        f"**Всего запросов:** {gaps['total']}  "
        f"**Уникальных:** {gaps['unique']}  "
        f"**Нет результатов:** {len(gaps['zero_result'])}  "
        f"**Мало результатов:** {len(gaps['low_result'])}",
        "",
    ]

    if gaps["zero_result"]:
        lines += [
            "## Критические пробелы (0 результатов)",
            "",
            "Эти запросы не нашли ни одного релевантного документа:",
            "",
        ]
        for q in gaps["zero_result"][:15]:
            related = related_map.get(q, [])
            rel_str = ", ".join(f"`{d.get('title','?')[:30]}`" for d in related[:2])
            lines.append(f"- **`{q}`**" + (f" → возможно связано: {rel_str}" if rel_str else ""))
        lines.append("")

    if gaps["low_result"]:
        lines += [
            "## Слабые зоны (< 3 результатов)",
            "",
        ]
        for q in gaps["low_result"][:10]:
            lines.append(f"- `{q}`")
        lines.append("")

    if gaps["high_demand"]:
        lines += [
            "## Высокоспросные темы (≥ 2 запросов)",
            "",
            "| Запрос | Частота |",
            "|--------|---------|",
        ]
        for q, cnt in gaps["high_demand"][:10]:
            lines.append(f"| {q[:55]} | **{cnt}** |")
        lines.append("")

    lines += [
        "## Рекомендации",
        "",
        "1. **Критические пробелы** → создать карточки-заглушки (`--apply`)",
        "2. **Слабые зоны** → обогатить существующие карточки (`improve_gap_filler.py`)",
        "3. **Высокоспросные темы** → приоритизировать в следующем цикле обогащения",
    ]
    return "\n".join(lines) + "\n"


# ── Main ──────────────────────────────────────────────────────────────────────

def main() -> int:
    args      = sys.argv[1:]
    apply     = "--apply" in args
    json_out  = "--json" in args
    days      = 7

    i = 0
    while i < len(args):
        if args[i] == "--days" and i + 1 < len(args):
            days = int(args[i + 1]); i += 2
        else:
            i += 1

    entries = load_log(days=days)
    gaps    = detect_gaps(entries)

    # Find related docs for each zero-result query
    related_map: dict[str, list[dict]] = {}
    for q in gaps["zero_result"][:15]:
        related_map[q] = _bm25_top(q, top_k=3)

    if json_out:
        print(json.dumps({
            "zero_result":  gaps["zero_result"],
            "low_result":   gaps["low_result"],
            "high_demand":  gaps["high_demand"],
            "total":        gaps["total"],
        }, ensure_ascii=False, indent=2))
        return 0

    report = build_report(gaps, related_map)
    OUT_MD.write_text(report, encoding="utf-8")

    # Save gap queue
    OUT_JSON.parent.mkdir(parents=True, exist_ok=True)
    with OUT_JSON.open("a", encoding="utf-8") as f:
        for q in gaps["zero_result"]:
            f.write(json.dumps({
                "ts":    datetime.now().strftime("%Y-%m-%dT%H:%M:%S"),
                "query": q,
                "type":  "zero_result",
            }, ensure_ascii=False) + "\n")

    print(f"🔄 Feedback Loop  (last {days} days)")
    print(f"   Запросов: {gaps['total']}  уникальных: {gaps['unique']}")
    print(f"   Критических пробелов: {len(gaps['zero_result'])}")
    print(f"   Слабых зон: {len(gaps['low_result'])}")
    print(f"   Высокоспросных тем: {len(gaps['high_demand'])}")

    created = []
    if apply and gaps["zero_result"]:
        print(f"\n  Создаю заглушки для {len(gaps['zero_result'][:10])} пробелов…")
        for q in gaps["zero_result"][:10]:
            related = related_map.get(q, [])
            stub = _create_stub(q, related)
            created.append(stub)
            print(f"  ✅ {stub.relative_to(ROOT)}")

    print(f"\n✅ {OUT_MD.relative_to(ROOT)}")
    if gaps["total"] == 0:
        print("\n  (Лог пустой — запусти gateway.py и сделай несколько /api/ask запросов)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
