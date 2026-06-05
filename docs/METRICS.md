# Метрики качества документации

<!-- summary -->
> Средний балл: **97.9/100** по 1226 документам

<!-- tags: quality, metrics, documentation, coverage -->

> [!TIP]
> Балл выше 85 означает хорошее качество документации.

<!-- alert-added -->

**Файлов:** 1226  **Средний балл:** 97.9/100

## Качество по разделам

| Раздел | Балл | Ссылок/1K слов | Код-блоков/1K | % с summary | % с тегами |
|--------|------|----------------|--------------|-------------|------------|
| **01-svyazi** | 99 | 33.4 | 1.6 | 100% | 100% |
| **02-anthropic-vacancies** | 100 | 70.8 | 2.3 | 100% | 100% |
| **03-technology-combinations** | 97 | 38.1 | 2.2 | 100% | 100% |
| **04-ai-collaborations** | 99 | 29.4 | 1.1 | 100% | 100% |
| **05-habr-projects** | 99 | 46.9 | 1.9 | 100% | 100% |
| **root** | 79 | 41.5 | 2.9 | 86% | 68% |

## Топ-15 лучших документов

| Документ | Балл | Слов |
|----------|------|------|
| `00-intro-part2` | 100 | 383 |
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
| `README` | 100 | 424 |

## Документы, требующие улучшения (3)

| Документ | Балл | Что отсутствует |
|----------|------|----------------|
| `ABBREVIATIONS` | 30 | summary, tags, TOC, callout |
| `MISSING` | 30 | summary, tags, TOC, callout |
| `QUESTIONS` | 30 | summary, tags, TOC, callout |

## Общие показатели

- Файлов с `<!-- summary -->`: **98.6%**
- Файлов с тегами: **97.0%**
- Файлов с оглавлением: **94.1%**
- Файлов с callout: **94.9%**
- Средний балл качества: **97.9/100**

## Использование

```bash
python scripts/improve_metrics.py
```

```bash
# Обновить метрики и проверить здоровье репозитория
python scripts/improve_metrics.py && python scripts/improve_health.py
```


## Смотрите также

- [HEALTH](HEALTH.md) — общее здоровье репозитория
- [BROKEN_LINKS](BROKEN_LINKS.md) — состояние внутренних ссылок
- [VALIDATION](VALIDATION.md) — валидация структуры
- [SCORING](SCORING.md) — готовность к запуску (Go/No-Go)

<!-- see-also -->

---

**Смотрите также:**
- [DIGEST_WEEKLY](DIGEST_WEEKLY.md)
- [HEALTH](HEALTH.md)
- [LLM_SUMMARIES](LLM_SUMMARIES.md)
- [TAGS](TAGS.md)


<!-- backlinks -->

---

**Кто ссылается на этот документ (63):**
- [QA](01-svyazi/QA.md)
- [QA](02-anthropic-vacancies/QA.md)
- [QA](03-technology-combinations/QA.md)
- [QA](04-ai-collaborations/QA.md)
- [QA](05-habr-projects/QA.md)
- [ACTION_ITEMS](ACTION_ITEMS.md)
- [ALERTS](ALERTS.md)
- [BROKEN_LINKS](BROKEN_LINKS.md)
- _...ещё 55_

