---
date: 2026-05-29
tags: [memory, rag, ingestion, architecture, collaboration]
state: normalized
---

# Law & Practice Ensemble RAG — юридический ассистент: законы + судебная практика

<!-- toc-auto -->
<!-- tags: law-practice-ensemble-rag, docs -->


<!-- summary -->
> Автор: OTUS (Хабр, 2025) Хабр: https://habr.com/ru/companies/otus/articles/946012/
Хабр: https://habr.com/ru/companies/otus/articles/946012/  
GitHub: не опубликован (архитектура и код разобраны в статье)  
Слой: knowledge / orchestration / ingestion  
Дата: 2025  
Уникальность: Ensemble RAG для юридическ


> [!WARNING]
> Документ содержит описание рисков и ограничений. Изучите их перед принятием архитектурных решений.

<!-- alert-added -->

**Автор:** OTUS (Хабр, 2025)  
**Хабр:** https://habr.com/ru/companies/otus/articles/946012/  
**GitHub:** не опубликован (архитектура и код разобраны в статье)  
**Слой:** knowledge / orchestration / ingestion  
**Дата:** 2025  
**Уникальность:** Ensemble RAG для юридических задач объединяет два типа источников с разными весами: нормативные акты (законы, кодексы) + судебная практика (решения судов). Ключевое: ответ на юридический вопрос требует обоих — закон даёт норму, практика — как суды реально её трактуют. Кейс: ассистент для недвижимостной отрасли.

## Проблема: почему vanilla RAG ломается на праве

```
Юридический вопрос: "Можно ли расторгнуть договор аренды досрочно?"

Vanilla RAG (один индекс):
  → находит статью 620 ГК РФ (основания расторжения)
  → отвечает по букве закона
  Проблема: суды иногда трактуют иначе, чем написано в законе
  → "правильный" ответ без судебной практики = неполный ответ

Law & Practice Ensemble RAG:
  → находит ст. 620 ГК РФ (что говорит закон)
  → находит 3 решения суда по аналогичным спорам (как применяется)
  → генерирует ответ: "Закон предусматривает X, при этом суды в 2023-2025
     придерживались позиции Y (дело №... / дело №...)"
  → ответ юридически полный
```

## Архитектура двухисточникового RAG

```python
# Два индекса с разными весами

class LawPracticeRAG:
    def __init__(self):
        # Индекс 1: нормативная база (законы, кодексы, ФЗ)
        self.law_index = VectorDB(
            source="regulatory_acts",
            chunking="by_article",  # каждая статья = отдельный чанк
            metadata=["law_name", "article_num", "effective_date"]
        )

        # Индекс 2: судебная практика (решения, постановления, определения)
        self.practice_index = VectorDB(
            source="court_decisions",
            chunking="by_reasoning",  # мотивировочная часть = чанк
            metadata=["court_level", "year", "category", "outcome"]
        )

    def retrieve(self, query: str) -> list[Document]:
        # Гибридный поиск с разными весами
        law_results = self.law_index.search(query, k=3)
        practice_results = self.practice_index.search(query, k=5)

        # Ранжирование: закон важнее для нормы, практика — для применения
        return rerank_with_weights(
            law_results, weight=0.6,
            practice_results, weight=0.4
        )
```

## Query Routing: разные стратегии для разных вопросов

```python
LEGAL_QUERY_TYPES = {
    "norm_question": {
        # "Какой срок исковой давности по договору аренды?"
        "pattern": "срок|размер|порядок|основания|требования",
        "strategy": "law_heavy",
        "weights": {"law": 0.8, "practice": 0.2}
    },
    "application_question": {
        # "Суды на практике удовлетворяют такие иски?"
        "pattern": "суды|практика|как правило|удовлетворяют",
        "strategy": "practice_heavy",
        "weights": {"law": 0.2, "practice": 0.8}
    },
    "comprehensive": {
        # "Как расторгнуть договор и что ждать от суда?"
        "pattern": ".*",  # default
        "strategy": "balanced",
        "weights": {"law": 0.6, "practice": 0.4}
    }
}

# Классификация запроса → стратегия поиска
query_type = classify_legal_query(user_question)
strategy = LEGAL_QUERY_TYPES[query_type]
results = rag.retrieve_with_weights(question, strategy["weights"])
```

## Промпт для юридического ответа

```python
LEGAL_ANSWER_PROMPT = """
Ты — опытный юрист-консультант. Ответь на вопрос клиента,
используя ТОЛЬКО предоставленные источники.

## Вопрос:
{question}

## Нормативная база:
{law_chunks}

## Судебная практика:
{practice_chunks}

## Правила ответа:
1. Сначала: что говорит закон (с указанием нормы)
2. Затем: как суды применяют это на практике (с примерами дел)
3. Вывод для клиента: практическая рекомендация
4. Если источников недостаточно — прямо скажи "требуется уточнение"
5. НЕ придумывай нормы или дела которых нет в контексте

Формат: структурированный ответ, без юридического жаргона для клиента
"""
```

## Специфика недвижимостного права (кейс)

```
Домен: операции с недвижимостью
  Нормативная база:
    → ГК РФ (гл. 34: аренда, гл. 30: купля-продажа)
    → ЖК РФ (жилищные правоотношения)
    → ФЗ-218 (регистрация прав)
    → ФЗ-135 (оценочная деятельность)

  Судебная практика:
    → Постановления Пленума ВС РФ
    → Обзоры практики ВС РФ
    → Решения арбитражных судов по сделкам

Примеры вопросов:
  "Продавец скрыл обременение — можно ли расторгнуть сделку?"
  "Как оспорить завышенную кадастровую стоимость?"
  "Арендатор улучшил помещение — кто возмещает расходы?"
```

## Метрики качества

```
Без судебной практики (только законы):
  Полнота ответа: 65% (нет практической составляющей)
  Галлюцинации: ~15% (модель "додумывает" трактовку)

С Law+Practice Ensemble:
  Полнота ответа: 89%
  Галлюцинации: ~4% (всегда есть источник в контексте)
  Цитируемость: 92% ответов содержат конкретные нормы/дела
```

## Применение к Lorenzo

Lorenzo анализирует документы из `docs/`. Legal RAG паттерн:

```python
# improve_legal_rag.py (паттерн):
# Lorenzo хранит проектные документы + решения (DECISIONS.md)
# Law+Practice = Docs+Decisions: два источника с разными весами

class LorenzoEnsembleRAG:
    def __init__(self):
        # "Нормативная база" Lorenzo = архитектурные решения
        self.decisions_index = index(docs_path="docs/DECISIONS.md")
        # "Судебная практика" = реальный опыт из проектных файлов
        self.projects_index = index(docs_path="docs/05-habr-projects/")

    def answer(self, question: str) -> str:
        # Решения дают "как правильно", проекты дают "как делается"
        return ensemble_answer(
            self.decisions_index.search(question),
            self.projects_index.search(question)
        )
```

## Возможные комбинации

| Комбинация | Новое свойство |
|------------|----------------|
| **Legal RAG + Contract Analysis (R22)** | RAG находит похожие договора → Claude анализирует риски с прецедентами |
| **Legal RAG + Graph RAG (R22)** | Neo4j граф: статьи ГК → решения судов → комментарии → все связаны |
| **Legal RAG + FRIDA (R18)** | FRIDA русские embeddings для поиска по юридическим текстам (юридическая терминология) |
| **Legal RAG + Docling (R19)** | PDF судебных решений → Docling таблицы/структура → индекс |
| **Legal RAG + Durable State (R23)** | Сессия юридической консультации с памятью — пользователь возвращается |

## Контакт

- Статья: https://habr.com/ru/companies/otus/articles/946012/ (2025)
- Смежная (нормоконтроль Directum): https://habr.com/ru/companies/directum/articles/980140/
- Смежная (анализ договорных рисков): https://habr.com/ru/articles/1005144/
- Смежная (ContentAI: LLM для юридических документов): https://habr.com/ru/companies/contentai/articles/932894/
- Consultant.ru — база нормативных актов (парсинг для индекса)

## Смотрите также
- [Главная](../../../README.md)
- [Метрики](../../../METRICS.md)
- [Здоровье](../../../HEALTH.md)
- [Глоссарий](../../../GLOSSARY.md)
- [Сущности](../../../ENTITIES.md)
