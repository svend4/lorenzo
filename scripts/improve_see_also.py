"""
improve_see_also.py — добавляет блок "See Also / Смотрите также"
в ключевые документы на основе тематического сходства.
Создаёт docs/SEE_ALSO.md (индекс) и вставляет блоки в файлы.
Запуск: python scripts/improve_see_also.py
"""
import re
from pathlib import Path
from collections import defaultdict

ROOT = Path(__file__).parent.parent
DOCS = ROOT / "docs"

MARKER = "<!-- see-also -->"
SKIP   = {"SEE_ALSO.md", "SIMILAR.md", "CROSSREFS.md", "BACKLINKS.md"}

STOPWORDS = {
    "и","в","не","на","что","с","по","это","как","из","для","к","а","но","то",
    "если","или","от","о","при","за","его","её","их","все","они","мы","вы",
    "the","a","an","of","in","to","and","is","are","for","with","by","from",
}

# Вручную заданные тематические связи для ключевых документов
CURATED = {
    "01-executive-summary.md": [
        "03-component-catalog.md",
        "04-ensembles-overview.md",
        "07-mvp-planning.md",
    ],
    "07-mvp-planning.md": [
        "09-architectural-gaps.md",
        "11-integration-contracts.md",
        "12-roadmap.md",
    ],
    "09-architectural-gaps.md": [
        "11-integration-contracts.md",
        "06-security-privacy.md",
        "07-mvp-planning.md",
    ],
    "DECISIONS.md":      ["ACTION_ITEMS.md", "PROGRESS.md", "ROADMAP.md"],
    "CONTACTS.md":       ["AUTHORS.md", "NETWORK.md", "PROGRESS.md"],
    "HEALTH.md":         ["VALIDATION.md", "METRICS.md", "REPORT.md"],
}


def tokenize(text: str) -> set[str]:
    text = re.sub(r'```.*?```', '', text, flags=re.DOTALL)
    words = re.findall(r'[а-яёa-z]{4,}', text.lower())
    return {w for w in words if w not in STOPWORDS}


def jaccard(a: set, b: set) -> float:
    if not a or not b:
        return 0.0
    return len(a & b) / len(a | b)


def find_related(fname: str, tokens: dict[str, set],
                 n: int = 4) -> list[tuple[str, float]]:
    my_tokens = tokens.get(fname, set())
    scores = []
    for other, other_tok in tokens.items():
        if other == fname:
            continue
        j = jaccard(my_tokens, other_tok)
        if j >= 0.08:
            scores.append((other, j))
    scores.sort(key=lambda x: -x[1])
    return scores[:n]


def build_see_also_block(related: list[tuple[str, Path]]) -> str:
    lines = [f"\n{MARKER}\n", "---\n", "**Смотрите также:**"]
    for name, fpath in related:
        stem = Path(name).stem
        try:
            rel = fpath.relative_to(ROOT)
        except ValueError:
            rel = fpath
        lines.append(f"- [{stem}]({rel})")
    lines.append("")
    return "\n".join(lines) + "\n"


def main():
    print("Добавление 'See Also' блоков...")

    # Загружаем токены
    all_files: dict[str, Path] = {}
    tokens:    dict[str, set]  = {}
    for f in sorted(DOCS.rglob("*.md")):
        if f.name in SKIP:
            continue
        text = f.read_text(encoding="utf-8")
        if len(text.split()) < 50:
            continue
        all_files[f.name] = f
        tokens[f.name]    = tokenize(text)

    # Строим карту see-also
    see_also_map: dict[str, list[tuple[str, Path]]] = {}

    for fname, fpath in all_files.items():
        # Curated (приоритет)
        if fname in CURATED:
            related = []
            for ref in CURATED[fname]:
                ref_path = all_files.get(ref) or (DOCS / ref)
                if ref_path.exists():
                    related.append((ref, ref_path))
            if related:
                see_also_map[fname] = related
                continue

        # Автоматически — Jaccard
        auto = find_related(fname, tokens)
        if auto:
            see_also_map[fname] = [
                (other, all_files[other])
                for other, _ in auto
                if other in all_files
            ]

    # Вставляем блоки в файлы
    inserted = 0
    for fname, related in see_also_map.items():
        fpath = all_files.get(fname)
        if not fpath or not fpath.exists():
            continue
        text = fpath.read_text(encoding="utf-8")
        if MARKER in text:
            continue
        block = build_see_also_block(related)
        fpath.write_text(text + block, encoding="utf-8")
        inserted += 1

    # SEE_ALSO.md — индекс
    lines = [
        "# Индекс «Смотрите также»\n",
        f"**Файлов с блоком See Also:** {inserted + sum(1 for f in all_files.values() if MARKER in f.read_text(encoding='utf-8'))}\n",
        "## Ключевые связи\n",
    ]
    for fname, related in list(see_also_map.items())[:30]:
        stem = Path(fname).stem
        refs = ", ".join(f"`{Path(r).stem}`" for r, _ in related)
        lines.append(f"- **{stem}** → {refs}")

    out = DOCS / "SEE_ALSO.md"
    out.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(f"  wrote: {out.relative_to(ROOT)}")
    print(f"  вставлено блоков: {inserted}, файлов в карте: {len(see_also_map)}")


if __name__ == "__main__":
    main()
