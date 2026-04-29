"""
improve_dedup.py — находит дублирующиеся файлы и похожие абзацы.
Создаёт docs/DUPLICATES.md с отчётом.
НЕ удаляет файлы автоматически — только сообщает о них.
Запуск: python scripts/improve_dedup.py
"""
import re
import hashlib
from pathlib import Path
from collections import defaultdict

ROOT = Path(__file__).parent.parent
DOCS = ROOT / "docs"


def file_hash(path: Path) -> str:
    text = path.read_text(encoding="utf-8")
    # Нормализуем пробелы для сравнения
    normalized = re.sub(r'\s+', ' ', text.strip())
    return hashlib.md5(normalized.encode()).hexdigest()


def paragraph_hashes(text: str) -> set[str]:
    """Хэши каждого абзаца длиннее 200 символов."""
    paras = re.split(r'\n{2,}', text)
    hashes = set()
    for p in paras:
        p = p.strip()
        if len(p) > 200:
            norm = re.sub(r'\s+', ' ', p)
            hashes.add(hashlib.md5(norm.encode()).hexdigest())
    return hashes


def find_exact_duplicates() -> list[list[Path]]:
    """Группы файлов с одинаковым содержимым."""
    hash_map: dict[str, list[Path]] = defaultdict(list)
    for f in DOCS.rglob("*.md"):
        h = file_hash(f)
        hash_map[h].append(f)
    return [paths for paths in hash_map.values() if len(paths) > 1]


def find_similar_files(threshold: float = 0.5) -> list[tuple[Path, Path, float]]:
    """Пары файлов с большим пересечением абзацев (Jaccard similarity)."""
    all_files = list(DOCS.rglob("*.md"))
    # Строим индекс: файл → множество хэшей абзацев
    para_map: dict[Path, set[str]] = {}
    for f in all_files:
        text = f.read_text(encoding="utf-8")
        hashes = paragraph_hashes(text)
        if hashes:
            para_map[f] = hashes

    similar = []
    files = list(para_map.items())
    for i in range(len(files)):
        for j in range(i + 1, len(files)):
            f1, h1 = files[i]
            f2, h2 = files[j]
            # Jaccard
            intersection = len(h1 & h2)
            union = len(h1 | h2)
            if union == 0:
                continue
            jaccard = intersection / union
            if jaccard >= threshold:
                similar.append((f1, f2, jaccard))

    return sorted(similar, key=lambda x: -x[2])


def main():
    print("Поиск точных дублей...")
    exact = find_exact_duplicates()

    print("Поиск похожих файлов (Jaccard ≥ 0.5)...")
    similar = find_similar_files(threshold=0.5)

    lines = [
        "# Отчёт о дублировании\n",
        f"Точных дублей: **{len(exact)}**  ",
        f"Похожих пар: **{len(similar)}**\n",
    ]

    if exact:
        lines.append("## Точные дубли (одинаковое содержимое)\n")
        lines.append("| Группа | Файлы |")
        lines.append("|--------|-------|")
        for i, group in enumerate(exact, 1):
            names = ", ".join(f"`{f.relative_to(ROOT)}`" for f in group)
            lines.append(f"| #{i} | {names} |")

    if similar:
        lines.append("\n## Похожие файлы (Jaccard ≥ 0.5)\n")
        lines.append("| Файл 1 | Файл 2 | Сходство |")
        lines.append("|--------|--------|----------|")
        for f1, f2, score in similar[:30]:
            lines.append(
                f"| `{f1.relative_to(ROOT)}` "
                f"| `{f2.relative_to(ROOT)}` "
                f"| {score:.0%} |"
            )
        if len(similar) > 30:
            lines.append(f"\n_...и ещё {len(similar)-30} пар._")

    lines.append("\n> Файлы не удалялись автоматически. "
                 "Проверьте вручную и удалите ненужные.")

    out = DOCS / "DUPLICATES.md"
    out.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(f"  wrote: {out.relative_to(ROOT)}")
    print(f"  точных дублей: {len(exact)}, похожих пар: {len(similar)}")


if __name__ == "__main__":
    main()
