"""
improve_component_matrix.py — матрица совместимости и возможностей компонентов.
Показывает какие компоненты поддерживают какие функции (memory, search, MCP, ...).
Создаёт docs/COMPONENT_MATRIX.md.
Запуск: python scripts/improve_component_matrix.py
"""
from pathlib import Path

ROOT = Path(__file__).parent.parent
DOCS = ROOT / "docs"

# Компоненты: (название, лицензия, статус, repo)
COMPONENTS = [
    ("CardIndex",       "MIT",       "stable",       "kksudo/card-index"),
    ("AgentFS",         "MIT",       "stable",       "kksudo/agentfs"),
    ("Yodoca",          "Apache 2.0","active",       "spbmolot/yodoca"),
    ("NGT-memory",      "BSL 1.1",   "active",       "—"),
    ("SENTINEL",        "MIT",       "active",       "—"),
    ("Rufler",          "—",         "experimental", "—"),
    ("knowledge-space", "MIT",       "stable",       "kksudo/knowledge-space"),
    ("Firecrawl",       "MIT",       "stable",       "mendableai/firecrawl"),
    ("Wikontic",        "—",         "unknown",      "—"),
    ("Memnet",          "—",         "experimental", "—"),
    ("agent-memory-mcp","MIT",       "experimental", "—"),
    ("LiteParse",       "—",         "unknown",      "—"),
    ("AI Factory",      "—",         "unknown",      "—"),
    ("agent-pool",      "—",         "unknown",      "—"),
]

# Возможности: (ключ, метка)
FEATURES = [
    ("memory",      "Долгосрочная память"),
    ("search",      "Поиск/индекс"),
    ("mcp",         "MCP-совместим"),
    ("graph",       "Граф знаний"),
    ("security",    "Безопасность/PII"),
    ("orchestrate", "Оркестрация"),
    ("crawl",       "Веб-краулинг"),
    ("storage",     "Хранилище данных"),
    ("api",         "Документированный API"),
    ("crdt",        "CRDT/sync"),
]

# Матрица: компонент → список поддерживаемых фич (✅) / частично (🟡) / нет (❌)
MATRIX = {
    "CardIndex":        ["✅","✅","✅","🟡","❌","❌","❌","✅","✅","❌"],
    "AgentFS":          ["🟡","✅","✅","❌","🟡","❌","❌","✅","✅","🟡"],
    "Yodoca":           ["✅","✅","🟡","❌","🟡","❌","❌","✅","🟡","❌"],
    "NGT-memory":       ["✅","✅","❌","✅","❌","❌","❌","✅","🟡","❌"],
    "SENTINEL":         ["❌","❌","✅","❌","✅","❌","❌","❌","✅","❌"],
    "Rufler":           ["❌","❌","✅","❌","❌","✅","❌","❌","🟡","❌"],
    "knowledge-space":  ["✅","✅","🟡","🟡","❌","❌","❌","✅","🟡","❌"],
    "Firecrawl":        ["❌","✅","✅","❌","❌","❌","✅","❌","✅","❌"],
    "Wikontic":         ["❌","✅","❌","✅","❌","❌","❌","✅","❌","❌"],
    "Memnet":           ["✅","🟡","❌","❌","❌","❌","❌","✅","❌","❌"],
    "agent-memory-mcp": ["✅","❌","✅","❌","❌","❌","❌","✅","🟡","❌"],
    "LiteParse":        ["❌","✅","❌","❌","❌","❌","✅","❌","❌","❌"],
    "AI Factory":       ["❌","❌","🟡","❌","❌","✅","❌","❌","❌","❌"],
    "agent-pool":       ["❌","❌","🟡","❌","❌","✅","❌","❌","❌","❌"],
}

STATUS_ICON = {"stable": "🟢", "active": "🔵", "experimental": "🟡", "unknown": "⚪"}
LICENSE_COLOR = {"MIT": "🟢", "Apache 2.0": "🟢", "BSL 1.1": "🟠", "—": "⚪"}


def main():
    print("Генерация матрицы компонентов...")

    feature_keys  = [f[0] for f in FEATURES]
    feature_labels = [f[1] for f in FEATURES]

    lines = [
        "# Матрица компонентов Svyazi 2.0\n",
        "_Совместимость и возможности 14 компонентов экосистемы._\n",
        "**Легенда:** ✅ Поддерживается · 🟡 Частично · ❌ Не поддерживается\n",

        "## Матрица возможностей\n",
    ]

    # Заголовок таблицы
    header = "| Компонент | Лицензия | Статус |"
    sep    = "|-----------|----------|--------|"
    for label in feature_labels:
        short = label[:8]
        header += f" {short} |"
        sep    += "---------|"
    lines += [header, sep]

    for name, license_, status, _ in COMPONENTS:
        feats = MATRIX.get(name, ["❌"] * len(FEATURES))
        lic_icon = LICENSE_COLOR.get(license_, "⚪")
        sta_icon = STATUS_ICON.get(status, "⚪")
        row = f"| **{name}** | {lic_icon} {license_} | {sta_icon} {status} |"
        for feat in feats:
            row += f" {feat} |"
        lines.append(row)

    # Подсчёт поддержки по фичам
    lines += [
        "\n## Покрытие возможностей\n",
        "| Возможность | Полная поддержка | Частичная | Итого |",
        "|-------------|-----------------|-----------|-------|",
    ]
    for i, (key, label) in enumerate(FEATURES):
        full    = sum(1 for n, *_ in COMPONENTS if MATRIX.get(n, [])[i:i+1] == ["✅"])
        partial = sum(1 for n, *_ in COMPONENTS if MATRIX.get(n, [])[i:i+1] == ["🟡"])
        lines.append(f"| {label} | {full} | {partial} | {full+partial}/{len(COMPONENTS)} |")

    # Таблица компонентов с репо
    lines += [
        "\n## Каталог компонентов\n",
        "| Компонент | Лицензия | Статус | Репозиторий |",
        "|-----------|----------|--------|-------------|",
    ]
    for name, license_, status, repo in COMPONENTS:
        lic_icon = LICENSE_COLOR.get(license_, "⚪")
        sta_icon = STATUS_ICON.get(status, "⚪")
        repo_str = f"`{repo}`" if repo != "—" else "—"
        lines.append(f"| **{name}** | {lic_icon} {license_} | {sta_icon} {status} | {repo_str} |")

    lines += [
        "\n## Рекомендуемые ансамбли\n",
        "| Ансамбль | Компоненты | Ключевая функция |",
        "|----------|-----------|-----------------|",
        "| Knowledge OS | CardIndex + AgentFS + knowledge-space | Индекс знаний + AI FS |",
        "| Memory Layer | Yodoca + NGT-memory + agent-memory-mcp | Долгосрочная память |",
        "| Security Runtime | SENTINEL + AgentFS | PII-защита + MCP allowlist |",
        "| Web Intelligence | Firecrawl + CardIndex + Yodoca | Краулинг → память |",
        "| Agent Orchestra | Rufler + agent-pool + AI Factory | Оркестрация агентов |\n",
    ]

    out = DOCS / "COMPONENT_MATRIX.md"
    out.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(f"  wrote: {out.relative_to(ROOT)}")
    print(f"  компонентов: {len(COMPONENTS)}, возможностей: {len(FEATURES)}")


if __name__ == "__main__":
    main()
