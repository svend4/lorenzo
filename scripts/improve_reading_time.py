"""
improve_reading_time.py — оценивает время чтения каждого документа.

Формула:
  - Средняя скорость чтения: 200 слов/мин (русский) / 250 слов/мин (английский)
  - Время на код: 50 слов/мин (или 30 сек/блок)
  - Минимум: 1 мин

Создаёт docs/READING_TIME.md.
Запуск: python scripts/improve_reading_time.py
        python scripts/improve_reading_time.py --wpm 180
        python scripts/improve_reading_time.py --section 05-habr-projects
"""
import re
import sys
from pathlib import Path
from datetime import date

ROOT = Path(__file__).parent.parent
DOCS = ROOT / "docs"
TODAY = date.today().isoformat()

WPM_RU = 200
WPM_EN = 250
WPM_CODE = 50

if "--wpm" in sys.argv:
    idx = sys.argv.index("--wpm")
    if idx + 1 < len(sys.argv):
        WPM_RU = WPM_EN = int(sys.argv[idx + 1])

SECTION_FILTER = None
if "--section" in sys.argv:
    idx = sys.argv.index("--section")
    if idx + 1 < len(sys.argv):
        SECTION_FILTER = DOCS / sys.argv[idx + 1]

SKIP_FILES = {"READING_TIME.md", "SEARCH.md"}


def _count_words_by_type(text: str) -> tuple[int, int, int]:
    """Возвращает (ru_words, en_words, code_blocks_count)."""
    # Извлекаем код-блоки
    code_blocks = re.findall(r'```[\s\S]*?```', text)
    n_code = len(code_blocks)

    # Убираем код, HTML-комментарии, URL
    clean = re.sub(r'```[\s\S]*?```', ' ', text)
    clean = re.sub(r'`[^`]+`', ' ', clean)
    clean = re.sub(r'<!--.*?-->', ' ', clean, flags=re.DOTALL)
    clean = re.sub(r'https?://\S+', ' ', clean)
    clean = re.sub(r'[#*|>\[\]_~]', ' ', clean)

    ru_words = len(re.findall(r'[а-яёА-ЯЁ]{2,}', clean))
    en_words = len(re.findall(r'[a-zA-Z]{2,}', clean))

    return ru_words, en_words, n_code


def estimate_reading_time(text: str) -> dict:
    ru_words, en_words, n_code = _count_words_by_type(text)
    total_words = ru_words + en_words

    if total_words < 50:
        return {}

    # Минуты: RU медленнее EN
    minutes = ru_words / WPM_RU + en_words / WPM_EN
    # Код: каждый блок ≈ 30 сек + слова кода по 50 wpm
    minutes += n_code * 0.5

    minutes = max(1.0, minutes)

    # Форматирование
    if minutes < 2:
        time_str = "~1 мин"
    elif minutes < 60:
        time_str = f"~{int(minutes)} мин"
    else:
        h = int(minutes // 60)
        m = int(minutes % 60)
        time_str = f"~{h}ч {m}мин"

    # Категория
    if minutes <= 3:
        category = "📗 Быстро"
    elif minutes <= 8:
        category = "📘 Средне"
    elif minutes <= 15:
        category = "📙 Долго"
    else:
        category = "📕 Очень долго"

    return {
        "minutes": round(minutes, 1),
        "time_str": time_str,
        "category": category,
        "words": total_words,
        "ru_words": ru_words,
        "en_words": en_words,
        "code_blocks": n_code,
    }


def main() -> None:
    print("⏱️  improve_reading_time.py — оценка времени чтения")
    print(f"   Скорость: {WPM_RU} слов/мин (ru), {WPM_EN} слов/мин (en)\n")

    target = SECTION_FILTER or DOCS
    files = [f for f in sorted(target.rglob("*.md")) if f.name not in SKIP_FILES]
    print(f"   Файлов: {len(files)}\n")

    results = []
    for f in files:
        try:
            text = f.read_text(encoding="utf-8")
        except Exception:
            continue
        metrics = estimate_reading_time(text)
        if metrics:
            results.append({"path": f.relative_to(ROOT), **metrics})

    results.sort(key=lambda x: -x["minutes"])

    total_minutes = sum(r["minutes"] for r in results)
    total_words = sum(r["words"] for r in results)

    # Форматирование итоговых часов
    total_h = int(total_minutes // 60)
    total_m = int(total_minutes % 60)
    total_str = f"{total_h}ч {total_m}мин"

    lines = [
        "# Время чтения документов\n",
        f"_Обновлено: {TODAY}_\n",
        f"Документов: **{len(results)}** | "
        f"Слов всего: **{total_words:,}** | "
        f"Время чтения всей базы: **{total_str}**\n",
        f"> Скорость: {WPM_RU} слов/мин (ru), {WPM_EN} слов/мин (en)\n",
        "## Все документы\n",
        "| Файл | Время | Слов | Категория |",
        "|------|-------|------|-----------|",
    ]

    for r in results:
        lines.append(
            f"| `{r['path']}` | {r['time_str']} | {r['words']} | {r['category']} |"
        )

    # Топ самых длинных
    long_docs = [r for r in results if r["minutes"] >= 10]
    if long_docs:
        lines += [
            f"\n## Самые длинные документы ({len(long_docs)})\n",
        ]
        for r in long_docs[:10]:
            lines.append(
                f"- `{r['path']}` — {r['time_str']}, {r['words']} слов"
            )

    # Статистика по категориям
    cats: dict[str, int] = {}
    for r in results:
        cats[r["category"]] = cats.get(r["category"], 0) + 1
    lines += ["\n## По категориям\n"]
    for cat, count in sorted(cats.items(), key=lambda x: -x[1]):
        lines.append(f"- {cat}: {count} документов")

    out = DOCS / "READING_TIME.md"
    out.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(f"  wrote: {out.relative_to(ROOT)}")
    print(f"  документов: {len(results)}, слов: {total_words:,}")
    print(f"  время всей базы: {total_str}")


if __name__ == "__main__":
    main()
