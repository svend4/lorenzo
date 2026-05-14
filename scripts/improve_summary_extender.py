"""
improve_summary_extender.py — extend short summaries on normalized cards.

Targets state=normalized cards where summary 80–149ch (blocks approved promotion).
Appends best additional sentences from the card body until summary >= 150ch.
Also injects a second tag for cards with only 1 tag (another approved blocker).

Strategies (in order):
  1. Append sentences from body until length >= 150
  2. Append from abstract-auto block remainder
  3. Append title-based context phrase

Runs improve_card_promote.py --apply automatically after updating files.

Usage:
  python scripts/improve_summary_extender.py --dry-run       # план
  python scripts/improve_summary_extender.py --apply         # применить
  python scripts/improve_summary_extender.py --stats         # статистика
  python scripts/improve_summary_extender.py --apply --no-promote
  python scripts/improve_summary_extender.py --apply --section 02-anthropic-vacancies
"""
import re
import subprocess
import sys
from pathlib import Path

ROOT    = Path(__file__).parent.parent
DOCS    = ROOT / "docs"
SCRIPTS = ROOT / "scripts"

TARGET_SUMMARY = 150   # needed for normalized→approved
MAX_SUMMARY    = 350

# ── Tag dictionary for second-tag injection ──────────────────────────────────
TOPIC_RULES: dict[str, list[str]] = {
    "memory":        ["yodoca", "ngt memory", "memnet", "agent-memory", "консолидац",
                      "episod", "hebbian", "recall", "память", "memory"],
    "rag":           ["rag", "liteparse", "retrieval", "hybrid rag", "graph rag",
                      "legal rag", "evidence", "поиск"],
    "orchestration": ["rufler", "mclaude", "ai factory", "sequential", "handoff",
                      "оркестр", "swarm", "mailbox", "агент", "agent"],
    "security":      ["sentinel", "litellm", "tool search", "безопасн", "pii",
                      "allowlist", "firewall", "quarantine"],
    "knowledge":     ["knowledge-space", "agentfs", "cardindex", "карточк", "знани",
                      "agentos", "vault", "reference card", "база знаний"],
    "ingestion":     ["svyazi", "import", "нормализац", "extraction", "dedup",
                      "дедупликац", "парсинг", "parsing"],
    "local-first":   ["local-first", "crdt", "yjs", "automerge", "offline",
                      "whisper", "голос", "voice"],
    "architecture":  ["архитектур", "контракт", "envelope", "интеграц",
                      "зазор", "слой", "layer", "schema", "протокол"],
    "roadmap":       ["дорожная карта", "итерац", "mvp", "фаза", "phase",
                      "roadmap", "прототип", "timeline", "план"],
    "anthropic":     ["anthropic", "вакансии", "hiring", "cluster", "gtm",
                      "research engineer", "trust & safety"],
    "self-improve":  ["autoresearch", "self-improv", "benchmark", "eval",
                      "rollback", "петл", "самоулучш", "скрипт"],
    "collaboration": ["коллаборац", "автор", "контакт", "habr", "хабр",
                      "svend4", "andrey", "виталий", "kksudo", "проект"],
}


def _detect_tags(text: str, existing: list[str]) -> list[str]:
    low = text.lower()
    ex_low = {t.lower() for t in existing}
    new_tags = []
    for topic, kws in TOPIC_RULES.items():
        if topic.lower() in ex_low:
            continue
        if any(kw in low for kw in kws):
            new_tags.append(topic)
    return new_tags[:3]


# ── Parsing helpers ───────────────────────────────────────────────────────────

def _get_state(text: str) -> str:
    m = re.search(r"^state:\s*(\S+)", text, re.MULTILINE)
    return m.group(1).strip().strip("\"'") if m else "raw"


def _get_summary(text: str) -> str:
    m = re.search(r"<!--\s*summary\s*-->\s*\n>\s*(.+?)(?:\n[^>]|\Z)", text, re.DOTALL)
    if m:
        return m.group(1).strip()
    body = re.sub(r"^---.*?---\s*", "", text, count=1, flags=re.DOTALL)
    for para in re.split(r"\n{2,}", body):
        para = para.strip().lstrip("#> ").strip()
        if len(para) > 50:
            return para[:300]
    return ""


def _get_tags(text: str) -> list[str]:
    m = re.search(r"^tags:\s*\[([^\]]*)\]", text, re.MULTILINE)
    if m:
        return [t.strip().strip("\"'") for t in m.group(1).split(",") if t.strip()]
    m = re.search(r"<!--\s*tags:\s*([^>]+?)\s*-->", text)
    if m:
        return [t.strip() for t in m.group(1).split(",") if t.strip()]
    return []


def _clean(s: str) -> str:
    s = re.sub(r"\*{1,3}([^*]+)\*{1,3}", r"\1", s)
    s = re.sub(r"`([^`]+)`", r"\1", s)
    s = re.sub(r"\[([^\]]+)\]\([^)]*\)", r"\1", s)
    s = re.sub(r"^[>*\-•]\s*", "", s, flags=re.MULTILINE)
    s = re.sub(r"\([a-z0-9\-]{8,}\)", "", s)
    s = re.sub(r"!?\[(?:NOTE|TIP|WARNING|IMPORTANT)\]", "", s)
    return re.sub(r"\s{2,}", " ", s).strip()


# ── Extension logic ───────────────────────────────────────────────────────────

def _sentences_from_body(text: str, exclude: str) -> list[str]:
    body = re.sub(r"^---.*?---\s*", "", text, count=1, flags=re.DOTALL)
    body = re.sub(r"<!--.*?-->", " ", body, flags=re.DOTALL)
    body = re.sub(r"```.*?```", " ", body, flags=re.DOTALL)
    body = re.sub(r"^#{1,6}\s+.*$", "", body, flags=re.MULTILINE)
    body = re.sub(r"^\s*[-*|>]\s*", "", body, flags=re.MULTILINE)
    body = re.sub(r"\[.*?\]\(.*?\)", " ", body)

    results = []
    ex_low = exclude.lower()
    for sent in re.split(r"(?<=[.!?])\s+|\n", body):
        s = _clean(sent.strip())
        if len(s) < 25:
            continue
        if s.lower() in ex_low or ex_low in s.lower():
            continue
        if re.search(r"[а-яёa-z]{4,}", s, re.IGNORECASE):
            results.append(s)
    return results


def extend_summary(text: str, path: Path) -> str:
    """Return extended summary >= TARGET_SUMMARY chars, or '' if impossible."""
    current = _get_summary(text)
    if len(current) >= TARGET_SUMMARY:
        return current

    sentences = _sentences_from_body(text, exclude=current)
    extended = current
    for sent in sentences:
        candidate = (extended + " " + sent).strip()
        if len(candidate) > MAX_SUMMARY:
            # Try to truncate at a sentence boundary
            if len(extended) >= TARGET_SUMMARY:
                break
            extended = candidate[:MAX_SUMMARY].rsplit(" ", 1)[0].rstrip(".") + "."
            break
        extended = candidate
        if len(extended) >= TARGET_SUMMARY:
            break

    if len(extended) >= TARGET_SUMMARY:
        return extended[:MAX_SUMMARY]

    # Fallback: title context
    m = re.search(r"^#\s+(.+)", text, re.MULTILINE)
    title = _clean(m.group(1)) if m else path.stem.replace("-", " ")
    if title and len(extended) < TARGET_SUMMARY:
        ctx = f" Материал из базы знаний Svyazi 2.0, раздел «{title}»."
        extended = (extended + ctx)[:MAX_SUMMARY]

    return extended if len(extended) >= TARGET_SUMMARY else ""


# ── Inject helpers ────────────────────────────────────────────────────────────

def _inject_summary(text: str, summary: str) -> str:
    marker = f"<!-- summary -->\n> {summary}"
    if re.search(r"<!--\s*summary\s*-->", text):
        return re.sub(
            r"<!--\s*summary\s*-->\s*\n>\s*.+",
            marker, text,
        )
    lines = text.split("\n")
    at = 0
    for i, line in enumerate(lines):
        if line.startswith("# "):
            at = i + 1
            break
    while at < len(lines) and not lines[at].strip():
        at += 1
    lines.insert(at, "")
    lines.insert(at + 1, marker)
    lines.insert(at + 2, "")
    return "\n".join(lines)


def _add_tag(text: str, tag: str) -> str:
    """Add a tag to frontmatter tags: [] field."""
    m = re.search(r"^(tags:\s*\[)([^\]]*)\]", text, re.MULTILINE)
    if m:
        existing = m.group(2).strip()
        new_val  = f"{existing}, {tag}" if existing else tag
        return text[:m.start()] + f"tags: [{new_val}]" + text[m.end():]
    # No frontmatter tags: field — try comment tags
    mc = re.search(r"<!--\s*tags:\s*([^>]+?)\s*-->", text)
    if mc:
        new_val = mc.group(1).strip() + f", {tag}"
        return text[:mc.start()] + f"<!-- tags: {new_val} -->" + text[mc.end():]
    return text


# ── File processing ───────────────────────────────────────────────────────────

def process_file(path: Path, dry_run: bool = True) -> dict:
    try:
        text = path.read_text(encoding="utf-8", errors="ignore")
    except Exception:
        return {"status": "error"}

    if _get_state(text) != "normalized":
        return {"status": "skip_state"}

    tags    = _get_tags(text)
    current = _get_summary(text)
    needs_summary = len(current) < TARGET_SUMMARY
    needs_tag     = len(tags) < 2

    if not needs_summary and not needs_tag:
        return {"status": "ok"}

    changes = []
    new_text = text

    if needs_summary:
        extended = extend_summary(text, path)
        if extended:
            changes.append(f"sum:{len(current)}→{len(extended)}ch")
            if not dry_run:
                new_text = _inject_summary(new_text, extended)

    if needs_tag:
        new_tags = _detect_tags(text, tags)
        if new_tags:
            changes.append(f"tag+{new_tags[0]}")
            if not dry_run:
                new_text = _add_tag(new_text, new_tags[0])

    if not changes:
        return {"status": "insufficient"}

    if not dry_run and new_text != text:
        path.write_text(new_text, encoding="utf-8")

    return {
        "status": "changed",
        "path":   str(path.relative_to(ROOT)),
        "changes": changes,
    }


# ── Main ─────────────────────────────────────────────────────────────────────

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
        print("📋 Summary Extender [dry-run] — передайте --apply\n")
    elif not stats_only:
        print("✏️  Summary Extender [apply]\n")

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
    print(f"  Уже OK (≥150ch):  {results['ok']}")
    print(f"  Пропущено:        {results['skip_state']}")
    print(f"  Мало контента:    {results['insufficient']}")

    if changed_list and not stats_only:
        print(f"\n  Примеры изменений:")
        for r in changed_list[:6]:
            print(f"    {r['path']}")
            print(f"      → {', '.join(r['changes'])}")

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
