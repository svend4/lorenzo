"""
improve_word_cloud.py — генерирует SVG word cloud из топ-слов репозитория.
Без внешних зависимостей: чистый SVG с псевдо-случайным размещением.
Создаёт docs/WORD_CLOUD.svg и docs/WORD_CLOUD.md.
Запуск: python scripts/improve_word_cloud.py
"""
import re
import math
import random
from pathlib import Path
from collections import Counter

ROOT = Path(__file__).parent.parent
DOCS = ROOT / "docs"

STOPWORDS = {
    "и","в","не","на","что","с","по","это","как","из","для","к","а","но","то",
    "если","или","от","о","при","за","уже","чем","так","же","его","её","их",
    "все","они","он","она","мы","вы","я","бы","только","ещё","также","этого",
    "этой","том","может","нет","да","такой","самый","один","два","три",
    "the","a","an","of","in","to","and","is","are","for","that","this","with",
    "be","by","as","at","or","not","it","its","but","from","on","was","were",
    "docs","md","http","https","www","com","ru","org","github",
}

SKIP = {"WORD_CLOUD.md", "WORD_FREQ.md"}

# Цвета для категорий слов
COLORS = [
    "#2563eb", "#16a34a", "#dc2626", "#9333ea", "#ea580c",
    "#0891b2", "#65a30d", "#d97706", "#db2777", "#475569",
]


def tokenize_all() -> Counter:
    all_words: list[str] = []
    for f in sorted(DOCS.rglob("*.md")):
        if f.name in SKIP:
            continue
        text = f.read_text(encoding="utf-8")
        text = re.sub(r'```.*?```', '', text, flags=re.DOTALL)
        text = re.sub(r'<!--.*?-->', '', text, flags=re.DOTALL)
        text = re.sub(r'https?://\S+', '', text)
        words = re.findall(r'[а-яёa-z]{4,}', text.lower())
        all_words.extend(w for w in words if w not in STOPWORDS)
    return Counter(all_words)


def font_size(count: int, min_c: int, max_c: int,
              min_fs: int = 11, max_fs: int = 52) -> int:
    if max_c == min_c:
        return (min_fs + max_fs) // 2
    ratio = (count - min_c) / (max_c - min_c)
    return int(min_fs + ratio * (max_fs - min_fs))


def place_words(words: list[tuple[str, int, int]],
                width: int, height: int) -> list[dict]:
    """Простое спиральное размещение слов."""
    placed = []
    random.seed(42)
    cx, cy = width // 2, height // 2

    for i, (word, count, fs) in enumerate(words):
        # Оцениваем размер слова
        char_w = fs * 0.6
        w_width  = int(len(word) * char_w)
        w_height = int(fs * 1.2)

        # Спиральный поиск позиции
        placed_ok = False
        for attempt in range(200):
            angle  = attempt * 0.5
            radius = attempt * 4
            x = int(cx + radius * math.cos(angle))
            y = int(cy + radius * math.sin(angle))

            # Проверяем границы
            if x - w_width//2 < 10 or x + w_width//2 > width - 10:
                continue
            if y - w_height < 10 or y > height - 10:
                continue

            # Простая проверка перекрытия
            overlap = False
            for p in placed:
                if (abs(x - p["x"]) < (w_width + p["w"]) // 2 + 5 and
                        abs(y - p["y"]) < (w_height + p["h"]) // 2 + 5):
                    overlap = True
                    break
            if not overlap:
                placed.append({
                    "word": word, "x": x, "y": y,
                    "fs": fs, "w": w_width, "h": w_height,
                    "color": COLORS[i % len(COLORS)],
                })
                placed_ok = True
                break

        if not placed_ok:
            # Fallback — просто поставить в случайное место
            x = random.randint(50, width - 50)
            y = random.randint(30, height - 30)
            placed.append({
                "word": word, "x": x, "y": y,
                "fs": fs, "w": w_width, "h": w_height,
                "color": COLORS[i % len(COLORS)],
            })

    return placed


def make_svg(placed: list[dict], width: int, height: int) -> str:
    lines = [
        f'<svg xmlns="http://www.w3.org/2000/svg" '
        f'width="{width}" height="{height}" '
        f'viewBox="0 0 {width} {height}">',
        f'<rect width="{width}" height="{height}" fill="#0f172a"/>',
        '<style>text { font-family: Arial, sans-serif; font-weight: 600; }</style>',
    ]
    for p in placed:
        opacity = 0.7 + 0.3 * min(p["fs"] / 52, 1)
        lines.append(
            f'<text x="{p["x"]}" y="{p["y"]}" '
            f'font-size="{p["fs"]}" fill="{p["color"]}" '
            f'opacity="{opacity:.2f}" text-anchor="middle">'
            f'{p["word"]}</text>'
        )
    lines.append("</svg>")
    return "\n".join(lines)


def main():
    print("Генерация word cloud...")

    counter = tokenize_all()
    top = counter.most_common(80)

    if not top:
        print("  нет слов для отображения")
        return

    min_c = top[-1][1]
    max_c = top[0][1]

    word_data = [
        (word, count, font_size(count, min_c, max_c))
        for word, count in top
    ]

    WIDTH, HEIGHT = 900, 500
    placed = place_words(word_data, WIDTH, HEIGHT)
    svg = make_svg(placed, WIDTH, HEIGHT)

    svg_out = DOCS / "WORD_CLOUD.svg"
    svg_out.write_text(svg, encoding="utf-8")

    # Markdown-обёртка
    md_lines = [
        "# Word Cloud\n",
        "Визуализация 80 самых частых слов репозитория.\n",
        "![Word Cloud](WORD_CLOUD.svg)\n",
        "## Топ-20 слов\n",
        "| # | Слово | Частота |",
        "|---|-------|---------|",
    ]
    for i, (word, count, _) in enumerate(word_data[:20], 1):
        md_lines.append(f"| {i} | **{word}** | {count:,} |")

    md_out = DOCS / "WORD_CLOUD.md"
    md_out.write_text("\n".join(md_lines) + "\n", encoding="utf-8")

    print(f"  wrote: {svg_out.relative_to(ROOT)}")
    print(f"  wrote: {md_out.relative_to(ROOT)}")
    print(f"  слов в облаке: {len(placed)}, размещено: {len(placed)}")


if __name__ == "__main__":
    main()
