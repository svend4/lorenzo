"""
improve_dependabot.py — мониторинг версий OSS-компонентов Svyazi 2.0.

Извлекает упоминания проектов + версий из docs/, сверяет с PyPI/GitHub
и сообщает об устаревших зависимостях.

Дополнительно: генерирует .github/dependabot.yml для автоматических PR.

Создаёт docs/DEPENDABOT.md.
Запуск:
    python scripts/improve_dependabot.py
    python scripts/improve_dependabot.py --check-pypi   # запросы к PyPI
    python scripts/improve_dependabot.py --generate-config   # .github/dependabot.yml
"""
import json
import re
import sys
import urllib.request
import urllib.error
from pathlib import Path
from datetime import date

ROOT = Path(__file__).parent.parent
DOCS = ROOT / "docs"
TODAY = date.today().isoformat()

CHECK_PYPI = "--check-pypi" in sys.argv
GEN_CONFIG = "--generate-config" in sys.argv

# Известные зависимости проекта (пакет → требуемая версия из docs)
KNOWN_DEPS: dict[str, dict] = {
    "anthropic": {"min_version": "0.25.0", "used_in": "scripts/improve_llm_*.py"},
    "pyspellchecker": {"min_version": "0.8.0", "used_in": "scripts/improve_spellcheck.py"},
    "mcp": {"min_version": "1.0.0", "used_in": "scripts/mcp_server.py"},
    "pre-commit": {"min_version": "3.0.0", "used_in": ".pre-commit-config.yaml"},
}

# OSS-проекты из базы знаний (не pip, но отслеживаем)
OSS_PROJECTS = {
    "AgentFS": "https://github.com/kksudo/agentfs",
    "NGT Memory": "https://github.com/spbmolot/ngt-memory",
    "Yodoca": "https://github.com/VitalyOborin/yodoca",
    "knowledge-space": "https://github.com/AnastasiyaW/knowledge-space",
}

DEPENDABOT_CONFIG = """\
# Автоматически создан improve_dependabot.py
version: 2
updates:
  - package-ecosystem: "pip"
    directory: "/"
    schedule:
      interval: "weekly"
    labels:
      - "dependencies"
      - "automated"
    commit-message:
      prefix: "deps"
    open-pull-requests-limit: 5

  - package-ecosystem: "github-actions"
    directory: "/"
    schedule:
      interval: "monthly"
    labels:
      - "ci"
      - "automated"
"""


def _check_pypi_version(package: str) -> str | None:
    try:
        url = f"https://pypi.org/pypi/{package}/json"
        req = urllib.request.Request(url, headers={"User-Agent": "Lorenzo-depcheck/1.0"})
        with urllib.request.urlopen(req, timeout=8) as resp:
            data = json.loads(resp.read())
            return data["info"]["version"]
    except Exception:
        return None


def _version_tuple(v: str) -> tuple:
    try:
        return tuple(int(x) for x in v.split('.')[:3])
    except Exception:
        return (0,)


def _extract_version_mentions(text: str) -> list[tuple[str, str]]:
    """Ищет упоминания 'пакет==версия' или 'пакет>=версия' в тексте."""
    found = []
    for m in re.finditer(r'([a-zA-Z][a-zA-Z0-9_-]{1,30})[=><]{1,2}([0-9]+\.[0-9.]+)', text):
        found.append((m.group(1), m.group(2)))
    return found


def main() -> None:
    print("📦 improve_dependabot.py — мониторинг версий зависимостей")
    if CHECK_PYPI:
        print("   Режим: проверка PyPI (HTTP-запросы)\n")

    if GEN_CONFIG:
        out = ROOT / ".github" / "dependabot.yml"
        out.parent.mkdir(parents=True, exist_ok=True)
        out.write_text(DEPENDABOT_CONFIG, encoding="utf-8")
        print(f"  wrote: {out.relative_to(ROOT)}")
        print("  Dependabot будет создавать PR при обновлении зависимостей.")
        return

    # Сканируем docs/ на упоминания версий
    version_mentions: dict[str, set[str]] = {}
    for f in DOCS.rglob("*.md"):
        try:
            text = f.read_text(encoding="utf-8")
        except Exception:
            continue
        for pkg, ver in _extract_version_mentions(text):
            if pkg.lower() in (k.lower() for k in KNOWN_DEPS):
                version_mentions.setdefault(pkg, set()).add(ver)

    # Проверяем PyPI если нужно
    pypi_versions: dict[str, str | None] = {}
    if CHECK_PYPI:
        for pkg in KNOWN_DEPS:
            print(f"  Проверяем {pkg}...", end=" ", flush=True)
            latest = _check_pypi_version(pkg)
            pypi_versions[pkg] = latest
            print(f"{latest or '❌'}")

    # Формируем отчёт
    lines = [
        "# Мониторинг зависимостей\n",
        f"_Обновлено: {TODAY}_\n",
        "## Python-зависимости\n",
        "| Пакет | Мин. версия | Последняя (PyPI) | Статус | Используется в |",
        "|-------|------------|-----------------|--------|----------------|",
    ]

    for pkg, info in sorted(KNOWN_DEPS.items()):
        latest = pypi_versions.get(pkg, "—")
        min_v = info["min_version"]
        if latest and latest != "—":
            ok = _version_tuple(latest) >= _version_tuple(min_v)
            status = "✅" if ok else "⚠️ обновить"
        else:
            status = "—"
        lines.append(
            f"| `{pkg}` | `{min_v}` | `{latest or '—'}` | {status} | `{info['used_in']}` |"
        )

    lines += [
        "\n## OSS-проекты (Svyazi 2.0)\n",
        "| Проект | Репозиторий | Статус |",
        "|--------|------------|--------|",
    ]
    for name, url in OSS_PROJECTS.items():
        lines.append(f"| {name} | [{url}]({url}) | — |")

    lines += [
        "\n## Автоматизация\n",
        "```bash",
        "# Генерировать .github/dependabot.yml",
        "python scripts/improve_dependabot.py --generate-config",
        "",
        "# Проверить актуальные версии PyPI",
        "python scripts/improve_dependabot.py --check-pypi",
        "```\n",
        "После `--generate-config` Dependabot автоматически откроет PR",
        "при выходе новых версий зависимостей.",
    ]

    out = DOCS / "DEPENDABOT.md"
    out.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(f"  wrote: {out.relative_to(ROOT)}")
    print(f"  отслеживается: {len(KNOWN_DEPS)} пакетов + {len(OSS_PROJECTS)} OSS-проектов")


if __name__ == "__main__":
    main()
