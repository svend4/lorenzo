"""
improve_export_csv.py — экспортирует метаданные всех docs/ в CSV.
Создаёт docs/export.csv — удобно для анализа в Excel / Google Sheets.
Запуск: python scripts/improve_export_csv.py
"""
import re
import csv
from pathlib import Path

ROOT = Path(__file__).parent.parent
DOCS = ROOT / "docs"

TAG_RE = re.compile(r'<!--\s*tags:\s*([^-]+)\s*-->')
SUMMARY_RE = re.compile(r'<!--\s*summary\s*-->\s*\n>\s*(.+?)(?:\n|$)')
PROJ_RE = re.compile(r'\*\*Проекты:\*\*\s*(.+)')

PROJECTS = [
    "Svyazi", "CardIndex", "AgentFS", "knowledge-space", "mclaude",
    "AI Factory", "Rufler", "LiteParse", "Legal RAG", "Hybrid RAG",
    "Graph RAG", "Yodoca", "NGT Memory", "MemNet", "SENTINEL",
    "LiteLLM", "Auto AI Router", "Tool Search", "AutoResearch",
    "Wikontic", "Firecrawl", "Yjs", "Automerge",
]

RISK_KW = ["риск", "risk", "опасн", "внимание", "ограничен", "не стоит"]
ACTION_KW = ["следующий шаг", "нужно", "рекомендуется", "начать с", "mvp"]


def get_title(text: str, path: Path) -> str:
    for line in text.split('\n'):
        if line.startswith('# '):
            return line[2:].strip()[:80]
    return path.name.replace('.md', '')


def get_tags(text: str) -> str:
    m = TAG_RE.search(text)
    return m.group(1).strip() if m else ""


def get_summary(text: str) -> str:
    m = SUMMARY_RE.search(text)
    return m.group(1).strip()[:200] if m else ""


def get_projects(text: str) -> str:
    low = text.lower()
    found = [p for p in PROJECTS if p.lower() in low]
    return "; ".join(found)


def has_risk(text: str) -> str:
    low = text.lower()
    return "да" if any(k in low for k in RISK_KW) else "нет"


def has_action(text: str) -> str:
    low = text.lower()
    return "да" if any(k in low for k in ACTION_KW) else "нет"


def get_section(path: Path) -> str:
    parts = path.relative_to(DOCS).parts
    return parts[0] if parts else ""


def main():
    print("Экспорт в CSV...")

    rows = []
    for f in sorted(DOCS.rglob("*.md")):
        skip = {"README.md", "export.csv"}
        if f.name in skip or not f.is_file():
            continue
        text = f.read_text(encoding="utf-8")
        if len(text) < 50:
            continue

        words = len(re.sub(r'[#*`>\[\]|<!--].*', '', text).split())
        rows.append({
            "path":          str(f.relative_to(ROOT)),
            "section":       get_section(f),
            "filename":      f.name,
            "title":         get_title(text, f),
            "words":         words,
            "chars":         len(text),
            "tags":          get_tags(text),
            "projects":      get_projects(text),
            "summary":       get_summary(text),
            "has_risk":      has_risk(text),
            "has_action":    has_action(text),
        })

    out = DOCS / "export.csv"
    fieldnames = ["path", "section", "filename", "title", "words", "chars",
                  "tags", "projects", "summary", "has_risk", "has_action"]

    with open(out, "w", newline="", encoding="utf-8-sig") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)

    size_kb = out.stat().st_size // 1024
    print(f"  wrote: {out.relative_to(ROOT)} ({size_kb} KB, {len(rows)} строк)")

    # Краткая статистика по разделам
    from collections import defaultdict, Counter
    by_section: dict[str, int] = defaultdict(int)
    for r in rows:
        by_section[r["section"]] += 1

    print("\n  Строк по разделам:")
    for section, count in sorted(by_section.items()):
        print(f"    {section}: {count}")


if __name__ == "__main__":
    main()
