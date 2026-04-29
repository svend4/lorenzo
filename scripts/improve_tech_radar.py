"""
improve_tech_radar.py — tech radar для технологий проекта Svyazi 2.0.
Классифицирует компоненты по 4 квадрантам: ADOPT / TRIAL / ASSESS / HOLD.
Создаёт docs/TECH_RADAR.md.
Запуск: python scripts/improve_tech_radar.py
"""
from pathlib import Path

ROOT = Path(__file__).parent.parent
DOCS = ROOT / "docs"

# Квадранты tech radar
RADAR = {
    "ADOPT": {
        "description": "Рекомендуем к использованию прямо сейчас. Проверено на практике.",
        "items": [
            ("MCP Protocol",    "Инструменты",  "Стандарт интеграции AI-инструментов — Anthropic"),
            ("CardIndex",       "Компоненты",   "785+ карточек знаний, MIT, стабильный API"),
            ("AgentFS",         "Компоненты",   "Файловая система для AI-агентов, MIT, kksudo"),
            ("Firecrawl",       "Инструменты",  "Веб-краулер для AI, MIT, активная разработка"),
            ("Python 3.11+",    "Платформа",    "Основной язык реализации всех компонентов"),
            ("Markdown docs",   "Практики",     "96% готовности, проверено на 460+ файлах"),
        ],
    },
    "TRIAL": {
        "description": "Стоит попробовать. Перспективно, но ещё требует проверки в вашем контексте.",
        "items": [
            ("Yodoca",          "Компоненты",   "Память с консолидацией, Apache 2.0, spbmolot"),
            ("SENTINEL",        "Компоненты",   "Allowlist безопасности для MCP"),
            ("Rufler",          "Компоненты",   "Оркестратор агентов, активная разработка"),
            ("RAG + Graph",     "Архитектура",  "Гибридный поиск: векторный + граф-обход"),
            ("claude-haiku-4-5","Модели",       "Оптимум цена/качество для enrichment задач"),
            ("CRDT-синхронизация","Архитектура","Бесконфликтная репликация для multi-agent"),
        ],
    },
    "ASSESS": {
        "description": "Изучаем. Интересно, но пока не готово к production-использованию.",
        "items": [
            ("NGT-memory",      "Компоненты",   "Ассоциативный граф памяти, BSL 1.1"),
            ("knowledge-space", "Компоненты",   "База знаний, MIT, нужна оценка API"),
            ("Wikontic",        "Компоненты",   "Граф знаний, статус неизвестен"),
            ("MCP Tool Search", "Компоненты",   "Динамический поиск инструментов"),
            ("claude-opus-4-7", "Модели",       "Для сложных reasoning задач, высокая стоимость"),
            ("Local-first P2P", "Архитектура",  "GDPR-safe распределённые данные"),
        ],
    },
    "HOLD": {
        "description": "Не рекомендуем для новых проектов. Используйте с осторожностью.",
        "items": [
            ("BSL 1.1 libs",    "Лицензии",     "Ограничения при коммерческом использовании"),
            ("Monolithic LLM",  "Архитектура",  "Один LLM вместо ансамбля — узкое место"),
            ("Без PII-защиты",  "Практики",     "Обработка данных без SENTINEL/quarantine"),
            ("Hard-coded prompts","Практики",   "Промпты без версионирования и тестов"),
        ],
    },
}

QUADRANT_ICONS = {"ADOPT": "🟢", "TRIAL": "🔵", "ASSESS": "🟡", "HOLD": "🔴"}


def make_ascii_radar(radar: dict) -> list[str]:
    """Простая ASCII-визуализация radar."""
    lines = ["```"]
    lines.append("┌─────────────────────────┬─────────────────────────┐")
    lines.append("│      🟢 ADOPT           │      🔵 TRIAL           │")

    adopt_items  = [i[0][:22] for i in radar["ADOPT"]["items"]]
    trial_items  = [i[0][:22] for i in radar["TRIAL"]["items"]]
    assess_items = [i[0][:22] for i in radar["ASSESS"]["items"]]
    hold_items   = [i[0][:22] for i in radar["HOLD"]["items"]]

    max_rows = max(len(adopt_items), len(trial_items))
    for i in range(max_rows):
        a = f"  • {adopt_items[i]:<22}" if i < len(adopt_items) else " " * 26
        t = f"  • {trial_items[i]:<22}" if i < len(trial_items) else " " * 26
        lines.append(f"│{a}│{t}│")

    lines.append("├─────────────────────────┼─────────────────────────┤")
    lines.append("│      🟡 ASSESS          │      🔴 HOLD            │")

    max_rows2 = max(len(assess_items), len(hold_items))
    for i in range(max_rows2):
        a = f"  • {assess_items[i]:<22}" if i < len(assess_items) else " " * 26
        h = f"  • {hold_items[i]:<22}"   if i < len(hold_items)   else " " * 26
        lines.append(f"│{a}│{h}│")

    lines.append("└─────────────────────────┴─────────────────────────┘")
    lines.append("```")
    return lines


def main():
    print("Генерация Tech Radar...")

    total = sum(len(v["items"]) for v in RADAR.values())

    lines = [
        "# Tech Radar — Svyazi 2.0\n",
        "_Оценка технологий и компонентов экосистемы по методологии ThoughtWorks._\n",
        f"**Всего позиций:** {total} · "
        f"Adopt: {len(RADAR['ADOPT']['items'])} · "
        f"Trial: {len(RADAR['TRIAL']['items'])} · "
        f"Assess: {len(RADAR['ASSESS']['items'])} · "
        f"Hold: {len(RADAR['HOLD']['items'])}\n",
        "## Обзор\n",
    ]
    lines += make_ascii_radar(RADAR)
    lines.append("")

    for quadrant, data in RADAR.items():
        icon = QUADRANT_ICONS[quadrant]
        lines += [
            f"\n## {icon} {quadrant}\n",
            f"_{data['description']}_\n",
            "| Технология / Компонент | Категория | Комментарий |",
            "|------------------------|-----------|------------|",
        ]
        for name, category, comment in data["items"]:
            lines.append(f"| **{name}** | {category} | {comment} |")

    lines += [
        "\n## Методология\n",
        "- **ADOPT** — используй сейчас, минимальные риски",
        "- **TRIAL** — стоит попробовать в пилоте",
        "- **ASSESS** — изучи, но не внедряй в production",
        "- **HOLD** — избегай для новых проектов\n",
        "_Radar обновляется вручную при существенных изменениях экосистемы._\n",
    ]

    out = DOCS / "TECH_RADAR.md"
    out.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(f"  wrote: {out.relative_to(ROOT)}")
    counts = ", ".join(f"{q}: {len(v['items'])}" for q, v in RADAR.items())
    print(f"  позиций: {total} ({counts})")


if __name__ == "__main__":
    main()
