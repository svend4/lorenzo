---
state: approved
---

# Комбинация 22: Russian-International OSS Stack

<!-- toc-auto -->
## Contents

- [Использование](#использование)
- [Смотрите также](#смотрите-также)
- [Кто ссылается на этот документ (3)](#кто-ссылается-на-этот-документ-3)


> [!NOTE]
> Документ создан на основе исследования. Ссылки ведут на связанные материалы.

<!-- alert-added -->

<!-- summary -->
> > Источник: MHTML‑снимок `Комбинирование технологий для новых свойств - Claude` (корень репозитория). Документ создан на основе исследования. Ссылки ведут на связанные материалы.

---
<!-- tags: rag, architecture, self-improvement -->

> [!NOTE]
> Документ создан на основе исследования. Ссылки ведут на связанные материалы.





> Источник: MHTML‑снимок `Комбинирование технологий для новых свойств - Claude` (корень репозитория).

Родители:

ClickHouse (Yandex, OLAP analytics)

CatBoost (Yandex, gradient boosting, beats XGBoost)

Crawl4AI (international, 60k+ GitHub stars)

Graph-RAG (Microsoft Research)

Дети:

ML-powered legal outcome prediction

Crawl4AI scrapes historical decisions → ClickHouse

Feature engineering in ClickHouse (SQL aggregations)

CatBoost trains on structured features

Graph-RAG retrieves similar precedents

Pipeline:

Historical data (ClickHouse) → Features
CatBoost model: predict(outcome | court, judge, §§, case_type)
Confidence: Graph-RAG finds 10 most similar cases

Output: "Based on 847 similar cases, 73% approval probability"

Hybrid Russian-Western analytics stack

Data layer: ClickHouse (Russian, proven at Yandex scale)

ML layer: CatBoost (Russian, better than XGBoost on categorical)

Scraping: Crawl4AI (international, community-driven)

Retrieval: Graph-RAG (Microsoft, state-of-art)

Advantage: Best-of-breed from both ecosystems

ROI: Performance + community support, no vendor lock-in

Уникальность: Demonstrates Russian OSS (ClickHouse, CatBoost) competing globally. CatBoost + ClickHouse specifically optimized for each other (both Yandex). Legal domain benefits from proven enterprise tech.

<!-- see-also -->

---

## Использование

```bash
# Поиск по теме документа
python scripts/improve_semantic_search.py --query "Комбинация 22 Russian International OSS"
```

## Смотрите также
- [21-legal-corpus-analytics-at-scale](21-legal-corpus-analytics-at-scale.md)
- 27-hybrid-[rag-with-ast-chunked-code](27-hybrid-rag-with-ast-chunked-code.md)
- [20-24-final](../synthesis-tables/20-24-final.md)
- [20-hybrid-olap-oltp-with-real-time-sync](20-hybrid-olap-oltp-with-real-time-sync.md)


<!-- backlinks -->

---

## Кто ссылается на этот документ (3)
- [components-by-name](../../glossary/components-by-name.md)
- [README](README.md)
- [20-24-final](../synthesis-tables/20-24-final.md)

_Документ индексирован в поисковой базе репозитория Lorenzo и доступен для семантического поиска._ _Документ индексирован в поисковой базе репозитория и доступен для поиска._ _Доступен семантический поиск._ _Индексировано._

<!-- similar-docs -->

---

**Похожие документы:**
- [22-russian-international-oss-stack](../../obsidian/technology-combinations/combinations/22-russian-international-oss-stack.md) (сходство 0.95)
- [20-24-final](../synthesis-tables/20-24-final.md) (сходство 0.33)
- [20-24-final](../../obsidian/technology-combinations/synthesis-tables/20-24-final.md) (сходство 0.33)

