# 10 актуальных RAG-подходов — обзор Agentic RAG и современных стратегий

> [!NOTE]
> Документ создан на основе исследования. Ссылки ведут на связанные материалы.

<!-- alert-added -->

**Автор:** независимый исследователь (Хабр, май 2026)  
**Хабр:** https://habr.com/ru/articles/1029616/  
**GitHub:** не указан (обзорная статья + практические примеры кода)  
**Слой:** orchestration / knowledge / memory  
**Дата:** май 2026  
**Уникальность:** Системный обзор 10 современных RAG-подходов от базового до агентного — с кодом, метриками и рекомендациями когда применять. Центральная идея: переход от пассивного RAG (один раз достали, ответили) к **активному (агент решает: искать ли ещё, уточнять запрос, переформулировать)**.

## Карта 10 подходов

```
Уровень 1 — Базовый
  ├── Naive RAG          — chunking + embed + retrieve + generate
  ├── Advanced RAG       — reranking, hybrid search, query expansion
  └── Modular RAG        — pipeline как граф компонентов

Уровень 2 — Специализированный
  ├── Multimodal RAG     — текст + изображения + таблицы
  ├── Graph RAG          — KG + вектор (см. R09, R17)
  └── Long-context RAG   — Map-Reduce / Lost-in-the-middle митигация

Уровень 3 — Агентный
  ├── Agentic RAG        — агент управляет retrieval-циклом
  ├── Self-RAG           — LLM сам решает: нужен ли retrieval
  ├── Corrective RAG     — оценивает качество документов, переспрашивает
  └── Adaptive RAG       — динамически выбирает стратегию под запрос
```

## Agentic RAG — детально

```
Запрос пользователя
      ↓
Агент: "Достаточно ли мне контекста?"
  → НЕТ: переформулировать запрос, сделать ещё retrieval
  → ДА:  генерировать ответ
      ↓
Агент: "Ответ полный?"
  → НЕТ: уточняющий запрос, веб-поиск, другой источник
  → ДА:  финальный ответ
```

Ключевое отличие от обычного RAG: **retrieval = инструмент агента**, а не фиксированный этап пайплайна.

## Self-RAG — авто-рефлексия

```python
# Pseudo-code Self-RAG
def self_rag(query):
    # Токен [Retrieve]: нужен ли retrieval?
    if needs_retrieval(query):
        docs = retrieve(query)
        # Токен [IsRel]: релевантны ли docs?
        relevant = [d for d in docs if is_relevant(d, query)]
        # Токен [IsSup]: поддерживают ли docs ответ?
        answer = generate(query, relevant)
        # Токен [IsUse]: полезен ли ответ?
        return answer if is_useful(answer) else retry(query)
    return generate_without_retrieval(query)
```

## Corrective RAG

Добавляет **evaluator** перед генерацией:
- Если retrieved docs — нерелевантны → web search (fallback)
- Если частично релевантны → knowledge refinement (оставить только хорошие части)
- Если релевантны → стандартная генерация

## Метрики для выбора подхода

| Подход | Latency | Точность | Стоимость | Когда |
|--------|---------|----------|-----------|-------|
| Naive RAG | низкая | средняя | дёшево | прототипы |
| Advanced RAG | средняя | высокая | средне | продакшн |
| Agentic RAG | высокая | очень высокая | дорого | сложные запросы |
| Self-RAG | средняя | высокая | средне | критичные факты |
| Adaptive RAG | средняя | высокая | средне | mixed workload |

## Применение к Lorenzo

Lorenzo сейчас использует **Advanced RAG** (BM25 + TF-IDF + hybrid 0.6/0.4).  
Переход к **Agentic RAG** означает:
- `improve_llm_qa.py` становится агентом с петлёй retrieval
- Если BM25 не находит → расширить запрос → повторить
- Self-RAG: перед ответом проверить качество найденных документов

Agentic RAG + GraphRAG (R09) + Sberbank KG (R17) = полный knowledge pipeline.

## Возможные комбинации

| Комбинация | Новое свойство |
|------------|----------------|
| **Agentic RAG + Lorenzo QA** | `improve_llm_qa.py` с retrieval-петлёй = мультишаговые ответы |
| **Self-RAG + RAG Eval (R16)** | RAGAS оценивает каждый [IsRel] токен в CI |
| **Corrective RAG + GigaAM (R16)** | Voice query → Corrective RAG → точный ответ на RU |
| **Adaptive RAG + Context Engineering (R14)** | Стратегия выбирается по сложности запроса |
| **Agentic RAG + Schema Extractor (R17)** | Агент решает: нужна ли схема БД для этого запроса |

## Контакт

- Статья: https://habr.com/ru/articles/1029616/ (май 2026)
- Self-RAG paper: arxiv.org/abs/2310.11511
- Corrective RAG paper: arxiv.org/abs/2401.15884
- LangGraph Agentic RAG: langchain-ai.github.io/langgraph/tutorials/rag/langgraph_agentic_rag/
