---
date: 2026-05-29
tags: [rag, orchestration, security, knowledge, ingestion]
state: normalized
---

# Финансовый RAG-ассистент: 4-головый гибридный ретривер и агентные стратегии для банковского домена

<!-- toc-auto -->
<!-- tags: runoi-finance-rag-four-head-hybrid-retriever, docs -->


<!-- summary -->
> `runoi-finance-rag-four-head-hybrid-retriever` — раздел документации проекта Lorenzo.


> [!WARNING]
> Документ содержит описание рисков и ограничений. Изучите их перед принятием архитектурных решений.

<!-- alert-added -->

**Автор:** Runoi  
**Хабр:** https://habr.com/ru/articles/963482/  
**GitHub:** есть (хакатон AI for Finance Hack 2025, Райффайзен Банк)  
**Слой:** orchestration / knowledge  
**Дата:** ноябрь 2025  
**Уникальность:** Многоагентный финансовый RAG-ассистент: 4-головый гибридный ретривер (векторный + TF-IDF + иерархический граф концептов + семантический поиск) с тремя агентными стратегиями запросов (ITERATIVE, DECOMPOSE, simple). 9.66/10 по LLM-as-a-Judge (Gemini-2.5-Pro), $0.98 за 500 запросов. Не трейдинг и не compliance — document Q&A по банковским продуктам: ОСАГО, лимиты вычетов, сравнение условий.

## Проблема: банковские документы требуют multi-hop reasoning

```
Финансовый Q&A ассистент Райффайзен Банк:
  → Пользователи задают вопросы по продуктам банка
  → "Какой лимит налогового вычета на обучение в 2024 vs 2023?"
  → "Сравни условия ОСАГО у двух продуктов"
  → "Что изменилось в правилах безопасности платежей?"

Проблема стандартного RAG:
  → Simple RAG: один поиск → один чанк → ответ
  → Не работает для: сравнений (нужны два разных документа)
  → Не работает для: изменений лимитов (нужны два периода)
  → Не работает для: multi-hop ("А влияет на Б, Б влияет на В")

Хакатон AI for Finance Hack 2025 (Райффайзен Банк):
  → 500 вопросов по банковским документам
  → LLM-as-a-Judge: Gemini-2.5-Pro оценивает ответы
  → Стоимость инференса: $0.98 на весь датасет
  → Время: ~1.6 часа на 500 вопросов
```

## 4-головый гибридный ретривер

```python
# Runoi: финансовый RAG-ассистент для AI for Finance Hack 2025
# habr.com/ru/articles/963482/

from dataclasses import dataclass
from typing import Literal
import numpy as np

RetrievalHead = Literal["vector", "bm25", "graph", "semantic"]

@dataclass
class RetrievalResult:
    """Результат одного retrieval-голова."""
    chunk_id: str
    content: str
    score: float
    head: RetrievalHead
    metadata: dict


class FourHeadHybridRetriever:
    """
    4-головый гибридный ретривер для финансовых документов.

    Голова 1 — Vector Search: dense embeddings, семантическое сходство
    Голова 2 — BM25/TF-IDF: точный термин-матчинг (числа, коды, даты)
    Голова 3 — Hierarchical Graph: концепт-граф документов (иерархия разделов)
    Голова 4 — Semantic Search: re-ranking через LLM cross-encoder

    Зачем 4 головы:
    - "лимит 120 000 руб." → BM25 находит точно, vector пропустит
    - "условия схожие с КАСКО" → vector находит, BM25 пропустит
    - "раздел 3.2 ссылается на приложение А" → граф находит, другие нет
    - Финальный ранкинг: cross-encoder отсеивает нерелевантные результаты
    """

    def __init__(self, docs_path: str):
        self.vector_index = self._build_vector_index(docs_path)
        self.bm25_index = self._build_bm25_index(docs_path)
        self.concept_graph = self._build_concept_graph(docs_path)

    def retrieve(self, query: str, top_k: int = 10) -> list[RetrievalResult]:
        """
        Гибридный retrieval: все 4 головы параллельно → RRF fusion.

        RRF (Reciprocal Rank Fusion):
        score = Σ 1/(rank_i + k) для каждого голова
        Объединяет ранки без нормализации скоров разных пространств.
        """
        import asyncio

        # Параллельный поиск по всем 4 головам
        results = {
            "vector": self._vector_search(query, top_k * 2),
            "bm25": self._bm25_search(query, top_k * 2),
            "graph": self._graph_search(query, top_k * 2),
        }

        # Fusion через RRF
        fused = self._reciprocal_rank_fusion(results, k=60)

        # Cross-encoder re-ranking (Голова 4)
        reranked = self._semantic_rerank(query, fused[:top_k * 2])

        return reranked[:top_k]

    def _build_concept_graph(self, docs_path: str) -> dict:
        """
        Иерархический граф концептов документов.

        Структура: документ → разделы → подразделы → концепты
        Рёбра: CONTAINS, REFERENCES, DEFINES, AMENDS

        Пример для банковского документа:
        Условия_ОСАГО → CONTAINS → Раздел_3_Лимиты
        Раздел_3_Лимиты → DEFINES → лимит_выплаты_2024
        лимит_выплаты_2024 → AMENDS → лимит_выплаты_2023

        Это позволяет отвечать на вопросы об изменениях:
        "Что изменилось в лимитах?" → найти AMENDS-рёбра → извлечь оба периода
        """
        graph = {}
        # Парсинг структуры документов через heading hierarchy
        # Извлечение REFERENCES через regex: "см. раздел X", "согласно п. Y.Z"
        return graph

    def _reciprocal_rank_fusion(self,
                                  results: dict[str, list[RetrievalResult]],
                                  k: int = 60) -> list[RetrievalResult]:
        """
        RRF: объединить результаты от нескольких ретриверов.
        Не требует нормализации скоров — только ранки.
        """
        scores = {}
        for head_name, head_results in results.items():
            for rank, result in enumerate(head_results):
                if result.chunk_id not in scores:
                    scores[result.chunk_id] = {"result": result, "rrf_score": 0}
                scores[result.chunk_id]["rrf_score"] += 1 / (rank + k)

        sorted_results = sorted(
            scores.values(),
            key=lambda x: x["rrf_score"],
            reverse=True
        )
        return [item["result"] for item in sorted_results]
```

## Три агентные стратегии запросов

```python
class FinancialRAGOrchestrator:
    """
    Оркестратор трёх стратегий:
    1. SIMPLE: прямой RAG (быстро, для простых фактических вопросов)
    2. ITERATIVE: итеративное уточнение через SeaAgent
    3. DECOMPOSE: разбивка complex/multi-hop через DecompositionAgent

    Роутинг: классификатор сложности запроса → выбор стратегии.
    Сложность определяется: длина запроса, наличие "сравни/изменилось/в чём разница".
    """

    def route_and_answer(self, query: str) -> dict:
        """
        Определить стратегию и выполнить retrieval + generation.
        """
        complexity = self._classify_complexity(query)

        if complexity == "simple":
            return self._simple_rag(query)
        elif complexity == "iterative":
            return self._iterative_rag(query)
        else:
            return self._decompose_rag(query)

    def _iterative_rag(self, query: str, max_rounds: int = 3) -> dict:
        """
        ITERATIVE стратегия через SeaAgent (Search-and-Evaluate).

        Цикл:
        1. Retrieve → Generate draft answer
        2. SeaAgent: оценить что упущено в ответе
        3. Сгенерировать follow-up запрос на недостающую информацию
        4. Повторить до max_rounds или пока ответ полный

        Для вопросов типа: "Расскажи подробнее об условиях X"
        — где нужно несколько чанков из разных мест документа.
        """
        context = []
        answer = ""

        for round_num in range(max_rounds):
            # Шаг 1: поиск по текущему запросу
            chunks = self.retriever.retrieve(query, top_k=5)
            context.extend(chunks)

            # Шаг 2: генерация черновика
            draft = self._generate(query, context)

            # Шаг 3: SeaAgent — проверить полноту
            gap_analysis = self._sea_agent_evaluate(query, draft, context)

            if gap_analysis["is_complete"]:
                answer = draft
                break

            # Шаг 4: уточняющий запрос на пропуск
            query = gap_analysis["follow_up_query"]

        return {"answer": answer, "context_chunks": len(context), "rounds": round_num + 1}

    def _decompose_rag(self, query: str) -> dict:
        """
        DECOMPOSE стратегия через DecompositionAgent.

        Для multi-hop вопросов: "Как изменился лимит X с 2023 по 2024?"
        → DecompositionAgent разбивает на:
          sub_q1: "Лимит X в 2023 году"
          sub_q2: "Лимит X в 2024 году"
        → Каждый sub-вопрос через simple RAG
        → Объединение ответов + сравнение
        """
        sub_questions = self._decomposition_agent(query)
        sub_answers = [self._simple_rag(sq) for sq in sub_questions]
        return self._synthesize_answers(query, sub_answers)


BENCHMARK_RESULTS = {
    "хакатон": "AI for Finance Hack 2025 (Райффайзен Банк)",
    "датасет": "500 вопросов по банковским документам",
    "метрики": {
        "LLM_judge_score": 9.66,
        "judge_model": "Gemini-2.5-Pro",
        "inference_cost": "$0.98 за 500 запросов",
        "time": "~1.6 часа на 500 вопросов"
    },
    "модели_LLM": ["Mistral Small", "Llama-3-70B", "Gemma-27B", "Grok-3 Mini"],
    "задачи_домена": [
        "Сравнительный анализ банковских продуктов",
        "Отслеживание изменений лимитов между периодами",
        "Вопросы по ОСАГО",
        "Безопасность платежей"
    ]
}
```

## Применение к Lorenzo

```python
# Lorenzo: 4-головый ретривер для docs/

class LorenzoHybridRetriever:
    """
    Runoi паттерн для Lorenzo:
    4-головый ретривер для поиска по базе знаний проектов Svyazi.
    Текущий: BM25 + TF-IDF (2 головы).
    Добавить: концепт-граф (рёбра USES, EXTENDS, COMPETES) + re-rank.

    SeaAgent паттерн для /api/ask:
    Если ответ неполный → автоматически дополнительный поиск по пробелу.
    """

    def upgrade_to_four_heads(self):
        """Добавить граф и re-ranker к существующему BM25+TF-IDF."""
        pass
```

## Возможные комбинации

| Комбинация | Новое свойство |
|------------|----------------|
| **Finance RAG + Temporal KG (R47)** | Граф изменений условий со временными метками: "какими были лимиты ОСАГО в Q1 2024?" |
| **Finance RAG + LangGraph (R44)** | ITERATIVE/DECOMPOSE стратегии как LangGraph граф с conditional routing |
| **Finance RAG + CLEV (R47)** | CLEV-консенсус для оценки качества финансовых ответов: судьи проверяют фактическую точность |
| **Finance RAG + Agent Evaluation (R48)** | Golden Set из банковских вопросов + RAGAS для тестирования retrieval стратегий |
| **Finance RAG + Lorenzo Gateway** | /api/ask с ITERATIVE стратегией: если BM25 не уверен → дополнительный поиск |

## Контакт

- Статья: https://habr.com/ru/articles/963482/ (ноябрь 2025)
- Автор: Runoi (Хабр), хакатон AI for Finance Hack 2025
- Организатор хакатона: Райффайзен Банк
- RRF: Cormack et al. "Reciprocal Rank Fusion outperforms Condorcet and individual Rank Learning Methods"
- SeaAgent: search-evaluate-adjust паттерн для итеративного RAG
- Смежная (Finam LLM трейдинг, R26): docs/06-discovery/round-26/
- Смежная (LLM финансовый compliance, R36): docs/06-discovery/round-36/
- Смежная (AML LLM советник, R42): docs/06-discovery/round-42/

## Смотрите также
- [Главная](../../../README.md)
- [Метрики](../../../METRICS.md)
- [Здоровье](../../../HEALTH.md)
- [Глоссарий](../../../GLOSSARY.md)
- [Сущности](../../../ENTITIES.md)
- [Решения](../../../DECISIONS.md)
