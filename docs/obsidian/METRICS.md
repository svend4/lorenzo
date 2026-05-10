---
title: "Метрики качества документации"
tags:
  - quality
  - metrics
  - documentation
  - coverage
  - general
date: 2026-05-10
---

# Метрики качества документации

<!-- summary -->
> Средний балл: **100.0/100** по 1209 документам

<!-- tags: quality, metrics, documentation, coverage -->

> [!TIP]
> Балл выше 85 означает хорошее качество документации.

<!-- alert-added -->

**Файлов:** 1209  **Средний балл:** 100.0/100

## Качество по разделам

| Раздел | Балл | Ссылок/1K слов | Код-блоков/1K | % с summary | % с тегами |
|--------|------|----------------|--------------|-------------|------------|
| **01-svyazi** | 100 | 21.7 | 1.8 | 100% | 100% |
| **02-anthropic-vacancies** | 100 | 67.5 | 2.3 | 100% | 100% |
| **03-technology-combinations** | 100 | 40.5 | 2.6 | 100% | 100% |
| **04-ai-collaborations** | 100 | 22.0 | 1.3 | 100% | 100% |
| **05-habr-projects** | 100 | 42.6 | 2.2 | 100% | 100% |
| **root** | 100 | 32.5 | 2.0 | 100% | 100% |

## Топ-15 лучших документов

| Документ | Балл | Слов |
|----------|------|------|
| `00-intro-part2` | 100 | 311 |
| `01-executive-summary` | 100 | 721 |
| `02-methodology` | 100 | 505 |
| `03-component-catalog` | 100 | 1483 |
| `04-ensembles-overview` | 100 | 1337 |
| `06-security-privacy` | 100 | 886 |
| `07-mvp-planning` | 100 | 1154 |
| `08-conclusions` | 100 | 439 |
| `09-architectural-gaps` | 100 | 844 |
| `10-second-order-ensembles` | 100 | 983 |
| `11-integration-contracts` | 100 | 824 |
| `12-roadmap` | 100 | 785 |
| `13-contacts` | 100 | 1051 |
| `14-limitations` | 100 | 707 |
| `QA` | 100 | 457 |

## Документы, требующие улучшения (0)

| Документ | Балл | Что отсутствует |
|----------|------|----------------|

## Общие показатели

- Файлов с `<!-- summary -->`: **100.0%**
- Файлов с тегами: **100.0%**
- Файлов с оглавлением: **100.0%**
- Файлов с callout: **100.0%**
- Средний балл качества: **100.0/100**

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

<!-- backlinks -->

---

**Кто ссылается на этот документ (3):**
- [READABILITY](../READABILITY.md)
- [READING_TIME](../READING_TIME.md)
- [SEARCH](../SEARCH.md)

