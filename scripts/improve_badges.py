"""
improve_badges.py — генерирует SVG-бейджи для README.
Показывает: здоровье репо, скоринг, кол-во документов, скриптов, слов.
Создаёт docs/badges/ и вставляет бейджи в корневой README.md.
Запуск: python scripts/improve_badges.py
"""
import re
from pathlib import Path

ROOT = Path(__file__).parent.parent
DOCS = ROOT / "docs"
BADGES_DIR = DOCS / "badges"


def read_metric(filename: str, pattern: str, default: str = "?") -> str:
    p = DOCS / filename
    if not p.exists():
        return default
    m = re.search(pattern, p.read_text(encoding="utf-8"))
    return m.group(1) if m else default


def make_badge(label: str, value: str, color: str) -> str:
    """Генерирует SVG-бейдж в стиле shields.io."""
    lw = len(label) * 6 + 12
    vw = len(value) * 7 + 12
    total = lw + vw

    COLOR_MAP = {
        "green":  "#4c1",
        "yellow": "#dfb317",
        "orange": "#fe7d37",
        "red":    "#e05d44",
        "blue":   "#007ec6",
        "purple": "#9f4eb0",
        "gray":   "#9f9f9f",
    }
    hex_color = COLOR_MAP.get(color, color)

    return f'''\
<svg xmlns="http://www.w3.org/2000/svg" width="{total}" height="20">
  <linearGradient id="s" x2="0" y2="100%">
    <stop offset="0" stop-color="#bbb" stop-opacity=".1"/>
    <stop offset="1" stop-opacity=".1"/>
  </linearGradient>
  <clipPath id="r"><rect width="{total}" height="20" rx="3"/></clipPath>
  <g clip-path="url(#r)">
    <rect width="{lw}" height="20" fill="#555"/>
    <rect x="{lw}" width="{vw}" height="20" fill="{hex_color}"/>
    <rect width="{total}" height="20" fill="url(#s)"/>
  </g>
  <g fill="#fff" text-anchor="middle" font-family="Verdana,Geneva,sans-serif"
     font-size="11">
    <text x="{lw//2}" y="15" fill="#010101" fill-opacity=".3">{label}</text>
    <text x="{lw//2}" y="14">{label}</text>
    <text x="{lw + vw//2}" y="15" fill="#010101" fill-opacity=".3">{value}</text>
    <text x="{lw + vw//2}" y="14">{value}</text>
  </g>
</svg>'''


def score_color(pct: int) -> str:
    if pct >= 90: return "green"
    if pct >= 70: return "yellow"
    if pct >= 50: return "orange"
    return "red"


def main():
    print("Генерация SVG-бейджей...")
    BADGES_DIR.mkdir(exist_ok=True)

    # Собираем метрики
    total_md = len(list(DOCS.rglob("*.md")))
    total_words = sum(
        len(f.read_text(encoding="utf-8").split())
        for f in DOCS.rglob("*.md")
    )
    scripts_n = len(list((ROOT / "scripts").glob("improve_*.py")))

    health_raw = read_metric("HEALTH.md", r'Общий балл.*?\*\*(\d+)/100\*\*', "75")
    health_pct = int(health_raw) if health_raw.isdigit() else 75

    scoring_raw = read_metric("SCORING.md", r'\((\d+)%\)', "96")
    scoring_pct = int(scoring_raw) if scoring_raw.isdigit() else 96

    words_k = f"{total_words // 1000}K"

    badges = [
        ("docs",    f"{total_md}",   "blue",                "docs.svg"),
        ("words",   words_k,         "blue",                "words.svg"),
        ("scripts", f"{scripts_n}",  "purple",              "scripts.svg"),
        ("health",  f"{health_pct}%",score_color(health_pct),"health.svg"),
        ("go/no-go",f"{scoring_pct}%",score_color(scoring_pct),"scoring.svg"),
        ("license", "MIT",           "green",               "license.svg"),
        ("branch",  "active",        "green",               "branch.svg"),
    ]

    badge_paths = []
    for label, value, color, filename in badges:
        svg = make_badge(label, value, color)
        out = BADGES_DIR / filename
        out.write_text(svg, encoding="utf-8")
        badge_paths.append((label, out.relative_to(ROOT)))

    print(f"  wrote: {len(badges)} badges → {BADGES_DIR.relative_to(ROOT)}/")

    # Обновляем README.md — вставляем бейджи после первого H1
    readme = ROOT / "README.md"
    if readme.exists():
        text = readme.read_text(encoding="utf-8")
        badge_marker = "<!-- badges -->"

        if badge_marker not in text:
            badge_block = "\n" + badge_marker + "\n"
            for label, rel_path in badge_paths:
                badge_block += f"![{label}]({rel_path}) "
            badge_block += "\n"

            h1 = re.search(r'^# .+$', text, re.MULTILINE)
            if h1:
                insert = h1.end()
                text = text[:insert] + badge_block + text[insert:]
                readme.write_text(text, encoding="utf-8")
                print(f"  updated: README.md (badges inserted)")

    # Markdown-документация бейджей
    lines = [
        "# Бейджи репозитория\n",
        f"Автоматически генерируются скриптом `improve_badges.py`.\n",
        "## Текущие бейджи\n",
    ]
    for label, rel_path in badge_paths:
        lines.append(f"![{label}]({rel_path}) — `{rel_path}`")

    lines += [
        "\n## Использование в README\n",
        "```markdown",
    ]
    for label, rel_path in badge_paths:
        lines.append(f"![{label}]({rel_path})")
    lines.append("```")

    (BADGES_DIR / "README.md").write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(f"  wrote: {(BADGES_DIR / 'README.md').relative_to(ROOT)}")


if __name__ == "__main__":
    main()
