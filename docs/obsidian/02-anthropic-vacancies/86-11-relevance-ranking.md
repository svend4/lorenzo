---
title: "11. Relevance Ranking"
tags:
  - anthropic
  - anthropic-vacancies
date: 2026-04-29
---

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
- [[84-9-consensus-algorithm]] (сходство 0.12)
- [[20-8-consensus-algorithm]] (сходство 0.10)


<!-- see-also -->

---

**Смотрите также:**
- [[84-9-consensus-algorithm]]
- [[22-10-queryresult-structure]]
- [[25-13-reference-implementation]]
- [[20-8-consensus-algorithm]]

<!-- backlinks-auto -->
## Упоминается в

- [[README|Вакансии Anthropic — Анализ по кластерам]]

<!-- related-auto -->
## Связанные документы

- [[84-9-consensus-algorithm|9. Consensus Algorithm]] _29%_
- [[20-8-consensus-algorithm|8. Consensus Algorithm]] _25%_
- [[22-10-queryresult-structure|10. QueryResult Structure]] _25%_
- [[103-appendix-b-change-log|Appendix B: Change Log]] _21%_
- [[81-6-adapter-interface|6. Adapter Interface]] _21%_
- [[89-14-sdk-contract-informative|14. SDK Contract (Informative)]] _21%_
- [[08-3-registry-nautilus-json|3. Registry (`nautilus.json`)]] _17%_
- [[141-4-nautilus-portal-as-reference-substrate|4. Nautilus Portal as Reference Substrate]] _17%_
