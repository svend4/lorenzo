"""
improve_readability_v2.py — индекс читаемости текстов.
Адаптированная метрика Флеша–Кинкейда для русского языка.
Формула: 206.835 - 1.015*(слов/предл.) - 84.6*(слогов/слово)
Дополнительно: средняя длина предложения, средняя длина слова.

Создаёт docs/READABILITY.md.
Запуск: python scripts/improve_readability_v2.py
        python scripts/improve_readability_v2.py --section 05-habr-projects
"""
import re
import sys
from pathlib import Path
from datetime import date

ROOT = Path(__file__).parent.parent
DOCS = ROOT / "docs"
TODAY = date.today().isoformat()

SECTION_FILTER = None
if "--section" in sys.argv:
    idx = sys.argv.index("--section")
    if idx + 1 < len(sys.argv):
        SECTION_FILTER = DOCS / sys.argv[idx + 1]

SKIP_FILES = {"READABILITY.md", "SEARCH.md"}

VOWELS_RU = set("аеёиоуыэюяАЕЁИОУЫЭЮЯ")
VOWELS_EN = set("aeiouAEIOU")


def count_syllables(word: str) -> int:
    """Считает слоги — по гласным (ru+en)."""
    return max(1, sum(1 for c in word if c in VOWELS_RU or c in VOWELS_EN))


def clean_text(text: str) -> str:
    """Убирает markdown-разметку и служебные блоки."""
    text = re.sub(r'```.*?```', ' ', text, flags=re.DOTALL)
    text = re.sub(r'`[^`]+`', ' ', text)
    text = re.sub(r'<!--.*?-->', ' ', text, flags=re.DOTALL)
    text = re.sub(r'https?://\S+', ' ', text)
    text = re.sub(r'[#*|>\[\]_~]', ' ', text)
    text = re.sub(r'\s+', ' ', text)
    return text.strip()


def compute_readability(text: str) -> dict:
    clean = clean_text(text)
    if len(clean) < 100:
        return {}

    # Предложения: разбиваем по . ! ?
    sentences = [s.strip() for s in re.split(r'[.!?]+', clean) if len(s.strip()) > 10]
    n_sentences = max(1, len(sentences))

    # Слова
    words = re.findall(r'[а-яёa-zA-Z]{2,}', clean)
    n_words = max(1, len(words))

    # Слоги
    n_syllables = sum(count_syllables(w) for w in words)

    avg_sent_len = n_words / n_sentences
    avg_word_syl = n_syllables / n_words

    # Flesch Reading Ease (адаптированный для RU)
    fre = 206.835 - 1.015 * avg_sent_len - 84.6 * avg_word_syl
    fre = max(0, min(100, fre))

    # Уровень: 60-70 хорошо, <30 сложно
    if fre >= 70:
        level = "🟢 Лёгкий"
    elif fre >= 50:
        level = "🟡 Средний"
    elif fre >= 30:
        level = "🟠 Сложный"
    else:
        level = "🔴 Очень сложный"

    return {
        "fre": round(fre, 1),
        "level": level,
        "words": n_words,
        "sentences": n_sentences,
        "avg_sent_len": round(avg_sent_len, 1),
        "avg_syllables": round(avg_word_syl, 2),
    }


def main() -> None:
    print("📖 improve_readability_v2.py — индекс читаемости (Flesch-Kincaid)")

    target = SECTION_FILTER or DOCS
    files = [f for f in sorted(target.rglob("*.md")) if f.name not in SKIP_FILES]
    print(f"   Файлов: {len(files)}\n")

    results = []
    for f in files:
        text = f.read_text(encoding="utf-8")
        metrics = compute_readability(text)
        if metrics:
            results.append({"path": f.relative_to(ROOT), **metrics})

    results.sort(key=lambda x: x["fre"])

    avg_fre = sum(r["fre"] for r in results) / len(results) if results else 0

    lines = [
        "# Читаемость документов (Flesch-Kincaid)\n",
        f"_Обновлено: {TODAY}_\n",
        f"Средний индекс FRE: **{avg_fre:.1f}/100**\n",
        "> FRE: 70-100 лёгкий, 50-70 средний, 30-50 сложный, <30 очень сложный\n",
        "## Все документы\n",
        "| Файл | FRE | Уровень | Слов | Пред. | Слов/пред. |",
        "|------|-----|---------|------|-------|-----------|",
    ]

    for r in results:
        lines.append(
            f"| `{r['path']}` | {r['fre']} | {r['level']} "
            f"| {r['words']} | {r['sentences']} | {r['avg_sent_len']} |"
        )

    # Топ самых сложных
    hardest = [r for r in results if r["fre"] < 30]
    if hardest:
        lines += [
            f"\n## Самые сложные тексты ({len(hardest)}) — рекомендуется упростить\n",
        ]
        for r in hardest[:10]:
            lines.append(
                f"- `{r['path']}` — FRE {r['fre']}, "
                f"среднее {r['avg_sent_len']} слов/предложение"
            )

    out = DOCS / "READABILITY.md"
    out.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(f"  wrote: {out.relative_to(ROOT)}")
    print(f"  средний FRE: {avg_fre:.1f}/100")
    print(f"  сложных (<30): {len([r for r in results if r['fre'] < 30])}")


if __name__ == "__main__":
    main()
