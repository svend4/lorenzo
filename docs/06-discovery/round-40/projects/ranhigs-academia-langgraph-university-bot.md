---
date: 2026-06-05
tags: [memory, rag, orchestration, security, ingestion]
state: normalized
---

# Академия РАНХиГС: LangGraph агент для 340K абитуриентов

<!-- toc-auto -->
<!-- tags: ranhigs-academia-langgraph-university-bot, docs -->


<!-- summary -->
> `ranhigs-academia-langgraph-university-bot` — раздел документации проекта Lorenzo.


> [!NOTE]
> Документ создан на основе исследования. Ссылки ведут на связанные материалы.

<!-- alert-added -->

**Автор:** SGERCEN (Боловцов Сергей, Исследовательский центр ИИ РАНХиГС)  
**Хабр:** https://habr.com/ru/articles/944500/  
**GitHub:** нет (закрытый код), Telegram: @AcademicLLM_bot  
**Слой:** orchestration  
**Дата:** сентябрь 2025  
**Уникальность:** Production LangGraph StateGraph агент для крупнейшего вуза России (340K заявлений на приёмную кампанию). 10+ узлов обработки: модерация → цензура → FAQ → контекстуализация → условное ветвление RAG/SQL/прямой ответ. Гибридный поиск: E5 multilingual + BM25 + Milvus. Отдельный SQL-агент для запросов к базе программ (~100 программ, ~20 параметров). 25K+ запросов от 10K+ пользователей за 2 месяца. Qwen3-32B-AWQ через vLLM на A6000.

## Проблема: 340K абитуриентов vs 5 операторов

```
РАНХиГС — крупнейший вуз России:
  → 340 000 заявлений в приёмную кампанию
  → Вопросы: "Сколько баллов нужно на юриспруденцию?"
             "Есть ли общежитие для иногородних?"
             "Какой проходной балл в 2024 году?"
  → 5 операторов call-центра не справляются

Проблема RAG для образования:
  → "Сколько стоит обучение?" — нужен SQL по базе программ
  → "Расскажи про льготы" — нужен RAG по нормативным документам
  → "Что лучше: юрист или экономист?" — нужен прямой ответ LLM
  → Один пайплайн не работает → нужна маршрутизация

LangGraph StateGraph:
  → Граф с условными переходами между режимами
  → Воронка: сначала модерация/цензура, потом ответ
  → 25K запросов от 10K пользователей за 2 месяца
```

## LangGraph StateGraph: 10+ узлов

```python
# РАНХиГС "Академия": LangGraph multi-node agent
# habr.com/ru/articles/944500

from langgraph.graph import StateGraph, END
from typing import TypedDict, Literal, Optional
from langchain_core.messages import BaseMessage

class AcademiaState(TypedDict):
    """Состояние агента через весь граф."""
    user_query: str
    messages: list[BaseMessage]

    # Результаты промежуточных узлов
    is_appropriate: bool          # прошла ли модерацию
    is_safe: bool                 # прошла ли цензуру
    faq_answer: Optional[str]     # ответ из FAQ если найден
    contextualized_query: str     # запрос с контекстом диалога
    route: Literal["rag", "sql", "direct"]  # выбранный режим
    retrieved_docs: list[str]     # RAG результаты
    sql_result: Optional[dict]    # SQL результаты
    final_answer: str             # итоговый ответ


class AcademiaAgent:
    """
    LangGraph StateGraph: воронка с условными переходами.
    """

    def build_graph(self) -> StateGraph:
        graph = StateGraph(AcademiaState)

        # Узел 1: Модерация (блокировка нерелевантных запросов)
        graph.add_node("moderation", self._moderate)

        # Узел 2: Цензура (блокировка небезопасного контента)
        graph.add_node("censorship", self._censorship_check)

        # Узел 3: FAQ-проверка (быстрые частые вопросы без RAG)
        graph.add_node("faq_check", self._check_faq)

        # Узел 4: Контекстуализация (учёт истории диалога)
        graph.add_node("contextualize", self._contextualize_query)

        # Узел 5: Маршрутизатор (RAG / SQL / прямой ответ)
        graph.add_node("router", self._route_query)

        # Узел 6: RAG ретривер (документы нормативной базы)
        graph.add_node("rag_retrieval", self._rag_retrieve)

        # Узел 7: SQL агент (база образовательных программ)
        graph.add_node("sql_agent", self._sql_query)

        # Узел 8: Генерация ответа
        graph.add_node("generate", self._generate_answer)

        # Узел 9: Постобработка (форматирование, ссылки)
        graph.add_node("postprocess", self._postprocess)

        # Связи с условными переходами
        graph.set_entry_point("moderation")

        graph.add_conditional_edges(
            "moderation",
            lambda s: "censorship" if s["is_appropriate"] else END
        )
        graph.add_conditional_edges(
            "censorship",
            lambda s: "faq_check" if s["is_safe"] else END
        )
        graph.add_conditional_edges(
            "faq_check",
            lambda s: END if s["faq_answer"] else "contextualize"
        )
        graph.add_edge("contextualize", "router")
        graph.add_conditional_edges(
            "router",
            lambda s: {
                "rag": "rag_retrieval",
                "sql": "sql_agent",
                "direct": "generate"
            }[s["route"]]
        )
        graph.add_edge("rag_retrieval", "generate")
        graph.add_edge("sql_agent", "generate")
        graph.add_edge("generate", "postprocess")
        graph.add_edge("postprocess", END)

        return graph.compile()

    def _moderate(self, state: AcademiaState) -> AcademiaState:
        """Узел 1: тематическая модерация — вопрос про вуз?"""
        prompt = f"""Вопрос: {state['user_query']}
Ответь: является ли это вопросом об образовании/поступлении/вузе?
Верни: yes/no"""
        answer = self.llm.invoke(prompt)
        state["is_appropriate"] = "yes" in answer.content.lower()
        return state

    def _route_query(self, state: AcademiaState) -> AcademiaState:
        """
        Узел 5: маршрутизация между тремя режимами.
        Ключевая логика: когда использовать SQL vs RAG vs прямой ответ.
        """
        query = state["contextualized_query"]

        # SQL — если вопрос о конкретных числах программ
        sql_keywords = ["баллы", "стоимость", "бюджет", "платно",
                         "проходной", "количество мест", "цена"]
        if any(kw in query.lower() for kw in sql_keywords):
            state["route"] = "sql"
            return state

        # RAG — если вопрос о документах, правилах, процедурах
        rag_keywords = ["порядок", "правила", "льготы", "документы",
                         "требования", "договор", "общежитие"]
        if any(kw in query.lower() for kw in rag_keywords):
            state["route"] = "rag"
            return state

        # Прямой ответ — общие вопросы
        state["route"] = "direct"
        return state
```

## Гибридный поиск: E5 + BM25 + Milvus

```python
from sentence_transformers import SentenceTransformer
from pymilvus import MilvusClient
from rank_bm25 import BM25Okapi

class HybridRetriever:
    """
    E5 multilingual (768-dim, COSINE) + BM25 → Reciprocal Rank Fusion.
    Документы: нормативная база РАНХиГС (правила приёма, уставы, положения).
    """

    def __init__(self):
        self.embedder = SentenceTransformer(
            "intfloat/multilingual-e5-base"
        )  # multilingual: работает с русским
        self.milvus = MilvusClient("academia.db")
        self.bm25 = None  # инициализируется при загрузке корпуса

    def retrieve(self, query: str, top_k: int = 5) -> list[dict]:
        # Dense retrieval (E5)
        query_embedding = self.embedder.encode(
            f"query: {query}",  # E5 требует префикс "query:"
            normalize_embeddings=True
        )
        dense_results = self.milvus.search(
            collection_name="academia_docs",
            data=[query_embedding.tolist()],
            limit=top_k * 2,  # overfetch для RRF
            output_fields=["text", "source", "doc_id"]
        )[0]

        # Sparse retrieval (BM25)
        tokenized_query = query.lower().split()
        bm25_scores = self.bm25.get_scores(tokenized_query)
        bm25_top_k = bm25_scores.argsort()[-top_k*2:][::-1]

        # Reciprocal Rank Fusion
        return self._rrf(dense_results, bm25_top_k, top_k=top_k)

    def _rrf(self, dense: list, sparse: list,
              top_k: int, k: int = 60) -> list[dict]:
        """
        RRF score = sum(1 / (k + rank_i)) для каждого документа.
        """
        scores = {}
        for rank, hit in enumerate(dense):
            doc_id = hit["entity"]["doc_id"]
            scores[doc_id] = scores.get(doc_id, 0) + 1 / (k + rank + 1)

        for rank, idx in enumerate(sparse):
            scores[idx] = scores.get(idx, 0) + 1 / (k + rank + 1)

        ranked = sorted(scores.items(), key=lambda x: x[1], reverse=True)
        return [self._get_doc(doc_id) for doc_id, _ in ranked[:top_k]]
```

## SQL-агент: LLM → SELECT по базе программ

```python
from langchain import SQLDatabase
from langchain.agents import create_sql_agent

class ProgramSQLAgent:
    """
    База данных образовательных программ:
    ~100 программ × ~20 параметров.
    LLM генерирует SELECT по вопросу абитуриента.
    """

    SCHEMA = """
    programs (
        id INT,
        name VARCHAR,          -- "Юриспруденция"
        level VARCHAR,         -- "бакалавриат"/"магистратура"
        form VARCHAR,          -- "очная"/"заочная"
        budget_places INT,     -- количество бюджетных мест
        paid_places INT,
        min_score INT,         -- минимальный балл ЕГЭ 2024
        cost_per_year DECIMAL, -- стоимость обучения/год
        has_dormitory BOOL,
        faculty VARCHAR
    )
    """

    def __init__(self):
        db = SQLDatabase.from_uri("postgresql://...")
        self.agent = create_sql_agent(
            llm=self.llm,
            db=db,
            agent_type="openai-tools",
            verbose=True
        )

    def query(self, question: str) -> dict:
        """
        Примеры вопросов → SQL:
        "Где меньше всего баллов нужно?" →
        SELECT name FROM programs ORDER BY min_score ASC LIMIT 5
        """
        result = self.agent.invoke({"input": question})
        return {
            "question": question,
            "sql_result": result["output"],
            "source": "database"
        }


PRODUCTION_METRICS = {
    "вуз": "РАНХиГС — крупнейший вуз России",
    "приёмная_кампания": "340 000 заявлений",
    "нагрузка": "25 000+ запросов от 10 000+ уникальных пользователей",
    "период": "2 месяца приёмной кампании",
    "telegram_bot": "@AcademicLLM_bot",

    "инфраструктура": {
        "llm": "Qwen3-32B-AWQ",
        "serving": "vLLM (NVIDIA A6000 GPU)",
        "api": "OpenAI-совместимый эндпоинт",
        "context": "128K токенов",
        "embeddings": "intfloat/multilingual-e5-base (768-dim)",
        "vector_db": "Milvus",
        "dialog_storage": "MongoDB",
        "monitoring": "Metabase",
        "sql_db": "PostgreSQL + SQLAlchemy"
    }
}
```

## Применение к Lorenzo

```python
# Lorenzo: LangGraph StateGraph для многорежимного Q&A

class LorenzoMultiModeQA:
    """
    Академия РАНХиГС паттерн для Lorenzo:
    - RAG режим: поиск по docs/
    - Граф режим: запросы к концептному графу
    - Прямой режим: вопросы о метаданных (скрипты, структура)

    Маршрутизация через StateGraph вместо монолитного пайплайна.
    """

    def build_graph(self) -> StateGraph:
        graph = StateGraph(...)
        graph.add_node("router", self._route)
        graph.add_node("bm25_retrieval", self._bm25)
        graph.add_node("graph_lookup", self._graph)
        graph.add_node("direct_answer", self._direct)
        graph.add_node("generate", self._generate)
        # ... условные переходы
        return graph.compile()
```

## Возможные комбинации

| Комбинация | Новое свойство |
|------------|----------------|
| **Академия + LangFuse (R38)** | Трейсинг каждого узла StateGraph: latency per node, маршруты |
| **Академия + Sequential (R38)** | Sequential протокол для панели экспертов по образовательным вопросам |
| **Академия + Graph RAG (R38)** | VectorCypher для поиска по документальной базе вуза |
| **Академия + Cognitive Memory (R31)** | SQLite память: помнить профиль и интересы конкретного абитуриента |
| **Академия + AISecurity (R37)** | FLAME guard перед StateGraph: защита от jailbreak в edu-контексте |

## Контакт

- Статья: https://habr.com/ru/articles/944500/ (сентябрь 2025)
- Telegram-бот: @AcademicLLM_bot
- Авторы: Боловцов Сергей (SGERCEN), Исследовательский центр ИИ РАНХиГС
- Milvus: milvus.io
- Смежная (НГУ Meno-Tiny + GraphRAG): https://habr.com/ru/companies/cloud_ru/articles/928132/
- Смежная (EduLLM-RU fine-tuning, R35): habr.com/ru/articles/1026516/

## Смотрите также
- [Главная](../../../README.md)
- [Метрики](../../../METRICS.md)
- [Здоровье](../../../HEALTH.md)
- [Глоссарий](../../../GLOSSARY.md)
- [Сущности](../../../ENTITIES.md)
- [Решения](../../../DECISIONS.md)
