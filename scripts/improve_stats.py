"""
improve_stats.py — детальная статистика по каждому разделу docs/.
Считает: файлы, слова, заголовки H1-H4, таблицы, code-блоки, ссылки, изображения.
Создаёт docs/STATS.md.
Запуск: python scripts/improve_stats.py
"""
import re
from pathlib import Path
from collections import defaultdict

ROOT = Path(__file__).parent.parent
DOCS = ROOT / "docs"

SKIP = {"STATS.md", "HEALTH.md", "COMPARE.md"}


def analyze_file(text: str) -> dict:
    return {
        "words":   len(text.split()),
        "chars":   len(text),
        "h1":      len(re.findall(r'^# ', text, re.MULTILINE)),
        "h2":      len(re.findall(r'^## ', text, re.MULTILINE)),
        "h3":      len(re.findall(r'^### ', text, re.MULTILINE)),
        "tables":  len(re.findall(r'^\|.*\|$', text, re.MULTILINE)) // 2,
        "code":    len(re.findall(r'```', text)) // 2,
        "links_i": len(re.findall(r'\[.+?\]\(.+?\)', text)),
        "links_e": len(re.findall(r'https?://', text)),
        "images":  len(re.findall(r'!\[', text)),
        "bold":    len(re.findall(r'\*\*[^*]+\*\*', text)),
        "todos":   len(re.findall(r'TODO|FIXME|HACK', text, re.IGNORECASE)),
    }


def main():
    print("Детальная статистика разделов...")

    section_stats: dict[str, dict] = defaultdict(lambda: defaultdict(int))
    section_files: dict[str, int]  = defaultdict(int)
    file_rows = []

    for f in sorted(DOCS.rglob("*.md")):
        if f.name in SKIP:
            continue
        text = f.read_text(encoding="utf-8")
        rel  = f.relative_to(DOCS)
        sec  = rel.parts[0] if len(rel.parts) > 1 else "root"

        stats = analyze_file(text)
        for k, v in stats.items():
            section_stats[sec][k] += v
        section_stats[sec]["files"] += 1
        section_files[sec] += 1

        file_rows.append({
            "file": str(f.relative_to(ROOT)),
            "sec":  sec,
            **stats,
        })

    # Глобальные итоги
    totals: dict = defaultdict(int)
    for sec_data in section_stats.values():
        for k, v in sec_data.items():
            totals[k] += v

    lines = [
        "# Детальная статистика репозитория\n",
        f"**Разделов:** {len(section_stats)}  "
        f"**Файлов:** {totals['files']}  "
        f"**Слов:** {totals['words']:,}  "
        f"**Символов:** {totals['chars']:,}\n",

        "## Сводная таблица по разделам\n",
        "| Раздел | Файлов | Слов | H2 | Таблиц | Блоков кода | Ссылок | Жирного |",
        "|--------|--------|------|----|--------|-------------|--------|---------|",
    ]

    for sec in sorted(section_stats.keys()):
        d = section_stats[sec]
        lines.append(
            f"| **{sec}** | {d['files']} | {d['words']:,} | {d['h2']} "
            f"| {d['tables']} | {d['code']} | {d['links_i']+d['links_e']} | {d['bold']} |"
        )

    # Итоговая строка
    lines.append(
        f"| **ИТОГО** | **{totals['files']}** | **{totals['words']:,}** | "
        f"**{totals['h2']}** | **{totals['tables']}** | **{totals['code']}** | "
        f"**{totals['links_i']+totals['links_e']}** | **{totals['bold']}** |"
    )

    # Топ-файлов по словам
    file_rows.sort(key=lambda x: -x["words"])
    lines += [
        "\n## Топ-20 файлов по объёму\n",
        "| Файл | Слов | H2 | Таблиц | Код |",
        "|------|------|----|--------|-----|",
    ]
    for r in file_rows[:20]:
        short = r["file"].split("/")[-1].replace(".md", "")[:40]
        lines.append(
            f"| `{short}` | {r['words']} | {r['h2']} | {r['tables']} | {r['code']} |"
        )

    # Интересные факты
    total_links = totals["links_i"] + totals["links_e"]
    avg_words = totals["words"] // max(totals["files"], 1)
    lines += [
        "\n## Ключевые показатели\n",
        f"- Среднее слов на файл: **{avg_words}**",
        f"- Всего заголовков H2: **{totals['h2']}**",
        f"- Всего таблиц: **{totals['tables']}**",
        f"- Всего code-блоков: **{totals['code']}**",
        f"- Всего ссылок: **{total_links}**",
        f"- Выделений жирным: **{totals['bold']}**",
        f"- TODO/FIXME меток: **{totals['todos']}**",
    ]

    out = DOCS / "STATS.md"
    out.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(f"  wrote: {out.relative_to(ROOT)}")
    print(f"  файлов: {totals['files']}, слов: {totals['words']:,}, "
          f"разделов: {len(section_stats)}")


if __name__ == "__main__":
    main()
