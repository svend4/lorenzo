---
date: 2026-05-29
tags: [memory, rag, orchestration, knowledge, ingestion]
state: normalized
---

# Темпоральные графы знаний для юридического RAG: SAT-Graph и point-in-time retrieval

<!-- toc-auto -->
<!-- tags: ekaterina-ya-temporal-knowledge-graph-legal-rag, docs -->


<!-- summary -->
> `ekaterina-ya-temporal-knowledge-graph-legal-rag` — раздел документации проекта Lorenzo.


> [!WARNING]
> Документ содержит описание рисков и ограничений. Изучите их перед принятием архитектурных решений.

<!-- alert-added -->

**Автор:** Ekaterina-ya  
**Хабр:** https://habr.com/ru/articles/964202/  
**GitHub:** нет (исследовательская архитектура)  
**Слой:** analytics / knowledge  
**Дата:** ноябрь 2025  
**Уникальность:** Динамические/темпоральные графы знаний с версионированием для юридических документов: SAT-Graph (Segment-Anchored Temporal Graph) позволяет делать point-in-time retrieval — задавать вопрос "какой была норма X на дату Y". MLR (Mean Legal Recall) 37.86% vs 16.39% у плоского векторного поиска. Уникальный угол: законодательство постоянно меняется → статичный граф устаревает → нужен темпоральный граф с версиями рёбер.

## Проблема: законодательство меняется, RAG не знает об этом

```
Плоский векторный RAG для юридических документов:
  → Индексируется текущая версия закона
  → "Какой штраф за X?" → ответ по актуальной редакции
  → Проблема: "какой был штраф за X в январе 2023?"
    → RAG не знает! Нет версионирования.

Юридический контекст:
  → Законы принимаются → изменяются поправками → отменяются
  → Договоры заключены под старую редакцию
  → Судебное дело рассматривается год → нормы за это время изменились
  → Нужен "снапшот" законодательства на конкретную дату

Статичный Knowledge Graph тоже не решает:
  → KG строится однажды → обновление = перестройка
  → Нет механизма для temporal queries
  → Нет версионирования рёбер и узлов
```

## SAT-Graph: Segment-Anchored Temporal Graph

```python
# Ekaterina-ya: темпоральные графы для юридического RAG
# habr.com/ru/articles/964202/

from dataclasses import dataclass, field
from datetime import date
from typing import Optional

@dataclass
class TemporalEntity:
    """Юридическая сущность с временным диапазоном существования."""
    entity_id: str
    entity_type: str     # "law", "article", "penalty", "requirement"
    text: str
    valid_from: date
    valid_to: Optional[date]  # None = действует по сей день
    source_document: str
    source_segment: str  # "anchor" сегмент → уникальный ID в документе


@dataclass
class TemporalRelation:
    """
    Ребро графа с временным диапазоном.
    Ключевое отличие от статичного KG: у каждого ребра есть (valid_from, valid_to).

    Примеры:
    - Article_125 --[SETS_PENALTY(2000 руб.)]-> Violation_A [2020-01-01, 2022-12-31]
    - Article_125 --[SETS_PENALTY(5000 руб.)]-> Violation_A [2023-01-01, None]
    """
    source_entity: str
    target_entity: str
    relation_type: str
    relation_value: Optional[str]  # числовое значение (штраф, срок)
    valid_from: date
    valid_to: Optional[date]
    confidence: float


class SATGraph:
    """
    Segment-Anchored Temporal Graph.

    "Segment-Anchored": каждая сущность привязана к конкретному
    сегменту документа (статья, пункт) → инкрементальное обновление
    при изменении закона затрагивает только нужные сегменты.

    "Temporal": рёбра и узлы имеют временные диапазоны → возможен
    point-in-time retrieval для любой исторической даты.
    """

    def __init__(self, db_path: str = "legal_kg.db"):
        import sqlite3
        self.db = sqlite3.connect(db_path)
        self._init_temporal_schema()

    def _init_temporal_schema(self):
        """Схема с поддержкой temporal queries."""
        self.db.executescript("""
            CREATE TABLE IF NOT EXISTS entities (
                id TEXT PRIMARY KEY,
                entity_type TEXT,
                text TEXT,
                valid_from DATE,
                valid_to DATE,
                source_document TEXT,
                source_segment TEXT
            );

            CREATE TABLE IF NOT EXISTS relations (
                source_id TEXT,
                target_id TEXT,
                relation_type TEXT,
                relation_value TEXT,
                valid_from DATE,
                valid_to DATE,
                confidence REAL
            );

            CREATE INDEX IF NOT EXISTS idx_entities_temporal
            ON entities(valid_from, valid_to);

            CREATE INDEX IF NOT EXISTS idx_relations_temporal
            ON relations(source_id, valid_from, valid_to);
        """)

    def add_temporal_entity(self, entity: TemporalEntity):
        """Добавить сущность с временным диапазоном."""
        self.db.execute("""
            INSERT OR REPLACE INTO entities
            VALUES (?, ?, ?, ?, ?, ?, ?)
        """, (
            entity.entity_id, entity.entity_type, entity.text,
            entity.valid_from.isoformat(),
            entity.valid_to.isoformat() if entity.valid_to else None,
            entity.source_document, entity.source_segment
        ))

    def update_law_amendment(self,
                               segment_id: str,
                               new_text: str,
                               amendment_date: date):
        """
        Применить поправку к закону.
        Segment-Anchored: обновляем только затронутый сегмент.

        1. Закрыть старое ребро (valid_to = amendment_date - 1 день)
        2. Добавить новое ребро (valid_from = amendment_date)
        """
        yesterday = date(amendment_date.year, amendment_date.month,
                         amendment_date.day - 1)

        # Закрыть старые рёбра этого сегмента
        self.db.execute("""
            UPDATE relations
            SET valid_to = ?
            WHERE source_id LIKE ? AND valid_to IS NULL
        """, (yesterday.isoformat(), f"{segment_id}%"))

        # Добавить новую версию сегмента
        new_entity = TemporalEntity(
            entity_id=f"{segment_id}_v{amendment_date.isoformat()}",
            entity_type="article",
            text=new_text,
            valid_from=amendment_date,
            valid_to=None,
            source_document="amendment_2023_12",
            source_segment=segment_id
        )
        self.add_temporal_entity(new_entity)
```

## Point-in-Time Retrieval

```python
class TemporalLegalRetriever:
    """
    Point-in-time retrieval: ответить на вопрос
    "какой была норма X на дату Y?"

    Гибридный подход:
    1. Graph traversal по темпоральному KG (точные связи)
    2. Vector search по сегментам документов (семантика)
    3. Ранжирование по temporal relevance score
    """

    def retrieve_at_date(self,
                          query: str,
                          as_of_date: date,
                          top_k: int = 5) -> list[dict]:
        """
        Retrieval с ограничением по дате.

        Все сущности и рёбра фильтруются:
        valid_from <= as_of_date AND (valid_to IS NULL OR valid_to >= as_of_date)
        """
        # Шаг 1: семантический поиск по query
        candidate_segments = self._vector_search(query, top_k=top_k * 3)

        # Шаг 2: фильтрация по дате (temporal filter)
        valid_segments = []
        for segment in candidate_segments:
            if self._is_valid_at_date(segment["entity_id"], as_of_date):
                valid_segments.append(segment)

        # Шаг 3: граф-расширение (связанные нормы на ту же дату)
        expanded = self._graph_expand(valid_segments, as_of_date)

        # Шаг 4: ранжирование
        return self._rank_results(expanded, query, as_of_date)[:top_k]

    def _is_valid_at_date(self, entity_id: str,
                           check_date: date) -> bool:
        """Проверить действовала ли норма на заданную дату."""
        row = self.db.execute("""
            SELECT valid_from, valid_to FROM entities
            WHERE id = ?
        """, (entity_id,)).fetchone()

        if not row:
            return False

        valid_from = date.fromisoformat(row[0])
        valid_to = date.fromisoformat(row[1]) if row[1] else date.today()

        return valid_from <= check_date <= valid_to

    def _graph_expand(self,
                       seed_segments: list[dict],
                       as_of_date: date) -> list[dict]:
        """
        Graph traversal от seed сегментов по рёбрам,
        действовавшим на заданную дату.
        Находит связанные нормы: "статья X ссылается на статью Y".
        """
        expanded = list(seed_segments)
        visited = {s["entity_id"] for s in seed_segments}

        for segment in seed_segments:
            # Найти исходящие рёбра, действовавшие на as_of_date
            related = self.db.execute("""
                SELECT target_id, relation_type, relation_value
                FROM relations
                WHERE source_id = ?
                  AND valid_from <= ?
                  AND (valid_to IS NULL OR valid_to >= ?)
            """, (segment["entity_id"],
                  as_of_date.isoformat(),
                  as_of_date.isoformat())).fetchall()

            for target_id, rel_type, rel_value in related:
                if target_id not in visited:
                    target = self._fetch_entity(target_id)
                    if target:
                        target["graph_relation"] = rel_type
                        target["graph_value"] = rel_value
                        expanded.append(target)
                        visited.add(target_id)

        return expanded


BENCHMARK_RESULTS = {
    "домен": "Российское законодательство (трудовое, гражданское, административное)",
    "датасет": "Вопросы с привязкой к историческим датам (юридические кейсы)",
    "метрика": "MLR (Mean Legal Recall) — полнота извлечения релевантных норм",

    "результаты": {
        "flat_vector_rag": {
            "MLR": 0.1639,
            "описание": "Плоский векторный поиск без темпоральной информации"
        },
        "static_kg_rag": {
            "MLR": 0.2841,
            "описание": "Статичный KG без версионирования"
        },
        "SAT_graph_temporal": {
            "MLR": 0.3786,
            "описание": "SAT-Graph с point-in-time retrieval",
            "vs_flat": "+2.3x улучшение vs плоский RAG"
        }
    },

    "ключевой_вывод": (
        "Для юридических вопросов с датой (~30% реальных запросов) "
        "темпоральный граф необходим. "
        "Плоский RAG отвечает по актуальной редакции → ошибка на исторических делах."
    )
}
```

## Архитектура обновления при принятии поправок

```python
class LegalKGUpdater:
    """
    Инкрементальное обновление KG при принятии новых поправок.
    Segment-Anchored: только изменённые сегменты пересчитываются.
    """

    def process_amendment(self,
                           amendment_document: str,
                           effective_date: date,
                           sat_graph: SATGraph) -> dict:
        """
        Обработать документ с поправками:
        1. Извлечь: какие сегменты изменяются
        2. Закрыть старые версии (valid_to = effective_date - 1)
        3. Добавить новые версии (valid_from = effective_date)
        4. Обновить рёбра между сегментами

        Полный перестрой НЕ нужен (vs статичный KG).
        """
        # LLM извлекает изменения из текста поправки
        changes = self._extract_changes_llm(amendment_document)

        updated_segments = []
        for change in changes:
            sat_graph.update_law_amendment(
                segment_id=change["segment_id"],
                new_text=change["new_text"],
                amendment_date=effective_date
            )
            updated_segments.append(change["segment_id"])

        return {
            "updated_segments": len(updated_segments),
            "effective_date": effective_date.isoformat(),
            "full_rebuild_required": False
        }

    def _extract_changes_llm(self, amendment_text: str) -> list[dict]:
        """
        LLM читает текст поправки и извлекает:
        - какой сегмент закона изменяется (ст. X, п. Y)
        - новая редакция сегмента
        """
        prompt = f"""Проанализируй документ с поправками к закону.
Для каждого изменения извлеки:
1. ID изменяемого сегмента (статья + пункт)
2. Новая редакция текста

Документ: {amendment_text}

Верни JSON: [{{"segment_id": "...", "new_text": "..."}}]"""
        # ... вызов LLM ...
```

## Применение к Lorenzo

```python
# Lorenzo: SAT-Graph для версионирования docs/

class LorenzoTemporalKnowledge:
    """
    Ekaterina-ya паттерн для Lorenzo:
    Темпоральный KG для docs/ — отслеживать как менялась
    архитектура Svyazi.

    "Какой была архитектура Итерации 1 до добавления Review Queue?"
    "Когда был добавлен LangFuse?"

    Каждый файл docs/ = сущность с valid_from (дата git commit).
    """

    def build_temporal_doc_graph(self, docs_path: str) -> SATGraph:
        """
        Построить SAT-Graph из git history docs/.
        Каждый коммит = amendment: новые версии файлов с датой.
        """
        import subprocess
        graph = SATGraph("lorenzo_temporal.db")

        # Получить git log для каждого файла
        result = subprocess.run(
            ["git", "log", "--format=%H %ai", "--follow", "--", docs_path],
            capture_output=True, text=True
        )

        for line in result.stdout.strip().split("\n"):
            commit_hash, commit_date = line.split(" ", 1)
            as_of = date.fromisoformat(commit_date[:10])
            # Добавить версию файла с этой датой
            # ...

        return graph
```

## Возможные комбинации

| Комбинация | Новое свойство |
|------------|----------------|
| **Temporal KG + Graph RAG (R38)** | Статический Graph RAG → темпоральный: добавить версионирование к VladSpace подходу |
| **Temporal KG + LoRA Embeddings (R44)** | LoRA-дообученные эмбеддинги для юридического домена + темпоральный KG = лучший legal RAG |
| **Temporal KG + LangGraph (R44)** | LangGraph с чекпоинтами хранит состояние запроса + темпоральный граф: agent помнит дату контекста |
| **Temporal KG + feeds.fun (R43)** | Новости тегируются → связи с законодательством на дату публикации = legal news RAG |
| **Temporal KG + Lorenzo docs/** | Версионирование знаний о проектах: "какой был статус в R30?" |

## Контакт

- Статья: https://habr.com/ru/articles/964202/ (ноябрь 2025)
- Автор: Ekaterina-ya (Хабр)
- SAT-Graph: Segment-Anchored Temporal Graph (оригинальная архитектура)
- Метрика: MLR (Mean Legal Recall) — специализированная для юридического RAG
- Смежная (Graph RAG v3, R38): docs/06-discovery/round-38/
- Смежная (Юридический RAG, R25): docs/06-discovery/round-25/
- Смежная (Legal NLP, R22): docs/06-discovery/round-22/

## Смотрите также
- [Главная](../../../README.md)
- [Метрики](../../../METRICS.md)
- [Здоровье](../../../HEALTH.md)
- [Глоссарий](../../../GLOSSARY.md)
- [Сущности](../../../ENTITIES.md)
- [Решения](../../../DECISIONS.md)
