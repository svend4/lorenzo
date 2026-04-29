---
title: "8. Consensus Algorithm"
tags:
  - rag
  - anthropic-vacancies
date: 2026-04-29
---

# 8. Consensus Algorithm

<!-- toc-auto -->
## Contents

- [8. Consensus Algorithm](#8-consensus-algorithm)
  - [8.1. Definition](#81-definition)
  - [8.2. v1.0 Consensus Strategy: String Normalization](#82-v10-consensus-strategy-string-normalization)
  - [8.3. Consensus Categories](#83-consensus-categories)
  - [8.4. Coverage Ratio](#84-coverage-ratio)
  - [8.5. Future Extensions (v2.0+)](#85-future-extensions-v20)


<!-- summary -->
> Когда один query возвращает результаты из нескольких Repos, Portal

---
<!-- tags: rag -->




## 8. Consensus Algorithm

### 8.1. Definition

Когда один query возвращает результаты из нескольких Repos, Portal 
вычисляет consensus — степень согласованности концепции между Repos.

### 8.2. v1.0 Consensus Strategy: String Normalization

v1.0 использует простое string matching после normalization:
```
def normalize(title: str) -> str:
return title.lower().strip().translate(PUNCT_STRIP)
def similar(a: str, b: str) -> bool:
return normalize(a) == normalize(b)
```
Два entry считаются одним концептом, если их `title` после 
normalization совпадают.

### 8.3. Consensus Categories

Для каждого уникального концепта, найденного в results:

- **Full Consensus**: концепт присутствует в **всех** Repos, 
  опрошенных в query
- **Partial Consensus**: концепт в 2+ Repos, но не во всех
- **Singular**: концепт только в одном Repo

### 8.4. Coverage Ratio

Дополнительный метрический показатель:
```
coverage_ratio = len(full_consensus) / total_unique_concepts
```
Значение близко к 1.0 означает высокую согласованность экосистемы 
по данному query. Близко к 0 — query попал в area, где Repos 
расходятся.

### 8.5. Future Extensions (v2.0+)

Будущие версии MAY использовать:

- Semantic similarity через embeddings (cross-lingual matching)
- Fuzzy matching с threshold
- Weighted consensus (разный вес от confidence adapter'а)

Эти расширения не breaking — они активируются через `algorithm` 
параметр в query, сохраняя v1.0 как default.

---

<!-- similar-docs -->

---

**Похожие документы:**
- [[84-9-consensus-algorithm]] (сходство 0.34)
- [[86-11-relevance-ranking]] (сходство 0.10)


<!-- see-also -->

---

**Смотрите также:**
- [[84-9-consensus-algorithm]]
- [[86-11-relevance-ranking]]
- [[22-10-queryresult-structure]]
- [[21-9-query-flow]]

<!-- backlinks-auto -->
## Упоминается в

- [[README|Вакансии Anthropic — Анализ по кластерам]]

<!-- related-auto -->
## Связанные документы

- [[84-9-consensus-algorithm|9. Consensus Algorithm]] _53%_
- [[86-11-relevance-ranking|11. Relevance Ranking]] _25%_
