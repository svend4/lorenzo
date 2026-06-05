"""
improve_progressive_summarize.py — second-pass summary extraction for blocked raw cards.

Targets raw cards that still have summary < 80ch after improve_auto_summarize.py.
Uses richer extraction strategies:
  1. <!-- abstract-auto --> block: extracts Problem/Approach/Result sentences
  2. ## Summary / ## Резюме / ## Аннотация section
  3. Aggressive multi-sentence join (up to 250ch from first usable paragraphs)
  4. Title-based descriptive template (fallback for section/nav files)

After updating summaries, automatically runs improve_card_promote.py --apply.

Usage:
  python scripts/improve_progressive_summarize.py --dry-run     # план
  python scripts/improve_progressive_summarize.py --apply       # применить
  python scripts/improve_progressive_summarize.py --stats       # только статистика
  python scripts/improve_progressive_summarize.py --apply --section 02-anthropic-vacancies
  python scripts/improve_progressive_summarize.py --apply --no-promote
"""
import re
import subprocess
import sys
from pathlib import Path

ROOT    = Path(__file__).parent.parent
DOCS    = ROOT / "docs"
SCRIPTS = ROOT / "scripts"

MIN_SUMMARY = 80
TARGET_SUMMARY = 250


# ── Extraction strategies ────────────────────────────────────────────────────

def _strip_frontmatter(text: str) -> str:
    return re.sub(r"^---.*?---\s*", "", text, count=1, flags=re.DOTALL)


def _clean_inline(s: str) -> str:
    """Remove markdown noise from inline text."""
    s = re.sub(r"\*{1,3}([^*]+)\*{1,3}", r"\1", s)
    s = re.sub(r"`([^`]+)`", r"\1", s)
    s = re.sub(r"\[([^\]]+)\]\([^)]*\)", r"\1", s)
    s = re.sub(r"^[>*\-•▸◦]\s*", "", s, flags=re.MULTILINE)
    s = re.sub(r"\([a-z0-9\-]{8,}\)", "", s)   # remove slug anchors like (some-long-slug)
    s = re.sub(r"!?\[(?:NOTE|TIP|WARNING|IMPORTANT)\]", "", s)
    s = re.sub(r"\s{2,}", " ", s)
    return s.strip()


def _from_abstract_auto(text: str) -> str:
    """Extract summary from <!-- abstract-auto --> block."""
    m = re.search(
        r"<!--\s*abstract-auto\s*-->\s*(.*?)(?=\n<!--|\n##|\Z)",
        text, re.DOTALL
    )
    if not m:
        return ""
    block = m.group(1)
    # Extract labelled parts: 🎯 Проблема, 🔧 Подход, ✅ Результат
    parts = []
    for emoji, label in [("🎯", "Проблем"), ("🔧", "Подход"), ("✅", "Результат"), ("📌", "")]:
        pat = rf"{re.escape(emoji)}[^:]*:\s*([^\n🎯🔧✅📌]+)"
        lm = re.search(pat, block)
        if lm:
            raw = _clean_inline(lm.group(1))
            if len(raw) > 20:
                parts.append(raw[:120].rstrip(",. "))

    if parts:
        summary = ". ".join(parts[:2])
        return summary[:TARGET_SUMMARY].strip()

    # Fallback: first quoted line > 30ch from block
    for line in block.splitlines():
        line = re.sub(r"^>\s*", "", line).strip()
        line = _clean_inline(line)
        if len(line) > 30:
            return line[:TARGET_SUMMARY]
    return ""


def _from_section_heading(text: str) -> str:
    """Extract content from ## Summary / ## Резюме / ## Аннотация / ## Описание."""
    body = _strip_frontmatter(text)
    patterns = [
        r"##\s+(?:Summary|Резюме|Аннотация|Описание|Overview|Обзор)\s*\n+(.*?)(?=\n##|\Z)",
        r"##\s+(?:TL;DR|TLDR|Кратко)\s*\n+(.*?)(?=\n##|\Z)",
    ]
    for pat in patterns:
        m = re.search(pat, body, re.IGNORECASE | re.DOTALL)
        if m:
            raw = m.group(1).strip()
            raw = re.sub(r"<!--.*?-->", " ", raw, flags=re.DOTALL)
            raw = re.sub(r"```.*?```", " ", raw, flags=re.DOTALL)
            raw = _clean_inline(raw)
            sentences = re.split(r"(?<=[.!?])\s+", raw)
            joined = ""
            for s in sentences:
                if len(s) < 15:
                    continue
                joined = (joined + " " + s).strip()
                if len(joined) >= MIN_SUMMARY:
                    return joined[:TARGET_SUMMARY]
    return ""


def _from_paragraphs(text: str) -> str:
    """Aggressive multi-paragraph extraction: join sentences up to TARGET_SUMMARY."""
    body = _strip_frontmatter(text)
    body = re.sub(r"<!--.*?-->", " ", body, flags=re.DOTALL)
    body = re.sub(r"```.*?```", " ", body, flags=re.DOTALL)
    body = re.sub(r"^#{1,6}\s+.*$", "", body, flags=re.MULTILINE)
    body = re.sub(r"^\s*[-*|>]\s*", "", body, flags=re.MULTILINE)
    body = re.sub(r"\[.*?\]\(.*?\)", " ", body)
    body = re.sub(r"\n{2,}", "\n", body).strip()

    collected = ""
    for sent in re.split(r"(?<=[.!?])\s+|\n", body):
        sent = _clean_inline(sent.strip())
        if len(sent) < 20:
            continue
        if re.search(r"^[→←↑↓•▸◦\-#|]", sent):
            continue
        collected = (collected + " " + sent).strip()
        if len(collected) >= MIN_SUMMARY:
            return collected[:TARGET_SUMMARY]
    return collected[:TARGET_SUMMARY] if len(collected) >= 30 else ""


def _title_template(text: str, path: Path) -> str:
    """Last-resort: use H1 title to build a descriptive stub summary."""
    m = re.search(r"^#\s+(.+)", text, re.MULTILINE)
    title = m.group(1).strip() if m else path.stem.replace("-", " ").replace("_", " ")
    title = _clean_inline(title)
    if not title or title in ("⬡", "---", ""):
        title = path.stem.replace("-", " ").replace("_", " ").title()
    # Determine section hint
    parts = path.parts
    section = ""
    for p in parts:
        if p.startswith("0") and "-" in p:
            section = p.split("-", 1)[1].replace("-", " ")
            break
    if section:
        return f"Документ «{title}» — раздел базы знаний {section}."[:TARGET_SUMMARY]
    return f"Документ «{title}» — материал базы знаний Svyazi 2.0."[:TARGET_SUMMARY]


def extract_best_summary(text: str, path: Path) -> str:
    """Try all strategies in order of quality."""
    for fn in (_from_abstract_auto, _from_section_heading, _from_paragraphs):
        result = fn(text)
        if len(result) >= MIN_SUMMARY:
            return result
    # title template always returns something
    return _title_template(text, path)


# ── File processing ──────────────────────────────────────────────────────────

def _get_state(text: str) -> str:
    m = re.search(r"^state:\s*(\S+)", text, re.MULTILINE)
    return m.group(1).strip().strip("\"'") if m else "raw"


def _get_current_summary(text: str) -> str:
    m = re.search(r"<!--\s*summary\s*-->\s*\n>\s*(.+?)(?:\n[^>]|\Z)", text, re.DOTALL)
    if m:
        return m.group(1).strip()
    return ""


def _inject_summary(text: str, summary: str) -> str:
    summary_line = f"<!-- summary -->\n> {summary}"
    if re.search(r"<!--\s*summary\s*-->", text):
        text = re.sub(
            r"<!--\s*summary\s*-->\s*\n>\s*.+",
            summary_line,
            text,
        )
        return text
    lines = text.split("\n")
    insert_at = 0
    for i, line in enumerate(lines):
        if line.startswith("# "):
            insert_at = i + 1
            break
    while insert_at < len(lines) and not lines[insert_at].strip():
        insert_at += 1
    lines.insert(insert_at, "")
    lines.insert(insert_at + 1, summary_line)
    lines.insert(insert_at + 2, "")
    return "\n".join(lines)


def process_file(path: Path, dry_run: bool = True) -> dict:
    try:
        text = path.read_text(encoding="utf-8", errors="ignore")
    except Exception:
        return {"status": "error"}

    state = _get_state(text)
    if state != "raw":
        return {"status": "skip_state"}

    current = _get_current_summary(text)
    if len(current) >= MIN_SUMMARY:
        return {"status": "ok"}

    best = extract_best_summary(text, path)
    if len(best) < MIN_SUMMARY:
        return {"status": "insufficient", "got": len(best)}

    if not dry_run:
        new_text = _inject_summary(text, best)
        if new_text != text:
            path.write_text(new_text, encoding="utf-8")

    return {
        "status": "changed",
        "path":   str(path.relative_to(ROOT)),
        "old_len": len(current),
        "new_len": len(best),
    }


# ── Main ────────────────────────────────────────────────────────────────────

def main():
    args       = sys.argv[1:]
    dry_run    = "--apply" not in args
    stats_only = "--stats" in args
    no_promote = "--no-promote" in args
    section    = ""

    for i, a in enumerate(args):
        if a == "--section" and i + 1 < len(args):
            section = args[i + 1]

    base = DOCS / section if section else DOCS

    if dry_run and not stats_only:
        print("📋 Progressive Summarize [dry-run] — передайте --apply\n")
    elif not stats_only:
        print("✏️  Progressive Summarize [apply]\n")

    paths = [
        p for p in base.rglob("*.md")
        if "obsidian" not in p.parts
        and not (p.parent == DOCS and p.stem.isupper())
    ]

    results: dict[str, int] = {
        "changed": 0, "ok": 0, "skip_state": 0, "insufficient": 0, "error": 0
    }
    changed_list: list[dict] = []

    for path in paths:
        r = process_file(path, dry_run=dry_run)
        st = r.get("status", "error")
        results[st] = results.get(st, 0) + 1
        if st == "changed":
            changed_list.append(r)

    print(f"  Файлов проверено: {len(paths)}")
    print(f"  Обновлено:        {results['changed']}")
    print(f"  Уже OK:           {results['ok']}")
    print(f"  Пропущено:        {results['skip_state']}")
    print(f"  Мало контента:    {results['insufficient']}")

    if changed_list and not stats_only:
        print(f"\n  Примеры:")
        for r in changed_list[:8]:
            print(f"    {r['path']}")
            print(f"      {r['old_len']}ch → {r['new_len']}ch")

    if not dry_run and results["changed"] > 0 and not no_promote:
        print(f"\n🔼 Запускаю promote...")
        subprocess.run(
            [sys.executable, str(SCRIPTS / "improve_card_promote.py"), "--apply"],
            cwd=ROOT,
        )

    if not dry_run:
        print(f"\n✅ Обновлено: {results['changed']} карточек")
    else:
        print(f"\nℹ️  Запустите с --apply для применения.")


if __name__ == "__main__":
    main()
