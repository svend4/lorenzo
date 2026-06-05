---
title: "10. Query Flow"
tags:
  - anthropic
  - rag
  - anthropic-vacancies
date: 2026-05-14
---

# 10. Query Flow

<!-- toc-auto -->
## Contents

- [10. Query Flow](#10-query-flow)
  - [10.1. Lifecycle](#101-lifecycle)
  - [10.2. Parallelism](#102-parallelism)
  - [10.3. Error Handling](#103-error-handling)
  - [10.4. Timeout Behavior](#104-timeout-behavior)
- [Похожие документы](#похожие-документы)
- [Использование](#использование)
- [Смотрите также](#смотрите-также)
- [Кто ссылается на этот документ (5)](#кто-ссылается-на-этот-документ-5)


> [!NOTE]
> Документ создан на основе исследования. Ссылки ведут на связанные материалы.

<!-- alert-added -->
<!-- tags: anthropic, rag -->


<!-- abstract-auto -->

> [!NOTE]
> Документ создан на основе исследования. Ссылки ведут на связанные материалы.

> **Абстракт** (авто)
>
> 🎯 **Проблема:** Error Handling(103-error-handling) - 10.4.
> 🔧 **Подход:** Portal вычисляет consensus по алгоритму раздела 9 7.
> ✅ **Результат:** Portal собирает resultsbyrepo: dictstr, listPortalEntry 6.
> 🏷️ **Ключевые слова:** `portal`, `query`, `adapter`, `timeout`, `anthropic`, `vacancies`, `interface`, `error`
>


<!-- summary -->
> Документ создан на основе исследования. Ссылки ведут на связанные материалы. Документ создан на основе исследования. 🎯 Проблема: Error Handling - 10.4.
Если adapter падает (exception, timeout), Portal MUST:
 Включить repo в   список QueryResult
 Продолжить обработку остальных
 Не падать целиком
Timeout per adapter RECOMMENDED: 5 секунд (было 10 в v1.0, снижено 
для лучшего UX).

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
8. Portal возвращает `[[02-общий-план-развития-nautilus-portal-protocol|QueryResult]]`

### 10.2. Parallelism

Adapter calls SHOULD быть параллельными (через thread pool, async, 
или multiprocessing). Это критично для performance при росте числа 
Repos.

### 10.3. Error Handling

Если adapter падает (exception, timeout), Portal MUST:

- Включить repo в `errors` список [[02-общий-план-развития-nautilus-portal-protocol|QueryResult]]
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

## Похожие документы
- [[21-9-query-flow]] (сходство 0.72)
- [[81-6-adapter-interface]] (сходство 0.12)
- [[18-6-adapter-interface]] (сходство 0.10)


<!-- see-also -->

---

## Использование
```bash
# Поиск по теме документа
python scripts/improve_semantic_search.py --query "10 Query Flow"
```

## Смотрите также
- [[21-9-query-flow]]
- [[22-10-queryresult-structure]]
- [[81-6-adapter-interface]]
- [[86-11-relevance-ranking]]


<!-- backlinks -->

---

## Кто ссылается на этот документ (5)
- [[18-6-adapter-interface]]
- [[21-9-query-flow]]
- [[22-10-queryresult-structure]]
- [[90-15-security-considerations]]
- [[README]]

