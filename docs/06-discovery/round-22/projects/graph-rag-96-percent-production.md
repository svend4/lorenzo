---
date: 2026-05-15
tags: [memory, rag, orchestration, knowledge, ingestion]
state: normalized
---

# Graph RAG 96.7% — production пайплайн из 5 научных статей за 5 дней

<!-- toc-auto -->
<!-- tags: graph-rag-96-percent-production, docs -->


<!-- summary -->
> Автор: независимый исследователь (Хабр) Хабр: https://habr.com/ru/articles/1003064/
Хабр: https://habr.com/ru/articles/1003064/  
GitHub: не опубликован (полная архитектура + код в статье)  
Слой: knowledge / orchestration / memory  
Дата: 2025  
Уникальность: Практический production-кейс: 5


> [!NOTE]
> Документ создан на основе исследования. Ссылки ведут на связанные материалы.

<!-- alert-added -->

**Автор:** независимый исследователь (Хабр)  
**Хабр:** https://habr.com/ru/articles/1003064/  
**GitHub:** не опубликован (полная архитектура + код в статье)  
**Слой:** knowledge / orchestration / memory  
**Дата:** 2025  
**Уникальность:** Практический production-кейс: 5 техник из последних научных статей → единый Graph RAG пайплайн → 96.7% точность (174/180) на двуязычном бенчмарке. Ключевые инновации: Neo4j + двухуровневые ноды (PhraseNode + PassageNode), cascading fallback retrieval (5 стратегий), декларативный reasoning engine.

## Метрики результата

```
Бенчмарк: 180 вопросов (RU + EN, bilingual)
Точность: 174/180 = 96.7%

По режимам retrieval:
  vector_search:        100% (30/30 вопросов)
  cypher_traverse:      100% (30/30)
  hybrid_search:        100% (30/30)
  comprehensive_search:  93% (28/30)
  full_document_read:    93% (28/30)
  fallback_chain:       97% avg

Zero persistent failures: все неверные ответы исправимы переформулировкой
```

## Архитектура Neo4j: двухуровневые ноды

```
Два типа нод:
  PhraseNode  = сущность (с embedding)
    properties: {name, type, pagerank_score, embedding: float[768]}
    e.g.: {name: "AgentFS", type: "PROJECT", pagerank: 0.89}

  PassageNode = текстовый чанк (с embedding)
    properties: {text, source, chunk_id, embedding: float[768]}
    e.g.: {text: "AgentFS хранит факты...", source: "agentfs.md"}

Рёбра:
  (PhraseNode) -[:MENTIONED_IN]-> (PassageNode)
  (PhraseNode) -[:RELATED_TO {weight: float}]-> (PhraseNode)
  (PhraseNode) -[:CO_OCCURS_WITH {count: int}]-> (PhraseNode)
```

Это позволяет делать запросы двух типов: **семантический** (через embedding) и **структурный** (через граф).

## Cascading Fallback: 5 стратегий retrieval

```python
RETRIEVAL_STRATEGIES = [
    "vector_search",       # быстрый: FRIDA embedding cosine
    "cypher_traverse",     # граф: MATCH (p:Phrase)-[:MENTIONED_IN]->(passage)
    "hybrid_search",       # BM25 + vector + RRF fusion
    "comprehensive_search",# расширить запрос + multi-hop traversal
    "full_document_read",  # последний resort: прочитать весь документ
]

def retrieve_with_fallback(query: str, threshold=0.7) -> list[Passage]:
    for strategy in RETRIEVAL_STRATEGIES:
        results = apply_strategy(strategy, query)
        quality_score = evaluate_relevance(results, query)  # LLM judge

        if quality_score >= threshold:
            return results  # качество достигнуто

        # иначе → следующая стратегия (escalate)
    return []  # fallback полностью не сработал (редко)
```

## Declarative Reasoning Engine

```python
# Не hardcoded логика — декларативные правила:
REASONING_RULES = {
    "comparison": {
        "pattern": "сравни|какой лучше|разница между",
        "strategy": "comprehensive_search",
        "require_multi_doc": True,
    },
    "factual": {
        "pattern": "кто|что|когда|где",
        "strategy": "vector_search",
        "require_multi_doc": False,
    },
    "analytical": {
        "pattern": "почему|как работает|объясни",
        "strategy": "hybrid_search",
        "require_multi_doc": True,
    }
}

# Маршрутизация автоматически по типу вопроса
query_type = classify_query(user_question)  # LLM classifier
strategy = REASONING_RULES[query_type]["strategy"]
```

## 5 научных статей в основе

| Статья | Техника | Применено |
|--------|---------|-----------|
| Microsoft GraphRAG | Community summaries | глобальный контекст |
| HippoRAG (2024) | PageRank для нод | pagerank_score в PhraseNode |
| RAPTOR (2023) | Иерархические чанки | PassageNode levels |
| Self-RAG (2023) | [IsRel] оценка | quality_score в fallback |
| CRAG (2024) | Corrective retrieval | web search при низком качестве |

## Сравнение с baseline

```
Naive RAG (vector only):     78% точность
Advanced RAG (hybrid):       85% точность
GraphRAG (Microsoft):        88% точность
Graph RAG (эта статья):     96.7% точность ← +8.7% vs Microsoft GraphRAG
```

## Построен за 5 дней: timeline

```
День 1: Прочитать 5 статей + выбрать техники + спроектировать схему Neo4j
День 2: Загрузить данные + построить граф (PhraseNode + PassageNode)
День 3: Реализовать 5 стратегий retrieval + fallback chain
День 4: Declarative Reasoning Engine + LLM judge для quality score
День 5: Бенчмарк 180 вопросов + анализ ошибок + документация
```

## Применение к Lorenzo

Lorenzo имеет `improve_concept_graph.py` → Mermaid/DOT/JSON.  
Upgrade path:

```python
# Сейчас: CONCEPT_GRAPH.md (Mermaid, статичный)
# Следующий шаг:

from neo4j import GraphDatabase

def ingest_to_neo4j(concept_graph_json: dict):
    """Lorenzo CONCEPT_GRAPH.md → Neo4j PhraseNode/PassageNode"""
    for concept in concept_graph_json["concepts"]:
        tx.run("""
            MERGE (p:PhraseNode {name: $name})
            SET p.type = $type, p.embedding = $embedding
        """, name=concept["name"], type=concept["type"],
             embedding=frida_embed(concept["name"]))

# Результат: SPARQL-style queries по Svyazi knowledge graph
# "Найди все проекты связанные с voice + edge AI" → cypher_traverse
```

Связь с Sberbank KG (R17): их Apache Jena → здесь Neo4j, идеи похожи но разные стеки.

## Возможные комбинации

| Комбинация | Новое свойство |
|------------|----------------|
| **Graph RAG + FRIDA (R18)** | FRIDA embeddings для PhraseNode/PassageNode в Neo4j |
| **Graph RAG + Agentic RAG (R18)** | Agentic петля выбирает стратегию из 5 fallback-режимов |
| **Graph RAG + Sberbank KG (R17)** | Sberbank KG паттерн + Neo4j (вместо Apache Jena) |
| **Graph RAG + Lorenzo concept_graph** | CONCEPT_GRAPH.md → Neo4j → 96.7% точность Q&A |
| **Graph RAG + RAG Eval (R16)** | RAGAS оценивает каждую из 5 стратегий отдельно |

## Контакт

- Статья: https://habr.com/ru/articles/1003064/ (2025)
- Neo4j: https://github.com/neo4j/neo4j (Enterprise/Community Edition)
- HippoRAG: arxiv.org/abs/2405.14831
- Self-RAG: arxiv.org/abs/2310.11511
- RAPTOR: arxiv.org/abs/2401.18059
- Смежная (GraphRAG теория): https://habr.com/ru/articles/871700/

## Смотрите также
- [Главная](../../../README.md)
- [Метрики](../../../METRICS.md)
- [Здоровье](../../../HEALTH.md)
- [Глоссарий](../../../GLOSSARY.md)
- [Сущности](../../../ENTITIES.md)
