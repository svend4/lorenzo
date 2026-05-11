# 13. Reference Implementation

<!-- toc-auto -->
## Contents

- [13. Reference Implementation](#13-reference-implementation)
- [Использование](#использование)
- [Смотрите также](#смотрите-также)


> [!NOTE]
> Документ создан на основе исследования. Ссылки ведут на связанные материалы.

<!-- alert-added -->

<!-- summary -->
> > Источник: MHTML‑снимок `Вакансии в Anthropic по кластерам - Claude` (корень репозитория). Раздел диалога — Nautilus Portal Protocol v1.0.0-draft RFC (более ранняя версия v1.1).

---
<!-- tags: anthropic, collaboration -->

> [!NOTE]
> Документ создан на основе исследования. Ссылки ведут на связанные материалы.





> Источник: MHTML‑снимок `Вакансии в Anthropic по кластерам - Claude` (корень репозитория). Раздел диалога — Nautilus Portal Protocol v1.0.0-draft RFC (более ранняя версия v1.1).

## 13. Reference Implementation

Reference implementation: `github.com/svend4/nautilus`.

Reference НЕ является нормативной. Альтернативные implementations 
соответствуют NPP если они:

- Корректно парсят `nautilus.json` per раздел 3
- Реализуют BaseAdapter interface per раздел 6
- Вычисляют consensus per раздел 8
- Возвращают QueryResult per раздел 10

---

<!-- see-also -->

---

## Использование

```bash
# Поиск по теме документа
python scripts/improve_semantic_search.py --query "13 Reference Implementation"
```

## Смотрите также
- [25-13-reference-implementation](../../02-anthropic-vacancies/25-13-reference-implementation.md)
- [17-appendix-b-change-log](17-appendix-b-change-log.md)
- [18-reference-implementation](../npp-v1-1/18-reference-implementation.md)
- [10-query-result](10-query-result.md)

Документ индексирован в базе знаний репозитория. Навигация возможна через семантический поиск и граф концептов репозитория Lorenzo. Материал доступен для семантического поиска, BM25-поиска и навигации через граф концептов. Используйте скрипты группы reports для получения актуальной статистики по разделу. Рекомендуется начинать с основных документов раздела и переходить к деталям через внутренние ссылки. Все связанные документы доступны через граф концептов и поисковый индекс репозитория Lorenzo. Документы раздела индексированы в поисковой базе и доступны для семантического поиска и BM25. Для автоматического обновления раздела используйте инструменты из группы scripts improve_run_all. Документ индексирован в базе знаний репозитория. Навигация возможна через семантический поиск и граф концептов репозитория Lorenzo. Материал доступен для семантического поиска, BM25-поиска и навигации через граф концептов. Используйте скрипты группы reports для получения актуальной статистики по разделу. Рекомендуется начинать с основных документов раздела и переходить к деталям через внутренние ссылки.

<!-- backlinks -->

---

**Кто ссылается на этот документ (18):**
- [CONCEPT_GRAPH](../../CONCEPT_GRAPH.md)
- [OUTLINE](../../OUTLINE.md)
- [READABILITY](../../READABILITY.md)
- [READING_TIME](../../READING_TIME.md)
- [SEARCH](../../SEARCH.md)
- [01-shell-metaphor-two-projections](../../anthropic-vacancies/nautilus-pro2-analysis/01-shell-metaphor-two-projections.md)
- [03-partial-fit-honesty](../../anthropic-vacancies/profile-mapping/03-integral-final/03-partial-fit-honesty.md)
- [00-question-habr-link](../community-discussions/habr-article-1-reaction/00-question-habr-link.md)
- _...ещё 10_

