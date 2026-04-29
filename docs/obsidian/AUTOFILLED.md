---
title: "Автозаполненные шаблоны"
tags:
  - ingestion
  - collaboration
  - general
date: 2026-04-29
---

# Автозаполненные шаблоны

<!-- summary -->
> _Источники: ENTITIES.md, SCORING.md, NETWORK.md, docs/templates/_
**Проекты:** Svyazi

---
<!-- tags: ingestion, collaboration -->




_Источники: ENTITIES.md, SCORING.md, NETWORK.md, docs/templates/_

**Создано файлов:** 13

## Файлы

- [[.md|`docs/autofilled/components/.md`]]
- [[cowork|`docs/autofilled/components/cowork.md`]]
- [[ingit|`docs/autofilled/components/ingit.md`]]
- [[kksudo|`docs/autofilled/components/kksudo.md`]]
- [[lorenzo|`docs/autofilled/components/lorenzo.md`]]
- [[nautilus|`docs/autofilled/components/nautilus.md`]]
- [[sgb|`docs/autofilled/components/sgb.md`]]
- [[spbmolot|`docs/autofilled/components/spbmolot.md`]]
- [[svend4|`docs/autofilled/components/svend4.md`]]
- [[svyazi|`docs/autofilled/components/svyazi.md`]]
- [[research-summary|`docs/autofilled/research-summary.md`]]

## Как работает

1. Читает шаблоны из `docs/templates/` с плейсхолдерами `{{name}}`
2. Собирает данные: ENTITIES (сущности), SCORING (статус), NETWORK (граф)
3. Заменяет плейсхолдеры реальными данными
4. Сохраняет результаты в `docs/autofilled/`

Повторный запуск перезаписывает файлы актуальными данными.

<!-- related-auto -->
## Связанные документы

- [[README|components]] _45%_
- [[.md|Антропик]] _25%_
- [[cowork]] _25%_
- [[ingit]] _25%_
- [[kksudo]] _25%_
- [[lorenzo]] _25%_
- [[nautilus]] _25%_
- [[sgb]] _25%_
## Связанные документы

- [[VERSION_DIFF|Diff базы знаний между версиями]] _25%_

<!-- see-also -->

---

**Смотрите также:**
- [[.md]]
- [[cowork]]
- [[ingit]]
- [[lorenzo]]

<!-- backlinks-auto -->
## Упоминается в

- [[README|docs]]
- [[TABLES|Все таблицы репозитория]]
- [[SITEMAP|Карта репозитория Lorenzo]]

<!-- similar-docs -->

---

**Похожие документы:**
- [[AUTOFILLED]] (сходство 0.83)
- [[svyazi]] (сходство 0.45)
- [[svend4]] (сходство 0.45)

