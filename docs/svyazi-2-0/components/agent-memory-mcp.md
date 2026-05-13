---
state: normalized
---

# agent-memory-mcp + Memory OS

<!-- toc-auto -->
## Contents

- [Описание](#описание)
- [Ключевые компоненты и паттерны](#ключевые-компоненты-и-паттерны)
- [Использование](#использование)
- [Смотрите также](#смотрите-также)
- [Кто ссылается на этот документ (3)](#кто-ссылается-на-этот-документ-3)


> [!NOTE]
> Документ создан на основе исследования. Ссылки ведут на связанные материалы.

<!-- alert-added -->

<!-- summary -->

> [!NOTE]
> Документ создан на основе исследования. Ссылки ведут на связанные материалы.

> - **Автор:** VitaliySemenov / moshael
**Проекты:** Svyazi, agent-memory-mcp

---
<!-- tags: memory, ingestion, architecture, roadmap, collaboration -->




- **Автор:** VitaliySemenov / moshael
- **Источник:** Хабр + GitHub + Хабр citeturn20view16turn15search3turn39view3
- **Лицензия:** для `agent-memory-mcp` — неуточнено; для Memory OS — неуточнено. citeturn15search3turn39view3
- **Maturity:** `agent-memory-mcp` — рабочий OSS; Memory OS — концептуально амбициозный кейс без явного публичного репо в статье. citeturn15search3turn39view3
- **Релевантность к Svyazi‑2.0:** высокая — слой typed memory и governance для более поздних итераций.

## Описание

Typed memory MCP плюс более тяжёлая концепция Memory OS с онтологией, gardener‑loop и bi‑temporal facts.

## Ключевые компоненты и паттерны

- SQLite + WAL
- Typed memories
- Repo / doc search
- Path guard
- Ontology
- Concept loop
- Maintenance contour
- Planner / scout / synthesizer

<!-- see-also -->

---

## Использование

```bash
# Поиск по теме документа
python scripts/improve_semantic_search.py --query "agent memory mcp Memory OS"
```

## Смотрите также
- [memnet](memnet.md)
- [yodoca](yodoca.md)
- [rufler](rufler.md)
- [ngt-memory](ngt-memory.md)


<!-- backlinks -->

---

## Кто ссылается на этот документ (3)
- [authors-by-name](../../glossary/authors-by-name.md)
- [components-by-name](../../glossary/components-by-name.md)
- [README](README.md)

Документ индексирован в базе знаний репозитория. Навигация возможна через семантический поиск и граф концептов репозитория Lorenzo. Материал доступен для семантического поиска, BM25-поиска и навигации через граф концептов. Используйте скрипты группы reports для получения актуальной статистики по разделу. Рекомендуется начинать с основных документов раздела и переходить к деталям через внутренние ссылки. Все связанные документы доступны через граф концептов и поисковый индекс репозитория Lorenzo. Документ индексирован в базе знаний репозитория.

<!-- similar-docs -->

---

**Похожие документы:**
- [agent-memory-mcp](../../obsidian/svyazi-2-0/components/agent-memory-mcp.md) (сходство 0.98)
- [rufler](rufler.md) (сходство 0.54)
- [yodoca](yodoca.md) (сходство 0.54)

