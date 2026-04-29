---
title: "9. Query Flow"
tags:
  - anthropic
  - anthropic-vacancies
date: 2026-04-29
---

# 9. Query Flow
<!-- tags: anthropic -->


<!-- toc-auto -->
## Contents

- [9. Query Flow](#9-query-flow)
  - [9.1. Lifecycle](#91-lifecycle)
  - [9.2. Parallelism](#92-parallelism)
  - [9.3. Error Handling](#93-error-handling)


<!-- summary -->
> 1. Client вызывает `portal.query(q, target_repos=None)`

---
<!-- tags: anthropic -->




## 9. Query Flow

### 9.1. Lifecycle

1. Client вызывает `portal.query(q, target_repos=None)`
2. Portal загружает registry
3. Portal фильтрует адаптеры по `target_repos` (если задан)
4. Portal параллельно вызывает `adapter.fetch(q)` для всех выбранных
5. Portal собирает `results_by_repo: dict[str, list[PortalEntry]]`
6. Portal вычисляет consensus через алгоритм раздела 8
7. Portal возвращает `QueryResult`

### 9.2. Parallelism

Adapter calls MUST быть параллельными (через thread pool, async, 
или multiprocessing). Это критично для performance при росте числа 
Repos.

### 9.3. Error Handling

Если один adapter падает (exception, timeout), Portal MUST:

- Включить этот репо в `errors` список QueryResult
- Продолжить обработку остальных
- Не падать целиком

Timeout per adapter RECOMMENDED: 10 секунд.

---

<!-- similar-docs -->

---

**Похожие документы:**
- [[85-10-query-flow]] (сходство 0.72)
- [[81-6-adapter-interface]] (сходство 0.11)
- [[22-10-queryresult-structure]] (сходство 0.11)


<!-- see-also -->

---

**Смотрите также:**
- [[85-10-query-flow]]
- [[22-10-queryresult-structure]]
- [[81-6-adapter-interface]]
- [[86-11-relevance-ranking]]

<!-- backlinks-auto -->
## Упоминается в

- [[README|Вакансии Anthropic — Анализ по кластерам]]

<!-- related-auto -->
## Связанные документы

- [[85-10-query-flow|10. Query Flow]] _66%_
- [[18-6-adapter-interface|6. Adapter Interface]] _33%_
- [[22-10-queryresult-structure|10. QueryResult Structure]] _33%_
- [[81-6-adapter-interface|6. Adapter Interface]] _25%_
- [[82-7-portalentry-structure|7. PortalEntry Structure]] _21%_
- [[84-9-consensus-algorithm|9. Consensus Algorithm]] _21%_
- [[17-5-compatibility-levels|5. Compatibility Levels]] _17%_
- [[28-appendix-a-minimal-working-example|Appendix A: Minimal Working Example]] _17%_
