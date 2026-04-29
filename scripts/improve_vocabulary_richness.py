"""
improve_vocabulary_richness.py — метрики богатства словаря документов.

Вычисляет:
  - TTR (Type-Token Ratio): уникальных слов / всего слов
  - STTR (Standardised TTR): средний TTR по окнам 100 слов
  - Unique per 1000: число уникальных слов на 1000 токенов
  - Hapax legomena: слова, встречающиеся ровно 1 раз
  - Lexical density: контентных слов / всех слов
  - Average word length (символов)

Создаёт docs/VOCABULARY.md.
Запуск:
    python scripts/improve_vocabulary_richness.py
    python scripts/improve_vocabulary_richness.py --section 05-habr-projects
    python scripts/improve_vocabulary_richness.py --window 150
    python scripts/improve_vocabulary_richness.py --top 20
"""
import re
import sys
from collections import Counter
from pathlib import Path
from datetime import date

ROOT = Path(__file__).parent.parent
DOCS = ROOT / "docs"
TODAY = date.today().isoformat()

STTR_WINDOW = 100   # размер окна для STTR
TOP_FILES   = 30    # показывать топ N файлов в отчёте

if "--window" in sys.argv:
    idx = sys.argv.index("--window")
    if idx + 1 < len(sys.argv):
        STTR_WINDOW = int(sys.argv[idx + 1])

if "--top" in sys.argv:
    idx = sys.argv.index("--top")
    if idx + 1 < len(sys.argv):
        TOP_FILES = int(sys.argv[idx + 1])

SECTION_FILTER = None
if "--section" in sys.argv:
    idx = sys.argv.index("--section")
    if idx + 1 < len(sys.argv):
        SECTION_FILTER = DOCS / sys.argv[idx + 1]

SKIP_FILES = {
    "VOCABULARY.md", "SEARCH.md", "NAMED_ENTITIES.md",
    "CONCEPT_GRAPH.md", "SOURCE_MAP.md", "TIMELINE.md",
    "KEYWORD_INDEX.md", "CONTRADICTIONS.md",
}

STOPWORDS = {
    "и", "в", "не", "на", "с", "по", "к", "из", "за", "для", "это",
    "как", "но", "или", "что", "был", "этот", "эта", "его", "её", "их",
    "мы", "вы", "он", "она", "они", "при", "от", "до", "об", "же",
    "бы", "ли", "да", "нет", "есть", "была", "были", "будет", "всё",
    "the", "a", "an", "is", "are", "was", "were", "be", "been",
    "have", "has", "had", "do", "does", "did", "will", "would",
    "can", "could", "should", "of", "in", "on", "at", "to", "for",
    "with", "by", "from", "as", "or", "and", "not", "but", "it",
    "its", "we", "you", "they", "their", "our", "this", "that",
}


def _clean(text: str) -> str:
    text = re.sub(r'```.*?```', ' ', text, flags=re.DOTALL)
    text = re.sub(r'<!--.*?-->', ' ', text, flags=re.DOTALL)
    text = re.sub(r'https?://\S+', ' ', text)
    text = re.sub(r'[*_`#|>\[\]()]', ' ', text)
    return text


def _all_tokens(text: str) -> list[str]:
    return re.findall(r'[а-яёa-z]{2,}', text.lower())


def _content_tokens(tokens: list[str]) -> list[str]:
    return [t for t in tokens if t not in STOPWORDS and len(t) >= 3]


def _ttr(tokens: list[str]) -> float:
    if not tokens:
        return 0.0
    return len(set(tokens)) / len(tokens)


def _sttr(tokens: list[str], window: int) -> float:
    """Standardised TTR: средний TTR по окнам фиксированного размера."""
    if len(tokens) < window:
        return _ttr(tokens)
    windows = [tokens[i:i + window] for i in range(0, len(tokens) - window + 1, window)]
    ttrs = [_ttr(w) for w in windows if w]
    return sum(ttrs) / len(ttrs) if ttrs else 0.0


def _hapax(tokens: list[str]) -> int:
    freq = Counter(tokens)
    return sum(1 for t, c in freq.items() if c == 1)


def _avg_word_len(tokens: list[str]) -> float:
    if not tokens:
        return 0.0
    return sum(len(t) for t in tokens) / len(tokens)


def _unique_per_1000(tokens: list[str]) -> float:
    if not tokens:
        return 0.0
    ratio = len(set(tokens)) / len(tokens)
    return round(ratio * 1000, 1)


def analyze_file(path: Path) -> dict | None:
    try:
        text = path.read_text(encoding="utf-8")
    except Exception:
        return None

    clean = _clean(text)
    all_tok = _all_tokens(clean)
    content_tok = _content_tokens(all_tok)

    if len(all_tok) < 50:
        return None

    return {
        "file": str(path.relative_to(ROOT)),
        "total_tokens": len(all_tok),
        "unique_tokens": len(set(all_tok)),
        "content_tokens": len(content_tok),
        "ttr": round(_ttr(all_tok), 4),
        "sttr": round(_sttr(all_tok, STTR_WINDOW), 4),
        "hapax": _hapax(all_tok),
        "hapax_ratio": round(_hapax(all_tok) / max(len(set(all_tok)), 1), 3),
        "lexical_density": round(len(content_tok) / max(len(all_tok), 1), 3),
        "avg_word_len": round(_avg_word_len(all_tok), 2),
        "unique_per_1000": _unique_per_1000(all_tok),
    }


def _grade(sttr: float) -> str:
    if sttr >= 0.72:
        return "🟢 Богатый"
    if sttr >= 0.60:
        return "🟡 Средний"
    if sttr >= 0.45:
        return "🟠 Бедный"
    return "🔴 Очень бедный"


def main() -> None:
    print("📚 improve_vocabulary_richness.py — богатство словаря")
    print(f"   STTR-окно: {STTR_WINDOW} токенов | Топ: {TOP_FILES}\n")

    target = SECTION_FILTER or DOCS
    files = [f for f in sorted(target.rglob("*.md"))
             if f.name not in SKIP_FILES
             and "obsidian" not in str(f)
             and "-parts" not in str(f)]
    print(f"   Файлов: {len(files)}\n")

    results = []
    for f in files:
        res = analyze_file(f)
        if res:
            results.append(res)

    if not results:
        print("  Нет данных.")
        return

    # Агрегаты по корпусу
    avg_ttr  = sum(r["ttr"]  for r in results) / len(results)
    avg_sttr = sum(r["sttr"] for r in results) / len(results)
    avg_ld   = sum(r["lexical_density"] for r in results) / len(results)
    avg_awl  = sum(r["avg_word_len"] for r in results) / len(results)
    total_tokens  = sum(r["total_tokens"]  for r in results)
    total_unique  = sum(r["unique_tokens"] for r in results)

    print(f"   Файлов проанализировано: {len(results)}")
    print(f"   Средний TTR:  {avg_ttr:.3f}")
    print(f"   Средний STTR: {avg_sttr:.3f}  ({_grade(avg_sttr)})")
    print(f"   Lexical density: {avg_ld:.3f}")
    print(f"   Avg word len: {avg_awl:.2f} символов")

    # Топ по STTR (богатейшие) и анти-топ (беднейшие)
    by_sttr = sorted(results, key=lambda x: -x["sttr"])

    lines = [
        "# Богатство словаря документов\n",
        f"_Обновлено: {TODAY}_\n",
        f"Файлов: **{len(results)}** | Токенов: **{total_tokens:,}** | "
        f"Уникальных: **{total_unique:,}**\n",
        "## Корпусная статистика\n",
        "| Метрика | Значение |",
        "|---------|----------|",
        f"| Средний TTR | {avg_ttr:.3f} |",
        f"| Средний STTR ({STTR_WINDOW}-токенное окно) | {avg_sttr:.3f} |",
        f"| Lexical density | {avg_ld:.3f} |",
        f"| Средняя длина слова | {avg_awl:.2f} |",
        f"| Общая оценка | {_grade(avg_sttr)} |",
        "\n## Топ файлов по богатству словаря (STTR)\n",
        "| Файл | STTR | TTR | Hapax% | Lex.Density | Токенов |",
        "|------|------|-----|--------|-------------|---------|",
    ]

    for r in by_sttr[:TOP_FILES]:
        fname = r["file"].split("/")[-1]
        lines.append(
            f"| `{fname}` | {r['sttr']:.3f} | {r['ttr']:.3f} | "
            f"{r['hapax_ratio']*100:.0f}% | {r['lexical_density']:.3f} | {r['total_tokens']} |"
        )

    lines += [
        "\n## Файлы с бедным словарём (требуют доработки)\n",
        "| Файл | STTR | Оценка | Токенов |",
        "|------|------|--------|---------|",
    ]

    poor = [r for r in by_sttr if r["sttr"] < 0.55][-TOP_FILES:]
    for r in reversed(poor):
        fname = r["file"].split("/")[-1]
        lines.append(
            f"| `{fname}` | {r['sttr']:.3f} | {_grade(r['sttr'])} | {r['total_tokens']} |"
        )

    lines += [
        "\n## Справка по метрикам\n",
        "- **TTR** (Type-Token Ratio) — уникальных слов / всего слов. Зависит от длины текста.",
        "- **STTR** — стандартизированный TTR по окнам, не зависит от длины.",
        "  - ≥ 0.72 → богатый, 0.60-0.72 → средний, 0.45-0.60 → бедный.",
        "- **Hapax%** — доля слов, встречающихся ровно 1 раз. Высокий % = разнообразный текст.",
        "- **Lexical density** — доля контентных слов (≠ стоп-слова). 0.4-0.6 — хороший диапазон.",
    ]

    out = DOCS / "VOCABULARY.md"
    out.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(f"\n  wrote: {out.relative_to(ROOT)}")
    print(f"  файлов с бедным словарём (STTR < 0.55): {len(poor)}")


if __name__ == "__main__":
    main()
