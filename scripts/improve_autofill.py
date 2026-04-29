"""
improve_autofill.py — заполняет шаблоны данными из документации (Ступень 2).
Берёт шаблоны из docs/templates/, подставляет реальные данные из ENTITIES,
TAGS, NETWORK, SCORING. Создаёт docs/autofilled/ с готовыми документами.
Запуск: python scripts/improve_autofill.py
"""
import re
from pathlib import Path
from collections import defaultdict

ROOT = Path(__file__).parent.parent
DOCS = ROOT / "docs"
TEMPLATES = DOCS / "templates"
OUTPUT    = DOCS / "autofilled"


def load_entities() -> dict[str, dict]:
    """Загружает сущности из ENTITIES.md."""
    p = DOCS / "ENTITIES.md"
    if not p.exists():
        return {}
    text = p.read_text(encoding="utf-8")
    entities: dict[str, dict] = {}
    # Парсим таблицы вида | Имя | Тип | Кол-во |
    for m in re.finditer(r'\|\s*\*?\*?([A-Za-zА-Яа-яёЁ][^\|]{2,40}?)\*?\*?\s*\|\s*([^\|]+?)\s*\|\s*(\d+)', text):
        name  = m.group(1).strip()
        etype = m.group(2).strip()
        count = int(m.group(3))
        entities[name] = {"type": etype, "count": count}
    return entities


def load_scoring() -> dict[str, str]:
    """Загружает Go/No-Go скоринг."""
    p = DOCS / "SCORING.md"
    if not p.exists():
        return {}
    text = p.read_text(encoding="utf-8")
    data: dict[str, str] = {}
    m = re.search(r'(\d+)/(\d+)', text)
    if m:
        data["score"]   = m.group(1)
        data["max"]     = m.group(2)
        data["pct"]     = str(int(int(m.group(1)) / int(m.group(2)) * 100))
    # Статус
    if "GO" in text:
        data["status"] = "GO 🟢"
    elif "PARTIAL" in text:
        data["status"] = "PARTIAL 🟡"
    else:
        data["status"] = "STOP 🔴"
    return data


def load_network_nodes() -> list[str]:
    """Загружает узлы сети компонентов."""
    p = DOCS / "NETWORK.md"
    if not p.exists():
        return []
    text = p.read_text(encoding="utf-8")
    nodes = []
    for m in re.finditer(r'"\s*([A-Za-z][A-Za-z0-9\-_]+)\s*"', text):
        n = m.group(1)
        if n not in nodes:
            nodes.append(n)
    return nodes[:20]


def fill_template(template_text: str, data: dict) -> str:
    """Заменяет {{placeholder}} на данные."""
    def replacer(m):
        key = m.group(1).strip().lower()
        return data.get(key, m.group(0))   # оставить как есть если нет данных
    return re.sub(r'\{\{([^}]+)\}\}', replacer, template_text)


def autofill_component_template(entities: dict, scoring: dict, nodes: list[str]) -> list[dict]:
    """Генерирует карточки для каждого компонента."""
    tpl_path = TEMPLATES / "component-card.md"
    if not tpl_path.exists():
        # Встроенный минимальный шаблон
        template = """# {{name}}

**Тип:** {{type}}
**Статус:** {{status}}
**Упоминаний:** {{count}}

## Описание
_Компонент экосистемы Svyazi 2.0_

## Ссылки
- [Исходники](#)
- [Документация](../README.md)
"""
    else:
        template = tpl_path.read_text(encoding="utf-8")

    results = []
    for name, info in list(entities.items())[:12]:
        data = {
            "name":    name,
            "type":    info.get("type", "компонент"),
            "status":  scoring.get("status", "—"),
            "count":   str(info.get("count", 0)),
            "score":   scoring.get("score", "—"),
            "max":     scoring.get("max", "—"),
            "pct":     scoring.get("pct", "—"),
        }
        filled = fill_template(template, data)
        results.append({"name": name, "content": filled})
    return results


def autofill_research_template(scoring: dict) -> str:
    """Заполняет шаблон исследовательского отчёта."""
    tpl_path = TEMPLATES / "research-note.md"
    if not tpl_path.exists():
        return ""
    template = tpl_path.read_text(encoding="utf-8")
    data = {
        "title":    "Svyazi 2.0 — Research Summary",
        "date":     "2025-Q1",
        "status":   scoring.get("status", "GO 🟢"),
        "score":    scoring.get("score", "159"),
        "max":      scoring.get("max", "164"),
        "pct":      scoring.get("pct", "96"),
        "author":   "svend4",
        "tags":     "AI, OSS, Knowledge OS, MCP, agents",
    }
    return fill_template(template, data)


def main():
    print("Автозаполнение шаблонов данными из документации...")
    OUTPUT.mkdir(exist_ok=True)

    entities = load_entities()
    scoring  = load_scoring()
    nodes    = load_network_nodes()

    print(f"  сущностей: {len(entities)}, узлов сети: {len(nodes)}")
    print(f"  скоринг: {scoring.get('score','?')}/{scoring.get('max','?')} ({scoring.get('status','?')})")

    written = 0

    # 1. Карточки компонентов
    components_dir = OUTPUT / "components"
    components_dir.mkdir(exist_ok=True)
    for item in autofill_component_template(entities, scoring, nodes):
        slug = re.sub(r'[^a-z0-9\-]', '-', item["name"].lower()).strip("-")
        out_path = components_dir / f"{slug}.md"
        out_path.write_text(item["content"], encoding="utf-8")
        written += 1

    # 2. Research note
    research = autofill_research_template(scoring)
    if research:
        rp = OUTPUT / "research-summary.md"
        rp.write_text(research, encoding="utf-8")
        written += 1

    # Отчёт
    lines = [
        "# Автозаполненные шаблоны\n",
        f"_Источники: ENTITIES.md, SCORING.md, NETWORK.md, docs/templates/_\n",
        f"**Создано файлов:** {written}\n",
        "## Файлы\n",
    ]
    for f in sorted(OUTPUT.rglob("*.md")):
        lines.append(f"- [`{f.relative_to(ROOT)}`]({f.relative_to(ROOT)})")

    lines += [
        "\n## Как работает\n",
        "1. Читает шаблоны из `docs/templates/` с плейсхолдерами `{{name}}`",
        "2. Собирает данные: ENTITIES (сущности), SCORING (статус), NETWORK (граф)",
        "3. Заменяет плейсхолдеры реальными данными",
        "4. Сохраняет результаты в `docs/autofilled/`\n",
        "Повторный запуск перезаписывает файлы актуальными данными.",
    ]

    (DOCS / "AUTOFILLED.md").write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(f"  wrote: docs/AUTOFILLED.md + {written} файлов в docs/autofilled/")


if __name__ == "__main__":
    main()
