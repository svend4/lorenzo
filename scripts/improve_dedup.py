"""
improve_dedup.py — находит дублирующиеся файлы и похожие абзацы.
Создаёт docs/DUPLICATES.md с отчётом.
НЕ удаляет файлы автоматически — только сообщает о них.

Новое: для каждой пары похожих файлов показывает сами совпавшие абзацы (до 3 штук).
Запуск: python scripts/improve_dedup.py
        python scripts/improve_dedup.py --threshold 0.3  # более чувствительный порог
"""
import re
import sys
import hashlib
from pathlib import Path
from collections import defaultdict

ROOT = Path(__file__).parent.parent
DOCS = ROOT / "docs"

# Порог Jaccard сходства (по умолчанию 0.5)
THRESHOLD = 0.5
for arg in sys.argv:
    if arg.startswith("--threshold="):
        THRESHOLD = float(arg.split("=", 1)[1])
if "--threshold" in sys.argv:
    idx = sys.argv.index("--threshold")
    if idx + 1 < len(sys.argv):
        THRESHOLD = float(sys.argv[idx + 1])


def file_hash(path: Path) -> str:
    text = path.read_text(encoding="utf-8")
    normalized = re.sub(r'\s+', ' ', text.strip())
    return hashlib.md5(normalized.encode()).hexdigest()


def split_paragraphs(text: str) -> list[str]:
    """Разбивает на абзацы длиннее 200 символов."""
    paras = re.split(r'\n{2,}', text)
    return [p.strip() for p in paras if len(p.strip()) > 200]


def paragraph_hash_map(text: str) -> dict[str, str]:
    """Возвращает {hash: paragraph_text} для каждого значимого абзаца."""
    result = {}
    for p in split_paragraphs(text):
        norm = re.sub(r'\s+', ' ', p)
        h = hashlib.md5(norm.encode()).hexdigest()
        result[h] = p
    return result


def find_exact_duplicates() -> list[list[Path]]:
    hash_map: dict[str, list[Path]] = defaultdict(list)
    for f in DOCS.rglob("*.md"):
        h = file_hash(f)
        hash_map[h].append(f)
    return [paths for paths in hash_map.values() if len(paths) > 1]


def find_similar_files(threshold: float = THRESHOLD) -> list[tuple[Path, Path, float, list[str]]]:
    """Пары файлов с большим пересечением абзацев + сами общие абзацы."""
    all_files = list(DOCS.rglob("*.md"))
    para_map: dict[Path, dict[str, str]] = {}
    for f in all_files:
        text = f.read_text(encoding="utf-8")
        hmap = paragraph_hash_map(text)
        if hmap:
            para_map[f] = hmap

    similar = []
    files = list(para_map.items())
    for i in range(len(files)):
        for j in range(i + 1, len(files)):
            f1, hmap1 = files[i]
            f2, hmap2 = files[j]
            h1 = set(hmap1.keys())
            h2 = set(hmap2.keys())
            intersection = h1 & h2
            union = h1 | h2
            if not union:
                continue
            jaccard = len(intersection) / len(union)
            if jaccard >= threshold:
                # Тексты общих абзацев (первые 3)
                shared_texts = [hmap1[h] for h in list(intersection)[:3]]
                similar.append((f1, f2, jaccard, shared_texts))

    return sorted(similar, key=lambda x: -x[2])


def _truncate(text: str, max_len: int = 200) -> str:
    """Обрезает абзац для отображения в отчёте."""
    text = text.replace("\n", " ").strip()
    if len(text) <= max_len:
        return text
    return text[:max_len] + "…"


def main():
    print(f"Поиск точных дублей...")
    exact = find_exact_duplicates()

    print(f"Поиск похожих файлов (Jaccard ≥ {THRESHOLD})...")
    similar = find_similar_files(threshold=THRESHOLD)

    lines = [
        "# Отчёт о дублировании\n",
        f"Порог сходства: **{THRESHOLD}**  ",
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
        lines.append("")

    if similar:
        lines.append(f"## Похожие файлы (Jaccard ≥ {THRESHOLD})\n")
        for f1, f2, score, shared in similar[:30]:
            rel1 = f1.relative_to(ROOT)
            rel2 = f2.relative_to(ROOT)
            lines.append(f"### {score:.0%} — `{rel1}` vs `{rel2}`\n")
            if shared:
                lines.append(f"**Общих абзацев:** {len(shared)}  ")
                lines.append("**Примеры совпадений:**\n")
                for para in shared[:3]:
                    lines.append(f"> {_truncate(para)}\n")
            lines.append("---\n")
        if len(similar) > 30:
            lines.append(f"_...и ещё {len(similar)-30} пар._\n")

    lines.append("> Файлы не удалялись автоматически. "
                 "Проверьте вручную и удалите ненужные.")

    out = DOCS / "DUPLICATES.md"
    out.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(f"  wrote: {out.relative_to(ROOT)}")
    print(f"  точных дублей: {len(exact)}, похожих пар: {len(similar)}")
    print(f"  Детальный отчёт с примерами совпадений: docs/DUPLICATES.md")


if __name__ == "__main__":
    main()
