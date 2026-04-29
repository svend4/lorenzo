"""
improve_status_badges.py — генератор SVG status badges для README.

Создаёт docs/badges/*.svg для:
  - tests        → 101 passing | 99 failing
  - templates    → 22 templates
  - skills       → 28 skills
  - mcp-servers  → 9 servers
  - manifests    → 13 manifests
  - health       → score из docs/HEALTH.md
  - validation   → 14 valid / 0 errors

Также пишет docs/BADGES.md с markdown-сниппетами для копипаста в README.

Запуск:
    python scripts/improve_status_badges.py
"""
import json
import re
import subprocess
import sys
from datetime import date
from pathlib import Path

ROOT = Path(__file__).parent.parent
BADGES_DIR = ROOT / "docs" / "badges"
DOCS = ROOT / "docs"


def shields_io(label: str, message: str, color: str) -> str:
    """URL для shields.io badge (URL-encoded)."""
    def _encode(s: str) -> str:
        return (s.replace("-", "--").replace("_", "__")
                .replace(" ", "_"))
    return f"https://img.shields.io/badge/{_encode(label)}-{_encode(message)}-{color}"


def svg_badge(label: str, message: str, color: str) -> str:
    """Минимальный SVG badge без зависимостей (статика)."""
    label_w = max(len(label) * 7, 40)
    msg_w = max(len(message) * 7, 40)
    total_w = label_w + msg_w
    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="{total_w}" height="20">
  <linearGradient id="g" x2="0" y2="100%">
    <stop offset="0" stop-color="#bbb" stop-opacity=".1"/>
    <stop offset="1" stop-opacity=".1"/>
  </linearGradient>
  <rect width="{total_w}" height="20" rx="3" fill="#555"/>
  <rect x="{label_w}" width="{msg_w}" height="20" rx="3" fill="{color}"/>
  <rect width="{total_w}" height="20" rx="3" fill="url(#g)"/>
  <g fill="#fff" text-anchor="middle" font-family="DejaVu Sans,Verdana,Geneva,sans-serif" font-size="11">
    <text x="{label_w//2}" y="14">{label}</text>
    <text x="{label_w + msg_w//2}" y="14">{message}</text>
  </g>
</svg>'''


def count_files(pattern: str, dir: Path = DOCS) -> int:
    if not dir.exists():
        return 0
    return len(list(dir.glob(pattern)))


def count_tests() -> tuple[int, int]:
    """Возвращает (passed, failed) для pytest."""
    result = subprocess.run(
        [sys.executable, "-m", "pytest", "tests/", "docs-toolkit/tests/", "-q",
         "--tb=no", "--no-header"],
        capture_output=True, text=True, cwd=ROOT, timeout=60
    )
    out = result.stdout + result.stderr
    m = re.search(r'(\d+)\s+passed', out)
    passed = int(m.group(1)) if m else 0
    m_fail = re.search(r'(\d+)\s+failed', out)
    failed = int(m_fail.group(1)) if m_fail else 0
    return passed, failed


def count_skills() -> int:
    return count_files("*.md", ROOT / ".claude" / "skills")


def count_templates() -> int:
    d = DOCS / "templates"
    if not d.exists():
        return 0
    return len([f for f in d.glob("*.md") if f.name != "README.md"])


def count_mcp_servers() -> int:
    cfg = ROOT / ".claude" / "mcp.json"
    if not cfg.exists():
        return 0
    return len(json.loads(cfg.read_text(encoding="utf-8")).get("mcpServers", {}))


def count_manifests() -> int:
    d = ROOT / "tasks" / "_generated"
    if not d.exists():
        return 0
    return len(list(d.glob("*.json")))


def count_scripts() -> int:
    return len(list((ROOT / "scripts").glob("improve_*.py")))


def get_health_score() -> int | None:
    health = DOCS / "HEALTH.md"
    if not health.exists():
        return None
    text = health.read_text(encoding="utf-8")
    m = re.search(r'Общий балл:\s*\*?\*?\s*(\d+)/100', text)
    return int(m.group(1)) if m else None


def validation_status() -> tuple[int, int]:
    val = DOCS / "VALIDATION.md"
    if not val.exists():
        return 0, 0
    text = val.read_text(encoding="utf-8")
    m_v = re.search(r'\*\*Валидно:\*\*\s*(\d+)', text)
    m_e = re.search(r'\*\*С ошибками:\*\*\s*(\d+)', text)
    return int(m_v.group(1)) if m_v else 0, int(m_e.group(1)) if m_e else 0


def color_for_score(score: int) -> str:
    if score >= 90:
        return "brightgreen"
    if score >= 75:
        return "green"
    if score >= 60:
        return "yellowgreen"
    if score >= 40:
        return "yellow"
    if score >= 20:
        return "orange"
    return "red"


def main():
    BADGES_DIR.mkdir(parents=True, exist_ok=True)

    badges: list[tuple[str, str, str]] = []  # name, message, color

    # Tests
    print("Подсчёт тестов...")
    passed, failed = count_tests()
    if failed == 0:
        badges.append(("tests", "tests", f"{passed}_passing", "brightgreen"))
    else:
        badges.append(("tests", "tests", f"{passed}_passing,_{failed}_failing", "red"))

    # Counts
    badges.append(("templates", "templates", str(count_templates()), "blue"))
    badges.append(("skills", "skills", str(count_skills()), "blue"))
    badges.append(("mcp-servers", "mcp_servers", str(count_mcp_servers()), "blue"))
    badges.append(("manifests", "manifests", str(count_manifests()), "blue"))
    badges.append(("scripts", "scripts", str(count_scripts()), "blue"))

    # Health
    health = get_health_score()
    if health is not None:
        badges.append(("health", "health", f"{health}/100", color_for_score(health)))

    # Validation
    valid, errors = validation_status()
    if errors == 0 and valid > 0:
        badges.append(("validation", "validation", f"{valid}_valid", "brightgreen"))
    elif errors > 0:
        badges.append(("validation", "validation", f"{errors}_errors", "red"))

    # Записываем SVG и markdown
    md_lines = ['# Status Badges\n', f'_Обновлено: {date.today().isoformat()}_\n',
                '\n## Превью\n']
    md_snippets = ['\n## Markdown сниппеты для README\n```markdown']

    for filename, label, message, color in badges:
        # SVG
        svg = svg_badge(label.replace("_", " "), message.replace("_", " "), _color_hex(color))
        svg_path = BADGES_DIR / f"{filename}.svg"
        svg_path.write_text(svg, encoding="utf-8")

        # Shields.io URL (надёжнее для README)
        url = shields_io(label.replace("_", "-"), message.replace("_", "-"), color)
        md_lines.append(f"- **{filename}** ![{label}]({url})")
        md_snippets.append(f"![{label}]({url})")

    md_snippets.append("```")

    badges_md = DOCS / "BADGES.md"
    badges_md.write_text('\n'.join(md_lines + md_snippets) + '\n', encoding='utf-8')

    print(f"\n→ {badges_md.relative_to(ROOT)}")
    print(f"→ {BADGES_DIR.relative_to(ROOT)}/ ({len(badges)} SVG)")
    return 0


def _color_hex(name: str) -> str:
    return {
        "brightgreen": "#4c1",
        "green": "#97ca00",
        "yellowgreen": "#a4a61d",
        "yellow": "#dfb317",
        "orange": "#fe7d37",
        "red": "#e05d44",
        "blue": "#007ec6",
        "lightgrey": "#9f9f9f",
    }.get(name, "#9f9f9f")


if __name__ == '__main__':
    sys.exit(main())
