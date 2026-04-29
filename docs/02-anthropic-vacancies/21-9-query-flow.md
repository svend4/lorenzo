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
- [85-10-query-flow](docs/02-anthropic-vacancies/85-10-query-flow.md) (сходство 0.72)
- [81-6-adapter-interface](docs/02-anthropic-vacancies/81-6-adapter-interface.md) (сходство 0.11)
- [22-10-queryresult-structure](docs/02-anthropic-vacancies/22-10-queryresult-structure.md) (сходство 0.11)


<!-- see-also -->

---

**Смотрите также:**
- [85-10-query-flow](docs/02-anthropic-vacancies/85-10-query-flow.md)
- [22-10-queryresult-structure](docs/02-anthropic-vacancies/22-10-queryresult-structure.md)
- [81-6-adapter-interface](docs/02-anthropic-vacancies/81-6-adapter-interface.md)
- [86-11-relevance-ranking](docs/02-anthropic-vacancies/86-11-relevance-ranking.md)

<!-- backlinks-auto -->
## Упоминается в

- [Вакансии Anthropic — Анализ по кластерам](docs/02-anthropic-vacancies/README.md)

<!-- related-auto -->
## Связанные документы

- [10. Query Flow](docs/02-anthropic-vacancies/85-10-query-flow.md) _66%_
- [6. Adapter Interface](docs/02-anthropic-vacancies/18-6-adapter-interface.md) _33%_
- [10. QueryResult Structure](docs/02-anthropic-vacancies/22-10-queryresult-structure.md) _33%_
- [6. Adapter Interface](docs/02-anthropic-vacancies/81-6-adapter-interface.md) _25%_
- [7. PortalEntry Structure](docs/02-anthropic-vacancies/82-7-portalentry-structure.md) _21%_
- [9. Consensus Algorithm](docs/02-anthropic-vacancies/84-9-consensus-algorithm.md) _21%_
- [5. Compatibility Levels](docs/02-anthropic-vacancies/17-5-compatibility-levels.md) _17%_
- [Appendix A: Minimal Working Example](docs/02-anthropic-vacancies/28-appendix-a-minimal-working-example.md) _17%_
