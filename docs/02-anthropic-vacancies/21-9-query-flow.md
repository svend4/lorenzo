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
- [85-10-query-flow](85-10-query-flow.md) (сходство 0.72)
- [81-6-adapter-interface](81-6-adapter-interface.md) (сходство 0.11)
- [22-10-queryresult-structure](22-10-queryresult-structure.md) (сходство 0.11)


<!-- see-also -->

---

**Смотрите также:**
- [85-10-query-flow](85-10-query-flow.md)
- [22-10-queryresult-structure](22-10-queryresult-structure.md)
- [81-6-adapter-interface](81-6-adapter-interface.md)
- [86-11-relevance-ranking](86-11-relevance-ranking.md)

<!-- backlinks-auto -->
## Упоминается в

- [10. Query Flow](85-10-query-flow.md)
- [10. QueryResult Structure](22-10-queryresult-structure.md)
- [15. Security Considerations](90-15-security-considerations.md)
- [6. Adapter Interface](18-6-adapter-interface.md)
- [6. Adapter Interface](81-6-adapter-interface.md)
- [8. Consensus Algorithm](20-8-consensus-algorithm.md)
- [9. Consensus Algorithm](84-9-consensus-algorithm.md)
- [Вакансии Anthropic — Анализ по кластерам](README.md)
## Упоминается в

- [Вакансии Anthropic — Анализ по кластерам](../README.md)

<!-- related-auto -->
## Связанные документы

- [10. Query Flow](85-10-query-flow.md) _66%_
- [6. Adapter Interface](18-6-adapter-interface.md) _33%_
- [6. Adapter Interface](81-6-adapter-interface.md) _29%_
- [10. QueryResult Structure](22-10-queryresult-structure.md) _25%_
- [9. Consensus Algorithm](84-9-consensus-algorithm.md) _21%_
- [7. PortalEntry Structure](82-7-portalentry-structure.md) _17%_
- [11. Relevance Ranking](86-11-relevance-ranking.md) _17%_
## Связанные документы

- [10. Query Flow](85-10-query-flow.md) _66%_
- [6. Adapter Interface](18-6-adapter-interface.md) _33%_
- [10. QueryResult Structure](22-10-queryresult-structure.md) _33%_
- [6. Adapter Interface](81-6-adapter-interface.md) _25%_
- [7. PortalEntry Structure](82-7-portalentry-structure.md) _21%_
- [9. Consensus Algorithm](84-9-consensus-algorithm.md) _21%_
- [5. Compatibility Levels](17-5-compatibility-levels.md) _17%_
- [Appendix A: Minimal Working Example](28-appendix-a-minimal-working-example.md) _17%_
