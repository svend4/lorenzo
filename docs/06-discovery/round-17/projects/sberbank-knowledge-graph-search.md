---
date: 2026-05-15
tags: [rag, orchestration, knowledge, ingestion, local-first]
state: normalized
---

# Sberbank Knowledge Graph — граф знаний улучшает качество поиска

<!-- toc-auto -->
<!-- tags: sberbank-knowledge-graph-search, docs -->


<!-- summary -->
> Автор: команда Сбербанка (поиск и AI) Хабр: https://habr.com/ru/companies/sberbank/articles/1029580/
Хабр: https://habr.com/ru/companies/sberbank/articles/1029580/  
GitHub: не найден (корпоративный проект, но с описанным стеком)  
Слой: knowledge / orchestration / search  
Дата: апрель 2026  
Уникальность: Pr


> [!NOTE]
> Документ создан на основе исследования. Ссылки ведут на связанные материалы.

<!-- alert-added -->

**Автор:** команда Сбербанка (поиск и AI)  
**Хабр:** https://habr.com/ru/companies/sberbank/articles/1029580/  
**GitHub:** не найден (корпоративный проект, но с описанным стеком)  
**Слой:** knowledge / orchestration / search  
**Дата:** апрель 2026  
**Уникальность:** Production-кейс: Сбербанк добавил граф знаний (Apache Jena Fuseki) поверх RAG и получил **Google Knowledge Panel** для внутреннего поиска. 5-стадийный агентный workflow: извлечение сущностей → ранжирование по node rank и edge weight → суммаризация через LLM. Гибридный поиск: граф + вектор.

## Архитектура

```
Запрос пользователя: "Кто такой Иван Петров из отдела X?"
        ↓
Stage 1: Entity Extraction (LLM извлекает сущности из запроса)
        ↓
Stage 2: Graph Traversal (Apache Jena Fuseki SPARQL)
  → найти узлы, связанные с сущностями
        ↓
Stage 3: Ranking (node rank + edge weight)
  → релевантные факты о сущности
        ↓
Stage 4: Vector Search (дополнительный контекст)
        ↓
Stage 5: LLM Summarization → Knowledge Panel
  {"photo": "...", "role": "...", "projects": [...], "facts": [...]}
```

## Стек

| Компонент | Технология | Назначение |
|-----------|-----------|-----------|
| Граф БД | **Apache Jena Fuseki** (RDF) | хранение графа знаний |
| API | Go | слой поверх графовой БД |
| Embedding | не указано | семантический поиск |
| LLM | GigaChat (Sber) | суммаризация + entity extraction |
| Результат | Knowledge Panel | карточка-ответ на запрос |

## Почему граф + вектор > только вектор

| Подход | Что не умеет |
|--------|-------------|
| Только вектор | "Покажи всех коллег Ивана Петрова" — нет явных связей |
| Только граф | "Расскажи о похожих проектах" — нет семантики |
| **Граф + вектор** | ✅ явные связи + семантика |

## LightRAG как open-source альтернатива

**LightRAG** — open-source RAG-фреймворк на основе графа знаний:  
dual-level retrieval: детальный локальный + широкий глобальный поиск.  
Является альтернативой Microsoft GraphRAG (R09) с акцентом на простоту.

## Применение к Lorenzo

Lorenzo имеет `improve_concept_graph.py` → `CONCEPT_GRAPH.md` (Mermaid/DOT/JSON).  
Следующий шаг: перенести граф в **FalkorDB / Apache Jena** для SPARQL-запросов:  
— «Какие проекты связаны с voice + edge AI?»  
— «Найди авторов, работающих в смежных нишах»

Это конкретизирует HyperCortex HMP (R09) и GraphRAG pipeline (R09) для Lorenzo.

## Возможные комбинации

| Комбинация | Новое свойство |
|------------|----------------|
| **KG + GraphRAG (R09)** | GraphRAG pipeline R09 + Apache Jena Fuseki = полный граф-стек |
| **KG + improve_concept_graph** | CONCEPT_GRAPH.md → Jena → SPARQL → Knowledge Panel для Lorenzo |
| **KG + Vector DB (R12)** | Sberbank паттерн: Jena (граф) + Qdrant (вектор) = hybrid search |
| **KG + LLM-Wiki (R17)** | Wiki-граф: связи между заметками как рёбра Knowledge Graph |

## Контакт

- Статья: https://habr.com/ru/companies/sberbank/articles/1029580/ (апрель 2026)
- Apache Jena Fuseki: https://jena.apache.org/documentation/fuseki2/ (Apache 2.0)
- LightRAG GitHub: https://github.com/HKUDS/LightRAG (MIT)
- Смежная: https://habr.com/ru/articles/908890/ (KG + RAG)

## Смотрите также
- [Главная](../../../README.md)
- [Метрики](../../../METRICS.md)
- [Здоровье](../../../HEALTH.md)
- [Глоссарий](../../../GLOSSARY.md)
- [Сущности](../../../ENTITIES.md)
