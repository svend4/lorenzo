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

- [components](autofilled/components/README.md) _45%_
- [Антропик](autofilled/components/.md) _25%_
- [Cowork](autofilled/components/cowork.md) _25%_
- [ingit](autofilled/components/ingit.md) _25%_
- [kksudo](autofilled/components/kksudo.md) _25%_
- [Lorenzo](autofilled/components/lorenzo.md) _25%_
- [Nautilus](autofilled/components/nautilus.md) _25%_
- [SGB](autofilled/components/sgb.md) _25%_
## Связанные документы

- [Diff базы знаний между версиями](VERSION_DIFF.md) _25%_

<!-- see-also -->

---

## Использование

```bash
# Поиск по теме документа
python scripts/improve_semantic_search.py --query "Автозаполненные шаблоны"
```

## Смотрите также
- [.md](autofilled/components/.md)
- [cowork](autofilled/components/cowork.md)
- [ingit](autofilled/components/ingit.md)
- [lorenzo](autofilled/components/lorenzo.md)

<!-- backlinks-auto -->
## Упоминается в

- [docs](README.md)
- [Все таблицы репозитория](TABLES.md)
- [Карта репозитория Lorenzo](SITEMAP.md)

<!-- backlinks -->

---

## Кто ссылается на этот документ (12)
- [README](README.md)
- [TABLES](TABLES.md)
- [cowork](autofilled/components/cowork.md)
- [ingit](autofilled/components/ingit.md)
- [kksudo](autofilled/components/kksudo.md)
- [lorenzo](autofilled/components/lorenzo.md)
- [nautilus](autofilled/components/nautilus.md)
- [sgb](autofilled/components/sgb.md)
- _...ещё 4_

_Документ индексирован в поисковой базе репозитория Lorenzo и доступен для семантического поиска._ _Документ индексирован в поисковой базе репозитория Lorenzo и доступен для семантического поиска._ _Документ индексирован в поисковой базе репозитория Lorenzo и доступен для анализа._ _Документ доступен для семантического поиска._ _Индексировано._

<!-- similar-docs -->

---

**Похожие документы:**
- [AUTOFILLED](obsidian/AUTOFILLED.md) (сходство 0.97)
- [svyazi](autofilled/components/svyazi.md) (сходство 0.49)
- [svend4](autofilled/components/svend4.md) (сходство 0.49)

