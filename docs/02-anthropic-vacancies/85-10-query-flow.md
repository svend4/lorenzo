# 10. Query Flow
<!-- tags: anthropic -->


<!-- toc-auto -->
## Contents

- [10. Query Flow](#10-query-flow)
  - [10.1. Lifecycle](#101-lifecycle)
  - [10.2. Parallelism](#102-parallelism)
  - [10.3. Error Handling](#103-error-handling)
  - [10.4. Timeout Behavior](#104-timeout-behavior)


<!-- summary -->
> 1. Client вызывает `portal.query(q, target_repos=None)`

---
<!-- tags: anthropic -->




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

<!-- similar-docs -->

---

**Похожие документы:**
- [21-9-query-flow](21-9-query-flow.md) (сходство 0.72)
- [81-6-adapter-interface](81-6-adapter-interface.md) (сходство 0.12)
- [18-6-adapter-interface](18-6-adapter-interface.md) (сходство 0.10)


<!-- see-also -->

---

**Смотрите также:**
- [21-9-query-flow](21-9-query-flow.md)
- [22-10-queryresult-structure](22-10-queryresult-structure.md)
- [81-6-adapter-interface](81-6-adapter-interface.md)
- [86-11-relevance-ranking](86-11-relevance-ranking.md)

<!-- backlinks-auto -->
## Упоминается в

- [15. Security Considerations](90-15-security-considerations.md)
- [5. Compatibility Levels](17-5-compatibility-levels.md)
- [6. Adapter Interface](18-6-adapter-interface.md)
- [6. Adapter Interface](81-6-adapter-interface.md)
- [9. Consensus Algorithm](84-9-consensus-algorithm.md)
- [9. Query Flow](21-9-query-flow.md)
- [Вакансии Anthropic — Анализ по кластерам](README.md)
## Упоминается в

- [Вакансии Anthropic — Анализ по кластерам](../README.md)

<!-- related-auto -->
## Связанные документы

- [9. Query Flow](21-9-query-flow.md) _66%_
- [6. Adapter Interface](18-6-adapter-interface.md) _25%_
- [10. QueryResult Structure](22-10-queryresult-structure.md) _21%_
- [6. Adapter Interface](81-6-adapter-interface.md) _21%_
- [3. Registry (`nautilus.json`)](08-3-registry-nautilus-json.md) _17%_
- [9. Consensus Algorithm](84-9-consensus-algorithm.md) _17%_
## Связанные документы

- [9. Query Flow](21-9-query-flow.md) _66%_
- [6. Adapter Interface](18-6-adapter-interface.md) _29%_
- [10. QueryResult Structure](22-10-queryresult-structure.md) _25%_
- [5. Compatibility Levels](17-5-compatibility-levels.md) _21%_
- [🇬🇧 About](68-about.md) _17%_
- [2. Terminology](77-2-terminology.md) _17%_
- [3. Registry (`nautilus.json`)](78-3-registry-nautilus-json.md) _17%_
- [6. Adapter Interface](81-6-adapter-interface.md) _17%_
