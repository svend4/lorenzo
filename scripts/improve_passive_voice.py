"""
improve_passive_voice.py — детектор пассивного залога и номинализаций (RU/EN).

Находит:
  - Пассивный залог RU: «был создан», «является», «используется», «осуществляется»
  - Пассивный залог EN: «was created», «is used», «has been»
  - Номинализации RU: слова на -ание/-ение/-ция/-изация/-ость (вместо глаголов)
  - Клише: «в рамках», «с целью», «в ходе», «посредством», «в связи с»
  - Избыточные связки: «является», «представляет собой», «выступает в роли»

Создаёт docs/PASSIVE_VOICE.md.
Запуск:
    python scripts/improve_passive_voice.py
    python scripts/improve_passive_voice.py --section 01-svyazi
    python scripts/improve_passive_voice.py --top 30
    python scripts/improve_passive_voice.py --verbose
"""
import re
import sys
from collections import Counter, defaultdict
from pathlib import Path
from datetime import date

ROOT = Path(__file__).parent.parent
DOCS = ROOT / "docs"
TODAY = date.today().isoformat()

VERBOSE = "--verbose" in sys.argv
TOP = 20
if "--top" in sys.argv:
    idx = sys.argv.index("--top")
    if idx + 1 < len(sys.argv):
        TOP = int(sys.argv[idx + 1])

SECTION_FILTER = None
if "--section" in sys.argv:
    idx = sys.argv.index("--section")
    if idx + 1 < len(sys.argv):
        SECTION_FILTER = DOCS / sys.argv[idx + 1]

SKIP_FILES = {
    "PASSIVE_VOICE.md", "SEARCH.md", "PARAGRAPH_QUALITY.md",
    "HEADING_AUDIT.md", "CONTRADICTIONS.md", "VOCABULARY.md",
}

# RU пассивный залог
PASSIVE_RU = re.compile(
    r'\b(?:был[аои]?\s+\w+н[ыоае]|'
    r'буд(?:ет|ут)\s+\w+н[ыоае]|'
    r'является\s+|'
    r'явля[ею]тся\s+|'
    r'используется\s+|'
    r'применяется\s+|'
    r'осуществляется\s+|'
    r'производится\s+|'
    r'выполняется\s+|'
    r'реализуется\s+)',
    re.I
)

# EN пассивный залог
PASSIVE_EN = re.compile(
    r'\b(?:is\s+\w+ed\b|'
    r'are\s+\w+ed\b|'
    r'was\s+\w+ed\b|'
    r'were\s+\w+ed\b|'
    r'has\s+been\s+\w+ed\b|'
    r'have\s+been\s+\w+ed\b|'
    r'will\s+be\s+\w+ed\b)',
    re.I
)

# Номинализации RU
NOMINAL_RU = re.compile(
    r'\b\w{5,}(?:ание|ение|ация|изация|ость|ство|тельность)\b',
    re.I
)

# Канцеляризмы и клише
CLICHE_RU = re.compile(
    r'\b(?:в\s+рамках|с\s+целью|в\s+ходе|посредством|'
    r'в\s+связи\s+с|в\s+контексте|на\s+предмет|'
    r'представляет\s+собой|выступает\s+в\s+роли|'
    r'в\s+настоящее\s+время|на\s+данный\s+момент|'
    r'в\s+данном\s+случае|следует\s+отметить|'
    r'необходимо\s+подчеркнуть)',
    re.I
)

ISSUE_TYPES = {
    "passive_ru":  "🔵 Пассив RU",
    "passive_en":  "🔵 Пассив EN",
    "nominal":     "🟡 Номинализация",
    "cliche":      "🟠 Канцеляризм",
}


def _clean(text: str) -> str:
    text = re.sub(r'```.*?```', ' ', text, flags=re.DOTALL)
    text = re.sub(r'<!--.*?-->', ' ', text, flags=re.DOTALL)
    text = re.sub(r'https?://\S+', ' ', text)
    return text


def _sentences(text: str) -> list[str]:
    clean = _clean(text)
    # Убираем заголовки
    clean = re.sub(r'^#{1,6}\s+.+$', '', clean, flags=re.MULTILINE)
    sents = re.split(r'(?<=[.!?])\s+', clean)
    return [s.strip() for s in sents if len(s.split()) >= 5]


def _count_nominals(text: str) -> int:
    return len(NOMINAL_RU.findall(text))


def analyze_file(path: Path) -> dict | None:
    try:
        text = path.read_text(encoding="utf-8")
    except Exception:
        return None

    sents = _sentences(text)
    if len(sents) < 5:
        return None

    passive_ru_sents = [s for s in sents if PASSIVE_RU.search(s)]
    passive_en_sents = [s for s in sents if PASSIVE_EN.search(s)]
    cliche_sents     = [s for s in sents if CLICHE_RU.search(s)]
    nominal_count    = _count_nominals(_clean(text))

    total = len(sents)
    passive_ratio = (len(passive_ru_sents) + len(passive_en_sents)) / total

    return {
        "file": str(path.relative_to(ROOT)),
        "total_sents": total,
        "passive_ru": len(passive_ru_sents),
        "passive_en": len(passive_en_sents),
        "cliches": len(cliche_sents),
        "nominals": nominal_count,
        "passive_ratio": round(passive_ratio, 3),
        "samples": {
            "passive_ru": [s[:120] for s in passive_ru_sents[:3]],
            "passive_en": [s[:120] for s in passive_en_sents[:2]],
            "cliche":     [s[:120] for s in cliche_sents[:3]],
        },
    }


def _grade(passive_ratio: float) -> str:
    if passive_ratio <= 0.05:
        return "🟢 Активный стиль"
    if passive_ratio <= 0.15:
        return "🟡 Умеренный пассив"
    if passive_ratio <= 0.30:
        return "🟠 Много пассива"
    return "🔴 Преимущественно пассив"


def main() -> None:
    print("✍️  improve_passive_voice.py — пассивный залог и канцеляризмы")

    target = SECTION_FILTER or DOCS
    files = [f for f in sorted(target.rglob("*.md"))
             if f.name not in SKIP_FILES
             and "-parts" not in str(f)
             and "obsidian" not in str(f)]
    print(f"   Файлов: {len(files)}\n")

    results = []
    for f in files:
        res = analyze_file(f)
        if res:
            results.append(res)

    if not results:
        print("  Нет данных.")
        return

    avg_passive = sum(r["passive_ratio"] for r in results) / len(results)
    total_cliches = sum(r["cliches"] for r in results)
    total_nominals = sum(r["nominals"] for r in results)

    print(f"   Средний пассив: {avg_passive*100:.1f}%  {_grade(avg_passive)}")
    print(f"   Канцеляризмов: {total_cliches}")
    print(f"   Номинализаций: {total_nominals}")

    by_passive = sorted(results, key=lambda x: -x["passive_ratio"])

    lines = [
        "# Пассивный залог и канцеляризмы\n",
        f"_Обновлено: {TODAY}_\n",
        f"Файлов: **{len(results)}** | Средний пассив: **{avg_passive*100:.1f}%** "
        f"({_grade(avg_passive)})\n",
        "## Корпусная статистика\n",
        "| Метрика | Значение |",
        "|---------|----------|",
        f"| Средний % пассива | {avg_passive*100:.1f}% |",
        f"| Всего канцеляризмов | {total_cliches} |",
        f"| Всего номинализаций | {total_nominals} |",
        f"| Оценка | {_grade(avg_passive)} |",
        "\n## Топ файлов по доле пассива\n",
        "| Файл | Пассив% | Оценка | Пред. RU | Пред. EN | Канцеляризмы |",
        "|------|---------|--------|----------|----------|--------------|",
    ]
    for r in by_passive[:TOP]:
        fname = r["file"].split("/")[-1]
        lines.append(
            f"| `{fname}` | {r['passive_ratio']*100:.0f}% | "
            f"{_grade(r['passive_ratio'])} | "
            f"{r['passive_ru']} | {r['passive_en']} | {r['cliches']} |"
        )

    if VERBOSE:
        lines += ["\n## Примеры пассивных конструкций\n"]
        for r in by_passive[:10]:
            if not any(r["samples"].values()):
                continue
            lines.append(f"### `{r['file'].split('/')[-1]}`\n")
            for typ, sents in r["samples"].items():
                if sents:
                    label = {"passive_ru": "Пассив RU", "passive_en": "Пассив EN",
                             "cliche": "Канцеляризм"}.get(typ, typ)
                    for s in sents:
                        lines.append(f"- **{label}:** {s}")
            lines.append("")

    out = DOCS / "PASSIVE_VOICE.md"
    out.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(f"\n  wrote: {out.relative_to(ROOT)}")
    print(f"  файлов с высоким пассивом (>15%): "
          f"{sum(1 for r in results if r['passive_ratio'] > 0.15)}")


if __name__ == "__main__":
    main()
