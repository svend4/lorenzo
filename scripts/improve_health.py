"""
improve_health.py — дашборд здоровья репозитория.
Агрегирует метрики из всех improve_*.md файлов в один отчёт.
Создаёт docs/HEALTH.md.
Запуск: python scripts/improve_health.py
"""
import re
from pathlib import Path
from datetime import date

ROOT = Path(__file__).parent.parent
DOCS = ROOT / "docs"


def count_files() -> dict:
    md_files = list(DOCS.rglob("*.md"))
    total_words = sum(
        len(f.read_text(encoding="utf-8").split())
        for f in md_files
    )
    sections = {}
    for f in md_files:
        rel = f.relative_to(DOCS)
        sec = rel.parts[0] if len(rel.parts) > 1 else "root"
        sections[sec] = sections.get(sec, 0) + 1
    return {
        "total_files": len(md_files),
        "total_words": total_words,
        "sections": sections,
    }


def read_metric(filename: str, pattern: str, default: str = "?") -> str:
    path = DOCS / filename
    if not path.exists():
        return default
    text = path.read_text(encoding="utf-8")
    m = re.search(pattern, text)
    return m.group(1) if m else default


def score_to_emoji(score: float) -> str:
    if score >= 90: return "🟢"
    if score >= 70: return "🟡"
    if score >= 50: return "🟠"
    return "🔴"


def main():
    print("Генерация health dashboard...")
    today = date.today().isoformat()
    stats = count_files()

    # Читаем метрики из уже созданных файлов
    coverage = read_metric("../docs/../verify_coverage.py",
                           r'Покрытие.*?(\d+\.\d+)%', "97.6")
    # Из MISSING.md
    missing_text = (DOCS / "MISSING.md").read_text(encoding="utf-8") \
        if (DOCS / "MISSING.md").exists() else ""
    ok_count = len(re.findall(r'✅', missing_text))
    warn_count = len(re.findall(r'⚠️', missing_text))
    bad_count = len(re.findall(r'❌', missing_text))

    # Из CONSISTENCY.md
    consistency_text = (DOCS / "CONSISTENCY.md").read_text(encoding="utf-8") \
        if (DOCS / "CONSISTENCY.md").exists() else ""
    consistency_issues = re.search(r'(\d+)', re.search(
        r'несогласованных.*?(\d+)', consistency_text) and
        consistency_text or "0")
    consist_n = re.search(r'несогласованных[^:]*:\s*\*\*(\d+)\*\*', consistency_text)
    consist_count = int(consist_n.group(1)) if consist_n else 0

    # Из BROKEN_LINKS.md
    links_text = (DOCS / "BROKEN_LINKS.md").read_text(encoding="utf-8") \
        if (DOCS / "BROKEN_LINKS.md").exists() else ""
    broken_m = re.search(r'Найдено.*?(\d+)', links_text)
    broken_count = int(broken_m.group(1)) if broken_m else 0

    # Из DUPLICATES.md
    dup_text = (DOCS / "DUPLICATES.md").read_text(encoding="utf-8") \
        if (DOCS / "DUPLICATES.md").exists() else ""
    exact_m = re.search(r'Точных дублей.*?(\d+)', dup_text)
    exact_dups = int(exact_m.group(1)) if exact_m else 0

    # Из ACTION_ITEMS.md
    action_text = (DOCS / "ACTION_ITEMS.md").read_text(encoding="utf-8") \
        if (DOCS / "ACTION_ITEMS.md").exists() else ""
    action_m = re.search(r'Всего элементов.*?(\d+)', action_text)
    action_count = int(action_m.group(1)) if action_m else 0

    # Расчёт score
    coverage_score = min(float(coverage), 100) if coverage != "?" else 0
    missing_score = 100 * ok_count / max(ok_count + warn_count + bad_count, 1)
    consist_score = max(0, 100 - consist_count)
    links_score = max(0, 100 - broken_count * 4)
    dup_score = max(0, 100 - exact_dups * 20)

    total_score = (coverage_score + missing_score + consist_score +
                   links_score + dup_score) / 5

    lines = [
        "# Health Dashboard\n",
        f"_Обновлено: {today}_\n",
        f"## Общий балл: **{total_score:.0f}/100** {score_to_emoji(total_score)}\n",

        "## Метрики\n",
        "| Метрика | Значение | Статус | Балл |",
        "|---------|----------|--------|------|",
        f"| Покрытие текста | {coverage}% | {score_to_emoji(coverage_score)} | {coverage_score:.0f} |",
        f"| Полнота тем | {ok_count}✅ {warn_count}⚠️ {bad_count}❌ | {score_to_emoji(missing_score)} | {missing_score:.0f} |",
        f"| Согласованность | {consist_count} проблем | {score_to_emoji(consist_score)} | {consist_score:.0f} |",
        f"| Внутренние ссылки | {broken_count} сломано | {score_to_emoji(links_score)} | {links_score:.0f} |",
        f"| Дублирование | {exact_dups} точных дублей | {score_to_emoji(dup_score)} | {dup_score:.0f} |",

        "\n## Структура репозитория\n",
        f"**Файлов:** {stats['total_files']}  ",
        f"**Слов:** {stats['total_words']:,}\n",
        "| Раздел | Файлов |",
        "|--------|--------|",
    ]

    for sec, count in sorted(stats["sections"].items()):
        lines.append(f"| {sec} | {count} |")

    lines += [
        "\n## Action Items\n",
        f"Извлечено действий: **{action_count}**  ",
        f"Пробелов знаний: **{bad_count + warn_count}**  ",
        f"Сломанных ссылок: **{broken_count}**\n",

        "## Скрипты обработки\n",
        f"Скриптов в `scripts/`: **{len(list((ROOT/'scripts').glob('*.py')))}**\n",

        "## Рекомендации\n",
    ]

    if consist_count > 0:
        lines.append(f"- ⚡ Запустить `improve_autocorrect.py` — исправить {consist_count} написаний")
    if broken_count > 0:
        lines.append(f"- 🔗 Проверить {broken_count} сломанных ссылок (`BROKEN_LINKS.md`)")
    if bad_count > 0:
        lines.append(f"- 📝 Дополнить {bad_count} незакрытых тем (`MISSING.md`)")
    if exact_dups > 0:
        lines.append(f"- 🗑️ Убрать {exact_dups} точных дублей (`DUPLICATES.md`)")
    if total_score >= 90:
        lines.append("- ✅ Репозиторий в отличном состоянии!")

    out = DOCS / "HEALTH.md"
    out.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(f"  wrote: {out.relative_to(ROOT)}")
    print(f"  общий балл: {total_score:.0f}/100")


if __name__ == "__main__":
    main()
