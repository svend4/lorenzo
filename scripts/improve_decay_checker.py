"""
improve_decay_checker.py — поиск кандидатов на decay в базе знаний Svyazi 2.0.

Находит карточки, которые потенциально устарели по следующим критериям:
  - Возраст > N дней без изменений
  - Пустой summary (< 50 символов) и нет тегов → stub-карточки
  - Дубль: другая карточка с похожим названием (cosine ≥ 0.7)
  - Broken links (state=raw, дата > 180 дней, нет рёбер)

Не меняет файлы автоматически — только список кандидатов.
Для применения decay: python scripts/mcp_server.py или decay_card MCP-инструмент.

Использование:
  python scripts/improve_decay_checker.py                    # показать все кандидаты
  python scripts/improve_decay_checker.py --age 180          # только старше N дней
  python scripts/improve_decay_checker.py --type stub        # только stubs
  python scripts/improve_decay_checker.py --type orphan      # давние raw без рёбер
  python scripts/improve_decay_checker.py --top 20           # топ-N кандидатов
  python scripts/improve_decay_checker.py --output DECAY_CANDIDATES.md  # сохранить
"""
import re
import sys
import json
from pathlib import Path
from datetime import datetime, timedelta

ROOT = Path(__file__).parent.parent
DOCS = ROOT / "docs"
OUT  = DOCS / "DECAY_CANDIDATES.md"

DEFAULT_AGE_DAYS  = 365
STUB_SUMMARY_LEN  = 50
ORPHAN_AGE_DAYS   = 180

DECAY_TYPES = {
    "stub":   "Пустой stub без summary/тегов",
    "orphan": "Давняя raw-карточка без рёбер",
    "aged":   "Не обновлялась более N дней",
}


def _parse_frontmatter(text: str) -> dict:
    fm_m = re.search(r"^---\n(.*?)\n---", text, re.DOTALL)
    meta: dict = {}
    if fm_m:
        for line in fm_m.group(1).splitlines():
            m = re.match(r"^(\w+):\s*(.+)", line)
            if m:
                meta[m.group(1)] = m.group(2).strip().strip("\"'")
    return meta


def _extract_summary(text: str) -> str:
    m = re.search(r"<!--\s*summary\s*-->\s*>\s*(.+)", text)
    if m:
        return m.group(1).strip()
    m = re.search(r"##\s*Summary\s*\n+(.+?)(?:\n\n|\Z)", text, re.DOTALL)
    if m:
        return m.group(1).strip()[:300]
    return ""


def _extract_tags(text: str) -> list[str]:
    m = re.search(r"^tags:\s*\[([^\]]*)\]", text, re.MULTILINE)
    if m:
        raw = m.group(1)
        return [t.strip().strip("\"'") for t in raw.split(",") if t.strip()]
    return []


def _extract_edges(text: str) -> list[str]:
    return re.findall(r'\[\[([^\]]+)\]\]|\[.*?\]\(([^)]+\.md)\)', text)


def _file_age_days(path: Path) -> float:
    try:
        mtime = path.stat().st_mtime
        return (datetime.now().timestamp() - mtime) / 86400
    except Exception:
        return 0.0


def _parse_date(meta: dict) -> datetime | None:
    date_str = meta.get("date", "")
    for fmt in ("%Y-%m-%d", "%Y-%m-%dT%H:%M:%S"):
        try:
            return datetime.strptime(date_str[:10], "%Y-%m-%d")
        except ValueError:
            pass
    return None


def _tokenize(text: str) -> list[str]:
    return re.findall(r"[а-яёa-z]{3,}", text.lower())


def _cosine(a: str, b: str) -> float:
    def tf(t: str) -> dict:
        freq: dict[str, int] = {}
        for w in _tokenize(t):
            freq[w] = freq.get(w, 0) + 1
        return freq
    fa, fb = tf(a), tf(b)
    keys = set(fa) | set(fb)
    dot  = sum(fa.get(k, 0) * fb.get(k, 0) for k in keys)
    na   = sum(v * v for v in fa.values()) ** 0.5
    nb   = sum(v * v for v in fb.values()) ** 0.5
    return dot / (na * nb) if na and nb else 0.0


def _collect_cards() -> list[dict]:
    cards = []
    for path in DOCS.rglob("*.md"):
        if "obsidian" in path.parts:
            continue
        if path.parent == DOCS and path.stem.isupper():
            continue
        try:
            text = path.read_text(encoding="utf-8", errors="ignore")
        except Exception:
            continue
        meta    = _parse_frontmatter(text)
        state   = meta.get("state", "raw")
        if state in ("decayed",):
            continue
        summary = _extract_summary(text)
        tags    = _extract_tags(text)
        edges   = _extract_edges(text)
        age     = _file_age_days(path)
        date    = _parse_date(meta)
        title_m = re.search(r"^#\s+(.+)", text, re.MULTILINE)
        title   = title_m.group(1).strip() if title_m else path.stem

        cards.append({
            "path":    path,
            "rel":     str(path.relative_to(ROOT)),
            "title":   title[:80],
            "state":   state,
            "summary": summary,
            "tags":    tags,
            "edges":   edges,
            "age":     age,
            "date":    date,
            "text":    text[:1000],
        })
    return cards


def find_stubs(cards: list[dict]) -> list[dict]:
    result = []
    for c in cards:
        if len(c["summary"]) < STUB_SUMMARY_LEN and len(c["tags"]) == 0:
            result.append({**c, "decay_type": "stub",
                           "reason": f"summary={len(c['summary'])}ch, tags=0"})
    return result


def find_orphans(cards: list[dict], age_days: int = ORPHAN_AGE_DAYS) -> list[dict]:
    result = []
    for c in cards:
        if (c["state"] == "raw"
                and len(c["edges"]) == 0
                and c["age"] > age_days):
            result.append({**c, "decay_type": "orphan",
                           "reason": f"raw, no edges, age={c['age']:.0f}d"})
    return result


def find_aged(cards: list[dict], age_days: int = DEFAULT_AGE_DAYS) -> list[dict]:
    result = []
    for c in cards:
        if c["age"] > age_days and c["state"] not in ("approved",):
            result.append({**c, "decay_type": "aged",
                           "reason": f"age={c['age']:.0f}d, state={c['state']}"})
    return result


def find_near_duplicates(cards: list[dict], threshold: float = 0.7,
                         sample: int = 200) -> list[dict]:
    """Find pairs with similar titles (cosine ≥ threshold). O(n²) — sample only."""
    result: list[dict] = []
    seen: set[str] = set()
    pool = sorted(cards, key=lambda c: -c["age"])[:sample]
    for i, a in enumerate(pool):
        for b in pool[i + 1:]:
            sim = _cosine(a["title"], b["title"])
            if sim >= threshold:
                key = tuple(sorted([a["rel"], b["rel"]]))
                if key not in seen:
                    seen.add(key)
                    result.append({
                        **a,
                        "decay_type": "near-dup",
                        "reason": f"sim={sim:.2f} with '{b['title'][:50]}'",
                        "dup_path": b["rel"],
                    })
    return result


def cmd_check(decay_type: str = "all", age_days: int = DEFAULT_AGE_DAYS,
              top: int = 50, output: str = "") -> None:
    cards = _collect_cards()
    print(f"🔍 Decay Checker — Svyazi 2.0")
    print(f"   Карточек проверено: {len(cards)}\n")

    candidates: list[dict] = []

    if decay_type in ("all", "stub"):
        stubs = find_stubs(cards)
        print(f"  📭 Stubs (пустые):     {len(stubs)}")
        candidates.extend(stubs)

    if decay_type in ("all", "orphan"):
        orphans = find_orphans(cards, age_days=ORPHAN_AGE_DAYS)
        print(f"  👻 Orphans (давние raw): {len(orphans)}")
        candidates.extend(orphans)

    if decay_type in ("all", "aged"):
        aged = find_aged(cards, age_days=age_days)
        print(f"  🕰  Aged (>{age_days}d):    {len(aged)}")
        candidates.extend(aged)

    if decay_type in ("all", "near-dup"):
        dups = find_near_duplicates(cards)
        print(f"  🔄 Near-dups (≥0.7):   {len(dups)}")
        candidates.extend(dups)

    # Дедупликация по пути
    seen_paths: set = set()
    unique: list[dict] = []
    for c in candidates:
        if c["rel"] not in seen_paths:
            seen_paths.add(c["rel"])
            unique.append(c)

    # Сортировка: stubs первыми, потом по age убыванию
    order = {"stub": 0, "orphan": 1, "near-dup": 2, "aged": 3}
    unique.sort(key=lambda c: (order.get(c["decay_type"], 9), -c["age"]))

    print(f"\n  Итого кандидатов: {len(unique)}")

    if not unique:
        print("\n✅ Кандидатов на decay не найдено.")
        return

    print(f"\n{'─' * 70}")
    for i, c in enumerate(unique[:top], 1):
        emoji = {"stub": "📭", "orphan": "👻", "aged": "🕰", "near-dup": "🔄"}.get(c["decay_type"], "?")
        print(f"  {i:3}. {emoji} [{c['decay_type']}] {c['title'][:55]}")
        print(f"       {c['rel']}")
        print(f"       Причина: {c['reason']}")

    if output or output == "":
        target = Path(output) if output else OUT
        _write_report(unique[:top], target)
        print(f"\n✅ Отчёт сохранён: {target.relative_to(ROOT)}")
        print(f"   Для применения: python scripts/mcp_server.py → decay_card")


def _write_report(candidates: list[dict], target: Path) -> None:
    date = datetime.now().strftime("%Y-%m-%d")
    lines = [
        "# Decay Candidates — Svyazi 2.0",
        "",
        f"_Сгенерировано: {date} · `python scripts/improve_decay_checker.py`_",
        "",
        f"Кандидатов на decay: **{len(candidates)}**",
        "",
        "## Как применить",
        "",
        "Через MCP (`decay_card`) или напрямую через `update_card_state`:",
        "```bash",
        "python scripts/mcp_server.py",
        "# затем вызов: decay_card(path=..., reason=...)",
        "```",
        "",
        "## Список кандидатов",
        "",
        "| # | Тип | Путь | Причина |",
        "|---|-----|------|---------|",
    ]
    emoji_map = {"stub": "📭", "orphan": "👻", "aged": "🕰", "near-dup": "🔄"}
    for i, c in enumerate(candidates, 1):
        emoji = emoji_map.get(c["decay_type"], "?")
        lines.append(
            f"| {i} | {emoji} {c['decay_type']} | `{c['rel']}` | {c['reason']} |"
        )
    target.write_text("\n".join(lines) + "\n", encoding="utf-8")


def main():
    args = sys.argv[1:]
    decay_type = "all"
    age_days   = DEFAULT_AGE_DAYS
    top        = 50
    output     = str(OUT)

    for i, arg in enumerate(args):
        if arg == "--type" and i + 1 < len(args):
            decay_type = args[i + 1]
        elif arg == "--age" and i + 1 < len(args):
            try:
                age_days = int(args[i + 1])
            except ValueError:
                pass
        elif arg == "--top" and i + 1 < len(args):
            try:
                top = int(args[i + 1])
            except ValueError:
                pass
        elif arg == "--output" and i + 1 < len(args):
            output = args[i + 1]

    cmd_check(decay_type=decay_type, age_days=age_days, top=top, output=output)


if __name__ == "__main__":
    main()
