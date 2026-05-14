"""
improve_knowledge_snapshot.py — point-in-time KPI snapshot for Svyazi 2.0.

Captures a comprehensive health picture of the knowledge base:
  - Corpus: total docs, words, cards by state, promote rate
  - Search: Hit Rate@10 (from docs/PRECISION_EVAL.md), ANN index status
  - Graph: nodes, edges, avg degree, top PageRank hubs
  - Activity: recent commits, active sections (from git)
  - Quality: avg skill score (from .claude/skill_quality.json)

Outputs:
  docs/KNOWLEDGE_SNAPSHOT.md  — human-readable dashboard
  docs/snapshots/YYYYMMDD.json — timestamped machine-readable snapshot
                                 (enables longitudinal KPI trends)

Usage:
  python scripts/improve_knowledge_snapshot.py           # take snapshot
  python scripts/improve_knowledge_snapshot.py --trend   # show trend from history
  python scripts/improve_knowledge_snapshot.py --json    # JSON only (no files written)
"""

import json
import re
import subprocess
import sys
from datetime import datetime
from pathlib import Path

ROOT     = Path(__file__).parent.parent
DOCS     = ROOT / "docs"
SNAP_DIR = DOCS / "snapshots"
OUT_MD   = DOCS / "KNOWLEDGE_SNAPSHOT.md"


# ── Data collectors ───────────────────────────────────────────────────────────

def _git(*args) -> str:
    r = subprocess.run(["git"] + list(args), cwd=ROOT,
                       capture_output=True, text=True)
    return r.stdout.strip()


def _collect_corpus() -> dict:
    total = approved = normalized = raw = words = 0
    for md in DOCS.rglob("*.md"):
        if any(p in md.parts for p in ("obsidian",)):
            continue
        try:
            text = md.read_text(encoding="utf-8", errors="ignore")
        except Exception:
            continue
        total += 1
        words += len(text.split())
        m = re.search(r"^state:\s*(\S+)", text, re.MULTILINE)
        state = m.group(1).strip("\"'") if m else "raw"
        if state == "approved":
            approved += 1
        elif state == "normalized":
            normalized += 1
        else:
            raw += 1
    return {
        "docs":         total,
        "words":        words,
        "approved":     approved,
        "normalized":   normalized,
        "raw":          raw,
        "promote_pct":  round(approved / max(total, 1) * 100, 1),
    }


def _collect_search() -> dict:
    # Read Hit Rate from most recent PRECISION_EVAL.md
    hit_rate = None
    mean_mrr = None
    p = DOCS / "PRECISION_EVAL.md"
    if p.exists():
        text = p.read_text(encoding="utf-8")
        m = re.search(r"Hit Rate@\d+.*?\*\*([\d.]+)\*\*", text)
        if m:
            hit_rate = float(m.group(1))
        m = re.search(r"Mean MRR.*?\|([\s\d.]+)\|", text)
        if m:
            try:
                mean_mrr = float(m.group(1).strip())
            except ValueError:
                pass
    ann_built = (DOCS / "ann_meta.json").exists()
    return {
        "hit_rate_10": hit_rate,
        "mean_mrr":    mean_mrr,
        "ann_built":   ann_built,
    }


def _collect_graph() -> dict:
    p = DOCS / "CARD_GRAPH.json"
    if not p.exists():
        return {"built": False}
    data = json.loads(p.read_text(encoding="utf-8"))
    stats = data.get("stats", {})
    nodes = data.get("nodes", [])
    top_hubs = sorted(nodes, key=lambda n: -n.get("pagerank", 0))[:3]
    return {
        "built":      True,
        "nodes":      stats.get("nodes", len(nodes)),
        "edges":      stats.get("edges", 0),
        "isolated":   stats.get("isolated", 0),
        "top_hubs":   [{"id": n["id"], "pr": n.get("pagerank", 0)} for n in top_hubs],
    }


def _collect_skills() -> dict:
    p = ROOT / ".claude" / "skill_quality.json"
    if not p.exists():
        return {}
    data = json.loads(p.read_text(encoding="utf-8"))
    return {
        "count":     data.get("count", 0),
        "avg_score": data.get("avg_score", 0),
    }


def _collect_activity() -> dict:
    log = _git("log", "--since=7 days ago", "--oneline", "--no-merges")
    commits = [l for l in log.splitlines() if l.strip()]
    # Active sections from recent diffs
    diff = _git("diff", f"--name-only", f"HEAD~{max(len(commits), 1)}", "HEAD")
    sections: dict[str, int] = {}
    for f in diff.splitlines():
        parts = Path(f).parts
        sec = parts[1] if len(parts) > 2 else parts[0]
        sections[str(sec)] = sections.get(str(sec), 0) + 1
    top_sections = sorted(sections.items(), key=lambda x: -x[1])[:3]
    return {
        "commits_7d":    len(commits),
        "top_sections":  top_sections,
    }


def _collect_queries() -> dict:
    p = ROOT / ".claude" / "query_log.jsonl"
    if not p.exists():
        return {"count": 0}
    lines = p.read_text(encoding="utf-8").splitlines()
    return {"count": len([l for l in lines if l.strip()])}


# ── Snapshot assembly ─────────────────────────────────────────────────────────

def take_snapshot() -> dict:
    ts = datetime.now().strftime("%Y-%m-%dT%H:%M:%S")
    return {
        "ts":       ts,
        "date":     ts[:10],
        "corpus":   _collect_corpus(),
        "search":   _collect_search(),
        "graph":    _collect_graph(),
        "skills":   _collect_skills(),
        "activity": _collect_activity(),
        "queries":  _collect_queries(),
    }


# ── Trend loading ─────────────────────────────────────────────────────────────

def load_history(limit: int = 10) -> list[dict]:
    if not SNAP_DIR.exists():
        return []
    snaps = sorted(SNAP_DIR.glob("*.json"), key=lambda p: p.stem, reverse=True)
    result = []
    for p in snaps[:limit]:
        try:
            result.append(json.loads(p.read_text(encoding="utf-8")))
        except Exception:
            continue
    return result


# ── Report ────────────────────────────────────────────────────────────────────

def build_report(snap: dict, history: list[dict]) -> str:
    c  = snap["corpus"]
    s  = snap["search"]
    g  = snap["graph"]
    sk = snap["skills"]
    a  = snap["activity"]
    q  = snap["queries"]

    hit_rate_str = f"{s['hit_rate_10']:.3f}" if s.get("hit_rate_10") else "—"
    mrr_str      = f"{s['mean_mrr']:.3f}"    if s.get("mean_mrr")    else "—"
    skill_str    = f"{sk['avg_score']}/100"  if sk.get("avg_score")  else "—"

    lines = [
        "# Knowledge Snapshot — Svyazi 2.0",
        "",
        f"_Сгенерировано: {snap['ts']}_",
        "",
        "## Корпус знаний",
        "",
        "| Метрика | Значение |",
        "|---------|---------|",
        f"| Документов (MD) | **{c['docs']}** |",
        f"| Всего слов | **{c['words']:,}** |",
        f"| ✅ Approved | **{c['approved']}** |",
        f"| ⚠️ Normalized | {c['normalized']} |",
        f"| ❌ Raw | {c['raw']} |",
        f"| Promote rate | **{c['promote_pct']}%** |",
        "",
        "## Поиск",
        "",
        "| Метрика | Значение |",
        "|---------|---------|",
        f"| Hit Rate@10 | **{hit_rate_str}** (порог ≥ 0.70) |",
        f"| Mean MRR | {mrr_str} |",
        f"| ANN index | {'✅ built' if s.get('ann_built') else '⚠️ not built'} |",
        f"| Запросов в лог | {q.get('count', 0)} |",
        "",
        "## Граф знаний",
        "",
    ]
    if g.get("built"):
        edges_per_node = round(g["edges"] / max(g["nodes"], 1), 1)
        lines += [
            "| Метрика | Значение |",
            "|---------|---------|",
            f"| Узлов | {g['nodes']} |",
            f"| Рёбер | {g['edges']} |",
            f"| Среднее out-degree | {edges_per_node} |",
            f"| Изолированных | {g.get('isolated', 0)} |",
            "",
            "**Топ-3 хаба:**",
            "",
        ]
        for h in g.get("top_hubs", []):
            lines.append(f"- `{h['id']}` (pagerank={h['pr']:.3f})")
        lines.append("")
    else:
        lines += ["_Граф не построен. Запустите `improve_card_graph.py`._", ""]

    lines += [
        "## Качество скилов",
        "",
        f"**Скилов:** {sk.get('count', 0)}  **Средний балл:** {skill_str}",
        "",
        "## Git активность (7 дней)",
        "",
        f"**Коммитов:** {a['commits_7d']}",
    ]
    if a.get("top_sections"):
        lines += ["", "Активные секции:"]
        for sec, cnt in a["top_sections"]:
            lines.append(f"- `{sec}/` — {cnt} изменений")
    lines.append("")

    # Historical trend table
    if history:
        lines += [
            "## Тренд (последние снапшоты)",
            "",
            "| Дата | Docs | Approved | Hit Rate | Skills |",
            "|------|------|---------|---------|--------|",
        ]
        for h in history[:7]:
            hc = h.get("corpus", {})
            hs = h.get("search", {})
            hsk = h.get("skills", {})
            hr_str = f"{hs['hit_rate_10']:.3f}" if hs.get("hit_rate_10") else "—"
            sk_str = str(hsk.get("avg_score", "—"))
            lines.append(
                f"| {h.get('date','?')} | {hc.get('docs','?')} "
                f"| {hc.get('approved','?')} | {hr_str} | {sk_str} |"
            )
        lines.append("")

    return "\n".join(lines) + "\n"


# ── Main ──────────────────────────────────────────────────────────────────────

def main() -> int:
    args      = sys.argv[1:]
    json_only = "--json" in args
    trend     = "--trend" in args

    snap    = take_snapshot()
    history = load_history()

    if json_only:
        print(json.dumps(snap, ensure_ascii=False, indent=2))
        return 0

    if trend:
        history_with_current = [snap] + history
        print(f"{'Date':<12} {'Docs':<6} {'Approved':<10} {'HitRate':<10} {'Skills'}")
        print("-" * 55)
        for h in history_with_current[:10]:
            hc  = h.get("corpus", {})
            hs  = h.get("search", {})
            hsk = h.get("skills", {})
            hr  = f"{hs['hit_rate_10']:.3f}" if hs.get("hit_rate_10") else "—"
            sk  = str(hsk.get("avg_score", "—"))
            print(f"{h.get('date','?'):<12} {hc.get('docs','?'):<6} {hc.get('approved','?'):<10} {hr:<10} {sk}")
        return 0

    # Save snapshot
    SNAP_DIR.mkdir(parents=True, exist_ok=True)
    snap_file = SNAP_DIR / f"{snap['date']}.json"
    snap_file.write_text(json.dumps(snap, ensure_ascii=False, indent=2), encoding="utf-8")

    report = build_report(snap, history)
    OUT_MD.write_text(report, encoding="utf-8")

    c = snap["corpus"]
    s = snap["search"]
    print(f"📸 Knowledge Snapshot — {snap['date']}")
    print(f"   Docs:       {c['docs']}  ({c['words']:,} words)")
    print(f"   Approved:   {c['approved']} / promote rate {c['promote_pct']}%")
    hit = s.get("hit_rate_10")
    print(f"   Hit Rate@10: {hit:.3f}" if hit else "   Hit Rate@10: —")
    if snap["skills"].get("avg_score"):
        print(f"   Skill quality: {snap['skills']['avg_score']}/100")
    print(f"\n✅ {OUT_MD.relative_to(ROOT)}")
    print(f"✅ {snap_file.relative_to(ROOT)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
