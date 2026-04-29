"""
improve_tags.py — тегирует каждый файл по темам, создаёт docs/TAGS.md
и добавляет строку тегов в начало каждого файла.
Запуск: python scripts/improve_tags.py
"""
import re
from pathlib import Path
from collections import defaultdict

ROOT = Path(__file__).parent.parent
DOCS = ROOT / "docs"

# Тема → ключевые слова для детекции
TOPIC_RULES: dict[str, list[str]] = {
    "memory":        ["yodoca", "ngt memory", "memnet", "agent-memory", "консолидац",
                      "forgetting", "episod", "hebbian", "recall"],
    "rag":           ["rag", "liteparse", "retrieval", "hybrid rag", "graph rag",
                      "legal rag", "bounding box", "page-level", "evidence"],
    "orchestration": ["rufler", "mclaude", "ai factory", "sequential", "handoff",
                      "оркестр", "swarm", "locks", "mailbox"],
    "security":      ["sentinel", "litellm", "tool search", "rlm-toolkit",
                      "безопасн", "pii", "allowlist", "firewall", "quarantine"],
    "knowledge":     ["knowledge-space", "agentfs", "cardindex", "карточк",
                      "agentos", "vault", "reference card"],
    "ingestion":     ["svyazi", "import", "нормализац", "extraction", "llm extraction",
                      "dedup", "дедупликац"],
    "local-first":   ["local-first", "crdt", "yjs", "automerge", "offline",
                      "whisper", "голос", "voice", "yttri"],
    "architecture":  ["архитектур", "контракт", "envelope", "интеграц",
                      "зазор", "слой", "layer", "schema"],
    "roadmap":       ["дорожная карта", "итерац", "mvp", "фаза", "phase",
                      "roadmap", "прототип", "timeline"],
    "anthropic":     ["anthropic", "вакансии", "hiring", "cluster", "gtm",
                      "research engineer", "trust & safety"],
    "self-improve":  ["autoresearch", "self-improv", "benchmark", "eval",
                      "rollback", "nightly", "петл", "самоулучш"],
    "collaboration": ["коллаборац", "автор", "контакт", "habr", "хабр",
                      "svend4", "andrey", "виталий", "kksudo"],
}

ALREADY_TAGGED = "<!-- tags:"


def detect_tags(text: str) -> list[str]:
    low = text.lower()
    tags = []
    for topic, keywords in TOPIC_RULES.items():
        if any(kw in low for kw in keywords):
            tags.append(topic)
    return tags


def tag_file(path: Path) -> list[str]:
    text = path.read_text(encoding="utf-8")
    if ALREADY_TAGGED in text:
        return []
    if len(text) < 100:
        return []

    tags = detect_tags(text)
    if not tags:
        return []

    tag_line = f"{ALREADY_TAGGED} {', '.join(tags)} -->\n"
    lines = text.split("\n")

    # Вставляем после первого заголовка (или в начало)
    insert_at = 0
    for i, line in enumerate(lines):
        if line.startswith("# "):
            insert_at = i + 1
            break

    # Если уже есть блок summary — вставляем после него
    for i in range(insert_at, min(insert_at + 8, len(lines))):
        if lines[i].startswith("---"):
            insert_at = i + 1
            break

    lines.insert(insert_at, tag_line)
    path.write_text("\n".join(lines), encoding="utf-8")
    return tags


def make_tags_index(tag_map: dict[str, list[str]]):
    """Создаёт docs/TAGS.md — индекс файлов по темам."""
    lines = [
        "# Индекс тегов\n",
        "Каждый файл помечен тегами по темам автоматически.\n",
    ]

    for topic in sorted(TOPIC_RULES.keys()):
        files = tag_map.get(topic, [])
        if not files:
            continue
        lines.append(f"\n## #{topic} ({len(files)} файлов)\n")
        for f in sorted(files)[:20]:
            lines.append(f"- `{f}`")
        if len(files) > 20:
            lines.append(f"- _...и ещё {len(files)-20}_")

    out = DOCS / "TAGS.md"
    out.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(f"  wrote: {out.relative_to(ROOT)}")


def main():
    tag_map: dict[str, list[str]] = defaultdict(list)
    updated = 0

    for f in sorted(DOCS.rglob("*.md")):
        if f.name in ("README.md", "TAGS.md", "GLOSSARY.md",
                      "CROSSREFS.md", "DUPLICATES.md", "TIMELINE.md",
                      "AUTHORS.md", "LINKS.md"):
            continue
        tags = tag_file(f)
        if tags:
            updated += 1
            for t in tags:
                tag_map[t].append(str(f.relative_to(ROOT)))

    make_tags_index(tag_map)
    print(f"Тегировано: {updated} файлов, {sum(len(v) for v in tag_map.values())} тег-записей")


if __name__ == "__main__":
    main()
