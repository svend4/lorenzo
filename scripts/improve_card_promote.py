"""
improve_card_promote.py — Card Lifecycle Promoter: raw → normalized → approved.

Переводит карточки из статуса `raw` в `normalized` по критериям качества,
и из `normalized` в `approved` если карточка прошла Review Queue.

Критерии raw → normalized:
  - summary ≥ 80 символов (есть блок <!-- summary --> или ## Summary)
  - теги ≥ 1 (есть <!-- tags: ... --> или поле tags в frontmatter)
  - body ≥ 150 слов (текст без заголовков и frontmatter)
  - нет флага state: rejected в frontmatter

Критерии normalized → approved (строже):
  - summary ≥ 150 символов
  - теги ≥ 2
  - body ≥ 300 слов
  - есть хотя бы 1 ссылка (внутренняя или внешняя)

Использование:
  python scripts/improve_card_promote.py               # показать статистику
  python scripts/improve_card_promote.py --dry-run     # план без изменений
  python scripts/improve_card_promote.py --apply       # применить
  python scripts/improve_card_promote.py --section 05-habr-projects --apply
  python scripts/improve_card_promote.py --stats       # только цифры
  python scripts/improve_card_promote.py --top 20      # топ кандидатов
"""
import re
import sys
import json
import argparse
from pathlib import Path
from datetime import datetime

ROOT  = Path(__file__).parent.parent
DOCS  = ROOT / "docs"

# ── Критерии промоушена ──────────────────────────────────────────────────────

CRITERIA_TO_NORMALIZED = {
    "min_summary_len": 80,
    "min_tags":        1,
    "min_body_words":  150,
}

CRITERIA_TO_APPROVED = {
    "min_summary_len": 150,
    "min_tags":        2,
    "min_body_words":  300,
    "min_links":       1,
}

# ── Парсинг карточки ─────────────────────────────────────────────────────────

_FRONTMATTER_RE = re.compile(r"^---\n(.*?)\n---\n", re.DOTALL)
_SUMMARY_RE     = re.compile(r"<!--\s*summary\s*-->\s*\n>\s*(.+?)(?:\n[^>]|\Z)", re.DOTALL)
_TAGS_FM_RE     = re.compile(r"^tags:\s*\[([^\]]*)\]", re.MULTILINE)
_TAGS_COMMENT_RE = re.compile(r"<!--\s*tags:\s*([^>]+?)\s*-->")
_STATE_FM_RE    = re.compile(r"^state:\s*(\S+)", re.MULTILINE)
_LINK_RE        = re.compile(r"\[.+?\]\(.+?\)|\[\[.+?\]\]")


def _strip_frontmatter(text: str) -> str:
    return _FRONTMATTER_RE.sub("", text, count=1)


def _extract_summary(text: str) -> str:
    m = _SUMMARY_RE.search(text)
    if m:
        return m.group(1).strip()
    # Fallback: первый абзац > 50 символов
    body = _strip_frontmatter(text)
    for para in re.split(r"\n{2,}", body):
        para = para.strip().lstrip("#> ").strip()
        if len(para) > 50:
            return para[:300]
    return ""


def _extract_tags(text: str) -> list[str]:
    m = _TAGS_FM_RE.search(text)
    if m:
        raw = m.group(1)
        tags = [t.strip().strip('"\'') for t in raw.split(",") if t.strip()]
        if tags:
            return tags
    m = _TAGS_COMMENT_RE.search(text)
    if m:
        raw = m.group(1)
        tags = [t.strip() for t in raw.split(",") if t.strip()]
        return tags
    return []


def _get_state(text: str) -> str:
    m = _STATE_FM_RE.search(text)
    return m.group(1).strip() if m else "raw"


def _set_state(text: str, new_state: str) -> str:
    """Обновить или добавить поле state в frontmatter."""
    if _STATE_FM_RE.search(text):
        text = _STATE_FM_RE.sub(f"state: {new_state}", text, count=1)
    else:
        # Вставить после первой строки frontmatter (после ---)
        text = re.sub(
            r"^(---\n)",
            f"---\nstate: {new_state}\n",
            text, count=1
        )
        # Если не было frontmatter — добавить в начало
        if not text.startswith("---"):
            text = f"---\nstate: {new_state}\n---\n\n" + text
    return text


def _count_body_words(text: str) -> int:
    body = _strip_frontmatter(text)
    # Убрать HTML-комментарии, заголовки, код
    body = re.sub(r"<!--.*?-->", "", body, flags=re.DOTALL)
    body = re.sub(r"```.*?```", "", body, flags=re.DOTALL)
    body = re.sub(r"^#{1,6}\s+.+", "", body, flags=re.MULTILINE)
    body = re.sub(r"[^\w\s]", " ", body)
    return len(body.split())


def _count_links(text: str) -> int:
    body = _strip_frontmatter(text)
    return len(_LINK_RE.findall(body))


# ── Оценка карточки ──────────────────────────────────────────────────────────

def evaluate_card(path: Path) -> dict:
    try:
        text = path.read_text(encoding="utf-8")
    except Exception:
        return {}

    state   = _get_state(text)
    summary = _extract_summary(text)
    tags    = _extract_tags(text)
    words   = _count_body_words(text)
    links   = _count_links(text)

    result = {
        "path":         str(path.relative_to(ROOT)),
        "state":        state,
        "summary_len":  len(summary),
        "tags_count":   len(tags),
        "body_words":   words,
        "links_count":  links,
        "summary":      summary[:120],
        "tags":         tags,
        "can_normalize": False,
        "can_approve":   False,
        "_path":        path,
        "_text":        text,
    }

    if state == "rejected":
        return result

    c_n = CRITERIA_TO_NORMALIZED
    result["can_normalize"] = (
        state == "raw"
        and result["summary_len"] >= c_n["min_summary_len"]
        and result["tags_count"]  >= c_n["min_tags"]
        and result["body_words"]  >= c_n["min_body_words"]
    )

    c_a = CRITERIA_TO_APPROVED
    result["can_approve"] = (
        state == "normalized"
        and result["summary_len"] >= c_a["min_summary_len"]
        and result["tags_count"]  >= c_a["min_tags"]
        and result["body_words"]  >= c_a["min_body_words"]
        and result["links_count"] >= c_a["min_links"]
    )

    return result


# ── Главная логика ───────────────────────────────────────────────────────────

def collect_cards(section: str = "") -> list[Path]:
    base = DOCS / section if section else DOCS
    paths = []
    for p in base.rglob("*.md"):
        # Пропустить авто-генерированные мета-файлы в корне docs/
        if p.parent == DOCS and p.stem.isupper():
            continue
        # Пропустить obsidian/ (дублирует основные файлы)
        if "obsidian" in p.parts:
            continue
        paths.append(p)
    return paths


def run(dry_run: bool = True, section: str = "", top: int = 0, stats_only: bool = False):
    paths = collect_cards(section)

    promoted_to_normalized = []
    promoted_to_approved   = []
    skipped = 0
    counts  = {"raw": 0, "normalized": 0, "approved": 0, "rejected": 0, "other": 0}
    candidates_n = []
    candidates_a = []

    for path in paths:
        ev = evaluate_card(path)
        if not ev:
            continue
        state = ev["state"]
        counts[state if state in counts else "other"] = counts.get(state, 0) + 1

        if ev["can_normalize"]:
            candidates_n.append(ev)
        elif ev["can_approve"]:
            candidates_a.append(ev)
        else:
            skipped += 1

    # Сортировать по качеству (больше слов и тегов — выше)
    candidates_n.sort(key=lambda e: e["body_words"] + e["tags_count"] * 50, reverse=True)
    candidates_a.sort(key=lambda e: e["body_words"] + e["tags_count"] * 50, reverse=True)

    if top:
        candidates_n = candidates_n[:top]
        candidates_a = candidates_a[:top]

    if stats_only:
        print("📊 Статусы карточек:")
        for s, n in sorted(counts.items()):
            print(f"  {s:<12} {n}")
        print(f"\n  Кандидатов raw→normalized:   {len(candidates_n)}")
        print(f"  Кандидатов normalized→approved: {len(candidates_a)}")
        return

    print(f"📋 Card Promoter {'(dry-run)' if dry_run else '(apply)'}")
    print(f"   Файлов проверено: {len(paths)}")
    print(f"   raw={counts['raw']} normalized={counts['normalized']} approved={counts['approved']}")

    # raw → normalized
    if candidates_n:
        print(f"\n🔼 raw → normalized ({len(candidates_n)} карточек):")
        for ev in candidates_n:
            print(f"  {ev['path']}")
            print(f"    summary={ev['summary_len']}ch  tags={ev['tags_count']}  words={ev['body_words']}")
            if not dry_run:
                new_text = _set_state(ev["_text"], "normalized")
                ev["_path"].write_text(new_text, encoding="utf-8")
                promoted_to_normalized.append(ev["path"])

    # normalized → approved
    if candidates_a:
        print(f"\n✅ normalized → approved ({len(candidates_a)} карточек):")
        for ev in candidates_a:
            print(f"  {ev['path']}")
            print(f"    summary={ev['summary_len']}ch  tags={ev['tags_count']}  words={ev['body_words']}  links={ev['links_count']}")
            if not dry_run:
                new_text = _set_state(ev["_text"], "approved")
                ev["_path"].write_text(new_text, encoding="utf-8")
                promoted_to_approved.append(ev["path"])

    if not dry_run:
        total = len(promoted_to_normalized) + len(promoted_to_approved)
        print(f"\n✅ Промоутировано: {len(promoted_to_normalized)} → normalized, {len(promoted_to_approved)} → approved")
        _write_promote_log(promoted_to_normalized, promoted_to_approved)
        # Пересобрать индекс
        import subprocess
        subprocess.run(
            ["python3", str(ROOT / "scripts" / "improve_index_update.py")],
            cwd=ROOT, capture_output=True, timeout=60,
        )
        print(f"   Индекс обновлён.")
    else:
        print(f"\nℹ️  Запустите с --apply чтобы применить изменения.")


def _write_promote_log(normalized: list, approved: list):
    log_path = DOCS / "PROMOTE_LOG.md"
    date = datetime.now().strftime("%Y-%m-%d %H:%M")
    lines = [f"\n\n## {date}\n"]
    if normalized:
        lines.append(f"### raw → normalized ({len(normalized)})")
        for p in normalized:
            lines.append(f"- `{p}`")
    if approved:
        lines.append(f"\n### normalized → approved ({len(approved)})")
        for p in approved:
            lines.append(f"- `{p}`")
    existing = log_path.read_text(encoding="utf-8") if log_path.exists() else "# Card Promote Log\n"
    log_path.write_text(existing + "\n".join(lines), encoding="utf-8")


def main():
    parser = argparse.ArgumentParser(description="Card Lifecycle Promoter: raw→normalized→approved")
    parser.add_argument("--dry-run",  action="store_true", default=True,  help="Показать план без изменений")
    parser.add_argument("--apply",    action="store_true",                 help="Применить изменения")
    parser.add_argument("--section",  default="",                          help="Ограничить раздел docs/")
    parser.add_argument("--top",      type=int, default=0,                 help="Показать только топ N кандидатов")
    parser.add_argument("--stats",    action="store_true",                 help="Только статистика")
    args = parser.parse_args()

    dry = not args.apply
    run(dry_run=dry, section=args.section, top=args.top, stats_only=args.stats)


if __name__ == "__main__":
    main()
