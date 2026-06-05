---
state: approved
---

# 9. Consensus Algorithm

<!-- toc-auto -->
## Contents

- [9. Consensus Algorithm](#9-consensus-algorithm)
  - [9.1. Definition](#91-definition)
  - [9.2. Consensus Structure](#92-consensus-structure)
  - [9.3. v1.1 Consensus Strategy: Real vs Fallback](#93-v11-consensus-strategy-real-vs-fallback)
  - [9.4. Algorithm](#94-algorithm)
  - [9.5. Future Extensions (v2.0+)](#95-future-extensions-v20)
- [Похожие документы](#похожие-документы)
- [Смотрите также](#смотрите-также)
- [Кто ссылается на этот документ (3)](#кто-ссылается-на-этот-документ-3)


> [!NOTE]
> Документ создан на основе исследования. Ссылки ведут на связанные материалы.

<!-- alert-added -->

<!-- abstract-auto -->
> **Абстракт** (авто)
>
> 🎯 **Проблема:** Consensus Algorithm(9-consensus-algorithm) - 9.1.
> ✅ **Результат:** Future Extensions (v2.0+)(95-future-extensions-v20) При query через portal, когда результаты возвращаются из нескольких --- 9.
> 🏷️ **Ключевые слова:** `consensus`, `algorithm`, `fallback`, `query`, `anthropic`, `vacancies`, `через`, `portal`
>


<!-- summary -->
> * Consensus Algorithm - 9.1. * Future Extensions (v2.0+) При query через portal, когда результаты возвращаются из нескольких --- 9 Документ создан на основе исследования.
v1.1 различает два типа coverage:
 — доля repos, вернувших реальные (не fallback) 
  entries, содержащие query
 — доля repos, вернувших любые 
  entries, включая fallback
Концепт считается agreed (полный конс

---
<!-- tags: rag, anthropic -->




## 9. Consensus Algorithm

### 9.1. Definition

При query через portal, когда результаты возвращаются из нескольких 
Repos, portal MUST вычислять **консенсус** — степень согласованности 
концепта между Repos.

### 9.2. Consensus Structure

Portal MUST возвращать Consensus объект со следующими полями:

```python
@dataclass
class Consensus:
    present_in: list[str]             # repos с real entries
    present_in_fallback: list[str]    # repos только с fallback
    missing_in: list[str]             # repos без entries
    coverage: float                   # len(present_in) / total_repos
    coverage_with_fallback: float     # включая fallback
    agreed: bool                      # coverage == 1.0
```

### 9.3. v1.1 Consensus Strategy: Real vs Fallback

v1.1 различает два типа coverage:

- **`coverage`** — доля repos, вернувших **реальные** (не fallback) 
  entries, содержащие query
- **`coverage_with_fallback`** — доля repos, вернувших **любые** 
  entries, включая fallback

Концепт считается **agreed** (полный консенсус), если 
`coverage == 1.0`.

### 9.4. Algorithm

Pseudo-code:

```python
def compute_consensus(
    query: str,
    results_by_repo: dict[str, list[PortalEntry]]
) -> Consensus:
    total_repos = len(results_by_repo)
    
    present_in = []
    present_in_fallback = []
    missing_in = []
    
    for repo_name, entries in results_by_repo.items():
        real_matches = [
            e for e in entries 
            if not e.is_fallback 
            and query_matches(query, e)
        ]
        fallback_matches = [
            e for e in entries
            if e.is_fallback
            and query_matches(query, e)
        ]
        
        if real_matches:
            present_in.append(repo_name)
        elif fallback_matches:
            present_in_fallback.append(repo_name)
        else:
            missing_in.append(repo_name)
    
    coverage = len(present_in) / total_repos
    coverage_with_fallback = (
        len(present_in) + len(present_in_fallback)
    ) / total_repos
    
    return Consensus(
        present_in=present_in,
        present_in_fallback=present_in_fallback,
        missing_in=missing_in,
        coverage=coverage,
        coverage_with_fallback=coverage_with_fallback,
        agreed=(coverage == 1.0)
    )
```

### 9.5. Future Extensions (v2.0+)

v2.0 MAY использовать:

- Semantic similarity через embeddings (cross-lingual matching)
- Weighted consensus (разный вес от confidence адаптера)
- Fuzzy matching с configurable threshold

Эти расширения не breaking — они будут активироваться через 
`algorithm` параметр в query, сохраняя v1.1 как default.

---

<!-- similar-docs -->

---

## Похожие документы
- [20-8-consensus-algorithm](20-8-consensus-algorithm.md) (сходство 0.34)
- [86-11-relevance-ranking](86-11-relevance-ranking.md) (сходство 0.12)


<!-- see-also -->

---

## Смотрите также
- [20-8-consensus-algorithm](20-8-consensus-algorithm.md)
- [86-11-relevance-ranking](86-11-relevance-ranking.md)
- [85-10-query-flow](85-10-query-flow.md)
- [129-примеры-запросов-в-claude](129-примеры-запросов-в-claude.md)


<!-- backlinks -->

---

## Кто ссылается на этот документ (3)
- [129-примеры-запросов-в-claude](129-примеры-запросов-в-claude.md)
- [21-9-query-flow](21-9-query-flow.md)
- [README](README.md)

