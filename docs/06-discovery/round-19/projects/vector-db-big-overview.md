---
date: 2026-05-15
tags: [memory, rag, orchestration, knowledge, ingestion]
state: normalized
---

# Выбираем векторную БД для AI-агентов и RAG — большой обзор 2025

<!-- toc-auto -->
<!-- tags: vector-db-big-overview, docs -->


<!-- summary -->
> Следующий шаг: Qdrant embedded (без сервера, встроен в процесс): LanceDB — альтернатива: Lance-формат, работает как SQLite (файл на диске).
 
LanceDB — альтернатива: Lance-формат, работает как SQLite (файл на диске).


> [!TIP]
> Документ содержит практические рекомендации и лучшие практики.

<!-- alert-added -->

**Автор:** независимый исследователь (Хабр, ноябрь 2025)  
**Хабр:** https://habr.com/ru/articles/961088/  
**GitHub:** не указан (сравнительный анализ + рекомендации)  
**Слой:** knowledge / memory / ingestion  
**Дата:** ноябрь 2025  
**Уникальность:** Самый полный русскоязычный обзор векторных СУБД для AI-систем в 2025: 12+ баз данных (Milvus, Qdrant, Weaviate, ChromaDB, pgvector, Redis, pgvectorscale, LanceDB, ClickHouse, Vespa, Marqo, ElasticSearch) с конкретными рекомендациями под сценарии. Впервые на русском описан сценарий agent memory storage.

## Карта 12+ векторных баз данных

```
Специализированные (vector-first):
  ├── Qdrant     — production-ready, Rust, отличная фильтрация
  ├── Milvus     — enterprise, масштаб, сложный деплой
  ├── Weaviate   — гибридный поиск из коробки, GraphQL
  ├── LanceDB    — Lance-формат, работает без сервера (embedded)
  └── Marqo      — multimodal из коробки (текст + изображения)

PostgreSQL-based:
  ├── pgvector   — расширение PG, production, простота
  ├── pgvectorscale — Timescale, конкурентен с Qdrant на 10-100M
  └── ClickHouse — аналитика + векторный поиск

Многофункциональные:
  ├── ChromaDB   — pip install chromadb, 3 строки кода → работает
  ├── Redis      — in-memory, низкая латентность, ephemeral
  ├── ElasticSearch — BM25 + векторный гибрид, legacy enterprise
  └── Vespa      — Yahoo open source, масштаб + типизация
```

## Рекомендации по сценариям

| Сценарий | Лучший выбор | Почему |
|---------|-------------|--------|
| Начало с нуля | **Qdrant** | простой деплой, отличная фильтрация, Rust |
| PoC / MVP / демо | **ChromaDB** | pip install, 3 строки, работает локально |
| Уже есть PostgreSQL | **pgvectorscale** | конкурентен с Qdrant на 10-100M, JOIN + ACID |
| Масштаб >1B векторов | **Milvus** | designed for scale (но сложный деплой) |
| Гибридный поиск | **Qdrant** или **Weaviate** | встроенный BM25 + dense |
| Multimodal (текст+фото) | **Marqo** | мультимодальный индекс из коробки |
| Agent memory (быстро) | **Redis** | in-memory, <1ms latency, ephemeral |
| Аналитика + поиск | **ClickHouse** | SQL + vector = единая система |

## Детали — Qdrant (рекомендуемый)

```python
from qdrant_client import QdrantClient
from qdrant_client.models import Distance, VectorParams, PointStruct

client = QdrantClient(":memory:")  # или url="http://localhost:6333"

# Создать коллекцию
client.create_collection(
    collection_name="lorenzo_docs",
    vectors_config=VectorParams(size=768, distance=Distance.COSINE)
)

# Добавить векторы с payload
client.upsert(
    collection_name="lorenzo_docs",
    points=[
        PointStruct(
            id=1,
            vector=embedding,  # FRIDA (R18) output
            payload={"path": "docs/01-svyazi/...", "section": "memory", "wc": 450}
        )
    ]
)

# Поиск с фильтрацией
results = client.search(
    collection_name="lorenzo_docs",
    query_vector=query_embedding,
    query_filter={"must": [{"key": "section", "match": {"value": "memory"}}]},
    limit=5
)
```

## Квантизация векторов (экономия памяти)

```
768-dim float32 = 3072 bytes/вектор
  ↓ scalar quantization (int8)
768-dim int8    =  768 bytes/вектор  (-75%)
  ↓ binary quantization
768-dim binary  =   96 bytes/вектор  (-97%)

На 2.5M векторов (Lorenzo-scale × 1000):
  float32:  ~7.5 GB RAM
  int8:     ~1.9 GB RAM
  binary:   ~240 MB RAM  ← агент может держать в памяти
```

Qdrant и Weaviate поддерживают все три режима.

## Гибридный поиск: BM25 + Dense

```
Запрос: "AgentFS файловая система для агента"
  ↓
BM25: находит "AgentFS" (точное совпадение) → высокий ранг
Dense: находит семантически близкое "filesystem for LLM" → средний ранг
  ↓
RRF fusion: AgentFS #1 (в обоих), "knowledge-space" #2 (только dense)
```

**Гибрид > чистый dense** для специализированных терминов (названия проектов, авторов).

## Применение к Lorenzo

Lorenzo сейчас: TF-IDF матрица в памяти Python процесса.  
Следующий шаг: **Qdrant embedded** (без сервера, встроен в процесс):

```python
# В improve_embedding_index.py:
from qdrant_client import QdrantClient
client = QdrantClient(path="./qdrant_data")  # embedded, без сервера

# FRIDA (R18) → Qdrant → hybrid search
# Фильтрация по section, author, date — бесплатно в Qdrant
```

LanceDB — альтернатива: Lance-формат, работает как SQLite (файл на диске).

## Возможные комбинации

| Комбинация | Новое свойство |
|------------|----------------|
| **Qdrant + FRIDA (R18)** | FRIDA embeddings → Qdrant → нейронный поиск по Lorenzo |
| **Qdrant + Agentic RAG (R18)** | Qdrant payload filter в retrieval-петле агента |
| **Qdrant + Sberbank KG (R17)** | Hybrid: Qdrant (вектор) + Apache Jena (граф) |
| **LanceDB + Lorenzo embedded** | Без сервера: LanceDB файл как замена search_index.json |
| **pgvectorscale + audit.db** | Один PostgreSQL: SQLite audit.db → PG + pgvector |
| **Weaviate + RAG Eval (R16)** | RAGAS оценивает качество Weaviate hybrid search |

## Контакт

- Статья: https://habr.com/ru/articles/961088/ (ноябрь 2025)
- Qdrant: https://github.com/qdrant/qdrant (Apache 2.0, Rust)
- Weaviate: https://github.com/weaviate/weaviate (BSD-3)
- LanceDB: https://github.com/lancedb/lancedb (Apache 2.0)
- ChromaDB: https://github.com/chroma-core/chroma (Apache 2.0)
- Milvus: https://github.com/milvus-io/milvus (Apache 2.0)
- ANN Benchmarks: ann-benchmarks.com

## Смотрите также
- [Главная](../../../README.md)
- [Метрики](../../../METRICS.md)
- [Здоровье](../../../HEALTH.md)
- [Глоссарий](../../../GLOSSARY.md)
- [Сущности](../../../ENTITIES.md)
