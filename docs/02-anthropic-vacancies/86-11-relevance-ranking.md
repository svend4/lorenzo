# 11. Relevance Ranking
<!-- tags: anthropic -->


<!-- toc-auto -->
## Contents

- [11. Relevance Ranking](#11-relevance-ranking)
  - [11.1. Scoring Formula](#111-scoring-formula)
  - [11.2. MAY Extensions](#112-may-extensions)


<!-- summary -->
> v1.1 нормализует алгоритм ранжирования из reference implementation.

---
<!-- tags: anthropic -->




## 11. Relevance Ranking

v1.1 нормализует алгоритм ранжирования из reference implementation.

### 11.1. Scoring Formula

Для каждого PortalEntry `e` и query `q` (оба normalized):

```python
def relevance_score(e: PortalEntry, q: str) -> float:
    score = 0.0
    q_lower = q.lower()
    title_lower = e.title.lower()
    content_lower = e.content.lower()
    id_lower = e.id.lower()
    
    if q_lower == title_lower:
        score += 1.0
    elif q_lower in title_lower:
        score += 0.7
    
    if q_lower in content_lower:
        score += 0.3
    
    if q_lower in id_lower:
        score += 0.4
    
    # Bonus for connectivity
    score += min(len(e.links) * 0.05, 0.2)
    
    # Penalty for fallback
    if e.is_fallback:
        score *= 0.5
    
    return score
```

### 11.2. MAY Extensions

Альтернативные алгоритмы ранжирования (TF-IDF, BM25, semantic 
embeddings) могут использоваться, но MUST быть опциональными через 
параметр `ranked=<algorithm>`. Default MUST оставаться формула 
раздела 11.1 для воспроизводимости между порталами.

---

<!-- similar-docs -->

---

**Похожие документы:**
- [84-9-consensus-algorithm](84-9-consensus-algorithm.md) (сходство 0.12)
- [20-8-consensus-algorithm](20-8-consensus-algorithm.md) (сходство 0.10)


<!-- see-also -->

---

**Смотрите также:**
- [84-9-consensus-algorithm](84-9-consensus-algorithm.md)
- [22-10-queryresult-structure](22-10-queryresult-structure.md)
- [25-13-reference-implementation](25-13-reference-implementation.md)
- [20-8-consensus-algorithm](20-8-consensus-algorithm.md)

<!-- backlinks-auto -->
## Упоминается в

- [10. Query Flow](85-10-query-flow.md)
- [10. QueryResult Structure](22-10-queryresult-structure.md)
- [6. Adapter Interface](81-6-adapter-interface.md)
- [8. Consensus Algorithm](20-8-consensus-algorithm.md)
- [9. Consensus Algorithm](84-9-consensus-algorithm.md)
- [9. Query Flow](21-9-query-flow.md)
- [Вакансии Anthropic — Анализ по кластерам](README.md)
- [Критерии выбора для фазы 3](71-критерии-выбора-для-фазы-3.md)
## Упоминается в

- [Вакансии Anthropic — Анализ по кластерам](../README.md)

<!-- related-auto -->
## Связанные документы

- [9. Consensus Algorithm](84-9-consensus-algorithm.md) _21%_
- [14. SDK Contract (Informative)](89-14-sdk-contract-informative.md) _21%_
- [8. Consensus Algorithm](20-8-consensus-algorithm.md) _17%_
- [9. Query Flow](21-9-query-flow.md) _17%_
- [10. QueryResult Structure](22-10-queryresult-structure.md) _17%_
## Связанные документы

- [9. Consensus Algorithm](84-9-consensus-algorithm.md) _29%_
- [8. Consensus Algorithm](20-8-consensus-algorithm.md) _25%_
- [10. QueryResult Structure](22-10-queryresult-structure.md) _25%_
- [Appendix B: Change Log](103-appendix-b-change-log.md) _21%_
- [6. Adapter Interface](81-6-adapter-interface.md) _21%_
- [14. SDK Contract (Informative)](89-14-sdk-contract-informative.md) _21%_
- [3. Registry (`nautilus.json`)](08-3-registry-nautilus-json.md) _17%_
- [4. Nautilus Portal as Reference Substrate](141-4-nautilus-portal-as-reference-substrate.md) _17%_
