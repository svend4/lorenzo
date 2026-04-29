"""
improve_kpi_snapshot.py — исторические снапшоты ключевых метрик.
Читает текущие метрики из docs/, добавляет запись с датой в историю,
строит таблицу трендов. Создаёт docs/KPI_HISTORY.md.
Запуск: python scripts/improve_kpi_snapshot.py
"""
import re
import json
from pathlib import Path
from datetime import datetime

ROOT = Path(__file__).parent.parent
DOCS = ROOT / "docs"
HISTORY_FILE = DOCS / "kpi_history.json"


def read_metric(fname: str, pattern: str, default: int = 0) -> int:
    p = DOCS / fname
    if not p.exists():
        return default
    m = re.search(pattern, p.read_text(encoding="utf-8"))
    if not m:
        return default
    val = m.group(1).replace(",", "").replace(" ", "")
    try:
        return int(val)
    except ValueError:
        return default


def collect_snapshot() -> dict:
    total_md    = len(list(DOCS.rglob("*.md")))
    total_words = sum(len(f.read_text(encoding="utf-8").split()) for f in DOCS.rglob("*.md"))
    n_scripts   = len(list((ROOT / "scripts").glob("improve_*.py")))

    scoring = read_metric("SCORING.md",  r'(\d+)%',         96)
    health  = read_metric("HEALTH.md",   r'(\d+)/100',       75)
    kpis    = read_metric("KPI.md",      r'(\d+)\s+KPI',   737)
    questions = read_metric("QUESTIONS.md", r'(\d+)\s+вопрос', 484)
    actions = read_metric("ACTION_ITEMS.md", r'(\d+)\s+задач', 0)

    return {
        "date":      datetime.now().strftime("%Y-%m-%d"),
        "docs":      total_md,
        "words":     total_words,
        "scripts":   n_scripts,
        "scoring":   scoring,
        "health":    health,
        "kpis":      kpis,
        "questions": questions,
        "actions":   actions,
    }


def load_history() -> list[dict]:
    if not HISTORY_FILE.exists():
        return []
    try:
        return json.loads(HISTORY_FILE.read_text(encoding="utf-8"))
    except Exception:
        return []


def save_history(history: list[dict]) -> None:
    HISTORY_FILE.write_text(json.dumps(history, ensure_ascii=False, indent=2), encoding="utf-8")


def trend(curr: int, prev: int) -> str:
    if prev == 0:
        return "→"
    delta = curr - prev
    if delta > 0:   return f"↑ +{delta}"
    if delta < 0:   return f"↓ {delta}"
    return "→ ="


def main():
    print("Снапшот метрик KPI...")

    snapshot = collect_snapshot()
    history  = load_history()

    # Проверяем, есть ли уже снапшот за сегодня
    today = snapshot["date"]
    history = [h for h in history if h["date"] != today]
    history.append(snapshot)
    # Храним последние 30 снапшотов
    history = history[-30:]
    save_history(history)

    print(f"  дата: {today}, всего снапшотов: {len(history)}")

    # Предыдущий снапшот для трендов
    prev = history[-2] if len(history) >= 2 else {}

    lines = [
        "# История метрик KPI\n",
        f"_Последнее обновление: {today} · Снапшотов в истории: {len(history)}_\n",

        "## Текущие метрики\n",
        "| Метрика | Значение | Тренд |",
        "|---------|---------|-------|",
        f"| Markdown документов | **{snapshot['docs']}** | {trend(snapshot['docs'], prev.get('docs', 0))} |",
        f"| Слов | **{snapshot['words']:,}** | {trend(snapshot['words'], prev.get('words', 0))} |",
        f"| Скриптов | **{snapshot['scripts']}** | {trend(snapshot['scripts'], prev.get('scripts', 0))} |",
        f"| Скоринг | **{snapshot['scoring']}%** | {trend(snapshot['scoring'], prev.get('scoring', 0))} |",
        f"| Здоровье | **{snapshot['health']}/100** | {trend(snapshot['health'], prev.get('health', 0))} |",
        f"| KPI показателей | **{snapshot['kpis']}** | {trend(snapshot['kpis'], prev.get('kpis', 0))} |",
        f"| Открытых вопросов | **{snapshot['questions']}** | {trend(snapshot['questions'], prev.get('questions', 0))} |\n",
    ]

    if len(history) > 1:
        lines += [
            "## История\n",
            "| Дата | Docs | Слов | Скриптов | Скоринг | Здоровье |",
            "|------|------|------|----------|---------|---------|",
        ]
        for h in reversed(history):
            lines.append(
                f"| {h['date']} | {h['docs']} | {h['words']:,} | "
                f"{h['scripts']} | {h['scoring']}% | {h['health']}/100 |"
            )

        # Мини-тренды ASCII
        if len(history) >= 3:
            lines += ["\n## Тренды (последние снапшоты)\n", "```"]
            for key, label in [("docs", "Docs"), ("scoring", "Score%"), ("scripts", "Scripts")]:
                vals = [h[key] for h in history[-8:]]
                mini = ""
                for i in range(1, len(vals)):
                    if vals[i] > vals[i-1]:   mini += "▲"
                    elif vals[i] < vals[i-1]: mini += "▼"
                    else:                     mini += "─"
                lines.append(f"{label:<10}: {mini}  (current: {vals[-1]})")
            lines.append("```\n")

    lines += [
        "---\n",
        "_История хранится в `docs/kpi_history.json`._\n",
        "_Запускать регулярно для получения трендов._\n",
    ]

    out = DOCS / "KPI_HISTORY.md"
    out.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(f"  wrote: {out.relative_to(ROOT)}")
    print(f"  docs: {snapshot['docs']}, words: {snapshot['words']:,}, scoring: {snapshot['scoring']}%")


if __name__ == "__main__":
    main()
