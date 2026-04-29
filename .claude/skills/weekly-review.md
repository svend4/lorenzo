# weekly-review

Еженедельное ревью: дайджест + аудит + ретро + план.

## Когда использовать

- "weekly review"
- "пятничный обход"
- "еженедельный отчёт"
- "что за неделю произошло"

## Композиция

1. [`audit-corpus`](audit-corpus.md)
2. [`track-decisions`](track-decisions.md)
3. [`find-gaps`](find-gaps.md)
4. Создание `weekly-digest.md` + `retrospective.md` + `kpi-snapshot.md`

## Шаги

1. **Сгенерировать дайджест**
   ```bash
   python scripts/improve_digest_weekly.py
   python scripts/improve_digest_auto.py --days 7
   ```

2. **Сделать аудит**
   - Применить `audit-corpus`
   - Сравнить балл с прошлой неделей (`docs/KPI_HISTORY.md`)

3. **Прогон quality-группы (опционально)**
   ```bash
   python scripts/improve_run_all.py --group quality --smart
   ```

4. **Решения за неделю**
   - Применить `track-decisions`
   - Новые ADR? Изменения статуса существующих?

5. **Контакты за неделю**
   ```bash
   git log --since="1 week ago" -- docs/contacts/
   ```
   - Кому написали
   - Кто ответил

6. **Создать KPI snapshot**
   ```bash
   python scripts/improve_kpi_snapshot.py
   python scripts/improve_template_init.py --type kpi-snapshot \
     --slug docs/kpi-snapshots/$(date +%Y-W%V).md \
     --vars period=weekly
   ```

7. **Создать weekly-digest**
   ```bash
   python scripts/improve_template_init.py --type weekly-digest \
     --slug docs/digests/$(date +%Y-W%V).md
   ```

8. **Заполнить дайджест:**
   - TL;DR — топ-5 событий
   - Что сделано (контент / скрипты / коммуникации)
   - Метрики (с дельтой)
   - Решения недели
   - Открытые вопросы
   - План на следующую

9. **Создать retrospective**
   ```bash
   python scripts/improve_template_init.py --type retrospective \
     --slug docs/retrospectives/$(date +%Y-W%V).md
   ```

10. **Заполнить ретро:**
   - ✅ Что прошло хорошо
   - ❌ Что плохо
   - 💡 Что узнали
   - Action items на следующую неделю

11. **Обновить INDEX.md** ссылками на новые артефакты

## Чеклист недельного ревью

- [ ] Сгенерирован weekly-digest
- [ ] Сгенерирован kpi-snapshot
- [ ] Сделана retrospective
- [ ] Балл HEALTH ≥ прошлой недели?
- [ ] Битых ссылок ≤ прошлой недели?
- [ ] Action items предыдущей недели закрыты или перенесены?
- [ ] Запланированы action items на следующую неделю?

## Связанные скилы
- [`daily-routine`](daily-routine.md) — ежедневная версия
- [`audit-corpus`](audit-corpus.md) — компонент еженедельного
- [`track-decisions`](track-decisions.md) — компонент
