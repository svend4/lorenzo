"""
improve_word_freq.py — частотный анализ слов по разделам.
Топ-30 слов в каждом разделе и общий топ-50.
Создаёт docs/WORD_FREQ.md.
Запуск: python scripts/improve_word_freq.py
"""
import re
from pathlib import Path
from collections import Counter, defaultdict

ROOT = Path(__file__).parent.parent
DOCS = ROOT / "docs"

STOPWORDS = {
    # Русские
    "и","в","не","на","что","с","по","это","как","из","для","к","а","но","то",
    "если","или","от","о","при","за","уже","чем","так","же","его","её","их",
    "все","они","он","она","мы","вы","я","бы","быть","только","ещё","также",
    "этого","этой","том","может","нет","да","такой","самый","один","два",
    "три","который","которые","которая","которого","которых","которым",
    "когда","тоже","даже","очень","без","через","до","после","под","над",
    "между","среди","против","здесь","там","где","куда","откуда",
    # Английские
    "the","a","an","of","in","to","and","is","are","for","that","this","with",
    "be","by","as","at","or","not","it","its","but","from","on","was","were",
    "have","has","had","can","will","would","could","should","may","might",
    "do","does","did","their","they","we","you","he","she","which","who",
    # Markdown артефакты
    "md","http","https","www","com","ru","org","github","docs",
}


def tokenize(text: str) -> list[str]:
    # Убираем код-блоки и HTML
    text = re.sub(r'```.*?```', '', text, flags=re.DOTALL)
    text = re.sub(r'<!--.*?-->', '', text, flags=re.DOTALL)
    text = re.sub(r'\bhttps?://\S+', '', text)

    words = re.findall(r'[а-яёa-z]{3,}', text.lower())
    return [w for w in words if w not in STOPWORDS and not w.isdigit()]


def top_words(words: list[str], n: int = 30) -> list[tuple[str, int]]:
    return Counter(words).most_common(n)


def make_bar(count: int, max_count: int, width: int = 20) -> str:
    filled = int(count / max_count * width)
    return "█" * filled + "░" * (width - filled)


def main():
    print("Частотный анализ слов...")
    section_words: dict[str, list[str]] = defaultdict(list)
    all_words: list[str] = []

    for f in sorted(DOCS.rglob("*.md")):
        skip = {"WORD_FREQ.md", "TAGS.md", "CROSSREFS.md", "GLOSSARY.md",
                "CLUSTERS.md", "PRIORITIES.md", "SEARCH.md"}
        if f.name in skip:
            continue
        text = f.read_text(encoding="utf-8")
        words = tokenize(text)
        rel = f.relative_to(DOCS)
        section = rel.parts[0] if len(rel.parts) > 1 else "root"
        section_words[section].extend(words)
        all_words.extend(words)

    lines = [
        "# Частотный анализ слов\n",
        f"**Всего слов (очищенных):** {len(all_words):,}\n",
    ]

    # Глобальный топ-50
    global_top = top_words(all_words, 50)
    max_count = global_top[0][1] if global_top else 1

    lines += [
        "## Глобальный топ-50 слов\n",
        "| # | Слово | Частота | Визуализация |",
        "|---|-------|---------|-------------|",
    ]
    for i, (word, count) in enumerate(global_top, 1):
        bar = make_bar(count, max_count)
        lines.append(f"| {i} | **{word}** | {count:,} | `{bar}` |")

    # Топ по разделам
    lines.append("\n## Топ-15 слов по разделам\n")
    for section in sorted(section_words.keys()):
        words = section_words[section]
        top = top_words(words, 15)
        if not top:
            continue
        max_c = top[0][1]
        lines.append(f"\n### {section} ({len(words):,} слов)\n")
        lines.append("| Слово | Частота | |")
        lines.append("|-------|---------|---|")
        for word, count in top:
            bar = make_bar(count, max_c, 15)
            lines.append(f"| **{word}** | {count} | `{bar}` |")

    # Уникальные слова каждого раздела (не встречающиеся в других)
    lines.append("\n## Уникальные слова разделов\n")
    lines.append("_(Слова, характерные только для этого раздела)_\n")
    all_set = Counter(all_words)

    for section in sorted(section_words.keys()):
        words = section_words[section]
        sec_count = Counter(words)
        # Слова где доля в разделе >> доля в корпусе
        unique = []
        for word, count in sec_count.most_common(200):
            global_freq = all_set[word] / len(all_words)
            local_freq = count / len(words)
            if local_freq > global_freq * 3 and count >= 3:
                unique.append(word)
        if unique:
            lines.append(f"**{section}:** {', '.join(unique[:12])}")

    out = DOCS / "WORD_FREQ.md"
    out.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(f"  wrote: {out.relative_to(ROOT)}")
    print(f"  уникальных слов: {len(set(all_words)):,}")


if __name__ == "__main__":
    main()
