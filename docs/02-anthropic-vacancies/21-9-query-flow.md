# 9. Query Flow

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

