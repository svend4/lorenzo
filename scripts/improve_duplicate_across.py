"""
improve_duplicate_across.py — поиск похожих текстов между репозиториями/папками.

Сравнивает docs/ с:
  a) Другой локальной папкой (--other-dir /path/to/repo2/docs)
  b) Другим git-репозиторием (--other-repo /path/to/other-repo)
  c) Поддиректориями внутри docs/ (--internal — сравнивает секции между собой)

Алгоритм сравнения:
  - Shingling (4-граммы токенов) + Jaccard для грубого фильтра
  - Далее точное слово-за-словом попадание для подтверждения

Создаёт docs/DUPLICATE_ACROSS.md.
Запуск:
    python scripts/improve_duplicate_across.py --internal
    python scripts/improve_duplicate_across.py --other-dir /path/to/other/docs
    python scripts/improve_duplicate_across.py --other-repo /path/to/repo
    python scripts/improve_duplicate_across.py --internal --threshold 0.4
    python scripts/improve_duplicate_across.py --internal --section 02-anthropic-vacancies
"""
import re
import sys
from collections import Counter, defaultdict
from pathlib import Path
from datetime import date

ROOT = Path(__file__).parent.parent
DOCS = ROOT / "docs"
TODAY = date.today().isoformat()

INTERNAL   = "--internal"    in sys.argv
OTHER_DIR  = None
OTHER_REPO = None

if "--other-dir" in sys.argv:
    idx = sys.argv.index("--other-dir")
    if idx + 1 < len(sys.argv):
        OTHER_DIR = Path(sys.argv[idx + 1])

if "--other-repo" in sys.argv:
    idx = sys.argv.index("--other-repo")
    if idx + 1 < len(sys.argv):
        OTHER_REPO = Path(sys.argv[idx + 1])

THRESHOLD = 0.3
if "--threshold" in sys.argv:
    idx = sys.argv.index("--threshold")
    if idx + 1 < len(sys.argv):
        THRESHOLD = float(sys.argv[idx + 1])

SECTION_FILTER = None
if "--section" in sys.argv:
    idx = sys.argv.index("--section")
    if idx + 1 < len(sys.argv):
        SECTION_FILTER = DOCS / sys.argv[idx + 1]

SKIP_FILES = {
    "README.md", "SEARCH.md", "READABILITY.md", "SPELLCHECK.md",
    "CONTENT_GAPS.md", "LINK_PREVIEW.md", "BROKEN_LINKS.md",
    "COVERAGE.md", "STALENESS.md", "OUTLINE.md", "COMPARE.md",
    "DUPLICATE_ACROSS.md", "SOURCE_MAP.md",
}

STOPWORDS = {
    "и", "в", "не", "на", "с", "по", "к", "из", "за", "для", "это",
    "как", "но", "или", "что", "был", "the", "a", "an", "is", "are",
    "of", "in", "on", "to", "for", "with", "by", "and", "not",
}

MIN_TOKENS = 30   # минимум токенов для сравнения
SHINGLE_N  = 4    # размер шингла


def _tokens(text: str) -> list[str]:
    clean = re.sub(r'```.*?```', ' ', text, flags=re.DOTALL)
    clean = re.sub(r'https?://\S+', ' ', clean)
    return [
        t for t in re.findall(r'[а-яёa-z]{3,}', clean.lower())
        if t not in STOPWORDS
    ]


def _shingles(tokens: list[str], n: int = SHINGLE_N) -> set[str]:
    """N-граммы токенов."""
    if len(tokens) < n:
        return set()
    return {' '.join(tokens[i:i+n]) for i in range(len(tokens) - n + 1)}


def _jaccard_shingle(sh_a: set, sh_b: set) -> float:
    if not sh_a or not sh_b:
        return 0.0
    return len(sh_a & sh_b) / len(sh_a | sh_b)


def _word_overlap(tok_a: list, tok_b: list) -> float:
    """Простое словарное пересечение."""
    s_a, s_b = set(tok_a), set(tok_b)
    return len(s_a & s_b) / max(1, len(s_a | s_b))


def _load_files(directory: Path) -> dict[str, dict]:
    """Загружает файлы и вычисляет их fingerprint."""
    result = {}
    for f in sorted(directory.rglob("*.md")):
        if f.name in SKIP_FILES:
            continue
        try:
            text = f.read_text(encoding="utf-8")
        except Exception:
            continue
        tok = _tokens(text)
        if len(tok) < MIN_TOKENS:
            continue
        result[str(f)] = {
            "path": f,
            "tokens": tok,
            "shingles": _shingles(tok),
            "words": len(text.split()),
        }
    return result


def _find_duplicates(corpus_a: dict, corpus_b: dict,
                     threshold: float) -> list[dict]:
    """Находит похожие пары между двумя корпусами."""
    pairs = []
    items_a = list(corpus_a.values())
    items_b = list(corpus_b.values())

    total = len(items_a) * len(items_b)
    checked = 0
    print(f"   Сравниваем {len(items_a)} × {len(items_b)} = {total} пар...", end=" ", flush=True)

    for a in items_a:
        for b in items_b:
            if a["path"] == b["path"]:
                continue
            # Быстрый фильтр по шинглам
            sh_sim = _jaccard_shingle(a["shingles"], b["shingles"])
            if sh_sim < threshold * 0.5:
                continue
            # Точная проверка
            w_sim = _word_overlap(a["tokens"], b["tokens"])
            combined = (sh_sim * 0.7 + w_sim * 0.3)
            if combined >= threshold:
                pairs.append({
                    "path_a": a["path"],
                    "path_b": b["path"],
                    "shingle_sim": round(sh_sim, 3),
                    "word_sim": round(w_sim, 3),
                    "combined": round(combined, 3),
                    "words_a": a["words"],
                    "words_b": b["words"],
                })

    print(f"готово, дублей: {len(pairs)}")
    return sorted(pairs, key=lambda x: -x["combined"])


def _verdict(sim: float) -> str:
    if sim >= 0.6:
        return "🔴 Вероятный дубликат"
    elif sim >= 0.4:
        return "🟡 Значительное перекрытие"
    return "🟢 Умеренное сходство"


def main() -> None:
    print("🔎 improve_duplicate_across.py — поиск дублей между источниками")
    print(f"   Порог схожести: {THRESHOLD}\n")

    target = SECTION_FILTER or DOCS

    if INTERNAL:
        print("   Режим: внутренний (между секциями docs/)\n")
        # Разбиваем по секциям
        sections: dict[str, dict] = {}
        for item in sorted(DOCS.iterdir()):
            if item.is_dir() and not item.name.startswith('.'):
                corpus = _load_files(item)
                if corpus:
                    sections[item.name] = corpus

        all_pairs = []
        section_names = list(sections.keys())
        for i in range(len(section_names)):
            for j in range(i + 1, len(section_names)):
                sa, sb = section_names[i], section_names[j]
                print(f"  {sa} ↔ {sb}")
                pairs = _find_duplicates(sections[sa], sections[sb], THRESHOLD)
                for p in pairs:
                    p["section_a"] = sa
                    p["section_b"] = sb
                all_pairs.extend(pairs)

        corpus_a = _load_files(target)
        corpus_b = {}  # не нужен в internal

    elif OTHER_DIR:
        if not OTHER_DIR.exists():
            print(f"❌ Папка не найдена: {OTHER_DIR}")
            return
        print(f"   Режим: сравнение с {OTHER_DIR}\n")
        corpus_a = _load_files(target)
        corpus_b = _load_files(OTHER_DIR)
        all_pairs = _find_duplicates(corpus_a, corpus_b, THRESHOLD)
        for p in all_pairs:
            p["section_a"] = str(target.relative_to(ROOT))
            p["section_b"] = str(OTHER_DIR)

    elif OTHER_REPO:
        # Ищем docs/ в другом репо
        other_docs = OTHER_REPO / "docs"
        if not other_docs.exists():
            other_docs = OTHER_REPO  # fallback: весь репо
        if not other_docs.exists():
            print(f"❌ Репозиторий не найден: {OTHER_REPO}")
            return
        print(f"   Режим: сравнение с репозиторием {OTHER_REPO}\n")
        corpus_a = _load_files(target)
        corpus_b = _load_files(other_docs)
        all_pairs = _find_duplicates(corpus_a, corpus_b, THRESHOLD)
        for p in all_pairs:
            p["section_a"] = str(target.relative_to(ROOT))
            p["section_b"] = str(OTHER_REPO)
    else:
        print("Использование:")
        print("  --internal                          сравнить секции внутри docs/")
        print("  --other-dir /path/to/other/docs     сравнить с другой папкой")
        print("  --other-repo /path/to/other-repo    сравнить с другим репозиторием")
        return

    # Формируем отчёт
    lines = [
        "# Поиск дублей между источниками\n",
        f"_Обновлено: {TODAY}_\n",
        f"Порог схожести: **{THRESHOLD}** | Найдено пар: **{len(all_pairs)}**\n",
    ]

    if all_pairs:
        lines += [
            "## Топ похожих пар\n",
            "| # | Файл A | Файл B | Схожесть | Вердикт |",
            "|---|--------|--------|----------|---------|",
        ]
        for i, p in enumerate(all_pairs[:50], 1):
            try:
                rel_a = p["path_a"].relative_to(ROOT)
            except ValueError:
                rel_a = p["path_a"]
            try:
                rel_b = p["path_b"].relative_to(ROOT)
            except ValueError:
                rel_b = p["path_b"]
            pct = int(p["combined"] * 100)
            verdict = _verdict(p["combined"])
            lines.append(f"| {i} | `{rel_a}` | `{rel_b}` | {pct}% | {verdict} |")

        # Детали топ-10
        lines += ["\n## Детали топ-10\n"]
        for p in all_pairs[:10]:
            try:
                rel_a = p["path_a"].relative_to(ROOT)
                rel_b = p["path_b"].relative_to(ROOT)
            except ValueError:
                rel_a, rel_b = p["path_a"], p["path_b"]
            lines.append(f"### {p['combined']*100:.0f}% — `{rel_a.name}` ↔ `{rel_b.name}`\n")
            lines.append(f"- Шингловое сходство: {p['shingle_sim']*100:.0f}%")
            lines.append(f"- Словарное пересечение: {p['word_sim']*100:.0f}%")
            lines.append(f"- Слов A: {p['words_a']} | Слов B: {p['words_b']}")
            lines.append(f"- **{_verdict(p['combined'])}**")
            if p["combined"] >= 0.5:
                lines.append("- 💡 Рекомендация: рассмотреть слияние → `improve_merge_by_topic.py`")
            lines.append("")
    else:
        lines.append(f"_Дублей не найдено при пороге {THRESHOLD}. "
                     "Попробуйте уменьшить --threshold._\n")

    out = DOCS / "DUPLICATE_ACROSS.md"
    out.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(f"\n  wrote: {out.relative_to(ROOT)}")
    print(f"  найдено пар: {len(all_pairs)}")
    if all_pairs:
        top3 = all_pairs[:3]
        for p in top3:
            print(f"    {p['combined']*100:.0f}%: {p['path_a'].name} ↔ {p['path_b'].name}")


if __name__ == "__main__":
    main()
