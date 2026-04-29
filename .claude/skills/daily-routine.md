# daily-routine

Ежедневная процедура: аудит → противоречия → пробелы → отчёт.

## Когда использовать

- "ежедневный обход"
- "что важного за день"
- "daily routine"
- "проверь репо в начале дня"

## Композиция

Этот скилл оркестрирует другие:
1. [`audit-corpus`](audit-corpus.md)
2. [`find-contradictions`](find-contradictions.md)
3. [`find-gaps`](find-gaps.md)
4. [`status`](status.md) — для контактов

## Шаги

1. **Запустить аудит**
   - Применить скилл `audit-corpus`
   - Если HEALTH < 70: остановиться, сообщить пользователю «нужны ремонтные работы»

2. **Сводка изменений со вчера**
   ```bash
   git log --since="1 day ago" --pretty=format:"%h %s"
   python scripts/improve_digest_auto.py --days 1
   ```

3. **Новые противоречия**
   - Применить `find-contradictions` без topic
   - Сравнить с `docs/CONTRADICTIONS.md` вчерашнего состояния (через `git show HEAD@{1.day.ago}:docs/CONTRADICTIONS.md`)
   - Новые → создать contradiction-record для каждого

4. **Новые пробелы**
   - Применить `find-gaps`
   - Топ-3 показать пользователю

5. **Контакты, требующие действий**
   ```bash
   python scripts/improve_contact_status.py --list
   ```
   - Кому отвечал, ждал ответа > 7 дней?
   - Кто в статусе `studied` уже неделю — пора писать?

6. **Финальный отчёт**

   ```markdown
   # Daily routine: [дата]

   ## Балл репо: XX/100 ([↑ / ↓])

   ## За сутки
   - Коммитов: N
   - Новых файлов: M
   - Изменённых: K

   ## ⚠️ Новое требующее внимания
   - 1 новое противоречие: …
   - 2 новых пробела: …

   ## Контакты
   - Ждут ответа > 7 дней: [список]
   - Готовы к follow-up: [список]

   ## План на день (предложение)
   1. …
   2. …
   ```

## Опционально: автозапуск

Можно настроить как cron / systemd timer:
```bash
# .claude/hooks/daily.sh
python scripts/improve_run_all.py --group quality --smart
```

## Связанные скилы
- [`weekly-review`](weekly-review.md) — недельная версия
- [`new-research`](new-research.md) — переход от daily к research
