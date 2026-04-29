# status

Быстрая сводка текущего состояния проекта Lorenzo без чтения множества файлов.

Когда использовать:
- «какой статус проекта?»
- «что сейчас происходит?»
- «сколько контактов написано?»
- «какой health score?»
- «что дальше делать?»
- «покажи прогресс»

---

## Шаг 1 — Собрать данные параллельно

```bash
grep -m1 "Общий балл\|Средний балл\|Итог" docs/HEALTH.md docs/METRICS.md docs/SCORING.md
python scripts/improve_contact_status.py --list
grep -A2 "Следующий шаг" docs/PROGRESS.md | head -5
```

Если нужны свежие данные (файлы устарели):
```bash
python scripts/improve_run_all.py --only improve_health,improve_metrics,improve_scoring,improve_progress_sync
```

## Шаг 2 — Сформировать ответ

Показать пользователю в таком порядке:

### Метрики качества
| Файл | Балл | Статус |
|------|------|--------|
| HEALTH.md | X/100 | 🟢/🟡/🔴 |
| METRICS.md | X/100 | 🟢/🟡/🔴 |
| SCORING.md | X% | GO/NO-GO |

Пороги: 🟢 ≥80, 🟡 60-79, 🔴 <60

### Контакты
- Всего авторов: N
- Изучено: N
- Написано: N
- Ответили: N

### Milestones
Прочитать из PROGRESS.md раздел `## Ключевые этапы`.

### Следующий шаг
Прочитать из PROGRESS.md раздел `## Следующий шаг`.

---

## Шаг 3 — Уточнить если нужно

Если пользователь хочет подробности по контактам:
```bash
cat docs/CONTACT_PRIORITY.md   # топ авторов по приоритету
```

Если хочет детали по метрикам:
```bash
Read: docs/HEALTH.md
Read: docs/METRICS.md
```

Если хочет что конкретно улучшить:
→ Смотри .claude/skills/improve.md → Ветка F (метрика)
