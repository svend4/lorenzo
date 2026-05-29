---
date: 2026-05-29
tags: [memory, rag, orchestration, security, knowledge]
state: normalized
---

# RAG своими руками: гибридный поиск для корпоративного AI-помощника МТС

<!-- toc-auto -->
<!-- tags: mts-enterprise-rag-hybrid-search, docs -->


<!-- summary -->
> Автор: Илья Парамошин (iliadev), МТС Хабр: https://habr.com/ru/companies/ru_mts/articles/970476/
Хабр: https://habr.com/ru/companies/ru_mts/articles/970476/  
GitHub: не опубликован (production-система МТС)  
Слой: ingestion / orchestration / knowledge  
Дата: декабрь 2025  
Уникальность: Редкий enterprise


> [!WARNING]
> Документ содержит описание рисков и ограничений. Изучите их перед принятием архитектурных решений.

<!-- alert-added -->

**Автор:** Илья Парамошин (iliadev), МТС  
**Хабр:** https://habr.com/ru/companies/ru_mts/articles/970476/  
**GitHub:** не опубликован (production-система МТС)  
**Слой:** ingestion / orchestration / knowledge  
**Дата:** декабрь 2025  
**Уникальность:** Редкий enterprise RAG с точной формулой гибридного ранжирования: `0.7×vector_score + 0.3×bm25_score` + многомерные буст-факторы (заголовок ×1.2, свежесть ×1.1, подтверждённые решения ×1.5). Полностью локальное развёртывание (BGE-m3 + Cotype Pro 2) без утечки данных. Zero-downtime инкрементальная индексация через content-hash.

## Проблема: корпоративный поиск знаний в МТС

```
Исходная ситуация:
  → Confluence: тысячи страниц документации
  → Jira: история инцидентов и решений
  → Сотрудники поддержки: 15-30 мин на поиск ответа
  → LLM без контекста: галлюцинирует корпоративную специфику

Требования к решению:
  → Данные не покидают контур МТС (152-ФЗ + корпоративная безопасность)
  → Права доступа как в Confluence/Jira (нельзя видеть чужие проекты)
  → Актуальность: изменения в базе знаний → сразу в поиске
  → Гибридность: точные совпадения (BM25) + семантика (векторный)
```

## Гибридная формула ранжирования

```python
class HybridRanker:
    """
    Ключевая инновация МТС: не просто BM25 + vector,
    а многомерные буст-факторы поверх базовой формулы.
    """

    # Базовые веса (подобраны на A/B тестах)
    VECTOR_WEIGHT = 0.7   # семантика важнее для смысловых вопросов
    BM25_WEIGHT   = 0.3   # но точные совпадения тоже критичны (имена, коды)

    # Буст-факторы
    TITLE_BOOST    = 1.2   # совпадение в заголовке > в теле
    FRESHNESS_BOOST = 1.1  # недавно обновлённые документы предпочтительнее
    SOLUTION_BOOST  = 1.5  # подтверждённые решения (флаг в Confluence)

    def score(self, doc: Document, query: str,
              vector_score: float, bm25_score: float) -> float:
        # Базовый гибридный скор
        base_score = (
            self.VECTOR_WEIGHT * vector_score +
            self.BM25_WEIGHT   * bm25_score
        )

        # Применить буст-факторы
        boost = 1.0
        if self._query_matches_title(query, doc.title):
            boost *= self.TITLE_BOOST
        if self._is_fresh(doc.updated_at, days_threshold=30):
            boost *= self.FRESHNESS_BOOST
        if doc.is_confirmed_solution:
            boost *= self.SOLUTION_BOOST

        return base_score * boost

    def _is_fresh(self, updated_at: datetime, days_threshold: int) -> bool:
        delta = datetime.utcnow() - updated_at
        return delta.days <= days_threshold
```

## Стек: полностью on-premise

```python
MTSRAG_STACK = {
    "embeddings": {
        "model": "BGE-m3",                    # multilingual, RU+EN
        "deployment": "внутри контура МТС",   # никаких внешних API-вызовов
        "caching": "LRU для повторных запросов",
        "dim": 1024
    },

    "llm": {
        "model": "Cotype Pro 2",              # корпоративная модель МТС
        "deployment": "on-premise GPU кластер",
        "context": "8192 токенов"
    },

    "vector_db": {
        "engine": "pgvector (PostgreSQL)",    # не отдельный сервис
        "metric": "cosine similarity",
        "index": "IVFFLAT для быстрого ANN"
    },

    "lexical_search": {
        "engine": "BM25 (PostgreSQL FTS)",    # встроено в Postgres
        "normalization": "синонимы + транслитерация в запросе"
    },

    "sources": ["Confluence", "Jira"],
    "access_control": "делегировано источникам (не реплицируется)"
}
```

## Инкрементальная индексация: zero-downtime

```python
class IncrementalIndexer:
    """
    Обновление индекса без перезапуска сервиса.
    Принцип: изменился контент → обновить; не изменился → пропустить.
    """

    async def sync_confluence(self, space_key: str):
        """Непрерывный поллинг Confluence → инкрементальное обновление."""
        async for page in self.confluence.iter_updated(space_key):
            current_hash = self._hash(page.body)
            stored_hash  = self.index.get_hash(page.id)

            if current_hash == stored_hash:
                continue  # контент не изменился → пропустить

            # Атомарный UPSERT: обновить или создать
            chunks = self._chunk(page.body, size=3000, overlap=0.10)
            embeddings = await self._embed_batch(chunks)

            async with self.db.transaction():
                # Soft-delete старых чанков (сохранить для отката)
                self.db.soft_delete_chunks(page_id=page.id)

                # Вставить новые
                self.db.upsert_chunks(
                    page_id=page.id,
                    chunks=chunks,
                    embeddings=embeddings,
                    content_hash=current_hash,
                    updated_at=page.updated_at
                )

    def _chunk(self, text: str, size: int, overlap: float) -> list[str]:
        """
        HTML → Markdown (сохраняем семантические границы),
        затем разбивка по ~3000 символов с 10% перекрытием.
        """
        markdown = self.html_to_md.convert(text)
        step = int(size * (1 - overlap))

        return [
            markdown[i:i+size]
            for i in range(0, len(markdown), step)
            if markdown[i:i+size].strip()
        ]
```

## Access Control: делегирование источникам

```python
class SourceDelegatedACL:
    """
    Не реплицировать права доступа в RAG-систему.
    Вместо этого: запрашивать только документы,
    доступные пользователю в источнике.
    """

    async def search_with_acl(self, query: str,
                               user_token: str) -> list[SearchResult]:
        # 1. Получить список ID документов, доступных пользователю
        accessible_ids = await self.confluence.get_accessible(
            user_token=user_token,
            space_keys=self.monitored_spaces
        )

        # 2. Семантический поиск только по доступным документам
        vector_results = await self.pgvector.search(
            embedding=await self._embed(query),
            filter={"page_id": {"$in": accessible_ids}},  # ACL filter
            top_k=20
        )

        # 3. BM25 поверх тех же ограниченных результатов
        bm25_results = self.bm25.search(
            query=query,
            corpus=[r.text for r in vector_results]
        )

        # 4. Гибридное ранжирование
        return self.ranker.merge(vector_results, bm25_results)

    # Ключевое свойство: если права изменились в Confluence → они сразу
    # отражаются в RAG (нет синхронизации ACL, нет задержки)
```

## Query Normalization: синонимы и транслитерация

```python
class QueryNormalizer:
    """
    Корпоративные запросы содержат аббревиатуры, транслитерацию,
    и специфические термины — нужна нормализация перед BM25.
    """

    SYNONYM_MAP = {
        "лк": "личный кабинет",
        "апи": "API",
        "бд": "база данных",
        "тех. поддержка": "техническая поддержка",
        "пк": "персональный компьютер",
    }

    TRANSLITERATION_MAP = {
        "wifi": "вайфай",
        "login": "логин",
        "password": "пароль",
    }

    def normalize(self, query: str) -> str:
        q = query.lower().strip()
        # Заменить аббревиатуры
        for abbr, full in self.SYNONYM_MAP.items():
            q = q.replace(abbr, full)
        # Транслитерация технических терминов
        for en, ru in self.TRANSLITERATION_MAP.items():
            q = q.replace(en, ru)
        return q
```

## Применение к Lorenzo

```python
# improve_enterprise_rag.py (паттерн):

class LorenzoEnterpriseRAG:
    """
    Lorenzo = корпоративная база знаний.
    МТС-паттерн применим напрямую.
    """

    HYBRID_WEIGHTS = {"vector": 0.7, "bm25": 0.3}

    BOOST_RULES = {
        "title_match":   1.2,
        "recent_30d":    1.1,
        "high_priority": 1.5,   # SCORING.md файлы с Go/No-Go
    }

    def search(self, query: str) -> list[Document]:
        # Уже реализовано в improve_semantic_search.py!
        # МТС-паттерн: добавить freshness boost и title boost
        results = self.hybrid_search(query)
        return self._apply_boost(results, query)
```

## Возможные комбинации

| Комбинация | Новое свойство |
|------------|----------------|
| **Enterprise RAG + Coreness Flow (R30)** | Composable RAG: источники как плагины (Confluence/Jira/GitLab) с hot-reload |
| **Enterprise RAG + HITL (R30)** | Неуверенные ответы RAG → HITL: эскалация к эксперту |
| **Enterprise RAG + MCP (R04)** | Корпоративный RAG как MCP-сервис (вариант из runner-up 983424) |
| **Enterprise RAG + Cognitive Memory (R31)** | RAG + персональная память агента: общие знания + личная история |
| **Enterprise RAG + LLM Judge (R28)** | Судья оценивает качество RAG-ответов перед отправкой пользователю |

## Контакт

- Статья: https://habr.com/ru/companies/ru_mts/articles/970476/ (декабрь 2025)
- МТС Tech: habr.com/ru/companies/ru_mts/
- Смежная (RAG как MCP-сервис, GitHub): https://habr.com/ru/articles/983424/
- Смежная (DAT dynamic alpha hybrid): https://habr.com/ru/articles/970594/
- BGE-M3: github.com/FlagOpen/FlagEmbedding (MIT)
- pgvector: github.com/pgvector/pgvector (PostgreSQL extension)

## Смотрите также
- [Главная](../../../README.md)
- [Метрики](../../../METRICS.md)
- [Здоровье](../../../HEALTH.md)
- [Глоссарий](../../../GLOSSARY.md)
- [Сущности](../../../ENTITIES.md)
