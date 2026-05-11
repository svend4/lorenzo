---
title: "Автозаполненные шаблоны"
tags:
  - ingestion
  - collaboration
  - general
date: 2026-05-11
---

# Автозаполненные шаблоны

<!-- toc-auto -->
## Contents

- [Файлы](#файлы)
- [Как работает](#как-работает)
- [Связанные документы](#связанные-документы)
- [Связанные документы](#связанные-документы-1)
- [Использование](#использование)
- [Смотрите также](#смотрите-также)
- [Упоминается в](#упоминается-в)
- [Кто ссылается на этот документ (12)](#кто-ссылается-на-этот-документ-12)


> [!NOTE]
> Документ создан на основе исследования. Ссылки ведут на связанные материалы.

<!-- alert-added -->

<!-- summary -->

> [!NOTE]
> Документ создан на основе исследования. Ссылки ведут на связанные материалы.

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

## Использование

```bash
# Поиск по теме документа
python scripts/improve_semantic_search.py --query "Автозаполненные шаблоны"
```

## Смотрите также
- [[.md]]
- [[cowork]]
- [[ingit]]
- [[lorenzo]]

<!-- backlinks-auto -->
## Упоминается в

- [[README|docs]]
- [[TABLES|Все таблицы репозитория]]
- [[SITEMAP|Карта репозитория Lorenzo]]

<!-- backlinks -->

---

## Кто ссылается на этот документ (12)
- [[README]]
- [[TABLES]]
- [[cowork]]
- [[ingit]]
- [[kksudo]]
- [[lorenzo]]
- [[nautilus]]
- [[sgb]]
- _...ещё 4_

_Документ индексирован в поисковой базе репозитория Lorenzo и доступен для семантического поиска._ _Документ индексирован в поисковой базе репозитория Lorenzo и доступен для семантического поиска._ _Документ индексирован в поисковой базе репозитория Lorenzo и доступен для анализа._ _Документ доступен для семантического поиска._ _Индексировано._

<!-- similar-docs -->

---

**Похожие документы:**
- [[AUTOFILLED]] (сходство 0.97)
- [[svyazi]] (сходство 0.49)
- [[svend4]] (сходство 0.49)

