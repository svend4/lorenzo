# 10. Query Flow

<!-- summary -->
> > Источник: MHTML‑снимок `Вакансии в Anthropic по кластерам - Claude` (корень репозитория). Раздел диалога — Nautilus Portal Protocol v1.1 RFC, написанный совместно с Claude.

---
<!-- tags: anthropic -->




> Источник: MHTML‑снимок `Вакансии в Anthropic по кластерам - Claude` (корень репозитория). Раздел диалога — Nautilus Portal Protocol v1.1 RFC, написанный совместно с Claude.

## 10. Query Flow

### 10.1. Lifecycle

1. Client вызывает `portal.query(q, target_repos=None)`
2. Portal загружает registry (cached)
3. Portal фильтрует адаптеры по `target_repos` (если задан)
4. Portal параллельно вызывает `adapter.fetch(q)` для всех выбранных
5. Portal собирает `results_by_repo: dict[str, list[PortalEntry]]`
6. Portal вычисляет consensus по алгоритму раздела 9
7. Portal вычисляет relevance ranking (раздел 11)
8. Portal возвращает `QueryResult`

### 10.2. Parallelism

Adapter calls SHOULD быть параллельными (через thread pool, async, 
или multiprocessing). Это критично для performance при росте числа 
Repos.

### 10.3. Error Handling

Если adapter падает (exception, timeout), Portal MUST:

- Включить repo в `errors` список QueryResult
- Продолжить обработку остальных
- Не падать целиком

Timeout per adapter RECOMMENDED: 5 секунд (было 10 в v1.0, снижено 
для лучшего UX).

### 10.4. Timeout Behavior

При timeout адаптера portal MUST:

- Отметить repo как error в `errors`
- Если у адаптера есть fallback entries — попытаться вернуть их
- Логировать timeout для telemetry

---

<!-- see-also -->

---

**Смотрите также:**
- [85-10-query-flow](docs/02-anthropic-vacancies/85-10-query-flow.md)
- [09-query-flow](docs/nautilus/npp-v1-0/09-query-flow.md)
- [21-9-query-flow](docs/02-anthropic-vacancies/21-9-query-flow.md)
- [11-relevance-ranking](docs/nautilus/npp-v1-1/11-relevance-ranking.md)


<!-- similar-docs -->

---

**Похожие документы:**
- [85-10-query-flow](docs/obsidian/02-anthropic-vacancies/85-10-query-flow.md) (сходство 0.74)
- [85-10-query-flow](docs/02-anthropic-vacancies/85-10-query-flow.md) (сходство 0.72)
- [09-query-flow](docs/nautilus/npp-v1-0/09-query-flow.md) (сходство 0.72)

