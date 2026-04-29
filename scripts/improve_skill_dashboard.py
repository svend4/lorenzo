"""
improve_skill_dashboard.py — статистика использования и оценок скилов.

Читает .claude/skill_metrics.jsonl и формирует docs/SKILL_DASHBOARD.md:
  - какие скилы используются чаще
  - средняя оценка по 4 осям
  - тренд за последние N дней
  - топ feedback'ов
  - неиспользуемые скилы (есть в .claude/skills/, но не в логе)

Запуск:
    python scripts/improve_skill_dashboard.py
"""
import json
import sys
from collections import Counter, defaultdict
from datetime import date, datetime, timedelta
from pathlib import Path

ROOT = Path(__file__).parent.parent
LOG_PATH = ROOT / ".claude" / "skill_metrics.jsonl"
SKILLS_DIR = ROOT / ".claude" / "skills"
OUT = ROOT / "docs" / "SKILL_DASHBOARD.md"


def main():
    all_skills = sorted(p.stem for p in SKILLS_DIR.glob('*.md')) if SKILLS_DIR.exists() else []

    if not LOG_PATH.exists():
        OUT.write_text(
            f"# Skill Dashboard\n\n_Обновлено: {date.today().isoformat()}_\n\n"
            f"_Лог метрик не найден ({LOG_PATH.relative_to(ROOT)})._\n\n"
            f"**Скилов в системе:** {len(all_skills)}\n\n"
            f"Чтобы начать сбор метрик, используйте `evaluate_skill` MCP-инструмент.\n",
            encoding='utf-8'
        )
        print(f"→ {OUT.relative_to(ROOT)} (без метрик)")
        return 0

    entries = []
    for line in LOG_PATH.read_text(encoding='utf-8').splitlines():
        try:
            entries.append(json.loads(line))
        except json.JSONDecodeError:
            continue

    by_skill: dict[str, list] = defaultdict(list)
    for e in entries:
        by_skill[e.get('skill', 'unknown')].append(e)

    # Используются за последние 7/30 дней
    now = datetime.now()
    last_7 = Counter()
    last_30 = Counter()
    for e in entries:
        try:
            ts = datetime.fromisoformat(e.get('ts', ''))
        except ValueError:
            continue
        delta = now - ts
        if delta <= timedelta(days=7):
            last_7[e.get('skill', '')] += 1
        if delta <= timedelta(days=30):
            last_30[e.get('skill', '')] += 1

    used = set(by_skill)
    unused = [s for s in all_skills if s not in used]

    lines = ['# Skill Dashboard\n', f'_Обновлено: {date.today().isoformat()}_\n']
    lines.append(f'**Всего записей:** {len(entries)}')
    lines.append(f'**Использовано скилов:** {len(used)} / {len(all_skills)}')
    lines.append(f'**За 7 дней:** {sum(last_7.values())} вызовов')
    lines.append(f'**За 30 дней:** {sum(last_30.values())} вызовов')

    # Топ-15 по использованию
    lines.append('\n## Топ-15 по использованию (всего)\n')
    lines.append('| Скилл | Вызовов | За 7д | За 30д | Avg helpful | Avg complete |')
    lines.append('|-------|---------|-------|--------|-------------|--------------|')
    top = sorted(by_skill.items(), key=lambda x: -len(x[1]))[:15]
    for skill, items in top:
        helpful_vals = [it['scores'].get('helpful') for it in items
                        if isinstance(it.get('scores'), dict) and 'helpful' in it['scores']]
        complete_vals = [it['scores'].get('complete') for it in items
                         if isinstance(it.get('scores'), dict) and 'complete' in it['scores']]
        avg_h = f"{sum(helpful_vals)/len(helpful_vals):.1f}" if helpful_vals else "—"
        avg_c = f"{sum(complete_vals)/len(complete_vals):.1f}" if complete_vals else "—"
        lines.append(f"| `{skill}` | {len(items)} | {last_7.get(skill, 0)} | {last_30.get(skill, 0)} | {avg_h} | {avg_c} |")

    # Низкие оценки
    low_scores = []
    for skill, items in by_skill.items():
        for it in items:
            scores = it.get('scores', {})
            if not isinstance(scores, dict):
                continue
            avg = sum(scores.values()) / len(scores) if scores else 0
            if 0 < avg < 3:
                low_scores.append((avg, skill, it.get('feedback', ''), it.get('ts', '')))
    if low_scores:
        lines.append('\n## Низкие оценки (avg < 3)\n')
        for avg, skill, fb, ts in sorted(low_scores)[:10]:
            lines.append(f"- `{skill}` ({ts}): avg={avg:.1f}")
            if fb:
                lines.append(f"  > {fb[:200]}")

    # Неиспользуемые
    if unused:
        lines.append(f'\n## Неиспользованные скилы ({len(unused)})\n')
        for s in unused:
            lines.append(f"- `{s}`")

    # Последние feedback'и
    feedbacks = [(e['ts'], e['skill'], e['feedback'])
                 for e in entries if e.get('feedback')][-10:]
    if feedbacks:
        lines.append('\n## Последние feedback\n')
        for ts, skill, fb in feedbacks:
            lines.append(f"- `{ts}` `{skill}`: {fb[:200]}")

    OUT.write_text('\n'.join(lines) + '\n', encoding='utf-8')
    print(f"→ {OUT.relative_to(ROOT)}")
    print(f"  записей: {len(entries)}, скилов в логе: {len(used)}, неиспользованных: {len(unused)}")
    return 0


if __name__ == '__main__':
    sys.exit(main())
