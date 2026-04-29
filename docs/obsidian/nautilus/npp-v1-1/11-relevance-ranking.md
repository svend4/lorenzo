---
title: "11. Relevance Ranking"
tags:
  - anthropic
  - nautilus
date: 2026-04-29
---

# 11. Relevance Ranking

<!-- summary -->
> > Источник: MHTML‑снимок `Вакансии в Anthropic по кластерам - Claude` (корень репозитория). Раздел диалога — Nautilus Portal Protocol v1.1 RFC, написанный совместно с Claude.

---
<!-- tags: anthropic -->




> Источник: MHTML‑снимок `Вакансии в Anthropic по кластерам - Claude` (корень репозитория). Раздел диалога — Nautilus Portal Protocol v1.1 RFC, написанный совместно с Claude.

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

if q_lower = title_lower:
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

<!-- see-also -->

---

**Смотрите также:**
- [[86-11-relevance-ranking]]
- [[17-appendix-b-change-log]]
- [[09-consensus-algorithm]]
- [[14-sdk]]


<!-- similar-docs -->

---

**Похожие документы:**
- [[86-11-relevance-ranking]] (сходство 0.58)
- [[86-11-relevance-ranking]] (сходство 0.58)
- [[13-reference-implementation]] (сходство 0.34)

