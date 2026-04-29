# 8. Consensus Algorithm (v1.0: string normalization)

<!-- summary -->
> > Источник: MHTML‑снимок `Вакансии в Anthropic по кластерам - Claude` (корень репозитория). Раздел диалога — Nautilus Portal Protocol v1.0.0-draft RFC (более ранняя версия v1.1).

---
<!-- tags: rag, anthropic -->




> Источник: MHTML‑снимок `Вакансии в Anthropic по кластерам - Claude` (корень репозитория). Раздел диалога — Nautilus Portal Protocol v1.0.0-draft RFC (более ранняя версия v1.1).

## 8. Consensus Algorithm

### 8.1. Definition

Когда один query возвращает результаты из нескольких Repos, Portal 
вычисляет consensus — степень согласованности концепции между Repos.

### 8.2. v1.0 Consensus Strategy: String Normalization

v1.0 использует простое string matching после normalization:

def normalize(title: str) -> str:
return title.lower().strip().translate(PUNCT_STRIP)

def similar(a: str, b: str) -> bool:
return normalize(a) = normalize(b)

Два entry считаются одним концептом, если их `title` после 
normalization совпадают.

### 8.3. Consensus Categories

Для каждого уникального концепта, найденного в results:

- **Full Consensus**: концепт присутствует в **всех** Repos, 
опрошенных в query
- **Partial Consensus**: концепт в 2+ Repos, но не во всех
- **Singular**: концепт только в одном Repo

### 8.4. Coverage Ratio

Дополнительный метрический показатель:

coverage_ratio = len(full_consensus) / total_unique_concepts

Значение близко к 1.0 означает высокую согласованность экосистемы 
по данному query. Близко к 0 — query попал в area, где Repos 
расходятся.

### 8.5. Future Extensions (v2.0+)

Будущие версии MAY использовать:

- Semantic similarity через embeddings (cross-lingual matching)
- Fuzzy matching с threshold
- Weighted consensus (разный вес от confidence adapter'а)

Эти расширения не breaking — они активируются через `algorithm` 
параметр в query, сохраняя v1.0 как default.

---

<!-- see-also -->

---

**Смотрите также:**
- [20-8-consensus-algorithm](docs/02-anthropic-vacancies/20-8-consensus-algorithm.md)
- [09-consensus-algorithm](docs/nautilus/npp-v1-1/09-consensus-algorithm.md)
- [84-9-consensus-algorithm](docs/02-anthropic-vacancies/84-9-consensus-algorithm.md)
- [10-query-result](docs/nautilus/npp-v1-0/10-query-result.md)

