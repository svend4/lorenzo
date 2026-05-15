---
date: 2026-05-15
tags: [memory, rag, orchestration, security, knowledge]
state: normalized
---

# Vector DB Guide — сравнение 12 векторных БД для AI-агентов и RAG

<!-- toc-auto -->
<!-- tags: vector-db-guide, docs -->


<!-- summary -->
> Автор: автор статьи (Хабр) Хабр: https://habr.com/ru/articles/961088/ GitHub: нет (сравнительная статья)
Хабр: https://habr.com/ru/articles/961088/  
GitHub: нет (сравнительная статья)  
Слой: knowledge / memory / ingestion  
Дата: 2025  
Уникальность: Наиболее полное (12 систем) русскоязычное сравнение векторных БД с конкре


> [!NOTE]
> Документ создан на основе исследования. Ссылки ведут на связанные материалы.

<!-- alert-added -->

**Автор:** автор статьи (Хабр)  
**Хабр:** https://habr.com/ru/articles/961088/  
**GitHub:** нет (сравнительная статья)  
**Слой:** knowledge / memory / ingestion  
**Дата:** 2025  
**Уникальность:** Наиболее полное (12 систем) русскоязычное сравнение векторных БД с конкретными рекомендациями по сценарию. Редкий случай: автор даёт чёткие «Когда использовать» вместо безопасного «зависит от задачи».

## Сравнительная матрица (из статьи)

| БД | Сценарий | Особенность |
|----|---------|-------------|
| **ChromaDB** | PoC / MVP | простой старт, встраиваемая |
| **pgvectorscale** | 10M–100M записей + PostgreSQL | TimescaleDB расширение, streaming updates |
| **Qdrant** | production RAG, фильтрация | Rust, payload-фильтры, хорошая производительность |
| **Milvus** | миллиарды записей | distributed, GPU-ускорение |
| **Weaviate** | граф + вектор | GraphQL API, модульные embeddings |
| **LanceDB** | колоночные данные | Apache Arrow, serverless |
| **pgvector** | простой PostgreSQL | без TimescaleDB, до ~5M записей |
| **Redis** | кэш + вектор | низкая латентность |
| **ClickHouse** | аналитика + вектор | ANN поиск в OLAP |
| **Vespa** | гибридный поиск + ранжирование | BM25 + вектор из коробки |
| **Marqo** | end-to-end multimodal | встроенные embeddings |
| **ElasticSearch** | enterprise + вектор | существующий стек |

## Ключевые рекомендации

### По размеру датасета
- **< 1M документов**: ChromaDB или pgvector — без overhead
- **1M–100M**: Qdrant или pgvectorscale (если уже PostgreSQL)
- **> 100M**: Milvus или Vespa

### По типу запроса
- **Только dense vector**: Qdrant, LanceDB
- **Hybrid (BM25 + vector)**: Vespa, Weaviate, ElasticSearch
- **Аналитика + вектор**: ClickHouse

## Что использует Lorenzo сейчас

Lorenzo использует **TF-IDF** + **BM25** (pure Python, без внешней БД).  
`improve_embedding_index.py` — 16472 токенов, в памяти.  
Нет постоянного векторного хранилища — это bottleneck при росте корпуса > 10K карточек.

## Почему важно для Svyazi

| Текущий статус Lorenzo | Следующий шаг |
|------------------------|---------------|
| BM25 + TF-IDF in memory | ChromaDB для PoC |
| 2483 карточки (< 1M) | pgvectorscale при росте |
| Нет гибридного поиска | Vespa / Weaviate при масштабе |

Статья даёт **готовую карту решений** для Итерации 5 (если Svyazi выйдет за рамки Lorenzo).

## Возможные комбинации

| Комбинация | Новое свойство |
|------------|----------------|
| **Vector DB + SocratiCode (R08)** | Qdrant (SocratiCode использует) + Lorenzo corpus → hybrid retrieval |
| **Vector DB + GraphRAG (R09)** | Neo4j (граф) + pgvectorscale (вектор) = полный GraphRAG стек |
| **Vector DB + BI Pattern (R12)** | векторный поиск метаданных таблиц → точный Text-to-SQL |
| **Vector DB + n8n Stack (R10)** | n8n+Qdrant уже в n8n AI Stack — production-ready |

## Контакт

- Статья: https://habr.com/ru/articles/961088/
- Автор: не установлен


## Использование
```bash
# Запуск
python scripts/improve_vector_db_guide.py
```

## Смотрите также
- [Главная](../../../README.md)
- [Метрики](../../../METRICS.md)
- [Здоровье](../../../HEALTH.md)
- [Глоссарий](../../../GLOSSARY.md)
- [Сущности](../../../ENTITIES.md)
