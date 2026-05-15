---
date: 2026-05-15
tags: [rag, orchestration, knowledge, local-first, architecture]
state: normalized
---

# Text2SQL с самопроверкой в production: X5 Tech, Qwen2.5-72B, M-Schema

<!-- toc-auto -->
<!-- tags: x5tech-text2sql-self-refinement, docs -->


<!-- summary -->
> Эволюция NL2SQL: почему наивный подход не работает M-Schema: обогащённое описание схемы
 
M-Schema: обогащённое описание схемы
 
Самопроверка: Self-Refinement Loop
 
Результаты на внутреннем бенчмарке X5
 
PET-SQL и мультимодельные ансамбли
 
Применение к Lorenzo
Lorenzo имеет   — Q&A п


> [!NOTE]
> Документ создан на основе исследования. Ссылки ведут на связанные материалы.

<!-- alert-added -->

**Автор:** Mikhail Kulyaskin (@alaska_bear), X5 Tech (Хабр, сентябрь 2025)  
**Хабр:** https://habr.com/ru/companies/X5Tech/articles/949694/  
**GitHub:** не опубликован (внутренняя система X5 Tech)  
**Слой:** orchestration / analytics  
**Дата:** сентябрь 2025  
**Уникальность:** Production NL2SQL X5 Group: Qwen2.5-72B + M-Schema (DDL с примерами и аннотациями типов) + самопроверка с автоматической коррекцией по traceback. Few-shot через vector embeddings похожих запросов. ~76% точность на внутреннем бенчмарке. Протестированы PET-SQL и мультимодельные ансамбли.

## Эволюция NL2SQL: почему наивный подход не работает

```
NL2SQL v1 (наивный):
  "Покажи продажи за квартал" → GPT → SELECT ... → выполнить
  
  Проблемы:
  ❌ Не знает схему БД (таблицы, связи, типы)
  ❌ Галлюцинирует названия колонок
  ❌ Нет проверки результата
  ❌ Точность: ~30-40% на реальных схемах

NL2SQL v2 (с самопроверкой, X5 Tech):
  "Покажи продажи за квартал"
    → M-Schema injection (схема + примеры)
    → Few-shot (похожие запросы из vector store)
    → CoT генерация SQL
    → Выполнить на БД
    → Если ошибка → traceback + повтор
    → Если пустой результат → объяснить почему
  Точность: ~76% на внутреннем бенчмарке
```

## M-Schema: обогащённое описание схемы

```python
# Стандартный DDL (недостаточно для LLM):
"""
CREATE TABLE orders (
    id INTEGER PRIMARY KEY,
    store_id INTEGER,
    amount DECIMAL(10,2),
    created_at TIMESTAMP
);
"""

# M-Schema (X5 Tech формат: DDL + аннотации + примеры):
M_SCHEMA_EXAMPLE = """
TABLE: orders
DESCRIPTION: Транзакции покупок во всех магазинах X5 Group

COLUMNS:
  id          INTEGER  PK  -- уникальный ID транзакции
  store_id    INTEGER  FK(stores.id)  -- магазин где совершена покупка
  amount      DECIMAL  -- сумма чека в рублях (без копеек)
  created_at  TIMESTAMP  -- UTC время создания заказа

EXAMPLE ROWS:
  (1001, 42, 1850.50, '2025-09-15 14:32:00')
  (1002, 17, 340.00, '2025-09-15 14:33:12')

COMMON QUERIES:
  -- Продажи за день по магазинам
  SELECT store_id, SUM(amount) FROM orders
  WHERE DATE(created_at) = CURRENT_DATE GROUP BY store_id;

RELATIONSHIPS:
  store_id → stores.id (каждый заказ принадлежит одному магазину)
"""

# Почему это важно:
# LLM знает не просто "есть колонка amount", а:
# - что это рубли без копеек
# - типичные значения (~340-1850₽)
# - как её обычно используют
```

## Самопроверка: Self-Refinement Loop

```python
class SelfRefiningSQL:
    """
    Ключевое: модель видит свою ошибку и исправляет
    Без человека в контуре
    """
    MAX_RETRIES = 3

    def generate_and_validate(self, question: str,
                               schema: str) -> SQLResult:
        # Шаг 1: Few-shot поиск похожих запросов
        similar_examples = self.vector_store.search(
            query=question,
            top_k=5,
            filter={"schema": schema}
        )

        # Шаг 2: Генерация SQL с CoT
        sql = self.llm.generate(
            prompt=SQL_GENERATION_PROMPT.format(
                question=question,
                schema=schema,
                examples=similar_examples
            )
        )

        # Шаг 3: Self-Refinement Loop
        for attempt in range(self.MAX_RETRIES):
            try:
                result = self.db.execute(sql)

                # Валидация пустого результата
                if result.is_empty():
                    explanation = self.llm.explain_empty(
                        sql=sql, question=question
                    )
                    # Если объяснение разумное → вернуть с объяснением
                    # Если нет → попробовать другой подход
                    if explanation.is_valid:
                        return SQLResult(sql=sql, data=[], explanation=explanation)
                    sql = self.llm.regenerate(question, schema, sql,
                                               hint="возможно неверные условия WHERE")
                else:
                    return SQLResult(sql=sql, data=result.rows)

            except DatabaseError as e:
                # Ошибка → traceback в промпт → LLM исправляет
                sql = self.llm.fix_sql(
                    original_sql=sql,
                    error_traceback=str(e),
                    schema=schema
                )

        return SQLResult(status="failed", last_sql=sql)


SQL_GENERATION_PROMPT = """
Ты — аналитик данных X5 Group. Генерируй точный SQL.

Схема базы данных:
{schema}

Похожие запросы (few-shot примеры):
{examples}

Вопрос: {question}

Шаг 1: Определи нужные таблицы
Шаг 2: Определи нужные JOIN-ы
Шаг 3: Определи условия WHERE и агрегации
Шаг 4: Напиши финальный SQL

SQL:
"""
```

## Результаты на внутреннем бенчмарке X5

```python
BENCHMARK_RESULTS = {
    "baseline_gpt4_zero_shot": {
        "accuracy": 0.41,
        "условия": "Без схемы, без примеров"
    },
    "with_schema_injection": {
        "accuracy": 0.58,
        "условия": "Стандартный DDL"
    },
    "with_m_schema": {
        "accuracy": 0.68,
        "условия": "M-Schema с аннотациями и примерами"
    },
    "with_few_shot_vector": {
        "accuracy": 0.72,
        "условия": "M-Schema + vector few-shot"
    },
    "with_self_refinement": {
        "accuracy": 0.76,  # финальный результат X5 Tech
        "условия": "Полный пайплайн с self-refinement",
        "модель": "Qwen2.5-72B"
    },
    "pet_sql_ensemble": {
        "accuracy": 0.79,  # лучший результат
        "условия": "Мультимодельный ансамбль PET-SQL",
        "недостаток": "3× дороже и медленнее"
    }
}
```

## PET-SQL и мультимодельные ансамбли

```python
# PET-SQL паттерн: несколько моделей генерируют → голосование

class PETSQLEnsemble:
    """Pre-Execution Template based SQL Generation"""

    def generate(self, question: str, schema: str) -> str:
        # Каждая модель генерирует независимо
        candidates = [
            self.model_a.generate(question, schema),  # Qwen2.5-72B
            self.model_b.generate(question, schema),  # DeepSeek Coder
            self.model_c.generate(question, schema),  # SQL Coder
        ]

        # Выполнить все кандидаты
        results = [(sql, self.db.execute(sql)) for sql in candidates]

        # Голосование: выбрать SQL с наиболее часто встречающимся результатом
        # (большинство моделей согласны → более вероятно правильный ответ)
        return self.majority_vote(results)

# X5 Tech вывод: PET-SQL +3% точности, но 3× дороже
# Решение: используем PET-SQL только для критичных запросов
```

## Применение к Lorenzo

Lorenzo имеет `improve_llm_qa.py` — Q&A по базе знаний. Text2SQL паттерн:

```python
# improve_text2docs.py (паттерн — Text2Docs вместо Text2SQL):

class LorenzoText2Docs:
    """
    Аналог Text2SQL, но для поиска документов Lorenzo.
    Вопрос на естественном языке → структурированный поиск
    """

    # "Схема" Lorenzo = типы документов и их поля
    DOCS_SCHEMA = """
    CORPUS: docs/
    DOCUMENT TYPES:
      project_file: title, author, layer, github_url, habr_url, combinations
      session_log:  round, date, topics, projects_found
      analysis:     type, section, generated_by

    SEARCH METHODS:
      bm25_passages: keyword search
      semantic:      tfidf similarity
      faceted:       by type, section, author
    """

    def answer(self, question: str) -> str:
        # Шаг 1: LLM планирует поиск (аналог SQL генерации)
        search_plan = self.llm.plan_search(question, self.DOCS_SCHEMA)

        # Шаг 2: Выполнить поиск
        results = self.execute_search(search_plan)

        # Шаг 3: Self-refinement если пусто
        if not results:
            search_plan = self.llm.refine_search(question, search_plan,
                                                   hint="попробуй другие ключевые слова")
            results = self.execute_search(search_plan)

        return self.llm.synthesize(question, results)
```

## Возможные комбинации

| Комбинация | Новое свойство |
|------------|----------------|
| **Text2SQL + LLM DBA (R17)** | LLM-DBA = Text2SQL + оптимизация + объяснение плана |
| **Text2SQL + LLM Judge (R28)** | LLM Judge верифицирует корректность сгенерированного SQL |
| **Text2SQL + CAVM (R26)** | CAVM агент получает данные через Text2SQL вместо ручных запросов |
| **Text2SQL + Langfuse (R13)** | Трейсинг: какие запросы требуют retry, где падает точность |
| **Text2SQL + Knowledge Graph (R17)** | Граф схемы БД → LLM лучше понимает JOIN-ы |

## Контакт

- Статья: https://habr.com/ru/companies/X5Tech/articles/949694/ (сентябрь 2025)
- Смежная (Postgres Pro LLM pipelines): https://habr.com/ru/companies/postgrespro/articles/907614/
- Смежная (NL2SQL обзор RAG+CoT): https://habr.com/ru/companies/bothub/articles/925632/
- Смежная (Sberbank fine-tuning SQL): https://habr.com/ru/companies/sberbank/articles/909730/
- Vanna AI: github.com/vanna-ai/vanna (MIT)
- SQL Coder (Defog): github.com/defog-ai/sqlcoder

## Смотрите также
- [Главная](../../../README.md)
- [Метрики](../../../METRICS.md)
- [Здоровье](../../../HEALTH.md)
- [Глоссарий](../../../GLOSSARY.md)
- [Сущности](../../../ENTITIES.md)
- [Решения](../../../DECISIONS.md)
