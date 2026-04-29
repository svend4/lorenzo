"""
improve_consistency.py — находит разные написания одного термина,
предлагает канонический вариант, создаёт docs/CONSISTENCY.md.
Запуск: python scripts/improve_consistency.py
"""
import re
from pathlib import Path
from collections import defaultdict, Counter

ROOT = Path(__file__).parent.parent
DOCS = ROOT / "docs"

# Группы вариантов написания одного термина
TERM_VARIANTS = {
    "knowledge-space": [
        "knowledge-space", "knowledge space", "knowledge_space", "knowledgespace",
    ],
    "AgentFS": [
        "AgentFS", "Agent FS", "agentfs", "agent-fs", "Agent-FS",
    ],
    "CardIndex": [
        "CardIndex", "Card Index", "card index", "cardindex", "card-index",
    ],
    "AI Factory": [
        "AI Factory", "AI-Factory", "AIFactory", "ai factory", "Ai Factory",
    ],
    "NGT Memory": [
        "NGT Memory", "NGT-Memory", "NGTMemory", "ngt memory", "NGT memory",
    ],
    "LiteParse": [
        "LiteParse", "Lite Parse", "liteparse", "lite-parse", "LiteParser",
    ],
    "Auto AI Router": [
        "Auto AI Router", "AutoAI Router", "Auto-AI-Router",
        "auto ai router", "AutoAIRouter",
    ],
    "local-first": [
        "local-first", "local first", "localfirst", "Local-First", "Local First",
    ],
    "agent-memory-mcp": [
        "agent-memory-mcp", "agent memory mcp", "AgentMemoryMCP",
        "agent_memory_mcp",
    ],
    "MclaDE / mclaude": [
        "mclaude", "McLaude", "MC-Claude", "mc-claude",
    ],
    "SENTINEL": [
        "SENTINEL", "Sentinel", "sentinel",
    ],
    "self-improvement": [
        "self-improvement", "self improvement", "self-improve",
        "selfimprovement", "Self-Improvement",
    ],
    "Svyazi 2.0": [
        "Svyazi 2.0", "Svyazi-2.0", "Svyazi2.0", "svyazi 2.0",
    ],
    "evidence envelope": [
        "Evidence Envelope", "evidence envelope", "Evidence-Envelope",
        "EvidenceEnvelope",
    ],
    "Card Envelope": [
        "Card Envelope", "card envelope", "Card-Envelope", "CardEnvelope",
    ],
}

# Канонические написания
CANONICAL = {
    "knowledge-space":     "knowledge-space",
    "AgentFS":             "AgentFS",
    "CardIndex":           "CardIndex",
    "AI Factory":          "AI Factory",
    "NGT Memory":          "NGT Memory",
    "LiteParse":           "LiteParse",
    "Auto AI Router":      "Auto AI Router",
    "local-first":         "local-first",
    "agent-memory-mcp":    "agent-memory-mcp",
    "MclaDE / mclaude":    "mclaude",
    "SENTINEL":            "SENTINEL",
    "self-improvement":    "self-improvement",
    "Svyazi 2.0":          "Svyazi 2.0",
    "evidence envelope":   "Evidence Envelope",
    "Card Envelope":       "Card Envelope",
}


def find_variants(term_group: str, variants: list[str]) -> dict[str, list[str]]:
    """Для каждого варианта — список файлов где он встречается."""
    found: dict[str, list[str]] = defaultdict(list)
    for f in DOCS.rglob("*.md"):
        text = f.read_text(encoding="utf-8")
        rel = str(f.relative_to(ROOT))
        for variant in variants:
            # Поиск без учёта регистра для non-canonical вариантов
            pattern = re.compile(re.escape(variant), re.IGNORECASE)
            if pattern.search(text):
                # Проверяем, что это именно этот вариант (не canonical)
                canonical = CANONICAL.get(term_group, variants[0])
                if variant.lower() != canonical.lower():
                    found[variant].append(rel)
    return found


def main():
    print("Проверка согласованности терминов...")
    lines = [
        "# Согласованность терминов\n",
        "Анализ различных написаний одних и тех же терминов.\n",
        "| Термин | Канонично | Вариант | Файлов |",
        "|--------|-----------|---------|--------|",
    ]

    total_issues = 0
    details = []

    for term_group, variants in TERM_VARIANTS.items():
        canonical = CANONICAL.get(term_group, variants[0])
        found = find_variants(term_group, variants)

        if not found:
            continue

        for variant, files in found.items():
            if not files:
                continue
            total_issues += len(files)
            sample = files[0].split("/")[-1] if files else ""
            lines.append(
                f"| **{term_group}** | `{canonical}` "
                f"| `{variant}` | {len(files)} |"
            )
            details.append({
                "group": term_group,
                "canonical": canonical,
                "variant": variant,
                "files": files,
            })

    lines += [
        f"\n**Всего несогласованных написаний: {total_issues}**\n",
        "\n## Детали по файлам\n",
    ]

    for d in details[:20]:
        lines.append(f"\n### `{d['variant']}` → должно быть `{d['canonical']}`\n")
        for f in d["files"][:5]:
            lines.append(f"- `{f}`")
        if len(d["files"]) > 5:
            lines.append(f"- _...и ещё {len(d['files'])-5}_")

    lines += [
        "\n## Как исправить\n",
        "```bash",
        "# Пример: заменить все вхождения в docs/",
        "find docs/ -name '*.md' -exec sed -i 's/old_term/new_term/g' {} +",
        "```",
    ]

    out = DOCS / "CONSISTENCY.md"
    out.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(f"  wrote: {out.relative_to(ROOT)}")
    print(f"  проблем найдено: {total_issues}")


if __name__ == "__main__":
    main()
