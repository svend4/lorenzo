# find-cinderella

Поиск «Cinderella Syndrome» — ценные проекты/идеи без видимости.

## Когда использовать

- "у кого Cinderella Syndrome в репо"
- "какие хорошие проекты недополучают внимания"
- "кому помочь усилить голос"
- "voiceless contributors"

## Контекст

«Cinderella Syndrome» (из `docs/nautilus/representative-agent-layer-en/`) — паттерн, когда квалифицированный автор не получает голоса в индустрии не из-за качества работы, а из-за:
- неудобной платформы (Habr вместо arxiv)
- языка (русский, не английский)
- отсутствия PR-канала
- скромности

Цель Representative Agent Layer — дать таким голос.

## Шаги

1. **Прочитать ключевые источники**
   ```bash
   find docs/nautilus -name "*representative*" -o -name "*cinderella*"
   ```

2. **Применить критерии Cinderella**

   | Признак | Где искать |
   |---|---|
   | Высокое тех. качество | `docs/05-habr-projects/`, `ENTITIES.md` |
   | Низкая видимость | мало звёзд / читателей |
   | Не на английском | RU-проекты в monorepo |
   | Малое community feedback | мало комментариев / issues |
   | Зрелый, но неизвестный | возраст репо vs популярность |

3. **Скрипт-поиск кандидатов**
   ```bash
   python scripts/improve_faceted_search.py --type projects --section "05-habr-projects"
   # Затем для каждого:
   python scripts/improve_passage_retrieval.py --query "<проект>" --top 5
   ```

4. **Шортлист с обоснованием**

   ```markdown
   # Cinderella кандидаты

   ## Топ-N проектов с потенциалом

   ### 1. [Проект X] — автор @handle
   - **Технические достоинства:** [конкретно]
   - **Текущая видимость:** [низкая, причины]
   - **Что нужно:** перевод / PR-канал / интеграция
   - **Связь с Lorenzo:** [как помочь / как использовать]
   - **Файл контакта:** [`docs/contacts/<slug>.md`]
   ```

5. **План помощи каждому:**
   - Краткосрочно: связаться, предложить collaboration
   - Среднесрочно: review/feedback, перевод материалов
   - Долгосрочно: интеграция в Lorenzo как Representative Agent

6. **Создать research-note для каждого:**
   ```bash
   python scripts/improve_template_init.py --type research-note \
     --slug docs/research/cinderella-<slug>.md \
     --vars title="Cinderella анализ: <проект>"
   ```

## Связанные скилы
- [`propose-collaboration`](propose-collaboration.md) — следующий шаг
- [`write-contact`](write-contact.md) — связаться с автором
- [`evaluate-tech`](evaluate-tech.md) — оценить тех. качество
