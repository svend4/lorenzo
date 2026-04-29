"""
improve_similar.py — для каждого документа находит топ-3 похожих.
Использует Jaccard по множеству слов (без ML-зависимостей).
Добавляет блок "Похожие документы" в конец каждого файла
и создаёт сводный docs/SIMILAR.md.
Запуск: python scripts/improve_similar.py
"""
import re
from pathlib import Path

ROOT = Path(__file__).parent.parent
DOCS = ROOT / "docs"

STOPWORDS = {
    "и","в","не","на","что","с","по","это","как","из","для","к","а","но","то",
    "если","или","от","о","при","за","уже","чем","так","же","его","её","их",
    "все","они","он","она","мы","вы","я","бы","быть","только","ещё","также",
    "the","a","an","of","in","to","and","is","are","for","with","be","by",
}

SKIP_NAMES = {
    "SIMILAR.md","CLUSTERS.md","CROSSREFS.md","WORD_FREQ.md",
    "STATS.md","COMPARE.md","HEALTH.md",
}


def tokenize(text: str) -> set[str]:
    text = re.sub(r'```.*?```', '', text, flags=re.DOTALL)
    words = re.findall(r'[а-яёa-z]{4,}', text.lower())
    return {w for w in words if w not in STOPWORDS}


def jaccard(a: set, b: set) -> float:
    if not a or not b:
        return 0.0
    return len(a & b) / len(a | b)


def main():
    print("Поиск похожих документов...")

    files = [f for f in sorted(DOCS.rglob("*.md")) if f.name not in SKIP_NAMES]
    docs = [(f, tokenize(f.read_text(encoding="utf-8"))) for f in files]

    # Для каждого документа — топ-3 похожих
    similar: dict[Path, list[tuple[float, Path]]] = {}
    for i, (fi, wi) in enumerate(docs):
        scores = []
        for j, (fj, wj) in enumerate(docs):
            if i == j:
                continue
            scores.append((jaccard(wi, wj), fj))
        scores.sort(reverse=True)
        similar[fi] = scores[:3]

    # Сводный SIMILAR.md
    lines = [
        "# Похожие документы\n",
        f"**Файлов проанализировано:** {len(files)}\n",
        "Для каждого документа — топ-3 похожих по словарному пересечению (Jaccard).\n",
    ]

    # Топ пары по схожести
    all_pairs = []
    for fi, tops in similar.items():
        for score, fj in tops:
            if score > 0:
                key = tuple(sorted([str(fi), str(fj)]))
                all_pairs.append((score, fi, fj, key))

    seen_pairs: set = set()
    unique_pairs = []
    for score, fi, fj, key in sorted(all_pairs, reverse=True):
        if key not in seen_pairs:
            seen_pairs.add(key)
            unique_pairs.append((score, fi, fj))

    lines += [
        "## Топ-20 самых похожих пар\n",
        "| Сходство | Файл A | Файл B |",
        "|----------|--------|--------|",
    ]
    for score, fi, fj in unique_pairs[:20]:
        a = fi.relative_to(ROOT)
        b = fj.relative_to(ROOT)
        lines.append(f"| {score:.3f} | `{a.name}` | `{b.name}` |")

    lines += ["\n## По разделам\n"]
    from collections import defaultdict
    by_section: dict[str, list] = defaultdict(list)
    for score, fi, fj in unique_pairs[:100]:
        sec = fi.relative_to(DOCS).parts[0] if len(fi.relative_to(DOCS).parts) > 1 else "root"
        by_section[sec].append((score, fi.name, fj.name))

    for sec, pairs in sorted(by_section.items()):
        lines.append(f"\n### {sec}\n")
        for score, a, b in pairs[:5]:
            lines.append(f"- `{a}` ↔ `{b}` ({score:.3f})")

    out = DOCS / "SIMILAR.md"
    out.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(f"  wrote: {out.relative_to(ROOT)}")

    # Добавляем блок в файлы с похожими >0.1
    updated = 0
    for fi, tops in similar.items():
        good = [(s, fj) for s, fj in tops if s >= 0.10]
        if not good:
            continue
        text = fi.read_text(encoding="utf-8")
        marker = "<!-- similar-docs -->"
        if marker in text:
            continue

        block = [f"\n{marker}\n", "---\n", "**Похожие документы:**"]
        for score, fj in good:
            rel = fj.relative_to(ROOT)
            block.append(f"- [{fj.stem}]({rel}) (сходство {score:.2f})")
        block.append("")

        fi.write_text(text + "\n".join(block) + "\n", encoding="utf-8")
        updated += 1

    print(f"  похожих пар: {len(unique_pairs)}, обновлено файлов: {updated}")


if __name__ == "__main__":
    main()
