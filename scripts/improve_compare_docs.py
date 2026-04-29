"""
improve_compare_docs.py — сравнивает два документа: общее, различия, пересечения.

Анализирует:
  - Общие темы (по ключевым словам TF)
  - Уникальные разделы (заголовки есть в одном, нет в другом)
  - Словарное пересечение (Jaccard)
  - Структурное сходство
  - Рекомендации: что взять из каждого

Также поддерживает режим --batch: сравнивает все файлы секции попарно
и находит наиболее похожие пары.

Запуск:
    python scripts/improve_compare_docs.py --a docs/file1.md --b docs/file2.md
    python scripts/improve_compare_docs.py --a docs/file1.md --b docs/file2.md --out docs/COMPARE.md
    python scripts/improve_compare_docs.py --batch --section 05-habr-projects
    python scripts/improve_compare_docs.py --batch --section 05-habr-projects --top 10
"""
import re
import sys
from collections import Counter
from pathlib import Path
from datetime import date

ROOT = Path(__file__).parent.parent
DOCS = ROOT / "docs"
TODAY = date.today().isoformat()

BATCH = "--batch" in sys.argv

FILE_A = FILE_B = None
if "--a" in sys.argv:
    idx = sys.argv.index("--a")
    if idx + 1 < len(sys.argv):
        FILE_A = ROOT / sys.argv[idx + 1]

if "--b" in sys.argv:
    idx = sys.argv.index("--b")
    if idx + 1 < len(sys.argv):
        FILE_B = ROOT / sys.argv[idx + 1]

OUT_FILE = None
if "--out" in sys.argv:
    idx = sys.argv.index("--out")
    if idx + 1 < len(sys.argv):
        OUT_FILE = ROOT / sys.argv[idx + 1]

TOP_N = 20
if "--top" in sys.argv:
    idx = sys.argv.index("--top")
    if idx + 1 < len(sys.argv):
        TOP_N = int(sys.argv[idx + 1])

SECTION_FILTER = None
if "--section" in sys.argv:
    idx = sys.argv.index("--section")
    if idx + 1 < len(sys.argv):
        SECTION_FILTER = DOCS / sys.argv[idx + 1]

STOPWORDS = {
    "и", "в", "не", "на", "с", "по", "к", "из", "за", "для", "это",
    "как", "но", "или", "что", "был", "the", "a", "an", "is", "are",
    "of", "in", "on", "to", "for", "with", "by", "and", "not",
    "это", "этот", "эта", "он", "она", "они",
}


def _clean(text: str) -> str:
    text = re.sub(r'```.*?```', ' ', text, flags=re.DOTALL)
    text = re.sub(r'`[^`]+`', ' ', text)
    text = re.sub(r'<!--.*?-->', ' ', text, flags=re.DOTALL)
    text = re.sub(r'https?://\S+', ' ', text)
    return text.lower()


def _tokens(text: str) -> list[str]:
    return [
        t for t in re.findall(r'[а-яёa-z]{4,}', _clean(text))
        if t not in STOPWORDS
    ]


def _top_words(text: str, n: int = 20) -> set[str]:
    return {w for w, _ in Counter(_tokens(text)).most_common(n)}


def _headings(text: str) -> list[str]:
    return [
        re.sub(r'[`*_]', '', m.group(2)).strip()
        for m in re.finditer(r'^(#{1,3})\s+(.+)$', text, re.MULTILINE)
    ]


def _word_count(text: str) -> int:
    return len(re.findall(r'\S+', text))


def _sentences(text: str) -> list[str]:
    clean = _clean(text)
    return [s.strip() for s in re.split(r'[.!?]+', clean) if len(s.strip()) > 30]


def compare_two(path_a: Path, path_b: Path) -> dict:
    """Основное сравнение двух файлов."""
    text_a = path_a.read_text(encoding="utf-8")
    text_b = path_b.read_text(encoding="utf-8")

    words_a = set(_tokens(text_a))
    words_b = set(_tokens(text_b))

    common_words = words_a & words_b
    only_a = words_a - words_b
    only_b = words_b - words_a
    jaccard = len(common_words) / max(1, len(words_a | words_b))

    heads_a = set(_headings(text_a))
    heads_b = set(_headings(text_b))
    common_heads = heads_a & heads_b
    only_heads_a = heads_a - heads_b
    only_heads_b = heads_b - heads_a

    # Топ уникальных слов каждого
    tf_a = Counter(_tokens(text_a))
    tf_b = Counter(_tokens(text_b))
    unique_a = [w for w, _ in tf_a.most_common(30) if w not in words_b][:10]
    unique_b = [w for w, _ in tf_b.most_common(30) if w not in words_a][:10]

    # Структурное сходство
    wc_a = _word_count(text_a)
    wc_b = _word_count(text_b)
    size_ratio = min(wc_a, wc_b) / max(1, max(wc_a, wc_b))

    return {
        "path_a": path_a, "path_b": path_b,
        "words_a": wc_a, "words_b": wc_b,
        "jaccard": round(jaccard, 3),
        "common_words": sorted(common_words)[:20],
        "unique_a": unique_a,
        "unique_b": unique_b,
        "common_heads": sorted(common_heads),
        "only_heads_a": sorted(only_heads_a),
        "only_heads_b": sorted(only_heads_b),
        "size_ratio": round(size_ratio, 2),
    }


def format_comparison(r: dict) -> list[str]:
    rel_a = r["path_a"].relative_to(ROOT)
    rel_b = r["path_b"].relative_to(ROOT)
    jaccard_pct = int(r["jaccard"] * 100)

    # Оценка сходства
    if r["jaccard"] >= 0.5:
        verdict = "🔴 Высокое сходство — возможно дублирование"
    elif r["jaccard"] >= 0.3:
        verdict = "🟡 Умеренное сходство — связанные темы"
    else:
        verdict = "🟢 Слабое сходство — разные темы"

    lines = [
        f"## Сравнение: `{rel_a}` vs `{rel_b}`\n",
        f"**Схожесть (Jaccard):** {jaccard_pct}% — {verdict}\n",
        f"| Параметр | {rel_a.name} | {rel_b.name} |",
        "|---------|---------|---------|",
        f"| Слов | {r['words_a']:,} | {r['words_b']:,} |",
        f"| Разделов | {len(r['common_heads']) + len(r['only_heads_a'])} | {len(r['common_heads']) + len(r['only_heads_b'])} |",
        "",
    ]

    if r["common_words"]:
        lines.append(f"**Общие темы:** {', '.join(f'`{w}`' for w in r['common_words'][:12])}\n")

    if r["common_heads"]:
        lines.append(f"**Общие разделы:** {', '.join(r['common_heads'][:5])}\n")

    if r["unique_a"]:
        lines.append(f"**Уникально в {rel_a.name}:** {', '.join(f'`{w}`' for w in r['unique_a'])}\n")

    if r["unique_b"]:
        lines.append(f"**Уникально в {rel_b.name}:** {', '.join(f'`{w}`' for w in r['unique_b'])}\n")

    if r["only_heads_a"]:
        lines.append(f"**Разделы только в A:** {', '.join(r['only_heads_a'][:4])}\n")

    if r["only_heads_b"]:
        lines.append(f"**Разделы только в B:** {', '.join(r['only_heads_b'][:4])}\n")

    # Рекомендации
    if r["jaccard"] >= 0.4:
        lines.append("**Рекомендация:** Рассмотреть слияние → `improve_merge_by_topic.py`\n")
    elif r["unique_a"] and r["unique_b"]:
        lines.append("**Рекомендация:** Добавить перекрёстные ссылки между документами\n")

    return lines


def batch_compare(files: list[Path]) -> list[dict]:
    """Попарное сравнение, возвращает топ похожих пар."""
    pairs = []
    n = len(files)
    print(f"   Вычисляем {n*(n-1)//2} пар...", end=" ", flush=True)

    # Предварительно кэшируем токены
    tokens_cache: dict[str, set[str]] = {}
    for f in files:
        try:
            text = f.read_text(encoding="utf-8")
            tokens_cache[str(f)] = set(_tokens(text))
        except Exception:
            tokens_cache[str(f)] = set()

    for i in range(n):
        for j in range(i + 1, n):
            a, b = files[i], files[j]
            ta = tokens_cache[str(a)]
            tb = tokens_cache[str(b)]
            if not ta or not tb:
                continue
            jaccard = len(ta & tb) / max(1, len(ta | tb))
            if jaccard >= 0.1:  # фильтр нерелевантных
                pairs.append({"path_a": a, "path_b": b, "jaccard": round(jaccard, 3)})

    print(f"готово, найдено {len(pairs)} пар с jaccard≥0.1")
    return sorted(pairs, key=lambda x: -x["jaccard"])[:TOP_N]


def main() -> None:
    print("🔍 improve_compare_docs.py — сравнение документов\n")

    if BATCH:
        target = SECTION_FILTER or DOCS
        files = [f for f in sorted(target.rglob("*.md"))
                 if f.name not in {"README.md", "SEARCH.md"}]
        print(f"   Файлов: {len(files)} | Режим: batch (топ-{TOP_N} пар)\n")

        top_pairs = batch_compare(files)

        lines = [
            "# Топ похожих пар документов\n",
            f"_Обновлено: {TODAY}_\n",
            f"Найдено пар: **{len(top_pairs)}**\n",
            "| # | Файл A | Файл B | Jaccard | Вердикт |",
            "|---|--------|--------|---------|---------|",
        ]
        for i, p in enumerate(top_pairs, 1):
            ra = p["path_a"].relative_to(ROOT)
            rb = p["path_b"].relative_to(ROOT)
            pct = int(p["jaccard"] * 100)
            verdict = "🔴 дубль?" if pct >= 50 else ("🟡 связь" if pct >= 30 else "🟢 слабо")
            lines.append(f"| {i} | `{ra}` | `{rb}` | {pct}% | {verdict} |")

        out = OUT_FILE or (DOCS / "COMPARE.md")
        out.write_text("\n".join(lines) + "\n", encoding="utf-8")
        print(f"\n  wrote: {out.relative_to(ROOT)}")
        return

    if not FILE_A or not FILE_B:
        print("Использование:")
        print("  python scripts/improve_compare_docs.py --a docs/file1.md --b docs/file2.md")
        print("  python scripts/improve_compare_docs.py --batch --section 05-habr-projects")
        return

    if not FILE_A.exists():
        print(f"❌ Файл не найден: {FILE_A}")
        return
    if not FILE_B.exists():
        print(f"❌ Файл не найден: {FILE_B}")
        return

    result = compare_two(FILE_A, FILE_B)
    report_lines = [
        "# Сравнение документов\n",
        f"_Обновлено: {TODAY}_\n",
    ]
    report_lines.extend(format_comparison(result))

    out = OUT_FILE or (DOCS / "COMPARE.md")
    out.write_text("\n".join(report_lines) + "\n", encoding="utf-8")

    print(f"  Jaccard: {int(result['jaccard']*100)}%")
    print(f"  Общих слов: {len(result['common_words'])}")
    print(f"  Общих разделов: {len(result['common_heads'])}")
    print(f"  wrote: {out.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
