"""
improve_metrics.py — метрики качества документации.
Считает: индекс покрытия, плотность ссылок, насыщенность примерами,
баланс разделов, индекс связности.
Создаёт docs/METRICS.md.
Запуск: python scripts/improve_metrics.py
"""
import re
from pathlib import Path
from collections import defaultdict

ROOT = Path(__file__).parent.parent
DOCS = ROOT / "docs"

SKIP = {"METRICS.md", "HEALTH.md", "STATS.md", "VALIDATION.md"}

SECTIONS = [
    "01-svyazi", "02-anthropic-vacancies",
    "03-technology-combinations", "04-ai-collaborations",
    "05-habr-projects",
]


def link_density(text: str) -> float:
    """Ссылок на 1000 слов."""
    words = max(len(text.split()), 1)
    links = len(re.findall(r'\[.+?\]\(.+?\)', text))
    return links / words * 1000


def example_density(text: str) -> float:
    """Code-блоков на 1000 слов."""
    words = max(len(text.split()), 1)
    blocks = len(re.findall(r'```', text)) // 2
    return blocks / words * 1000


def heading_ratio(text: str) -> float:
    """Заголовков на 100 слов."""
    words = max(len(text.split()), 1)
    heads = len(re.findall(r'^#{1,4}\s', text, re.MULTILINE))
    return heads / words * 100


def has_summary(text: str) -> bool:
    return "<!-- summary" in text


def has_tags(text: str) -> bool:
    return "<!-- tags" in text


def has_toc(text: str) -> bool:
    return "## Содержание" in text or "## Table of Contents" in text


def has_callout(text: str) -> bool:
    return "> [!" in text


def quality_score(f_data: dict) -> float:
    score = 0.0
    w = f_data["words"]
    if w >= 100:
        score += 20
    if f_data["has_h1"]:
        score += 10
    if f_data["has_summary"]:
        score += 15
    if f_data["has_tags"]:
        score += 10
    if f_data["link_density"] >= 1:
        score += 15
    if w >= 300 and f_data["has_toc"]:
        score += 10
    if f_data["example_density"] >= 0.5:
        score += 10
    if f_data["has_callout"]:
        score += 10
    return min(score, 100)


def main():
    print("Метрики качества документации...")

    section_metrics: dict[str, dict] = defaultdict(lambda: defaultdict(float))
    section_counts:  dict[str, int]  = defaultdict(int)
    file_rows = []

    for f in sorted(DOCS.rglob("*.md")):
        if f.name in SKIP:
            continue
        text = f.read_text(encoding="utf-8")
        words = len(text.split())
        if words < 20:
            continue

        rel = f.relative_to(DOCS)
        sec = rel.parts[0] if len(rel.parts) > 1 else "root"

        ld  = link_density(text)
        ed  = example_density(text)
        hr  = heading_ratio(text)
        hs  = has_summary(text)
        ht  = has_tags(text)
        htoc = has_toc(text)
        hc  = has_callout(text)
        h1  = bool(re.search(r'^# ', text, re.MULTILINE))

        fd = {
            "file": str(f.relative_to(ROOT)),
            "sec": sec, "words": words,
            "link_density": ld, "example_density": ed,
            "heading_ratio": hr,
            "has_h1": h1, "has_summary": hs, "has_tags": ht,
            "has_toc": htoc, "has_callout": hc,
        }
        fd["score"] = quality_score(fd)
        file_rows.append(fd)

        section_metrics[sec]["link_density"]    += ld
        section_metrics[sec]["example_density"] += ed
        section_metrics[sec]["score"]           += fd["score"]
        section_metrics[sec]["has_summary"]     += int(hs)
        section_metrics[sec]["has_tags"]        += int(ht)
        section_counts[sec] += 1

    # Средние по разделу
    for sec in section_metrics:
        n = max(section_counts[sec], 1)
        for k in section_metrics[sec]:
            section_metrics[sec][k] /= n

    avg_score = sum(r["score"] for r in file_rows) / max(len(file_rows), 1)

    lines = [
        "# Метрики качества документации\n",
        f"**Файлов:** {len(file_rows)}  "
        f"**Средний балл:** {avg_score:.1f}/100\n",

        "## Качество по разделам\n",
        "| Раздел | Балл | Ссылок/1K слов | Код-блоков/1K | % с summary | % с тегами |",
        "|--------|------|----------------|--------------|-------------|------------|",
    ]
    for sec in SECTIONS + ["root"]:
        m = section_metrics.get(sec)
        if not m:
            continue
        lines.append(
            f"| **{sec}** | {m['score']:.0f} | {m['link_density']:.1f} "
            f"| {m['example_density']:.1f} | {m['has_summary']*100:.0f}% "
            f"| {m['has_tags']*100:.0f}% |"
        )

    # Топ по качеству
    file_rows.sort(key=lambda x: -x["score"])
    lines += [
        "\n## Топ-15 лучших документов\n",
        "| Документ | Балл | Слов |",
        "|----------|------|------|",
    ]
    for r in file_rows[:15]:
        short = r["file"].split("/")[-1].replace(".md", "")[:40]
        lines.append(f"| `{short}` | {r['score']:.0f} | {r['words']} |")

    # Нижние по качеству
    poor = [r for r in file_rows if r["score"] < 40 and r["words"] >= 100]
    poor.sort(key=lambda x: x["score"])
    lines += [
        f"\n## Документы, требующие улучшения ({len(poor)})\n",
        "| Документ | Балл | Что отсутствует |",
        "|----------|------|----------------|",
    ]
    for r in poor[:20]:
        missing = []
        if not r["has_h1"]:      missing.append("H1")
        if not r["has_summary"]: missing.append("summary")
        if not r["has_tags"]:    missing.append("tags")
        if not r["has_toc"]:     missing.append("TOC")
        if not r["has_callout"]: missing.append("callout")
        short = r["file"].split("/")[-1].replace(".md", "")[:35]
        lines.append(f"| `{short}` | {r['score']:.0f} | {', '.join(missing) or '—'} |")

    # Индексы
    pct_summary  = sum(1 for r in file_rows if r["has_summary"])  / max(len(file_rows), 1) * 100
    pct_tags     = sum(1 for r in file_rows if r["has_tags"])     / max(len(file_rows), 1) * 100
    pct_toc      = sum(1 for r in file_rows if r["has_toc"])      / max(len(file_rows), 1) * 100
    pct_callout  = sum(1 for r in file_rows if r["has_callout"])  / max(len(file_rows), 1) * 100

    lines += [
        "\n## Общие показатели\n",
        f"- Файлов с `<!-- summary -->`: **{pct_summary:.1f}%**",
        f"- Файлов с тегами: **{pct_tags:.1f}%**",
        f"- Файлов с оглавлением: **{pct_toc:.1f}%**",
        f"- Файлов с callout: **{pct_callout:.1f}%**",
        f"- Средний балл качества: **{avg_score:.1f}/100**",
    ]

    out = DOCS / "METRICS.md"
    out.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(f"  wrote: {out.relative_to(ROOT)}")
    print(f"  файлов: {len(file_rows)}, средний балл: {avg_score:.1f}/100")


if __name__ == "__main__":
    main()
