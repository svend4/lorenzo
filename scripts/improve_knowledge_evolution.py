"""
improve_knowledge_evolution.py — трекер эволюции базы знаний Svyazi 2.0.

Делает снапшот ключевых KPI и сохраняет историю в docs/KNOWLEDGE_EVOLUTION.md.
Каждый запуск добавляет строку в таблицу: дата, карточки, lifecycle, proposals,
RFC, индексы, proposals coverage.

Использование:
  python scripts/improve_knowledge_evolution.py          # снапшот + отчёт
  python scripts/improve_knowledge_evolution.py --stats  # только текущие KPI
  python scripts/improve_knowledge_evolution.py --plot   # ASCII-график трендов
"""
import re
import sys
import json
from pathlib import Path
from datetime import datetime

ROOT  = Path(__file__).parent.parent
DOCS  = ROOT / "docs"
OUT   = DOCS / "KNOWLEDGE_EVOLUTION.md"
HIST  = DOCS / "knowledge_evolution.json"


def _count_cards_by_state() -> dict[str, int]:
    state_re = re.compile(r"^state:\s*(\S+)", re.MULTILINE)
    counts: dict[str, int] = {}
    for p in DOCS.rglob("*.md"):
        if "obsidian" in p.parts:
            continue
        if p.parent == DOCS and p.stem.isupper():
            continue
        try:
            text = p.read_text(encoding="utf-8", errors="ignore")
        except Exception:
            continue
        m = state_re.search(text)
        state = m.group(1) if m else "raw"
        counts[state] = counts.get(state, 0) + 1
    return counts


def _count_rfcs() -> dict[str, int]:
    rfcs_dir = DOCS / "rfcs"
    if not rfcs_dir.exists():
        return {"total": 0}
    status_re = re.compile(r"^status:\s*(\S+)", re.MULTILINE)
    counts: dict[str, int] = {"total": 0}
    for p in rfcs_dir.glob("RFC-*.md"):
        try:
            text = p.read_text(encoding="utf-8", errors="ignore")
        except Exception:
            continue
        m = status_re.search(text)
        status = m.group(1) if m else "Draft"
        counts[status] = counts.get(status, 0) + 1
        counts["total"] += 1
    return counts


def _count_proposals() -> int:
    proposals_dir = DOCS / "04-ai-collaborations" / "proposals"
    if not proposals_dir.exists():
        return 0
    return len(list(proposals_dir.glob("proposal-*.md")))


def _count_total_docs() -> int:
    n = 0
    for p in DOCS.rglob("*.md"):
        if "obsidian" not in p.parts:
            n += 1
    return n


def _index_sizes() -> dict[str, int]:
    result: dict[str, int] = {}
    si = DOCS / "search_index.json"
    if si.exists():
        try:
            data = json.loads(si.read_text(encoding="utf-8"))
            result["search_index"] = len(data) if isinstance(data, list) else 0
        except Exception:
            result["search_index"] = 0

    sem = DOCS / "semantic_index.json"
    if sem.exists():
        try:
            data = json.loads(sem.read_text(encoding="utf-8"))
            if isinstance(data, dict):
                result["semantic_index"] = data.get("meta", {}).get("docs", 0) or data.get("doc_count", 0)
            else:
                result["semantic_index"] = 0
        except Exception:
            result["semantic_index"] = 0

    passages = DOCS / "passages.json"
    if not passages.exists():
        passages = ROOT / "passages.json"
    if passages.exists():
        try:
            data = json.loads(passages.read_text(encoding="utf-8"))
            if isinstance(data, list):
                result["passages"] = len(data)
            elif isinstance(data, dict):
                result["passages"] = len(data.get("passages", data.get("docs", [])))
            else:
                result["passages"] = 0
        except Exception:
            result["passages"] = 0

    return result


def snapshot() -> dict:
    states  = _count_cards_by_state()
    rfcs    = _count_rfcs()
    indexes = _index_sizes()
    total   = _count_total_docs()

    approved   = states.get("approved", 0)
    normalized = states.get("normalized", 0)
    raw        = states.get("raw", 0)
    decayed    = states.get("decayed", 0)
    lifecycle_total = approved + normalized + raw + decayed

    promote_rate = round((approved + normalized) / lifecycle_total * 100, 1) if lifecycle_total else 0.0

    return {
        "date":           datetime.now().strftime("%Y-%m-%d"),
        "total_docs":     total,
        "cards_raw":      raw,
        "cards_normalized": normalized,
        "cards_approved": approved,
        "cards_decayed":  decayed,
        "promote_rate":   promote_rate,
        "proposals":      _count_proposals(),
        "rfcs_total":     rfcs.get("total", 0),
        "rfcs_accepted":  rfcs.get("Accepted", 0),
        "search_index":   indexes.get("search_index", 0),
        "semantic_index": indexes.get("semantic_index", 0),
        "passages":       indexes.get("passages", 0),
    }


def load_history() -> list[dict]:
    if not HIST.exists():
        return []
    try:
        return json.loads(HIST.read_text(encoding="utf-8"))
    except Exception:
        return []


def save_history(history: list[dict]) -> None:
    HIST.write_text(json.dumps(history, ensure_ascii=False, indent=2), encoding="utf-8")


def _ascii_trend(values: list[int | float], width: int = 20) -> str:
    if not values or max(values) == min(values):
        return "─" * width
    lo, hi = min(values), max(values)
    chars = "▁▂▃▄▅▆▇█"
    result = []
    for v in values[-width:]:
        idx = int((v - lo) / (hi - lo) * (len(chars) - 1))
        result.append(chars[idx])
    return "".join(result)


def cmd_stats(snap: dict) -> None:
    print("📊 Текущий снапшот базы знаний:\n")
    print(f"  Дата:            {snap['date']}")
    print(f"  Документов:      {snap['total_docs']}")
    print(f"  Карточки:")
    print(f"    approved:      {snap['cards_approved']}")
    print(f"    normalized:    {snap['cards_normalized']}")
    print(f"    raw:           {snap['cards_raw']}")
    print(f"    decayed:       {snap['cards_decayed']}")
    print(f"    promote rate:  {snap['promote_rate']}%")
    print(f"  Proposals:       {snap['proposals']}")
    print(f"  RFC:             {snap['rfcs_total']} (Accepted: {snap['rfcs_accepted']})")
    print(f"  Индексы:")
    print(f"    search_index:  {snap['search_index']} docs")
    print(f"    semantic:      {snap['semantic_index']} docs")
    print(f"    passages:      {snap['passages']} paragraphs")


def cmd_plot(history: list[dict]) -> None:
    if len(history) < 2:
        print("Недостаточно данных для графика (нужно ≥ 2 снапшота).")
        return
    print("📈 Тренды (ASCII):\n")
    metrics = [
        ("approved",   "cards_approved"),
        ("normalized", "cards_normalized"),
        ("proposals",  "proposals"),
        ("docs",       "total_docs"),
        ("promote%",   "promote_rate"),
    ]
    for label, key in metrics:
        values = [h.get(key, 0) for h in history]
        trend  = _ascii_trend(values)
        last   = values[-1]
        delta  = values[-1] - values[0] if len(values) > 1 else 0
        sign   = "+" if delta >= 0 else ""
        print(f"  {label:<12} {trend}  {last:>6}  ({sign}{delta})")


def cmd_update(history: list[dict], snap: dict) -> None:
    # Не дублируем записи того же дня
    if history and history[-1]["date"] == snap["date"]:
        history[-1] = snap
    else:
        history.append(snap)

    lines = [
        "# Knowledge Evolution — Svyazi 2.0",
        "",
        "_Обновляется автоматически: `python scripts/improve_knowledge_evolution.py`_",
        "",
        "## История снапшотов",
        "",
        "| Дата | Docs | Approved | Normalized | Raw | Promote% | Proposals | RFC |",
        "|------|------|----------|-----------|-----|----------|-----------|-----|",
    ]
    for h in history:
        lines.append(
            f"| {h['date']} "
            f"| {h['total_docs']} "
            f"| {h['cards_approved']} "
            f"| {h['cards_normalized']} "
            f"| {h['cards_raw']} "
            f"| {h['promote_rate']}% "
            f"| {h['proposals']} "
            f"| {h['rfcs_accepted']}/{h['rfcs_total']} |"
        )

    lines += [
        "",
        "## Тренды",
        "",
    ]
    if len(history) >= 2:
        metrics = [
            ("approved",    "cards_approved"),
            ("normalized",  "cards_normalized"),
            ("proposals",   "proposals"),
            ("total_docs",  "total_docs"),
            ("promote%",    "promote_rate"),
        ]
        for label, key in metrics:
            values = [h.get(key, 0) for h in history]
            trend  = _ascii_trend(values)
            delta  = values[-1] - values[0] if len(values) > 1 else 0
            sign   = "+" if delta >= 0 else ""
            lines.append(f"- **{label}**: `{trend}` ({sign}{delta} за всё время)")
    else:
        lines.append("_Нужно ≥ 2 снапшота для трендов._")

    lines += [
        "",
        "## Индексы",
        "",
        f"- search_index.json: **{snap['search_index']}** docs",
        f"- semantic_index.json: **{snap['semantic_index']}** docs",
        f"- passages.json: **{snap['passages']}** paragraphs",
        "",
        f"_Последнее обновление: {snap['date']}_",
    ]

    OUT.write_text("\n".join(lines) + "\n", encoding="utf-8")
    save_history(history)
    print(f"✅ Обновлено: {OUT.relative_to(ROOT)}")
    print(f"   История: {len(history)} снапшотов")


def main():
    args = sys.argv[1:]
    snap    = snapshot()
    history = load_history()

    if "--stats" in args:
        cmd_stats(snap)
        return

    if "--plot" in args:
        cmd_stats(snap)
        print()
        cmd_plot(history)
        return

    cmd_stats(snap)
    print()
    cmd_update(history, snap)


if __name__ == "__main__":
    main()
