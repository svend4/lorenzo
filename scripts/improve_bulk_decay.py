"""
improve_bulk_decay.py — bulk decay for empty stub cards.

Identifies stub cards that have no meaningful content and marks them decayed.
Uses frontmatter date: field for age (mtime is unreliable after batch ops).

Decay criteria (ALL must be true):
  - state = raw
  - no frontmatter tags: [...] field
  - body has zero real sentences (only headings, lists, or empty)
  - body word count (clean text) < 60 words
  - frontmatter date older than --min-age days (default: 90)

Safety:
  - --dry-run is the default; nothing written without --apply
  - Never touches approved, normalized, decayed, rejected
  - Every decay written to .claude/mcp_write_log.jsonl

Usage:
  python scripts/improve_bulk_decay.py                # dry-run
  python scripts/improve_bulk_decay.py --apply        # apply
  python scripts/improve_bulk_decay.py --apply --min-age 60
  python scripts/improve_bulk_decay.py --stats
  python scripts/improve_bulk_decay.py --section docs/ai-collaborations
"""
import json
import re
import sys
from datetime import datetime, timedelta
from pathlib import Path

ROOT      = Path(__file__).parent.parent
DOCS      = ROOT / "docs"
AUDIT_LOG = ROOT / ".claude" / "mcp_write_log.jsonl"

MAX_BODY_WORDS  = 60
DEFAULT_MIN_AGE = 90   # days from frontmatter date


def _parse_fm_date(text: str) -> datetime | None:
    m = re.search(r"^date:\s*(\S+)", text, re.MULTILINE)
    if not m:
        return None
    ds = m.group(1).strip().strip("\"'")[:10]
    try:
        return datetime.strptime(ds, "%Y-%m-%d")
    except ValueError:
        return None


def _fm_age_days(text: str) -> float | None:
    dt = _parse_fm_date(text)
    if dt is None:
        return None
    return (datetime.now() - dt).days


def _get_state(text: str) -> str:
    m = re.search(r"^state:\s*(\S+)", text, re.MULTILINE)
    return m.group(1).strip().strip("\"'") if m else "raw"


def _get_fm_tags(text: str) -> list[str]:
    m = re.search(r"^tags:\s*\[([^\]]*)\]", text, re.MULTILINE)
    if m:
        return [t.strip().strip("\"'") for t in m.group(1).split(",") if t.strip()]
    return []


def _clean_body(text: str) -> str:
    body = re.sub(r"^---.*?---\s*", "", text, count=1, flags=re.DOTALL)
    body = re.sub(r"<!--.*?-->", " ", body, flags=re.DOTALL)
    body = re.sub(r"```.*?```", " ", body, flags=re.DOTALL)
    body = re.sub(r"^#{1,6}\s.*$", "", body, flags=re.MULTILINE)
    body = re.sub(r"^\s*[-*|>]\s*.*$", "", body, flags=re.MULTILINE)
    body = re.sub(r"\[.*?\]\(.*?\)", " ", body)
    return body.strip()


def _has_real_sentences(text: str) -> bool:
    clean = _clean_body(text)
    for line in clean.splitlines():
        line = line.strip()
        if len(line) > 40 and re.search(r"[а-яёa-z]{3,}", line, re.IGNORECASE):
            return True
    return False


def find_decay_candidates(
    base: Path,
    min_age_days: int = DEFAULT_MIN_AGE,
) -> list[dict]:
    candidates = []
    for path in base.rglob("*.md"):
        if "obsidian" in path.parts:
            continue
        if path.parent == DOCS and path.stem.isupper():
            continue
        try:
            text = path.read_text(encoding="utf-8", errors="ignore")
        except Exception:
            continue

        state = _get_state(text)
        if state in ("approved", "normalized", "decayed", "rejected"):
            continue

        fm_tags = _get_fm_tags(text)
        if fm_tags:
            continue

        age = _fm_age_days(text)
        if age is None or age < min_age_days:
            continue

        clean = _clean_body(text)
        wc    = len(clean.split())
        if wc >= MAX_BODY_WORDS:
            continue

        if _has_real_sentences(text):
            continue

        candidates.append({
            "path":  path,
            "rel":   str(path.relative_to(ROOT)),
            "wc":    wc,
            "age":   age,
            "state": state,
        })

    candidates.sort(key=lambda c: -c["age"])
    return candidates


def _apply_decay(path: Path, reason: str) -> None:
    text = path.read_text(encoding="utf-8", errors="ignore")
    now  = datetime.now().strftime("%Y-%m-%dT%H:%M:%S")
    if re.search(r"^state:\s*\S+", text, re.MULTILINE):
        text = re.sub(r"^state:\s*\S+", "state: decayed", text, flags=re.MULTILINE)
    elif re.search(r"^---", text):
        text = re.sub(r"(^---\n)", r"\1state: decayed\n", text, count=1)
    else:
        text = f"---\nstate: decayed\n---\n\n" + text
    text = text.rstrip() + f"\n\n<!-- decay_event: raw → decayed | {now} | {reason} -->\n"
    path.write_text(text, encoding="utf-8")


def _audit(path: Path, reason: str) -> None:
    try:
        AUDIT_LOG.parent.mkdir(parents=True, exist_ok=True)
        entry = json.dumps({
            "ts":     datetime.now().strftime("%Y-%m-%dT%H:%M:%S"),
            "tool":   "bulk_decay",
            "args":   {"path": str(path.relative_to(ROOT)), "reason": reason},
            "result": "decayed",
        }, ensure_ascii=False)
        with open(AUDIT_LOG, "a", encoding="utf-8") as f:
            f.write(entry + "\n")
    except Exception:
        pass


def main():
    args       = sys.argv[1:]
    dry_run    = "--apply" not in args
    stats_only = "--stats" in args
    min_age    = DEFAULT_MIN_AGE
    section    = ""

    for i, a in enumerate(args):
        if a == "--min-age" and i + 1 < len(args):
            try:
                min_age = int(args[i + 1])
            except ValueError:
                pass
        if a == "--section" and i + 1 < len(args):
            section = args[i + 1]

    base = Path(section) if section else DOCS
    if not base.is_absolute():
        base = ROOT / section

    if dry_run and not stats_only:
        print("📋 Bulk Decay [dry-run] — передайте --apply для применения\n")
    elif not stats_only:
        print("🗑  Bulk Decay [apply]\n")

    candidates = find_decay_candidates(base, min_age_days=min_age)

    print(f"  Кандидатов на decay: {len(candidates)}")
    print(f"  Критерии: нет fm-тегов, clean-wc < {MAX_BODY_WORDS}, нет предложений, date > {min_age}d")

    if stats_only or not candidates:
        if not candidates:
            print("\n✅ Кандидатов на автоматический decay не найдено.")
            print("   (Файлы слишком новые или содержат предложения/теги)")
        return

    print(f"\n  Топ кандидатов:")
    for c in candidates[:15]:
        print(f"    [{c['age']:.0f}d] wc={c['wc']:3d} {c['rel']}")

    if dry_run:
        print(f"\nℹ️  Запустите с --apply для применения ({len(candidates)} файлов).")
        return

    decayed = 0
    for c in candidates:
        reason = f"bulk_stub: clean_wc={c['wc']}, no fm-tags, no sentences, date_age={c['age']:.0f}d"
        try:
            _apply_decay(c["path"], reason)
            _audit(c["path"], reason)
            decayed += 1
        except Exception as e:
            print(f"  ⚠ Ошибка {c['rel']}: {e}")

    print(f"\n✅ Помечено как decayed: {decayed} карточек")
    print(f"   Запустите: python scripts/improve_card_promote.py --stats")


if __name__ == "__main__":
    main()
