# generate-rfc

Создание RFC-документа по теме с подтягиванием контекста из корпуса.

## Когда использовать

- "напиши RFC по X"
- "оформи спецификацию для Y"
- "создай протокол для Z"
- "формализуй идею в RFC"

## Шаги

1. **Уточнить scope**
   - Тема одной строкой
   - Какую проблему RFC решает
   - Кто аудитория (внутренние авторы / open-source / коммерческие)

2. **Собрать контекст**
   ```bash
   # Поиск релевантных документов
   python scripts/improve_passage_retrieval.py --query "тема RFC" --top 15

   # Связанные ADR
   grep -i "тема" docs/DECISIONS.md
   ```

3. **Подтянуть существующие RFC**
   ```bash
   find docs -name "*rfc*" -o -name "RFC-*"
   find docs/nautilus/npp-v1-1 -name "*.md"  # пример формата
   ```

4. **Создать каркас**

   ```bash
   python scripts/improve_template_init.py --type rfc \
     --slug docs/rfcs/RFC-NNNN.md \
     --vars rfc_id=RFC-NNNN title="..." authors='["имя"]' status=draft
   ```

5. **Заполнить секции**

   | Секция | Источник данных |
   |---|---|
   | Abstract | синтез от пользователя или из релевантных источников |
   | Motivation | из `CONTENT_GAPS.md` или существующих ADR |
   | Specification | основная работа автора |
   | Architecture | mermaid-схема + ссылки на компоненты |
   | Compatibility | из `DEPENDENCY_MAP.md` |
   | Security | из существующих ADR |
   | References | из `CITATION_INDEX.md` |

6. **Связать с корпусом**
   - Добавить ссылки на компоненты в `docs/svyazi-2-0/components/`
   - Если есть подобный RFC в `docs/nautilus/` — отметить связь
   - Создать ADR об принятии RFC: `python scripts/improve_template_init.py --type decision-record`

7. **Валидация**
   ```bash
   python scripts/improve_validate_templates.py --file docs/rfcs/RFC-NNNN.md
   ```

8. **Опубликовать**
   - Обновить `docs/INDEX.md` — добавить ссылку
   - Обновить `docs/CHANGELOG.md`

## Антипаттерны

- ❌ RFC без motivation — никто не поймёт зачем
- ❌ RFC без open questions — значит не подумали
- ❌ RFC без change log — невозможно отследить эволюцию
- ❌ Один автор без референсов — не похоже на RFC, скорее заметка

## Связанные скилы
- [`search`](search.md) — собрать контекст
- [`compare`](compare.md) — сопоставить с существующими RFC
- [`track-decisions`](track-decisions.md) — связать с ADR
