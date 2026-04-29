---
title: "Комбинация 22: Russian-International OSS Stack"
tags:
  - technology-combinations
date: 2026-04-29
---

# Комбинация 22: Russian-International OSS Stack

<!-- summary -->
> > Источник: MHTML‑снимок `Комбинирование технологий для новых свойств - Claude` (корень репозитория).

---
<!-- tags: rag, architecture, self-improvement -->




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

**Смотрите также:**
- [[21-legal-corpus-analytics-at-scale]]
- [[27-hybrid-rag-with-ast-chunked-code]]
- [[20-24-final]]
- [[20-hybrid-olap-oltp-with-real-time-sync]]


<!-- similar-docs -->

---

**Похожие документы:**
- [[21-legal-corpus-analytics-at-scale]] (сходство 0.28)
- [[20-24-final]] (сходство 0.26)
- [[27-hybrid-rag-with-ast-chunked-code]] (сходство 0.24)

