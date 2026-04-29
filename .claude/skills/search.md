# search

Полнотекстовый поиск по базе знаний Lorenzo.

## Когда использовать

Когда пользователь хочет найти что-то в корпусе:
- "найди про X"
- "что есть о Y"
- "где упоминается Z"
- "поиск по теме N"
- "файлы про K"

## Шаги

1. **Понять запрос**
   - Извлечь ключевые слова (термины, имена проектов, авторов)
   - Если есть ограничения (раздел, тип файла, период) — учесть

2. **Выбрать стратегию поиска**

   | Запрос | Инструмент |
   |---|---|
   | Точное слово/фраза | `grep -r "термин" docs/ --include="*.md"` |
   | Тематический поиск | `python scripts/improve_faceted_search.py --query "X"` |
   | Поиск по абзацам с ранжированием | `python scripts/improve_passage_retrieval.py --query "X" --top 10` |
   | Сходство с темой | `python scripts/improve_reading_list.py --query "X" --top 15` |
   | По именованной сущности | `python scripts/improve_faceted_search.py --entity "AgentFS"` |
   | По типу сущности | `python scripts/improve_faceted_search.py --type projects` |

3. **Выполнить поиск**
   - Запустить выбранный инструмент
   - Если `passages.json` отсутствует — сначала `python scripts/improve_passage_retrieval.py --index`

4. **Обогатить результаты**
   - Для топ-3 результатов прочитать первые 30 строк каждого файла
   - Подтянуть теги через `<!-- tags: ... -->`
   - Связать с глоссарием: `docs/glossary/components-by-name.md`

5. **Представить ответ**
   - Структура: «Найдено N документов» + ранжированный список
   - Каждый результат: путь, title, 1-2 предложения релевантного контекста
   - Если 0 результатов — предложить близкие термины из `docs/CONCEPTS.md`

## Шаблон ответа

```markdown
**Найдено: N документов по запросу «X»**

1. [`docs/path/file.md`](docs/path/file.md) — [title]
   _[1-2 предложения релевантного контекста]_
   Теги: tag1, tag2

2. [`docs/path/file2.md`](docs/path/file2.md) — [title]
   _[контекст]_

**Близкие темы:** [тема1], [тема2]

**Дальнейшие шаги:**
- Уточнить запрос: ...
- Расширить: `python scripts/improve_reading_list.py --query "...."`
```

## Пример

Пользователь: «найди про forensic RAG»

```bash
python scripts/improve_passage_retrieval.py --query "forensic RAG" --top 10
```

Ответ:
> **Найдено: 7 документов по запросу «forensic RAG»**
>
> 1. [`docs/svyazi-2-0/architecture/forensic-rag.md`](...) — Forensic RAG architecture
>    _Использует liteparse + bounding box для page-level evidence_
>    Теги: rag, evidence, legal
>
> ...

## Связанные скилы
- [`summarize`](summarize.md) — после поиска можно резюмировать найденные документы
- [`compare`](compare.md) — сравнить найденные подходы
