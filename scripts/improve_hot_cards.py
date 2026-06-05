"""
improve_hot_cards.py — surface "hot" cards for Svyazi 2.0.

A card is "hot" when multiple independent signals agree it is relevant:
  1. PageRank (graph topology) — high in-degree from authoritative cards
  2. Query frequency (usage) — appeared in search results recently
  3. Promote state — approved cards rank higher than normalized/raw
  4. Summary quality — cards with long rich summaries preferred

Composite hot-score (0-1):
  hot = 0.40 × pr_norm
      + 0.30 × query_freq_norm
      + 0.20 × state_bonus        (approved=1.0, normalized=0.5, raw=0.1)
      + 0.10 × summary_quality    (len(summary)/350, capped at 1.0)

Outputs:
  docs/HOT_CARDS.md  — top-50 hot cards with scores
  .claude/hot_cards.json — machine-readable for gateway/other scripts

Usage:
  python scripts/improve_hot_cards.py           # generate report
  python scripts/improve_hot_cards.py --top 20  # top N
  python scripts/improve_hot_cards.py --json    # JSON only
  python scripts/improve_hot_cards.py --state approved  # filter by state
"""

import json
import re
import sys
from collections import Counter
from datetime import datetime
from pathlib import Path

ROOT       = Path(__file__).parent.parent
DOCS       = ROOT / "docs"
GRAPH_PATH = DOCS / "CARD_GRAPH.json"
INDEX_PATH = DOCS / "search_index.json"
LOG_FILE   = ROOT / ".claude" / "query_log.jsonl"
OUT_MD     = DOCS / "HOT_CARDS.md"
OUT_JSON   = ROOT / ".claude" / "hot_cards.json"

_PR_CAP = 0.4  # same cap used by gateway


# ── Data loading ──────────────────────────────────────────────────────────────

def _load_index() -> list[dict]:
    if not INDEX_PATH.exists():
        return []
    return json.loads(INDEX_PATH.read_text(encoding="utf-8"))


def _load_pagerank() -> dict[str, float]:
    if not GRAPH_PATH.exists():
        return {}
    data = json.loads(GRAPH_PATH.read_text(encoding="utf-8"))
    return {n["id"]: min(n.get("pagerank", 0), _PR_CAP)
            for n in data.get("nodes", [])}


def _load_query_freq() -> Counter:
    """Count how many times each result-path appeared in search logs."""
    # We don't have per-result logging yet; approximate from query keywords
    # matching card titles/tags — simple but effective for now.
    if not LOG_FILE.exists():
        return Counter()
    counts: Counter = Counter()
    for line in LOG_FILE.read_text(encoding="utf-8").splitlines():
        try:
            e = json.loads(line)
            counts[e.get("query", "").lower()] += 1
        except json.JSONDecodeError:
            continue
    return counts


def _state_bonus(state: str) -> float:
    return {"approved": 1.0, "normalized": 0.5}.get(state, 0.1)


def _summary_quality(summary: str) -> float:
    if not summary:
        return 0.0
    return min(len(summary) / 350, 1.0)


def _tokenize(text: str) -> list[str]:
    return re.findall(r"[а-яёa-z0-9]{3,}", text.lower())


# ── Scoring ───────────────────────────────────────────────────────────────────

def compute_hot_scores(
    docs: list[dict],
    pagerank: dict[str, float],
    query_counts: Counter,
) -> list[dict]:
    """Return docs annotated with hot-score, sorted descending."""

    # Query-frequency signal: for each doc, sum query counts that mention
    # any token from title/tags
    def _query_relevance(d: dict) -> float:
        tokens = set(_tokenize((d.get("title") or "") + " " + " ".join(d.get("tags") or [])))
        score = 0
        for q, cnt in query_counts.items():
            if any(t in q for t in tokens):
                score += cnt
        return score

    # Pre-compute raw signals
    pr_raw    = {d.get("path", ""): pagerank.get(d.get("path", ""), 0) for d in docs}
    qf_raw    = {d.get("path", ""): _query_relevance(d) for d in docs}

    # Normalise to [0, 1]
    pr_max = max(pr_raw.values(), default=1) or 1
    qf_max = max(qf_raw.values(), default=1) or 1

    scored = []
    for d in docs:
        path = d.get("path", "")
        state   = d.get("state", "raw")
        summary = d.get("summary") or ""

        pr_norm = pr_raw[path] / pr_max
        qf_norm = qf_raw[path] / qf_max
        sb      = _state_bonus(state)
        sq      = _summary_quality(summary)

        hot = (0.40 * pr_norm +
               0.30 * qf_norm +
               0.20 * sb      +
               0.10 * sq)

        scored.append({
            **d,
            "_hot":        round(hot, 4),
            "_pr":         round(pr_raw[path], 4),
            "_qf":         round(qf_norm, 4),
            "_state_bonus": sb,
        })

    scored.sort(key=lambda x: x["_hot"], reverse=True)
    return scored


# ── Report ────────────────────────────────────────────────────────────────────

def build_report(scored: list[dict], top_n: int = 50) -> str:
    date  = datetime.now().strftime("%Y-%m-%d")
    top   = scored[:top_n]
    total = len(scored)

    lines = [
        "# Hot Cards — Svyazi 2.0",
        "",
        f"_Сгенерировано: {date}_",
        "",
        f"**Карточек всего:** {total}  "
        f"**Показано топ:** {min(top_n, total)}",
        "",
        "Горячий балл = 0.40×PageRank + 0.30×query_freq + 0.20×state + 0.10×summary_quality",
        "",
        "## Топ горячих карточек",
        "",
        "| # | Hot | PR | QF | State | Путь |",
        "|---|-----|----|----|-------|------|",
    ]

    for i, d in enumerate(top, 1):
        state = d.get("state", "raw")
        badge = {"approved": "✅", "normalized": "⚠️"}.get(state, "❌")
        title = (d.get("title") or d.get("path", "?"))[:55]
        lines.append(
            f"| {i} | {d['_hot']:.3f} | {d['_pr']:.3f} | {d['_qf']:.3f} "
            f"| {badge} | `{d.get('path','')[:50]}` · {title} |"
        )

    return "\n".join(lines) + "\n"


# ── Public API ────────────────────────────────────────────────────────────────

def hot_cards(top_k: int = 20, state_filter: str = "") -> list[dict]:
    """Return top-k hot cards. Usable by gateway or other scripts."""
    docs     = _load_index()
    pr       = _load_pagerank()
    qf       = _load_query_freq()
    scored   = compute_hot_scores(docs, pr, qf)
    if state_filter:
        scored = [d for d in scored if d.get("state") == state_filter]
    return scored[:top_k]


# ── Main ──────────────────────────────────────────────────────────────────────

def main() -> int:
    args         = sys.argv[1:]
    top_n        = 50
    json_out     = "--json" in args
    state_filter = ""

    i = 0
    while i < len(args):
        if args[i] == "--top" and i + 1 < len(args):
            top_n = int(args[i + 1]); i += 2
        elif args[i] == "--state" and i + 1 < len(args):
            state_filter = args[i + 1]; i += 2
        else:
            i += 1

    docs   = _load_index()
    pr     = _load_pagerank()
    qf     = _load_query_freq()

    if not docs:
        print("⚠  search_index.json не найден.")
        return 1
    if not pr:
        print("⚠  CARD_GRAPH.json не найден. Запустите: python scripts/improve_card_graph.py")

    scored = compute_hot_scores(docs, pr, qf)
    if state_filter:
        scored = [d for d in scored if d.get("state") == state_filter]

    if json_out:
        print(json.dumps(scored[:top_n], ensure_ascii=False, indent=2))
        return 0

    report = build_report(scored, top_n)
    OUT_MD.write_text(report, encoding="utf-8")

    # Machine-readable snapshot
    OUT_JSON.parent.mkdir(parents=True, exist_ok=True)
    OUT_JSON.write_text(
        json.dumps({
            "generated": datetime.now().strftime("%Y-%m-%dT%H:%M:%S"),
            "total":     len(scored),
            "top":       scored[:top_n],
        }, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )

    top10 = scored[:10]
    print(f"🔥 Hot Cards  (total={len(scored)}, state_filter={state_filter or 'all'})")
    for i, d in enumerate(top10, 1):
        title = (d.get("title") or d.get("path", "?"))[:60]
        print(f"  {i:2d}. [{d['_hot']:.3f}]  {title}")
    print(f"\n✅ {OUT_MD.relative_to(ROOT)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
