"""
improve_summaries.py — добавляет краткую аннотацию в начало каждого файла.
Аннотация = первые 3 значимые строки + список найденных проектов в файле.
НЕ использует LLM — работает детерминированно.
Запуск: python scripts/improve_summaries.py
"""
import re
from pathlib import Path

ROOT = Path(__file__).parent.parent
DOCS = ROOT / "docs"

PROJECTS = [
    "Svyazi", "CardIndex", "AgentFS", "knowledge-space", "mclaude",
    "AI Factory", "Rufler", "LiteParse", "Legal RAG", "Hybrid RAG",
    "Graph RAG", "Yodoca", "NGT Memory", "MemNet", "agent-memory-mcp",
    "SENTINEL", "LiteLLM", "Auto AI Router", "Tool Search", "AutoResearch",
    "Wikontic", "Firecrawl", "Yjs", "Automerge", "Whisper", "Yttri",
]

ALREADY_HAS_SUMMARY = "<!-- summary -->"


def extract_annotation(text: str) -> tuple[str, list[str]]:
    """Возвращает (первый_абзац, список_проектов_в_файле)."""
    lines = [l.strip() for l in text.split("\n") if l.strip()]
    # Первый непустой абзац не-заголовок
    snippet = ""
    for line in lines:
        if not line.startswith("#") and not line.startswith("|") and len(line) > 30:
            snippet = line[:200]
            break

    # Проекты, упомянутые в файле
    found = [p for p in PROJECTS if p.lower() in text.lower()]
    return snippet, found


def add_summary(path: Path) -> bool:
    text = path.read_text(encoding="utf-8")

    if ALREADY_HAS_SUMMARY in text:
        return False  # уже обработан
    if len(text) < 150:
        return False  # слишком короткий

    snippet, projects = extract_annotation(text)
    if not snippet:
        return False

    proj_line = ""
    if projects:
        proj_line = f"\n**Проекты:** {', '.join(projects[:8])}"

    summary_block = (
        f"{ALREADY_HAS_SUMMARY}\n"
        f"> {snippet}{proj_line}\n\n"
        f"---\n\n"
    )

    # Вставляем после первого заголовка
    lines = text.split("\n")
    insert_at = 0
    for i, line in enumerate(lines):
        if line.startswith("# "):
            insert_at = i + 1
            break

    lines.insert(insert_at, "\n" + summary_block)
    path.write_text("\n".join(lines), encoding="utf-8")
    return True


def main():
    import sys
    sys.path.insert(0, str(Path(__file__).parent))
    try:
        from utils_docignore import is_ignored
    except ImportError:
        is_ignored = lambda p: False

    updated = 0
    skipped = 0
    for f in sorted(DOCS.rglob("*.md")):
        if f.name == "README.md":
            continue
        if is_ignored(f):
            skipped += 1
            continue
        if add_summary(f):
            updated += 1
        else:
            skipped += 1
    print(f"Обновлено: {updated} файлов, пропущено: {skipped}")


if __name__ == "__main__":
    main()
