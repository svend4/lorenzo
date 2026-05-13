---
title: "Метрики качества документации"
tags:
  - quality
  - metrics
  - documentation
  - coverage
  - general
date: 2026-05-13
---

# Метрики качества документации

<!-- summary -->
> Средний балл: **95.9/100** по 1226 документам

<!-- tags: quality, metrics, documentation, coverage -->

> [!TIP]
> Балл выше 85 означает хорошее качество документации.

<!-- alert-added -->

**Файлов:** 1226  **Средний балл:** 95.9/100

## Качество по разделам

| Раздел | Балл | Ссылок/1K слов | Код-блоков/1K | % с summary | % с тегами |
|--------|------|----------------|--------------|-------------|------------|
| **01-svyazi** | 100 | 33.1 | 1.8 | 100% | 100% |
| **02-anthropic-vacancies** | 100 | 70.6 | 2.3 | 100% | 100% |
| **03-technology-combinations** | 100 | 36.4 | 3.1 | 100% | 100% |
| **04-ai-collaborations** | 99 | 29.3 | 1.3 | 100% | 100% |
| **05-habr-projects** | 100 | 45.8 | 2.2 | 100% | 100% |
| **root** | 92 | 45.3 | 2.4 | 86% | 89% |

## Топ-15 лучших документов

| Документ | Балл | Слов |
|----------|------|------|
| `00-intro-part2` | 100 | 365 |
| `01-executive-summary` | 100 | 750 |
| `02-methodology` | 100 | 567 |
| `03-component-catalog` | 100 | 1516 |
| `04-ensembles-overview` | 100 | 1385 |
| `06-security-privacy` | 100 | 941 |
| `07-mvp-planning` | 100 | 1187 |
| `08-conclusions` | 100 | 470 |
| `09-architectural-gaps` | 100 | 878 |
| `10-second-order-ensembles` | 100 | 1011 |
| `11-integration-contracts` | 100 | 858 |
| `12-roadmap` | 100 | 840 |
| `13-contacts` | 100 | 1080 |
| `14-limitations` | 100 | 765 |
| `QA` | 100 | 261 |

## Документы, требующие улучшения (5)

| Документ | Балл | Что отсутствует |
|----------|------|----------------|
| `BACKLINKS` | 30 | summary, tags, TOC, callout |
| `CLUSTERS` | 30 | summary, tags, TOC, callout |
| `CROSSREFS` | 30 | summary, tags, TOC, callout |
| `PRIORITIES` | 30 | summary, tags, TOC, callout |
| `WORD_FREQ` | 30 | summary, tags, TOC, callout |

## Общие показатели

- Файлов с `<!-- summary -->`: **92.8%**
- Файлов с тегами: **93.0%**
- Файлов с оглавлением: **97.1%**
- Файлов с callout: **94.7%**
- Средний балл качества: **95.9/100**

## Использование

```bash
python scripts/improve_metrics.py
```

```bash
# Обновить метрики и проверить здоровье репозитория
python scripts/improve_metrics.py && python scripts/improve_health.py
```


## Смотрите также

- [[HEALTH]] — общее здоровье репозитория
- [[BROKEN_LINKS]] — состояние внутренних ссылок
- [[VALIDATION]] — валидация структуры
- [[SCORING]] — готовность к запуску (Go/No-Go)

<!-- similar-docs -->

---

**Похожие документы:**
- [[METRICS]] (сходство 0.97)
- [[DIGEST_WEEKLY]] (сходство 0.29)
- [[DIGEST_WEEKLY]] (сходство 0.29)


<!-- see-also -->

---

**Смотрите также:**
- [[DIGEST_WEEKLY]]
- [[HEALTH]]
- [[LLM_SUMMARIES]]
- [[COVERAGE]]


<!-- backlinks -->

---

**Кто ссылается на этот документ (34):**
- [[BROKEN_LINKS]]
- [[CHANGELOG_AUTO]]
- [[CITATION_INDEX]]
- [[CONCEPT_GRAPH]]
- [[CONTRADICTIONS]]
- [[CROSS_SECTION]]
- [[DEPENDENCY_MAP]]
- [[DIGEST_AUTO]]
- _...ещё 26_

