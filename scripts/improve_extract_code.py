"""
improve_extract_code.py — извлекает все code-блоки из docs/.
Разделяет по языкам: mermaid, python, yaml, bash, json, другие.
Создаёт docs/CODE_BLOCKS.md.
Запуск: python scripts/improve_extract_code.py
"""
import re
from pathlib import Path
from collections import defaultdict

ROOT = Path(__file__).parent.parent
DOCS = ROOT / "docs"

CODE_RE = re.compile(r'```(\w*)\n(.*?)```', re.DOTALL)

LANG_LABELS = {
    "mermaid":    "📊 Диаграммы Mermaid",
    "python":     "🐍 Python",
    "yaml":       "📋 YAML",
    "bash":       "💻 Bash / Shell",
    "json":       "📦 JSON",
    "dot":        "🕸️ Graphviz DOT",
    "sql":        "🗄️ SQL",
    "javascript": "🌐 JavaScript",
    "":           "📝 Без языка",
}


def extract_blocks(text: str, filepath: Path) -> list[dict]:
    blocks = []
    for m in CODE_RE.finditer(text):
        lang = m.group(1).lower().strip()
        code = m.group(2).strip()
        if len(code) < 10:
            continue

        # Контекст: ближайший заголовок перед блоком
        before = text[:m.start()]
        headers = re.findall(r'^#{1,3}\s+(.+)$', before, re.MULTILINE)
        context = headers[-1] if headers else ""

        blocks.append({
            "lang": lang,
            "code": code,
            "context": context[:60],
            "file": str(filepath.relative_to(ROOT)),
            "lines": code.count('\n') + 1,
        })
    return blocks


def main():
    print("Извлечение code-блоков...")
    by_lang: dict[str, list[dict]] = defaultdict(list)
    total = 0

    for f in sorted(DOCS.rglob("*.md")):
        skip = {"CODE_BLOCKS.md", "MINDMAP.md", "GRAPH.md"}
        if f.name in skip:
            continue
        text = f.read_text(encoding="utf-8")
        for block in extract_blocks(text, f):
            by_lang[block["lang"]].append(block)
            total += 1

    # Статистика
    lang_stats = {lang: len(blocks) for lang, blocks in by_lang.items()}
    print(f"  найдено блоков: {total}")
    for lang, count in sorted(lang_stats.items(), key=lambda x: -x[1]):
        print(f"    {lang or '(без языка)'}: {count}")

    lines = [
        "# Code-блоки репозитория\n",
        f"**Всего блоков:** {total}\n",
        "| Язык | Блоков |",
        "|------|--------|",
    ]
    for lang, count in sorted(lang_stats.items(), key=lambda x: -x[1]):
        label = LANG_LABELS.get(lang, lang)
        lines.append(f"| {label} | {count} |")

    # По языкам
    priority_langs = ["mermaid", "python", "yaml", "bash", "json", "dot", ""]
    for lang in priority_langs + [l for l in by_lang if l not in priority_langs]:
        blocks = by_lang.get(lang, [])
        if not blocks:
            continue
        label = LANG_LABELS.get(lang, lang or "Прочие")
        lines.append(f"\n## {label} ({len(blocks)})\n")

        for b in blocks[:15]:  # не более 15 на язык
            ctx = b["context"] or b["file"].split("/")[-1].replace(".md","")
            lines.append(f"\n### {ctx}")
            lines.append(f"_`{b['file']}` | {b['lines']} строк_\n")
            lines.append(f"```{lang}")
            lines.append(b["code"][:800])  # обрезаем очень длинные
            if len(b["code"]) > 800:
                lines.append("# ... (обрезано)")
            lines.append("```")

        if len(blocks) > 15:
            lines.append(f"\n_...и ещё {len(blocks)-15} блоков этого языка_")

    out = DOCS / "CODE_BLOCKS.md"
    out.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(f"  wrote: {out.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
