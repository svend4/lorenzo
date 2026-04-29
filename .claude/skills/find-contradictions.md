# find-contradictions

Поиск противоречий между документами по теме или в целом.

## Когда использовать

- "где противоречия про X"
- "что в моих документах конфликтует"
- "проверь нет ли несостыковок про Y"
- "найди противоречивые утверждения"

## Шаги

1. **Прочитать `docs/CONTRADICTIONS.md`**
   - Если файла нет — `python scripts/improve_contradiction_check.py` сначала
   - Иначе сразу идти на шаг 2

2. **Если запрос с темой — отфильтровать**
   ```bash
   grep -B2 -A8 "тема" docs/CONTRADICTIONS.md
   ```

3. **Углубиться в конкретное противоречие**
   - Для каждого выявленного — прочитать оба источника
   - Проверить: реально противоречат, или контексты разные?

4. **Классифицировать**
   - `low` — формулировки, не суть (пример: «memory» vs «память»)
   - `medium` — нюансы (пример: «всегда X» vs «обычно X»)
   - `high` — реальный конфликт (пример: «Yodoca под MIT» vs «Yodoca под Apache»)
   - `critical` — архитектурный конфликт (несовместимые подходы)

5. **Предложить разрешение**

   Использовать шаблон `contradiction-record.md`:
   ```bash
   python scripts/improve_template_init.py --type contradiction-record \
     --slug docs/contradictions/CONTRA-NNNN.md \
     --vars title="..." severity=medium
   ```

   В файле зафиксировать: оба источника, в чём конфликт, 4 интерпретации, предложение.

6. **Если решение очевидно — обновить источники**
   - Обновить устаревший файл
   - Добавить запись в `DECISIONS.md`
   - Перезапустить `improve_contradiction_check.py` для верификации

## Пример

Пользователь: «где противоречия про CRDT»

```bash
grep -B1 -A5 -i "crdt" docs/CONTRADICTIONS.md
```

Если найдено противоречие, читаю оба файла и формирую отчёт:
> **CONTRA-0007: CRDT в hot vs cold path**
> - **A:** [`docs/05-habr-projects/memory/yodoca.md`](...) — «CRDT использовать только в hot path»
> - **B:** [`docs/03-technology-combinations/combinations/20-hybrid.md`](...) — «CRDT для cold синхронизации»
> - **Severity:** medium
> - **Интерпретация:** контексты разные. Yodoca — про in-process; combinations 20 — про cross-DC.
> - **Действие:** добавить разделение в глоссарий «CRDT scope».

## Связанные скилы
- [`search`](search.md) — найти источники до проверки
- [`compare`](compare.md) — детальное сравнение двух утверждений
- [`audit-corpus`](audit-corpus.md) — общий аудит включает противоречия
