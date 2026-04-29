# 11. Relevance Ranking

<!-- toc-auto -->
## Contents

- [11. Relevance Ranking](#11-relevance-ranking)
  - [11.1. Scoring Formula](#111-scoring-formula)
  - [11.2. MAY Extensions](#112-may-extensions)


<!-- summary -->
> v1.1 нормализует алгоритм ранжирования из reference implementation.

---



## 11. Relevance Ranking

v1.1 нормализует алгоритм ранжирования из reference implementation.

### 11.1. Scoring Formula

Для каждого [PortalEntry](../docs/02-anthropic-vacancies/01-интегральный-анализ-профиля-svend4.md) `e` и query `q` (оба normalized):

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
- [84-9-consensus-algorithm](docs/02-anthropic-vacancies/84-9-consensus-algorithm.md) (сходство 0.12)
- [20-8-consensus-algorithm](docs/02-anthropic-vacancies/20-8-consensus-algorithm.md) (сходство 0.10)


<!-- see-also -->

---

**Смотрите также:**
- [84-9-consensus-algorithm](docs/02-anthropic-vacancies/84-9-consensus-algorithm.md)
- [22-10-queryresult-structure](docs/02-anthropic-vacancies/22-10-queryresult-structure.md)
- [25-13-reference-implementation](docs/02-anthropic-vacancies/25-13-reference-implementation.md)
- [20-8-consensus-algorithm](docs/02-anthropic-vacancies/20-8-consensus-algorithm.md)

