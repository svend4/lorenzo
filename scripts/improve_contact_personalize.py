"""
improve_contact_personalize.py — template-based contact message drafts.

Reads each docs/contacts/*.md file, extracts frontmatter metadata (author,
projects, platform, layer), and generates a short personalized first-contact
message. The draft is saved to docs/contacts/{author}_draft.md.

No LLM required — uses project-specific templates filled with known data.
For LLM-enhanced messages: python scripts/improve_llm_contact.py

Templates are chosen based on the author's primary project:
  - memory     → memory-layer integration pitch
  - knowledge  → knowledge-layer integration pitch
  - orchestration → orchestration-layer integration pitch
  - default    → generic Svyazi collaboration pitch

Usage:
  python scripts/improve_contact_personalize.py           # all contacts
  python scripts/improve_contact_personalize.py --author kksudo
  python scripts/improve_contact_personalize.py --dry-run # preview only
  python scripts/improve_contact_personalize.py --stats   # summary table
"""

import re
import sys
from datetime import datetime
from pathlib import Path

ROOT     = Path(__file__).parent.parent
DOCS     = ROOT / "docs"
CONTACTS = DOCS / "contacts"

# ── Project → layer mapping ───────────────────────────────────────────────────

PROJECT_LAYERS = {
    "agentfs":         "knowledge/filesystem",
    "knowledge-space": "knowledge/cards",
    "mclaude":         "knowledge/orchestration",
    "rufler":          "orchestration/YAML",
    "wikontic":        "knowledge/graph",
    "research-docs":   "knowledge/ingestion",
    "liteparse":       "knowledge/ingestion",
    "yodoca":          "memory/consolidation",
    "memnet":          "memory/research",
    "ngt-memory":      "memory/associative",
    "agent-memory-mcp": "memory/typed",
}

PROJECT_DESCRIPTIONS = {
    "AgentFS":         "файловой агент-памяти на базе виртуальной FS",
    "knowledge-space": "граф карточек знаний MIT-лицензии",
    "mclaude":         "MCP-оркестратора на Python",
    "Rufler":          "YAML-декларативного агент-swarm движка",
    "Wikontic":        "семантического графа нормализации",
    "research-docs":   "системы извлечения структурных доказательств",
    "Yodoca":          "SQLite-консолидатора эпизодической памяти",
    "MemNet":          "RAG-вектора памяти с Docling/FAISS",
    "ngt-memory":      "ассоциативного графа NGT-памяти",
    "agent-memory-mcp": "типизированного MCP-интерфейса памяти",
}

LAYER_PITCH = {
    "memory": (
        "Мы строим Svyazi 2.0 — локальную community intelligence platform, "
        "где несколько агентов разделяют единую память. "
        "Ваш проект закрывает критический слой памяти в нашей архитектуре."
    ),
    "knowledge": (
        "Мы строим Svyazi 2.0 — Knowledge OS на базе открытых OSS-проектов. "
        "Ваш проект покрывает слой знаний, который нам нужен как core-компонент."
    ),
    "orchestration": (
        "Мы строим Svyazi 2.0 — мультиагентную платформу. "
        "Ваш оркестратор — один из ключевых слоёв в нашей архитектуре."
    ),
}

# ── Frontmatter parser ────────────────────────────────────────────────────────

def _parse_frontmatter(text: str) -> dict:
    m = re.match(r"^---\s*\n(.*?)\n---", text, re.DOTALL)
    if not m:
        return {}
    fm: dict = {}
    for line in m.group(1).splitlines():
        kv = line.split(":", 1)
        if len(kv) == 2:
            k, v = kv[0].strip(), kv[1].strip().strip('"\'')
            # parse simple lists ["a", "b"]
            if v.startswith("["):
                items = re.findall(r'"([^"]+)"|\'([^\']+)\'|([^\s,\[\]]+)', v)
                v = [next(x for x in t if x) for t in items]
            fm[k] = v
    return fm


def _detect_layer(projects: list, author: str) -> str:
    """Detect primary layer from projects list."""
    proj_lower = [p.lower() for p in projects]
    for key, layer in PROJECT_LAYERS.items():
        if any(key in p for p in proj_lower):
            return layer.split("/")[0]
    return "knowledge"


def _project_description(projects: list) -> str:
    for proj in projects:
        if proj in PROJECT_DESCRIPTIONS:
            return PROJECT_DESCRIPTIONS[proj]
    return f"вашего проекта ({', '.join(projects[:2])})"


# ── Draft generators ──────────────────────────────────────────────────────────

def _github_draft(fm: dict) -> str:
    author   = fm.get("author", "")
    handle   = fm.get("author_handle", f"@{author}")
    projects = fm.get("projects", []) if isinstance(fm.get("projects"), list) else [fm.get("projects", "")]
    layer    = _detect_layer(projects, author)
    proj_desc = _project_description(projects)
    pitch    = LAYER_PITCH.get(layer, LAYER_PITCH["knowledge"])
    proj_str = " и ".join(projects[:2])

    return f"""Привет, {handle}!

Я изучаю {proj_desc} и вижу большой потенциал для коллаборации.

{pitch}

{proj_str} — один из проектов, которые я рассматриваю как core-компонент
слоя {layer}. Мне интересно обсудить:

1. Возможность интеграции {proj_str} в единую архитектуру
2. Ваше видение направления развития проекта
3. Готовность к коллаборации или ревью идей

Если это интересно, я готов поделиться документацией и архитектурными
решениями. Ссылка на репо с исследованием: github.com/svend4/lorenzo

С уважением,
svend4"""


def _telegram_draft(fm: dict) -> str:
    author   = fm.get("author", "")
    projects = fm.get("projects", []) if isinstance(fm.get("projects"), list) else [fm.get("projects", "")]
    layer    = _detect_layer(projects, author)
    proj_str = projects[0] if projects else "вашего проекта"
    pitch    = LAYER_PITCH.get(layer, LAYER_PITCH["knowledge"])

    return f"""Добрый день!

Меня зовут svend4, я строю Svyazi 2.0 — Knowledge OS на базе OSS-проектов с Хабра.

{pitch}

Ваш проект {proj_str} — именно то, что нужно для слоя {layer}.
Хотел бы обсудить возможность интеграции и коллаборации.

Если интересно — напишите, пришлю детали архитектуры."""


def _habr_draft(fm: dict) -> str:
    author   = fm.get("author", "")
    projects = fm.get("projects", []) if isinstance(fm.get("projects"), list) else [fm.get("projects", "")]
    proj_str = " и ".join(projects[:2])

    return f"""Здравствуйте!

Читал вашу статью о {proj_str} с большим интересом.
Строю похожую систему — Svyazi 2.0, Knowledge OS для мультиагентных пайплайнов.

Вижу сильную синергию с вашим подходом. Было бы здорово обменяться идеями
и, возможно, скоординировать развитие совместимых интерфейсов.

Готовы к короткому разговору или переписке?"""


PLATFORM_DRAFTS = {
    "GitHub":   _github_draft,
    "Telegram": _telegram_draft,
    "Habr":     _habr_draft,
}


# ── Main logic ────────────────────────────────────────────────────────────────

def generate_draft(contact_file: Path, dry_run: bool = False) -> dict | None:
    text = contact_file.read_text(encoding="utf-8", errors="ignore")
    fm   = _parse_frontmatter(text)

    author   = fm.get("author") or contact_file.stem
    platform = fm.get("platform", "GitHub")
    status   = fm.get("status", "")
    priority = int(fm.get("priority", 5) or 5)
    projects = fm.get("projects", []) if isinstance(fm.get("projects"), list) else [str(fm.get("projects", ""))]

    # Skip if already messaged
    if status in ("messaged", "replied", "partner"):
        return {"author": author, "status": "skipped", "reason": f"status={status}"}

    gen_fn = PLATFORM_DRAFTS.get(platform, _github_draft)
    draft  = gen_fn(fm)

    if dry_run:
        return {
            "author":   author,
            "platform": platform,
            "priority": priority,
            "projects": projects,
            "draft_preview": draft[:200] + "…",
        }

    out = CONTACTS / f"{author}_draft.md"
    out.write_text(
        f"---\nauthor: {author}\nplatform: {platform}\npriority: {priority}\n"
        f"generated: {datetime.now().strftime('%Y-%m-%d')}\nstatus: draft\n---\n\n"
        f"# Черновик сообщения — {author} ({platform})\n\n"
        f"**Проекты:** {', '.join(projects)}\n\n"
        f"---\n\n{draft}\n",
        encoding="utf-8",
    )
    return {"author": author, "platform": platform, "file": str(out.relative_to(ROOT))}


def main() -> int:
    args     = sys.argv[1:]
    dry_run  = "--dry-run" in args
    stats    = "--stats" in args
    author_f = ""

    i = 0
    while i < len(args):
        if args[i] == "--author" and i + 1 < len(args):
            author_f = args[i + 1]; i += 2
        else:
            i += 1

    if not CONTACTS.exists():
        print("⚠  Папка docs/contacts/ не найдена.")
        return 1

    contact_files = [
        p for p in CONTACTS.glob("*.md")
        if p.stem not in ("README", "QA") and not p.stem.endswith("_draft")
    ]
    if author_f:
        contact_files = [p for p in contact_files if author_f.lower() in p.stem.lower()]

    if stats:
        print(f"{'Author':<20} {'Platform':<12} {'Status':<12} {'Priority':<8} {'Projects'}")
        print("-" * 75)
        for cf in sorted(contact_files):
            fm = _parse_frontmatter(cf.read_text(encoding="utf-8", errors="ignore"))
            projs = fm.get("projects", [])
            if isinstance(projs, list):
                projs_str = ", ".join(projs[:2])
            else:
                projs_str = str(projs)
            print(f"{cf.stem:<20} {fm.get('platform','?'):<12} "
                  f"{fm.get('status','?'):<12} {fm.get('priority','?'):<8} {projs_str}")
        return 0

    results = []
    for cf in sorted(contact_files):
        r = generate_draft(cf, dry_run=dry_run)
        if r:
            results.append(r)

    generated = [r for r in results if r.get("file")]
    skipped   = [r for r in results if r.get("status") == "skipped"]
    previewed = [r for r in results if r.get("draft_preview")]

    if dry_run:
        print(f"📋 Dry-run: {len(previewed)} черновиков / {len(skipped)} пропущено\n")
        for r in previewed[:5]:
            print(f"  [{r['priority']}] {r['author']} ({r['platform']}) — {', '.join(r['projects'])}")
            print(f"       {r['draft_preview'][:120]}")
            print()
    else:
        print(f"✉️  Персонализированные черновики")
        print(f"   Сгенерировано: {len(generated)}")
        print(f"   Пропущено: {len(skipped)} (уже в контакте)")
        for r in generated:
            print(f"   ✅ {r['author']} ({r['platform']}) → {r['file']}")

    return 0


if __name__ == "__main__":
    sys.exit(main())
