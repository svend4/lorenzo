"""
improve_sentiment.py — тональный анализ документов.
Оценивает: оптимизм, скептицизм, срочность, неопределённость.
Создаёт docs/SENTIMENT.md.
Запуск: python scripts/improve_sentiment.py
"""
import re
from pathlib import Path
from collections import defaultdict

ROOT = Path(__file__).parent.parent
DOCS = ROOT / "docs"

SKIP = {"SENTIMENT.md", "HEALTH.md", "STATS.md"}

# Словари тональности
POSITIVE = [
    "отлично", "прекрасно", "идеально", "эффективн", "оптимальн",
    "преимущест", "выгодн", "успешн", "перспективн", "уникальн",
    "инновацион", "мощн", "гибк", "надёжн", "масштабируем",
    "рекомендуется", "лучший", "превосходн", "ключевой",
    "excellent", "optimal", "efficient", "powerful", "robust",
    "scalable", "innovative", "best", "great", "strong",
]

NEGATIVE = [
    "риск", "опасност", "проблем", "сложност", "ограничен",
    "недостат", "слабост", "хаос", "нестабильн", "ломает",
    "не стоит", "нельзя", "избегать", "осторожн", "критическ",
    "risk", "problem", "issue", "limitation", "weakness",
    "danger", "avoid", "critical", "unstable", "broken",
]

URGENT = [
    "срочно", "немедленно", "критически", "обязательно", "необходимо",
    "must", "critical", "urgent", "immediately", "required", "essential",
    "приоритет", "первоочередн", "ключевой", "важнейш",
]

UNCERTAIN = [
    "возможно", "вероятно", "предположительно", "может быть", "не ясно",
    "неизвестно", "требует уточнения", "открытый вопрос", "пока не",
    "maybe", "possibly", "unclear", "uncertain", "unknown", "tbd",
    "предстоит", "планируется", "рассматривается",
]


def count_words(text: str, word_list: list[str]) -> int:
    low = text.lower()
    return sum(low.count(w.lower()) for w in word_list)


def tone_label(pos: int, neg: int, urg: int, unc: int, total: int) -> str:
    if total == 0:
        return "нейтральный"
    if pos > neg * 2 and pos > urg:
        return "🟢 оптимистичный"
    if neg > pos * 1.5:
        return "🔴 скептичный"
    if urg > pos and urg > neg:
        return "🟠 срочный"
    if unc > pos and unc > neg:
        return "🟡 неопределённый"
    return "⚪ нейтральный"


def main():
    print("Тональный анализ...")

    section_data: dict[str, dict] = defaultdict(lambda: defaultdict(int))
    file_rows = []

    for f in sorted(DOCS.rglob("*.md")):
        if f.name in SKIP:
            continue
        text = f.read_text(encoding="utf-8")
        # Убираем code-блоки
        text = re.sub(r'```.*?```', '', text, flags=re.DOTALL)
        words = len(text.split())
        if words < 100:
            continue

        pos = count_words(text, POSITIVE)
        neg = count_words(text, NEGATIVE)
        urg = count_words(text, URGENT)
        unc = count_words(text, UNCERTAIN)
        tone = tone_label(pos, neg, urg, unc, words)

        rel = f.relative_to(DOCS)
        sec = rel.parts[0] if len(rel.parts) > 1 else "root"

        for k, v in [("pos", pos), ("neg", neg), ("urg", urg), ("unc", unc), ("words", words)]:
            section_data[sec][k] += v

        file_rows.append({
            "file":  str(f.relative_to(ROOT)),
            "sec":   sec,
            "words": words,
            "pos":   pos, "neg": neg, "urg": urg, "unc": unc,
            "tone":  tone,
        })

    lines = [
        "# Тональный анализ документов\n",
        f"**Файлов проанализировано:** {len(file_rows)}\n",

        "## Тональность по разделам\n",
        "| Раздел | Оптимизм | Скептицизм | Срочность | Неопределённость | Тон |",
        "|--------|----------|------------|-----------|-----------------|-----|",
    ]

    for sec in sorted(section_data.keys()):
        d = section_data[sec]
        w = max(d["words"], 1)
        pos_r = round(d["pos"] / w * 1000, 1)
        neg_r = round(d["neg"] / w * 1000, 1)
        urg_r = round(d["urg"] / w * 1000, 1)
        unc_r = round(d["unc"] / w * 1000, 1)
        tone  = tone_label(d["pos"], d["neg"], d["urg"], d["unc"], w)
        lines.append(
            f"| **{sec}** | {pos_r}‰ | {neg_r}‰ | {urg_r}‰ | {unc_r}‰ | {tone} |"
        )

    # Самые оптимистичные файлы
    pos_top = sorted(file_rows, key=lambda x: -(x["pos"] / max(x["words"], 1)))
    lines += [
        "\n## Самые оптимистичные документы\n",
        "| Документ | Оптимизм‰ | Тон |",
        "|----------|----------|-----|",
    ]
    for r in pos_top[:10]:
        ratio = round(r["pos"] / max(r["words"], 1) * 1000, 1)
        short = r["file"].split("/")[-1].replace(".md", "")[:35]
        lines.append(f"| `{short}` | {ratio} | {r['tone']} |")

    # Самые скептичные
    neg_top = sorted(file_rows, key=lambda x: -(x["neg"] / max(x["words"], 1)))
    lines += [
        "\n## Самые скептичные / риск-ориентированные\n",
        "| Документ | Скептицизм‰ | Тон |",
        "|----------|------------|-----|",
    ]
    for r in neg_top[:10]:
        ratio = round(r["neg"] / max(r["words"], 1) * 1000, 1)
        short = r["file"].split("/")[-1].replace(".md", "")[:35]
        lines.append(f"| `{short}` | {ratio} | {r['tone']} |")

    # Распределение тонов
    tone_dist: dict[str, int] = defaultdict(int)
    for r in file_rows:
        tone_dist[r["tone"]] += 1

    lines += ["\n## Распределение тональности\n",
              "| Тон | Файлов |",
              "|-----|--------|"]
    for tone, cnt in sorted(tone_dist.items(), key=lambda x: -x[1]):
        lines.append(f"| {tone} | {cnt} |")

    out = DOCS / "SENTIMENT.md"
    out.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(f"  wrote: {out.relative_to(ROOT)}")
    print(f"  файлов: {len(file_rows)}")


if __name__ == "__main__":
    main()
