---
title: "9. Query Flow"
tags:
  - anthropic
  - nautilus
date: 2026-04-29
---

# 9. Query Flow

<!-- summary -->
> > Источник: MHTML‑снимок `Вакансии в Anthropic по кластерам - Claude` (корень репозитория). Раздел диалога — Nautilus Portal Protocol v1.0.0-draft RFC (более ранняя версия v1.1).

---
<!-- tags: anthropic -->




> Источник: MHTML‑снимок `Вакансии в Anthropic по кластерам - Claude` (корень репозитория). Раздел диалога — Nautilus Portal Protocol v1.0.0-draft RFC (более ранняя версия v1.1).

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

<!-- see-also -->

---

**Смотрите также:**
- [[10-query-flow]]
- [[21-9-query-flow]]
- [[85-10-query-flow]]
- [[17-appendix-b-change-log]]


<!-- similar-docs -->

---

**Похожие документы:**
- [[10-query-flow]] (сходство 0.72)
- [[21-9-query-flow]] (сходство 0.65)
- [[21-9-query-flow]] (сходство 0.65)

