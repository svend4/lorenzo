# Скилл: review-docs

## Когда использовать
Когда нужно проверить качество или найти проблемы в документации:
- "Проверь документацию"
- "Что нужно улучшить в docs/?"
- "Есть ли противоречия в документах?"
- "Какие файлы неполные?"

## Алгоритм

1. Прочитай `docs/VALIDATION.md` — список ошибок/предупреждений
2. Прочитай `docs/METRICS.md` — качество каждого файла (65.7/100 сейчас)
3. Прочитай `docs/LLM_GAPS.md` — семантические пробелы (если есть)
4. Прочитай `docs/ORPHANS.md` — несвязанные файлы
5. Прочитай `docs/HEALTH.md` — общее здоровье репозитория

## Что проверять

### Структурные проблемы
```bash
python scripts/improve_validate.py  # ошибки форматирования
python scripts/improve_orphans.py   # несвязанные файлы
python scripts/improve_health.py    # общее здоровье
```

### Семантические проблемы
```bash
python scripts/improve_llm_gaps.py  # LLM-анализ пробелов (требует API ключ)
```

### Метрики качества
```bash
python scripts/improve_metrics.py   # детальные метрики
python scripts/improve_scoring.py   # Go/No-Go скоринг
```

## Формат отчёта о ревью

```markdown
## Результаты ревью docs/

**Статус:** 🟢 GO / 🟡 PARTIAL / 🔴 STOP

### Критические проблемы
- ...

### Улучшения
- ...

### Приоритеты
1. ...
2. ...
```

## Быстрый старт
```bash
python scripts/improve_run_all.py --group quality
```
