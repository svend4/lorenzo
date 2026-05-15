---
date: 2026-05-15
tags: [rag, orchestration, knowledge, ingestion, architecture]
state: normalized
---

# Agentic Graph RAG: Skeleton Indexing + VectorCypher + PyMangle Datalog

<!-- toc-auto -->
<!-- tags: agentic-graph-rag-skeleton-indexing-pymangle, docs -->


<!-- summary -->
> `agentic-graph-rag-skeleton-indexing-pymangle` — раздел документации проекта Lorenzo.


> [!NOTE]
> Документ создан на основе исследования. Ссылки ведут на связанные материалы.

<!-- alert-added -->

**Автор:** VladSpace  
**Хабр:** https://habr.com/ru/articles/1003064/  
**GitHub:** https://github.com/vpakspace/agentic-graph-rag  
**Слой:** knowledge / orchestration  
**Дата:** февраль 2026  
**Уникальность:** Graph RAG с 96.7% точностью на билингвальном бенчмарке. Skeleton Indexing — выборочное извлечение сущностей только из top-25% чанков по PageRank (радикально снижает шум в графе). VectorCypher Retrieval комбинирует embedding-поиск с Cypher-траверсалом в одном запросе. Реимплементация Datalog-движка PyMangle (2919 строк) для декларативного рассуждения с полным provenance-трейсингом. 16 206 строк Python, 586 тестов.

## Проблема: стандартный Graph RAG шумный и медленный

```
Наивный Graph RAG:
  → Извлечь сущности из ВСЕХ чанков → граф с тысячами шумных узлов
  → Vector search + отдельный Cypher запрос → 2 round-trips к Neo4j
  → LLM рассуждение над графом: непрозрачно, нет provenance

Skeleton Indexing решает шум:
  → PageRank по чанкам → top-25% информационно плотных
  → Только они участвуют в извлечении сущностей
  → Граф в 4× меньше, точность выше

VectorCypher решает latency:
  → 1 запрос к Neo4j: embedding search + граф-траверсал
  → Neo4j vector index + native Cypher в одном вызове

PyMangle решает непрозрачность:
  → Datalog: декларативные правила вывода
  → Каждый шаг рассуждения: провenance + trace
```

## Skeleton Indexing: PageRank фильтрация чанков

```python
# github.com/vpakspace/agentic-graph-rag

import networkx as nx
import numpy as np
from typing import NamedTuple

class Chunk(NamedTuple):
    id: str
    text: str
    pagerank_score: float = 0.0

class SkeletonIndexer:
    """
    Ключевая инновация: не все чанки равны.
    Top-25% по PageRank → "скелет" документа → извлечение сущностей только из них.
    """

    def __init__(self, top_pct: float = 0.25):
        self.top_pct = top_pct

    def build_chunk_graph(self, chunks: list[Chunk]) -> nx.DiGraph:
        """
        Построить граф смежности чанков: чанки с общими терминами связаны.
        Позволяет PageRank найти информационно центральные чанки.
        """
        G = nx.DiGraph()
        for chunk in chunks:
            G.add_node(chunk.id, text=chunk.text)

        # Связать чанки с пересечением ключевых слов
        for i, c1 in enumerate(chunks):
            words1 = set(c1.text.lower().split())
            for c2 in chunks[i+1:]:
                words2 = set(c2.text.lower().split())
                overlap = len(words1 & words2) / max(len(words1), len(words2))
                if overlap > 0.15:  # порог схожести
                    G.add_edge(c1.id, c2.id, weight=overlap)
                    G.add_edge(c2.id, c1.id, weight=overlap)

        return G

    def select_skeleton_chunks(self, chunks: list[Chunk]) -> list[Chunk]:
        """
        Запустить PageRank → выбрать top-25% информационно плотных чанков.
        """
        G = self.build_chunk_graph(chunks)
        pagerank = nx.pagerank(G, weight="weight")

        # Назначить PageRank scores
        ranked_chunks = [
            chunk._replace(pagerank_score=pagerank.get(chunk.id, 0))
            for chunk in chunks
        ]
        ranked_chunks.sort(key=lambda c: c.pagerank_score, reverse=True)

        # Top-25%
        top_n = max(1, int(len(chunks) * self.top_pct))
        skeleton = ranked_chunks[:top_n]

        print(f"Skeleton: {len(skeleton)}/{len(chunks)} чанков → "
              f"извлечение сущностей из {self.top_pct*100:.0f}%")
        return skeleton

    def extract_entities_from_skeleton(self,
                                        skeleton: list[Chunk]) -> list[dict]:
        """
        LLM извлечение сущностей только из скелетных чанков.
        Результат: чистый граф без шумных периферийных упоминаний.
        """
        entities = []
        for chunk in skeleton:
            extracted = self.llm.extract_entities(
                text=chunk.text,
                prompt=ENTITY_EXTRACTION_PROMPT
            )
            for entity in extracted:
                entity["source_chunk"] = chunk.id
                entity["source_pagerank"] = chunk.pagerank_score
            entities.extend(extracted)
        return entities
```

## VectorCypher: поиск и граф за один запрос

```python
from neo4j import GraphDatabase
from langchain_openai import OpenAIEmbeddings

class VectorCypherRetriever:
    """
    1 запрос к Neo4j = embedding поиск + граф-траверсал.
    Neo4j vector index + native Cypher в одном вызове.
    Устраняет 2 round-trips стандартного подхода.
    """

    def __init__(self, uri: str, auth: tuple):
        self.driver = GraphDatabase.driver(uri, auth=auth)
        self.embedder = OpenAIEmbeddings(model="text-embedding-3-small")

    def retrieve(self, query: str, top_k: int = 10,
                  hops: int = 2) -> list[dict]:
        """
        VectorCypher: найти похожие узлы + обойти граф за 1 запрос.
        """
        query_embedding = self.embedder.embed_query(query)

        cypher = """
        // Шаг 1: Vector similarity search (Neo4j vector index)
        CALL db.index.vector.queryNodes(
            'phrase-embeddings',
            $top_k,
            $query_embedding
        ) YIELD node AS seed_node, score AS similarity

        // Шаг 2: Граф-траверсал от найденных узлов (без доп. round-trip)
        MATCH path = (seed_node)-[:RELATED_TO*1..{hops}]-(neighbor)
        WHERE neighbor:PhraseNode OR neighbor:PassageNode

        // Шаг 3: Вернуть всё в одном ответе
        RETURN
            seed_node.text AS seed_text,
            similarity,
            collect(DISTINCT neighbor.text) AS context_nodes,
            collect(DISTINCT [r IN relationships(path) | type(r)]) AS relation_types
        ORDER BY similarity DESC
        LIMIT $top_k
        """

        with self.driver.session() as session:
            result = session.run(cypher.format(hops=hops), {
                "top_k": top_k,
                "query_embedding": query_embedding
            })
            return [record.data() for record in result]
```

## PyMangle: Datalog движок для декларативного рассуждения

```python
class PyMangleDatalog:
    """
    Реимплементация Datalog-движка (2919 строк Python).
    Декларативные правила вывода + полный provenance-трейсинг.

    Почему Datalog, а не LLM-рассуждение:
    → Детерминированный вывод (нет галлюцинаций)
    → Полный trace: как пришли к выводу
    → Переиспользуемые правила (не зависят от модели)
    """

    # Пример Datalog правил для рассуждения по графу знаний
    SAMPLE_RULES = """
    % Правило: кто является автором через цепочку связей
    authored_by(X, Author) :-
        paper(X),
        wrote(Author, X).

    % Правило: транзитивная "цитирует"
    cites_transitively(A, B) :-
        cites(A, B).
    cites_transitively(A, C) :-
        cites(A, B),
        cites_transitively(B, C).

    % Правило: релевантные документы через общие концепты
    related_documents(D1, D2) :-
        mentions_concept(D1, C),
        mentions_concept(D2, C),
        D1 != D2.
    """

    def query(self, rules: str, facts: list[tuple],
               goal: str) -> list[dict]:
        """
        Выполнить Datalog запрос с provenance.

        Args:
            rules: Datalog правила (текст)
            facts: список (predicate, arg1, arg2, ...)
            goal: целевой предикат для поиска

        Returns:
            Список решений с полным trace derivation
        """
        program = self._parse_program(rules)
        database = self._load_facts(facts)
        solutions = self._semi_naive_evaluation(program, database, goal)

        return [
            {
                "solution": sol.bindings,
                "provenance": sol.derivation_tree,  # полный trace
                "depth": sol.derivation_depth
            }
            for sol in solutions
        ]

    def explain(self, solution: dict) -> str:
        """
        Человекочитаемое объяснение вывода.
        Каждый шаг рассуждения прослеживается.
        """
        tree = solution["provenance"]
        return self._render_derivation_tree(tree)
```

## Dual-node граф: PhraseNode + PassageNode

```python
NEO4J_SCHEMA = {
    "nodes": {
        "PhraseNode": {
            "properties": ["text", "embedding", "pagerank_score", "source_doc"],
            "description": "Именованные сущности и ключевые фразы",
            "vector_index": "phrase-embeddings"
        },
        "PassageNode": {
            "properties": ["text", "embedding", "chunk_id", "pagerank_score"],
            "description": "Текстовые чанки из скелета документа",
            "vector_index": "passage-embeddings"
        }
    },
    "relationships": [
        "RELATED_TO",      # фраза связана с фразой
        "MENTIONED_IN",    # фраза упомянута в чанке
        "CITES",          # чанк цитирует другой
        "DEFINES",        # чанк определяет фразу
    ]
}

BENCHMARK_RESULTS = {
    "dataset": "Билингвальный (RU + EN), собственный бенчмарк",
    "total_questions": 180,

    "modes": {
        "Vector":      {"correct": 160, "accuracy": 0.889},
        "Hybrid":      {"correct": 174, "accuracy": 0.967},  # победитель
        "Agent(Mangle)": {"correct": 180, "accuracy": 1.000, "note": "только простые вопросы"},
        "Baseline_RAG": {"correct": 131, "accuracy": 0.728}
    },

    "stack": {
        "llm": ["GPT-4o", "GPT-4o-mini"],
        "embeddings": "text-embedding-3-small (1536 dim)",
        "graph_db": "Neo4j 5.x",
        "api": "FastAPI + FastMCP",
        "datalog": "PyMangle (2919 строк, реимплементация)",
        "tests": 586,
        "code_lines": 16_206
    }
}
```

## Каскадная маршрутизация запросов

```python
class CascadeQueryRouter:
    """
    Маршрутизация по типу вопроса: Datalog → LLM → regex.
    Каждый уровень дешевле и быстрее предыдущего.
    """

    def route(self, query: str, graph_context: list[dict]) -> dict:
        # Уровень 1: Datalog (детерминированный, быстро)
        datalog_result = self.mangle.query(
            rules=STANDARD_RULES,
            facts=self._context_to_facts(graph_context),
            goal="answer"
        )
        if datalog_result:
            return {"answer": datalog_result[0], "mode": "datalog",
                    "provenance": datalog_result[0]["provenance"]}

        # Уровень 2: LLM над графом
        llm_result = self.llm.reason_over_graph(query, graph_context)
        if llm_result["confidence"] > 0.8:
            return {"answer": llm_result, "mode": "llm"}

        # Уровень 3: Regex/BM25 fallback
        return {"answer": self.bm25.search(query), "mode": "fallback"}
```

## Применение к Lorenzo

```python
# Lorenzo использует BM25 + TF-IDF для поиска.
# Skeleton Indexing + VectorCypher = следующий уровень.

class LorenzoGraphRAG:
    """
    Обогатить Lorenzo поисковый индекс Neo4j графом концептов.
    Skeleton Indexing: PageRank по docs → top-25% → граф знаний.
    """

    def build_graph_from_docs(self, docs_dir: str):
        # 1. Загрузить документы, разбить на чанки
        chunks = self.chunker.chunk_directory(docs_dir)

        # 2. Skeleton Indexing: PageRank → top-25%
        skeleton = self.indexer.select_skeleton_chunks(chunks)

        # 3. Извлечь сущности только из скелета
        entities = self.indexer.extract_entities_from_skeleton(skeleton)

        # 4. Загрузить в Neo4j с embeddings
        self.loader.load_to_neo4j(entities, chunks)

    def search(self, query: str) -> list[dict]:
        # VectorCypher: 1 запрос вместо 2
        return self.retriever.retrieve(query, top_k=10, hops=2)
```

## Возможные комбинации

| Комбинация | Новое свойство |
|------------|----------------|
| **Graph RAG + Wikontic (R01)** | Wikontic семантический граф + Skeleton Indexing = более чистый граф знаний |
| **Graph RAG + LangFuse (R38)** | PyMangle provenance → LangFuse trace: аудитируемый вывод |
| **Graph RAG + Enterprise RAG МТС (R32)** | Skeleton Indexing для корпоративных документов МТС |
| **Graph RAG + Coreness Flow (R30)** | Composable ретриверы: VectorCypher как один из heads |
| **Graph RAG + Lorenzo Gateway** | /api/ask → Graph RAG вместо BM25: structured provenance в ответах |

## Контакт

- Статья: https://habr.com/ru/articles/1003064/ (февраль 2026)
- GitHub: https://github.com/vpakspace/agentic-graph-rag (16K строк, 586 тестов)
- Neo4j vector index: neo4j.com/docs/cypher-manual/current/indexes/semantic-indexes/vector-indexes/
- Смежная (GraphRAG production): habr.com/ru/articles (R09, R22)
- Смежная (финансовый RAG с 4 головами): https://habr.com/ru/articles/963482/

## Смотрите также
- [Главная](../../../README.md)
- [Метрики](../../../METRICS.md)
- [Здоровье](../../../HEALTH.md)
- [Глоссарий](../../../GLOSSARY.md)
- [Сущности](../../../ENTITIES.md)
- [Решения](../../../DECISIONS.md)
