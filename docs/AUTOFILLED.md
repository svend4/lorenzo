# Автозаполненные шаблоны

<!-- summary -->
> _Источники: ENTITIES.md, SCORING.md, NETWORK.md, docs/templates/_
**Проекты:** Svyazi

---
<!-- tags: ingestion, collaboration -->




_Источники: ENTITIES.md, SCORING.md, NETWORK.md, docs/templates/_

**Создано файлов:** 13

## Файлы

- [`docs/autofilled/components/.md`](docs/autofilled/components/.md)
- [`docs/autofilled/components/cowork.md`](docs/autofilled/components/cowork.md)
- [`docs/autofilled/components/ingit.md`](docs/autofilled/components/ingit.md)
- [`docs/autofilled/components/kksudo.md`](docs/autofilled/components/kksudo.md)
- [`docs/autofilled/components/lorenzo.md`](docs/autofilled/components/lorenzo.md)
- [`docs/autofilled/components/nautilus.md`](docs/autofilled/components/nautilus.md)
- [`docs/autofilled/components/sgb.md`](docs/autofilled/components/sgb.md)
- [`docs/autofilled/components/spbmolot.md`](docs/autofilled/components/spbmolot.md)
- [`docs/autofilled/components/svend4.md`](docs/autofilled/components/svend4.md)
- [`docs/autofilled/components/svyazi.md`](docs/autofilled/components/svyazi.md)
- [`docs/autofilled/research-summary.md`](docs/autofilled/research-summary.md)

## Как работает

1. Читает шаблоны из `docs/templates/` с плейсхолдерами `{{name}}`
2. Собирает данные: ENTITIES (сущности), SCORING (статус), NETWORK (граф)
3. Заменяет плейсхолдеры реальными данными
4. Сохраняет результаты в `docs/autofilled/`

Повторный запуск перезаписывает файлы актуальными данными.

<!-- see-also -->

---

**Смотрите также:**
- [CONCEPT_GRAPH](docs/CONCEPT_GRAPH.md)
- [WORD_CLOUD](docs/WORD_CLOUD.md)
- [NETWORK](docs/NETWORK.md)
- [nlaik](docs/contacts/nlaik.md)

