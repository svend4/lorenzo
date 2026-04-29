"""
improve_language_split.py — анализ языкового состава документов.

Для каждого файла определяет:
  - Долю русского текста (кириллица)
  - Долю английского текста (латиница)
  - Классификацию: RU / EN / MIX / CODE
  - Файлы с неожиданным языком (EN в RU-секции и наоборот)

Режимы:
  --report            только отчёт (по умолч.)
  --split             создаёт отдельные файлы .ru.md / .en.md для MIX-файлов
  --min-mix 0.2       порог для классификации MIX (по умолч.: 0.2)
  --section

Запуск:
    python scripts/improve_language_split.py
    python scripts/improve_language_split.py --section 05-habr-projects
    python scripts/improve_language_split.py --min-mix 0.3
"""
import re
import sys
from collections import Counter
from pathlib import Path
from datetime import date

ROOT = Path(__file__).parent.parent
DOCS = ROOT / "docs"
TODAY = date.today().isoformat()

SPLIT_MODE = "--split" in sys.argv
MIN_MIX = 0.2

if "--min-mix" in sys.argv:
    idx = sys.argv.index("--min-mix")
    if idx + 1 < len(sys.argv):
        MIN_MIX = float(sys.argv[idx + 1])

SECTION_FILTER = None
if "--section" in sys.argv:
    idx = sys.argv.index("--section")
    if idx + 1 < len(sys.argv):
        SECTION_FILTER = DOCS / sys.argv[idx + 1]

SKIP_FILES = {
    "LANGUAGE_STATS.md", "SEARCH.md", "HEADING_AUDIT.md",
    "PARAGRAPH_QUALITY.md", "VOCABULARY.md", "KEYWORD_INDEX.md",
}

# Ожидаемый язык для каждой секции
SECTION_LANG: dict[str, str] = {
    "01-svyazi": "ru",
    "02-anthropic-vacancies": "ru",
    "03-technology-combinations": "ru",
    "04-ai-collaborations": "ru",
    "05-habr-projects": "ru",
    "contacts": "ru",
}


def _section_of(path: Path) -> str:
    try:
        rel = path.relative_to(DOCS)
        parts = rel.parts
        return parts[0] if len(parts) > 1 else "root"
    except ValueError:
        return "unknown"


def _clean_for_lang(text: str) -> str:
    text = re.sub(r'```.*?```', ' ', text, flags=re.DOTALL)
    text = re.sub(r'<!--.*?-->', ' ', text, flags=re.DOTALL)
    text = re.sub(r'https?://\S+', ' ', text)
    text = re.sub(r'[*_`#|>\[\]()]', ' ', text)
    return text


def _lang_stats(text: str) -> dict:
    clean = _clean_for_lang(text)
    words = re.findall(r'[а-яёА-ЯЁa-zA-Z]{2,}', clean)
    if not words:
        return {"ru": 0, "en": 0, "total": 0, "label": "empty", "ru_ratio": 0, "en_ratio": 0}

    ru = sum(1 for w in words if re.match(r'^[а-яёА-ЯЁ]+$', w))
    en = sum(1 for w in words if re.match(r'^[a-zA-Z]+$', w))
    total = len(words)
    ru_r = ru / total
    en_r = en / total

    if ru_r >= (1 - MIN_MIX):
        label = "RU"
    elif en_r >= (1 - MIN_MIX):
        label = "EN"
    elif ru_r >= MIN_MIX and en_r >= MIN_MIX:
        label = "MIX"
    else:
        label = "OTHER"

    return {
        "ru": ru, "en": en, "total": total,
        "ru_ratio": round(ru_r, 3),
        "en_ratio": round(en_r, 3),
        "label": label,
    }


def _split_paragraphs_by_lang(text: str) -> tuple[str, str]:
    """Разделяет смешанный текст на RU и EN абзацы."""
    paras = re.split(r'\n{2,}', text)
    ru_parts, en_parts = [], []
    for p in paras:
        stats = _lang_stats(p)
        if stats["ru_ratio"] > stats["en_ratio"]:
            ru_parts.append(p)
        else:
            en_parts.append(p)
    return "\n\n".join(ru_parts), "\n\n".join(en_parts)


def analyze_file(path: Path) -> dict | None:
    try:
        text = path.read_text(encoding="utf-8")
    except Exception:
        return None
    stats = _lang_stats(text)
    if stats["total"] < 20:
        return None
    stats["file"] = str(path.relative_to(ROOT))
    stats["section"] = _section_of(path)
    stats["expected"] = SECTION_LANG.get(stats["section"], "?")
    stats["unexpected"] = (
        stats["expected"] == "ru" and stats["label"] == "EN"
    ) or (
        stats["expected"] == "en" and stats["label"] == "RU"
    )
    stats["path"] = path
    return stats


def main() -> None:
    print("🌐 improve_language_split.py — анализ языка документов")
    print(f"   MIN_MIX порог: {MIN_MIX} | Режим: {'SPLIT' if SPLIT_MODE else 'report'}\n")

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

    label_counts: Counter = Counter(r["label"] for r in results)
    unexpected = [r for r in results if r.get("unexpected")]

    print(f"   RU: {label_counts['RU']}  EN: {label_counts['EN']}  "
          f"MIX: {label_counts['MIX']}  OTHER: {label_counts['OTHER']}")
    print(f"   Неожиданный язык: {len(unexpected)}\n")

    lines = [
        "# Языковой состав документов\n",
        f"_Обновлено: {TODAY}_\n",
        f"Файлов: **{len(results)}**\n",
        "## Распределение\n",
        "| Язык | Файлов |",
        "|------|--------|",
        f"| 🇷🇺 RU (≥{100-MIN_MIX*100:.0f}% кириллица) | {label_counts['RU']} |",
        f"| 🇬🇧 EN (≥{100-MIN_MIX*100:.0f}% латиница) | {label_counts['EN']} |",
        f"| 🔀 MIX | {label_counts['MIX']} |",
        f"| ❓ OTHER | {label_counts['OTHER']} |",
    ]

    if unexpected:
        lines += [
            "\n## Файлы с неожиданным языком\n",
            "| Файл | Язык | Ожидалось | RU% | EN% |",
            "|------|------|-----------|-----|-----|",
        ]
        for r in sorted(unexpected, key=lambda x: -x["en_ratio"]):
            fname = r["file"].split("/")[-1]
            lines.append(
                f"| `{fname}` | {r['label']} | {r['expected'].upper()} | "
                f"{r['ru_ratio']*100:.0f}% | {r['en_ratio']*100:.0f}% |"
            )

    mix_files = [r for r in results if r["label"] == "MIX"]
    if mix_files:
        lines += [
            "\n## Смешанные файлы (MIX)\n",
            "| Файл | RU% | EN% |",
            "|------|-----|-----|",
        ]
        for r in sorted(mix_files, key=lambda x: -max(x["ru_ratio"], x["en_ratio"])):
            fname = r["file"].split("/")[-1]
            lines.append(f"| `{fname}` | {r['ru_ratio']*100:.0f}% | {r['en_ratio']*100:.0f}% |")

    # По секциям
    section_stats: dict[str, Counter] = {}
    for r in results:
        sec = r["section"]
        if sec not in section_stats:
            section_stats[sec] = Counter()
        section_stats[sec][r["label"]] += 1

    lines += ["\n## По секциям\n", "| Секция | RU | EN | MIX |", "|--------|----|----|-----|"]
    for sec, cnt in sorted(section_stats.items()):
        lines.append(f"| `{sec}` | {cnt['RU']} | {cnt['EN']} | {cnt['MIX']} |")

    out = DOCS / "LANGUAGE_STATS.md"
    out.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(f"  wrote: {out.relative_to(ROOT)}")

    if SPLIT_MODE:
        split_count = 0
        for r in mix_files:
            try:
                text = r["path"].read_text(encoding="utf-8")
            except Exception:
                continue
            ru_text, en_text = _split_paragraphs_by_lang(text)
            base = r["path"]
            if ru_text.strip():
                (base.parent / (base.stem + ".ru.md")).write_text(ru_text, encoding="utf-8")
            if en_text.strip():
                (base.parent / (base.stem + ".en.md")).write_text(en_text, encoding="utf-8")
            split_count += 1
        print(f"  разделено MIX-файлов: {split_count}")


if __name__ == "__main__":
    main()
