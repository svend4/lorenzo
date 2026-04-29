# track-decisions

Отслеживание архитектурных решений (ADR) по теме / в хронологии.

## Когда использовать

- "какие решения по X приняты"
- "история решений по архитектуре"
- "почему мы выбрали Y, а не Z"
- "когда последний раз меняли подход к W"

## Шаги

1. **Прочитать `docs/DECISIONS.md`**
   - Это автогенерированный список из `improve_decisions.py`

2. **Если запрос с темой — отфильтровать**
   ```bash
   grep -B1 -A8 -i "тема" docs/DECISIONS.md
   ```

3. **Если есть формальные ADR — собрать**
   ```bash
   find docs -name "ADR-*.md" -o -name "adr-*.md"
   find docs -path "*decisions*" -name "*.md"
   ```

4. **Хронологический рассказ:**

   ```markdown
   # Решения по теме «X»

   **Найдено:** 7 записей за период 2024-01 — 2026-04

   ## Хронология

   ### 2024-03 — ADR-0001: Выбор векторной БД
   **Статус:** accepted
   **Решение:** Qdrant
   **Обоснование:** open source, Rust, не требует управляемой инфры
   **Файл:** [`docs/svyazi-2-0/decisions/ADR-0001.md`](...)

   ### 2024-09 — ADR-0007: Замена Qdrant на pgvector
   **Статус:** accepted (supersedes ADR-0001)
   **Причина:** не нужна была отдельная БД, проще держать в Postgres
   **Файл:** [`docs/svyazi-2-0/decisions/ADR-0007.md`](...)

   ### 2026-04 — ADR-0023: pgvector + ClickHouse гибрид
   **Статус:** proposed
   **Файл:** [`docs/svyazi-2-0/decisions/ADR-0023.md`](...)
   ```

5. **Идентифицировать паттерн:**
   - Сколько раз меняли решение?
   - Тренд: упрощают или усложняют?
   - Есть ли откаты к предыдущим решениям?

6. **Если запрашивают «почему X а не Y»:**
   - Найти ADR с status=rejected где обсуждалась Y
   - Прочитать секцию «Рассмотренные варианты»

7. **Если запрашивают создать новый ADR:**
   ```bash
   python scripts/improve_template_init.py --type decision-record \
     --slug docs/decisions/ADR-NNNN.md \
     --vars adr_id=ADR-NNNN title="..." status=proposed
   ```

## Антипаттерны
- ❌ Не использовать `DECISIONS.md` как «список замечаний» — это автогенерируемое
- ❌ Не дублировать ADR в нескольких местах (только в `docs/decisions/`)

## Связанные скилы
- [`generate-rfc`](generate-rfc.md) — после ADR может появиться RFC
- [`audit-corpus`](audit-corpus.md) — общий аудит включает свежесть решений
- [`find-contradictions`](find-contradictions.md) — старые решения могут противоречить новым
