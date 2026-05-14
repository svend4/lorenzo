# Graph RAG Production Pipeline (96.7% точность)

**Автор:** неизвестен (статья февраль 2026 — уточнить профиль)  
**Хабр:** https://habr.com/ru/articles/1003064/  
**GitHub:** не найден явно — уточнить  
**Слой:** knowledge / RAG / graph  
**Дата:** февраль 2026  
**Уникальность:** Production-ready GraphRAG-пайплайн на Neo4j: **174/180 (96.7%) на двуязычном бенчмарке** из 30 вопросов в 6 режимах поиска. Объединяет 5 техник из научных статей в один декларативный pipeline с полным provenance-трейсингом и типизированным API. Построен за 5 дней.

## Архитектура (два типа узлов в Neo4j)

| Узел | Поля | Роль |
|------|------|------|
| **PhraseNode** | name, type, PageRank score, embedding | Именованная сущность |
| **PassageNode** | content, embedding | Текстовый чанк |

**Рёбра:** `MENTIONED_IN` (сущность → чанк), `RELATED_TO` (со-встречаемость между сущностями)

## Гибридный поиск (3 фазы)

1. **Vector Index** → ближайшие PhraseNode через cosine similarity
2. **Cypher Traversal** → обход графа от PhraseNode к PassageNode
3. **Re-ranking** → cosine re-rank по настоящим PassageNode-эмбеддингам

**Ключевой инсайт:** cosine re-rank по PassageNode-эмбеддингам из Neo4j превосходит RRF-фьюжн.

## Результат

- **174/180 = 96.7%** на двуязычном бенчмарке
- 5 техник из научных статей в одном пайплайне
- Полный provenance: каждый ответ трейсируется до исходного чанка

## Почему важно для Svyazi

Lorenzo уже имеет `improve_concept_graph.py` и `improve_passage_retrieval.py`.  
Этот паттерн — следующий уровень: не просто граф + поиск, а **единый hybrid retriever** с Cypher traversal.  
PhraseNode+PassageNode → замена TF-IDF + BM25 на Knowledge Graph retrieval.

## Возможные комбинации

| Комбинация | Новое свойство |
|------------|----------------|
| **GraphRAG + improve_concept_graph** | Граф концептов → Neo4j PhraseNode, семантический поиск через Cypher |
| **GraphRAG + improve_passage_retrieval** | BM25 passages → GraphRAG hybrid retrieval (96.7% vs текущего ~70%) |
| **GraphRAG + SocratiCode (R08)** | Кодовая база в графе + документы Lorenzo — единый knowledge graph |
| **GraphRAG + Natasha (R05)** | Natasha NER → PhraseNode, русские сущности в Neo4j |

## Контакт

- Статья: https://habr.com/ru/articles/1003064/ (февраль 2026)
- ⚠️ Нужно найти GitHub через профиль автора
