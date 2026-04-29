"""
improve_alerts.py — добавляет GitHub Markdown callout-блоки в ключевые файлы.
Форматы: > [!NOTE], > [!WARNING], > [!TIP], > [!IMPORTANT].
Анализирует содержимое и вставляет подходящий callout в начало файла.
Запуск: python scripts/improve_alerts.py
"""
import re
from pathlib import Path

ROOT = Path(__file__).parent.parent
DOCS = ROOT / "docs"

MARKER = "<!-- alert-added -->"

SKIP = {
    "README.md", "GLOSSARY.md", "ALERTS.md", "HEALTH.md",
    "VALIDATION.md", "REPORT.md", "ORPHANS.md",
}

# Паттерны для определения типа callout
RISK_KEYWORDS = [
    "риск", "опасност", "нельзя", "не стоит", "осторожн",
    "критическ", "сломает", "проблем", "ограничен", "warning",
]

TIP_KEYWORDS = [
    "рекомендуется", "лучший выбор", "оптимальн", "совет",
    "практический", "tip", "best practice", "рекомендация",
]

IMPORTANT_KEYWORDS = [
    "ключевой", "главный", "важнейший", "приоритет", "первоочередн",
    "critical", "важно", "обязательно", "must",
]

MVP_KEYWORDS = ["mvp", "прототип", "первая итерация", "начать с"]


def detect_callout(text: str) -> tuple[str, str] | None:
    low = text.lower()
    words = text.split()
    if len(words) < 50:
        return None

    risk_score = sum(low.count(k) for k in RISK_KEYWORDS)
    tip_score  = sum(low.count(k) for k in TIP_KEYWORDS)
    imp_score  = sum(low.count(k) for k in IMPORTANT_KEYWORDS)
    mvp_score  = sum(low.count(k) for k in MVP_KEYWORDS)

    # MVP → TIP
    if mvp_score >= 2:
        return ("TIP", "Этот документ описывает MVP-подход. "
                "Начните с него для быстрого прототипа.")

    # Много рисков → WARNING
    if risk_score >= 3 and risk_score > tip_score:
        return ("WARNING", "Документ содержит описание рисков и ограничений. "
                "Изучите их перед принятием архитектурных решений.")

    # Советы → TIP
    if tip_score >= 2 and tip_score >= risk_score:
        return ("TIP", "Документ содержит практические рекомендации "
                "и лучшие практики.")

    # Ключевой документ → IMPORTANT
    if imp_score >= 3:
        return ("IMPORTANT", "Ключевой документ для понимания архитектуры. "
                "Рекомендуется прочитать в первую очередь.")

    return None


def extract_summary(text: str, max_words: int = 25) -> str:
    """Первое значимое предложение из текста."""
    clean = re.sub(r'```.*?```', '', text, flags=re.DOTALL)
    clean = re.sub(r'^#{1,6}.*$', '', clean, flags=re.MULTILINE)
    clean = re.sub(r'[*_`\[\]|>]', '', clean)
    clean = re.sub(r'\s+', ' ', clean).strip()
    sentences = re.split(r'(?<=[.!?])\s+', clean)
    for s in sentences:
        words = s.split()
        if len(words) >= 5:
            return " ".join(words[:max_words])
    return ""


def main():
    print("Добавление callout-блоков...")
    added = 0
    stats = {"NOTE": 0, "TIP": 0, "WARNING": 0, "IMPORTANT": 0}

    # Специальные файлы — всегда NOTE с summary
    special = {
        "01-executive-summary.md": ("IMPORTANT",
            "Главный документ проекта. Начните чтение отсюда."),
        "07-mvp-planning.md": ("TIP",
            "Описывает минимальный прототип — с чего начать реализацию."),
        "09-architectural-gaps.md": ("WARNING",
            "Содержит критические архитектурные пробелы, требующие решения."),
        "06-security-privacy.md": ("WARNING",
            "Политики безопасности и приватности. Обязательны к соблюдению."),
        "12-roadmap.md": ("IMPORTANT",
            "Дорожная карта проекта — план на 12-18 месяцев."),
        "13-contacts.md": ("TIP",
            "Контакты ключевых разработчиков для сотрудничества."),
    }

    import sys
    sys.path.insert(0, str(Path(__file__).parent))
    try:
        from utils_docignore import is_ignored
    except ImportError:
        is_ignored = lambda p: False

    for f in sorted(DOCS.rglob("*.md")):
        if f.name in SKIP:
            continue
        if is_ignored(f):
            continue
        text = f.read_text(encoding="utf-8")
        if MARKER in text:
            continue
        if len(text.split()) < 50:
            continue

        # Проверяем специальные файлы
        callout = special.get(f.name)

        # Иначе — автоопределение
        if callout is None:
            callout = detect_callout(text)

        if callout is None:
            continue

        ctype, cmsg = callout

        # Вставляем после первого H1
        h1_match = re.search(r'^# .+$', text, re.MULTILINE)
        if not h1_match:
            continue

        insert_pos = h1_match.end()
        callout_block = f"\n\n> [!{ctype}]\n> {cmsg}\n\n{MARKER}"

        new_text = text[:insert_pos] + callout_block + text[insert_pos:]
        f.write_text(new_text, encoding="utf-8")
        added += 1
        stats[ctype] += 1

    lines = [
        "# Callout-блоки\n",
        f"Добавлено **{added}** callout-блоков в документы.\n",
        "| Тип | Количество | Назначение |",
        "|-----|------------|------------|",
        f"| `[!NOTE]` | {stats['NOTE']} | Нейтральная заметка |",
        f"| `[!TIP]` | {stats['TIP']} | Практический совет |",
        f"| `[!WARNING]` | {stats['WARNING']} | Предупреждение о риске |",
        f"| `[!IMPORTANT]` | {stats['IMPORTANT']} | Ключевой документ |",
        "\n## Пример синтаксиса\n",
        "```markdown",
        "> [!NOTE]",
        "> Это заметка.",
        "",
        "> [!TIP]",
        "> Практический совет.",
        "",
        "> [!WARNING]",
        "> Предупреждение.",
        "",
        "> [!IMPORTANT]",
        "> Важная информация.",
        "```",
        "\n_Поддерживается в GitHub Markdown с 2023 года._",
    ]

    out = DOCS / "ALERTS.md"
    out.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(f"  wrote: {out.relative_to(ROOT)}")
    print(f"  добавлено callout: {added} "
          f"(TIP={stats['TIP']}, WARNING={stats['WARNING']}, IMPORTANT={stats['IMPORTANT']})")


if __name__ == "__main__":
    main()
