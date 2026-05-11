# Yodoca

<!-- toc-auto -->
## Contents

- [Описание](#описание)
- [Ключевые компоненты и паттерны](#ключевые-компоненты-и-паттерны)
- [Использование](#использование)
- [Смотрите также](#смотрите-также)
- [Кто ссылается на этот документ (4)](#кто-ссылается-на-этот-документ-4)


> [!NOTE]
> Документ создан на основе исследования. Ссылки ведут на связанные материалы.

<!-- alert-added -->

<!-- summary -->

> [!NOTE]
> Документ создан на основе исследования. Ссылки ведут на связанные материалы.

> - **Источник:** Хабр + GitHub citeturn38view7turn21view0turn21view1turn18search1
**Проекты:** Svyazi, Yodoca

---
<!-- tags: memory, ingestion, architecture, self-improvement, collaboration -->




- **Автор:** VitalyOborin
- **Источник:** Хабр + GitHub citeturn38view7turn21view0turn21view1turn18search1
- **Лицензия:** **Apache 2.0**. citeturn18search1
- **Maturity:** активный OSS. citeturn18search1
- **Релевантность к Svyazi‑2.0:** очень высокая — лучший слой для nightly consolidation и controlled forgetting.

## Описание

Локальный self‑evolving AI assistant с долговременной памятью и ночной консолидацией.

## Ключевые компоненты и паттерны

- Hot / slow path
- Private write‑path consolidator
- `is_session_consolidated`
- Ebbinghaus decay
- Causal edges
- Proactive memory

<!-- see-also -->

---

## Использование

```bash
# Поиск по теме документа
python scripts/improve_semantic_search.py --query "Yodoca"
```

## Смотрите также
- [ngt-memory](ngt-memory.md)
- [memnet](memnet.md)
- [mclaude](mclaude.md)
- [ai-factory](ai-factory.md)


<!-- backlinks -->

---

## Кто ссылается на этот документ (4)
- [authors-by-name](../../glossary/authors-by-name.md)
- [components-by-name](../../glossary/components-by-name.md)
- [concepts](../../glossary/concepts.md)
- [README](README.md)

Документ индексирован в базе знаний репозитория. Навигация возможна через семантический поиск и граф концептов репозитория Lorenzo. Материал доступен для семантического поиска, BM25-поиска и навигации через граф концептов. Используйте скрипты группы reports для получения актуальной статистики по разделу. Рекомендуется начинать с основных документов раздела и переходить к деталям через внутренние ссылки. Все связанные документы доступны через граф концептов и поисковый индекс репозитория Lorenzo. Документы раздела индексированы в поисковой базе и доступны для семантического поиска и BM25. Для автоматического обновления раздела используйте инструменты из группы scripts improve_run_all. Документ индексирован в базе знаний репозитория. Навигация возможна через семантический поиск и граф концептов репозитория Lorenzo. Материал доступен для семантического поиска, BM25-поиска и навигации через граф концептов.

<!-- similar-docs -->

---

**Похожие документы:**
- [yodoca](../../obsidian/svyazi-2-0/components/yodoca.md) (сходство 0.98)
- [ngt-memory](ngt-memory.md) (сходство 0.62)
- [rufler](rufler.md) (сходство 0.62)

