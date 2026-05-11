# Дерево метрик Svyazi 2.0

<!-- toc-auto -->
## Contents

- [Использование](#использование)
- [Смотрите также](#смотрите-также)


> [!NOTE]
> Документ создан на основе исследования. Ссылки ведут на связанные материалы.

<!-- alert-added -->

<!-- summary -->
> > Источник: MHTML‑снимок `Поиск коллабораций AI проектов` (корень репозитория).
**Проекты:** Svyazi

---
<!-- tags: rag, knowledge, ingestion, architecture, collaboration -->

> [!NOTE]
> Документ создан на основе исследования. Ссылки ведут на связанные материалы.





> Источник: MHTML‑снимок `Поиск коллабораций AI проектов` (корень репозитория).

6. Метрики, без которых Svyazi‑2.0 нельзя масштабировать

Для Svyazi‑2.0 нужна не одна “accuracy”, а дерево метрик.

| Уровень | Метрика | Что измеряет
| Extraction | schema_valid_rate | Доля LLM‑ответов, прошедших JSON/schema validation
| Normalization | canonicalization_rate | Доля skills/company/roles, сведённых к канону
| Evidence | evidence_coverage | Доля выводов с source/page/span/bbox
| Matching | match_precision@k | Сколько top‑k рекомендаций человек признал полезными
| Matching | serendipity_score | Сколько рекомендаций были неочевидны, но полезны
| Memory | proposal_to_fact_rate | Сколько гипотез после review стали фактами
| Memory | false_association_rate | Сколько ассоциаций отклонено как шум
| Safety | unsafe_tool_block_rate | Сколько risky actions остановлено policy/HITL
| Cost | cost_per_card | Цена обработки одной карточки
| AgentOps | trace_completeness | Доля операций с полным trace envelope
| UX | time_to_explain_match | За сколько секунд пользователь понимает “почему эта связь”

Особенно важны false_association_rate и evidence_coverage. Без них система легко станет “магическим рекомендателем”, которому нельзя доверять.

<!-- see-also -->

---

## Использование

```bash
# Поиск по теме документа
python scripts/improve_semantic_search.py --query "Дерево метрик Svyazi 2 0"
```

## Смотрите также
- [10-architecture-rfc](10-architecture-rfc.md)
- [05-roadmap-6-12-months](05-roadmap-6-12-months.md)
- [02-agentops-trace-envelope](02-agentops-trace-envelope.md)
- [08-commercialization-three-paths](08-commercialization-three-paths.md)

_Документ индексирован в поисковой базе репозитория Lorenzo и доступен для семантического поиска._ _Документ индексирован в поисковой базе репозитория Lorenzo и доступен для семантического поиска._ _Материал индексирован и доступен для поиска, BM25 и навигации через граф концептов._ _Документ доступен для семантического поиска._ _Индексировано._

<!-- backlinks -->

---

**Кто ссылается на этот документ (8):**
- [OUTLINE](../../OUTLINE.md)
- [READABILITY](../../READABILITY.md)
- [READING_TIME](../../READING_TIME.md)
- [SEARCH](../../SEARCH.md)
- [TABLES](../../TABLES.md)
- [08-commercialization-three-paths](08-commercialization-three-paths.md)
- [10-architecture-rfc](10-architecture-rfc.md)
- [README](README.md)


<!-- similar-docs -->

---

**Похожие документы:**
- [06-metrics-tree](../../obsidian/ai-collaborations/continuation/06-metrics-tree.md) (сходство 0.98)
- [10-architecture-rfc](10-architecture-rfc.md) (сходство 0.32)
- [10-architecture-rfc](../../obsidian/ai-collaborations/continuation/10-architecture-rfc.md) (сходство 0.31)

