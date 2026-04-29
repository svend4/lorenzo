"""
improve_risk_register.py — реестр рисков проекта Svyazi 2.0.
Извлекает риски из документов (слова: риск, проблема, блокер, угроза),
дополняет курированным списком, строит матрицу вероятность × влияние.
Создаёт docs/RISK_REGISTER.md.
Запуск: python scripts/improve_risk_register.py
"""
import re
from pathlib import Path
from collections import defaultdict

ROOT = Path(__file__).parent.parent
DOCS = ROOT / "docs"

# Курированные риски: (название, категория, вероятность 1-5, влияние 1-5, митигация)
RISKS = [
    ("Авторы компонентов не ответят на запросы",
     "Команда", 3, 5,
     "Подготовить альтернативные компоненты; форкнуть при необходимости"),
    ("Лицензия BSL 1.1 (NGT) ограничит коммерческое использование",
     "Правовой", 3, 4,
     "Использовать только для внутренних нужд или найти MIT-альтернативу"),
    ("Высокая стоимость Claude API при масштабировании",
     "Финансовый", 4, 3,
     "Кешировать промпты; использовать Haiku для рутинных задач; батчинг"),
    ("Зависимость от закрытого API Anthropic",
     "Технический", 2, 4,
     "Абстрагировать через провайдер-интерфейс; поддержать Ollama/local LLM"),
    ("Устаревание документации при быстром развитии компонентов",
     "Качество", 4, 3,
     "CI-обновление docs; improve_watcher.py; еженедельные дайджесты"),
    ("PII-утечки через MCP-инструменты",
     "Безопасность", 3, 5,
     "SENTINEL allowlist обязателен; quarantine для внешних данных"),
    ("AgentFS не поддерживает concurrent multi-agent доступ",
     "Технический", 3, 4,
     "CRDT-синхронизация или lock-файлы на уровне Knowledge OS"),
    ("Одиночный разработчик — bus factor 1",
     "Команда", 4, 5,
     "Документировать всё; привлечь авторов OSS-компонентов как контрибьюторов"),
    ("Прототип Knowledge OS займёт дольше запланированного",
     "Сроки", 3, 3,
     "Начать с минимальным ансамблем: Svyazi + CardIndex + AgentFS"),
    ("Конкурирующие OSS-проекты могут обогнать",
     "Рынок", 2, 3,
     "Уникальность — ансамблевый подход; интеграция > замена"),
]

PROB_LABELS = {1: "Очень низкая", 2: "Низкая", 3: "Средняя", 4: "Высокая", 5: "Очень высокая"}
IMPACT_LABELS = {1: "Минимальное", 2: "Малое", 3: "Среднее", 4: "Большое", 5: "Критическое"}

RISK_KEYWORDS = re.compile(
    r'(?:риск|проблем[аы]|блокер|угроз[аы]|ограничени[ея]|зависимост[ьи]'
    r'|уязвимост[ьи]|опасност[ьи])',
    re.IGNORECASE
)


def extract_doc_risks() -> list[tuple[str, str]]:
    """Извлекает упоминания рисков из документов."""
    found: list[tuple[str, str]] = []
    seen: set = set()
    for f in sorted(DOCS.rglob("*.md"))[:80]:
        text = f.read_text(encoding="utf-8")
        for m in RISK_KEYWORDS.finditer(text):
            start = max(0, m.start() - 30)
            end   = min(len(text), m.end() + 100)
            snippet = re.sub(r'\s+', ' ', text[start:end]).strip()[:150]
            key = snippet[:40].lower()
            if key not in seen and len(snippet) > 40:
                seen.add(key)
                src = str(f.relative_to(ROOT)).split("/")[-1].replace(".md", "")
                found.append((src, snippet))
            if len(found) >= 15:
                break
        if len(found) >= 15:
            break
    return found


def risk_score(prob: int, impact: int) -> int:
    return prob * impact


def risk_level(score: int) -> str:
    if score >= 16: return "🔴 КРИТИЧЕСКИЙ"
    if score >= 9:  return "🟠 ВЫСОКИЙ"
    if score >= 4:  return "🟡 СРЕДНИЙ"
    return "🟢 НИЗКИЙ"


def make_matrix() -> list[str]:
    """5×5 матрица рисков."""
    lines = ["```"]
    lines.append("Влияние ↑  Вероятность →")
    lines.append("          1-Оч.низк  2-Низкая   3-Средняя  4-Высокая  5-Оч.выс.")
    for impact in range(5, 0, -1):
        row = f"  {impact}-{IMPACT_LABELS[impact][:8]:<9}|"
        for prob in range(1, 6):
            sc = prob * impact
            if sc >= 16: cell = "  🔴 КРИТ "
            elif sc >= 9: cell = "  🟠 ВЫСК "
            elif sc >= 4: cell = "  🟡 СРЕД "
            else:         cell = "  🟢 НИЗК "
            row += cell + "|"
        lines.append(row)
    lines.append("```")
    return lines


def main():
    print("Генерация реестра рисков...")

    doc_risks = extract_doc_risks()

    # Сортируем по убыванию score
    sorted_risks = sorted(RISKS, key=lambda r: -risk_score(r[2], r[3]))

    lines = [
        "# Реестр рисков — Svyazi 2.0\n",
        f"_Курированных рисков: {len(RISKS)} · Из документов: {len(doc_risks)}_\n",

        "## Матрица рисков (Вероятность × Влияние)\n",
    ]
    lines += make_matrix()

    lines += [
        "\n## Реестр\n",
        "| # | Риск | Категория | Вероятн. | Влияние | Score | Уровень |",
        "|---|------|-----------|----------|---------|-------|---------|",
    ]
    for i, (name, cat, prob, impact, _) in enumerate(sorted_risks, 1):
        sc = risk_score(prob, impact)
        level = risk_level(sc)
        lines.append(
            f"| {i} | {name[:50]} | {cat} | "
            f"{prob} ({PROB_LABELS[prob][:6]}) | "
            f"{impact} ({IMPACT_LABELS[impact][:6]}) | **{sc}** | {level} |"
        )

    lines += ["\n## Митигации\n"]
    for i, (name, cat, prob, impact, mitigation) in enumerate(sorted_risks, 1):
        sc  = risk_score(prob, impact)
        lines += [f"### {i}. {name}\n", f"**Уровень:** {risk_level(sc)} (score {sc})\n",
                  f"**Митигация:** {mitigation}\n"]

    if doc_risks:
        lines += [
            "## Упоминания рисков в документах\n",
            "| Источник | Фрагмент |",
            "|----------|---------|",
        ]
        for src, snippet in doc_risks[:12]:
            lines.append(f"| `{src}` | {snippet[:100]}… |")

    lines += [
        "\n## Итоговая статистика\n",
        f"| Уровень | Кол-во |",
        f"|---------|--------|",
    ]
    by_level: dict[str, int] = defaultdict(int)
    for name, cat, prob, impact, _ in RISKS:
        by_level[risk_level(risk_score(prob, impact))] += 1
    for level, count in sorted(by_level.items()):
        lines.append(f"| {level} | {count} |")

    out = DOCS / "RISK_REGISTER.md"
    out.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(f"  wrote: {out.relative_to(ROOT)}")
    print(f"  рисков: {len(RISKS)}, из docs: {len(doc_risks)}")


if __name__ == "__main__":
    main()
