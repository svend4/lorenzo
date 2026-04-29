# Автозаполненные шаблоны

<!-- summary -->
> _Источники: ENTITIES.md, SCORING.md, NETWORK.md, docs/templates/_
**Проекты:** Svyazi

---
<!-- tags: ingestion, collaboration -->




_Источники: ENTITIES.md, SCORING.md, NETWORK.md, docs/templates/_

**Создано файлов:** 13

## Файлы

- [`docs/autofilled/components/.md`](autofilled/components/.md)
- [`docs/autofilled/components/cowork.md`](autofilled/components/cowork.md)
- [`docs/autofilled/components/ingit.md`](autofilled/components/ingit.md)
- [`docs/autofilled/components/kksudo.md`](autofilled/components/kksudo.md)
- [`docs/autofilled/components/lorenzo.md`](autofilled/components/lorenzo.md)
- [`docs/autofilled/components/nautilus.md`](autofilled/components/nautilus.md)
- [`docs/autofilled/components/sgb.md`](autofilled/components/sgb.md)
- [`docs/autofilled/components/spbmolot.md`](autofilled/components/spbmolot.md)
- [`docs/autofilled/components/svend4.md`](autofilled/components/svend4.md)
- [`docs/autofilled/components/svyazi.md`](autofilled/components/svyazi.md)
- [`docs/autofilled/research-summary.md`](autofilled/research-summary.md)

## Как работает

1. Читает шаблоны из `docs/templates/` с плейсхолдерами `{{name}}`
2. Собирает данные: ENTITIES (сущности), SCORING (статус), NETWORK (граф)
3. Заменяет плейсхолдеры реальными данными
4. Сохраняет результаты в `docs/autofilled/`

Повторный запуск перезаписывает файлы актуальными данными.

<!-- related-auto -->
## Связанные документы

- [Diff базы знаний между версиями](VERSION_DIFF.md) _25%_

<!-- see-also -->

---

**Смотрите также:**
- [.md](autofilled/components/.md)
- [cowork](autofilled/components/cowork.md)
- [ingit](autofilled/components/ingit.md)
- [lorenzo](autofilled/components/lorenzo.md)

