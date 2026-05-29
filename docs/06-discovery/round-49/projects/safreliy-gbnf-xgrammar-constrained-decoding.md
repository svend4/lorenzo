---
date: 2026-05-29
tags: [rag, orchestration, security, knowledge, ingestion]
state: normalized
---

# Будущее ИИ — формальные грамматики: GBNF, XGrammar и constrained decoding для LLM

<!-- toc-auto -->
<!-- tags: safreliy-gbnf-xgrammar-constrained-decoding, docs -->


<!-- summary -->
> `safreliy-gbnf-xgrammar-constrained-decoding` — раздел документации проекта Lorenzo.


> [!WARNING]
> Документ содержит описание рисков и ограничений. Изучите их перед принятием архитектурных решений.

<!-- alert-added -->

**Автор:** Safreliy (Postgres Professional)  
**Хабр:** https://habr.com/ru/companies/postgrespro/articles/922260/  
**GitHub:** нет (теоретическая + практическая статья с примерами кода)  
**Слой:** orchestration / knowledge  
**Дата:** июнь 2025  
**Уникальность:** Углубление ниже JSON Mode и Pydantic/Instructor — полная механика constrained decoding через иерархию Хомского: GBNF-синтаксис, устранение левой рекурсии, контекстно-зависимые vs контекстно-независимые токены в XGrammar. Интеграция в vLLM через `guided_grammar`. Три production-кейса: корректный SQL по версии БД, DSL миграций (18 операций), RAG Fusion query reformulation. XGrammar сокращает 99% проверок логитов и встроен как дефолтный бэкенд в vLLM и TensorRT-LLM.

## Проблема: JSON mode недостаточен для сложных структур

```
Уровни structured output (иерархия сложности):
  Уровень 1 (JSON Mode): {"key": "value"} — гарантирует JSON, но не схему
  Уровень 2 (Pydantic/Instructor): валидация + retry при ошибке — post-hoc
  Уровень 3 (Constrained Decoding): грамматика ограничивает генерацию на уровне логитов

Проблема уровней 1-2:
  → LLM генерирует, потом проверяем → ошибка → retry → 2x latency
  → Для сложных структур (SQL, DSL) retry-цикл нестабилен
  → Невозможно гарантировать семантическую корректность
    (несуществующие таблицы в SQL, недопустимые комбинации операций)

Constrained Decoding решает иначе:
  → Грамматика определяет ЧТО может быть следующим токеном
  → На каждом шаге генерации: маскируем недопустимые токены (логит = -∞)
  → LLM физически не может сгенерировать невалидную структуру
  → Нулевое число retry
```

## Иерархия Хомского и GBNF

```python
# Safreliy (PostgresPro): constrained decoding через формальные грамматики
# habr.com/ru/companies/postgrespro/articles/922260/

# GBNF (GGML BNF) — расширение EBNF с regex-поддержкой
# Используется в llama.cpp, vLLM, TensorRT-LLM

GBNF_EXAMPLE_JSON = r"""
# Простая JSON-грамматика на GBNF
root   ::= object
value  ::= object | array | string | number | ("true" | "false" | "null") ws

object ::= "{" ws (string ":" ws value ("," ws string ":" ws value)*)? "}" ws
array  ::= "[" ws (value ("," ws value)*)? "]" ws

string ::= "\"" (
  [^\\"\x7F\x00-\x1F] |
  "\\" (["\\/bfnrt] | "u" [0-9a-fA-F] [0-9a-fA-F] [0-9a-fA-F] [0-9a-fA-F])
)* "\"" ws

number ::= ("-"? ([0-9] | [1-9] [0-9]*)) ("." [0-9]+)? (([eE] [-+]? [0-9]+))? ws
ws ::= ([ \t\n] ws)?
"""

# Более сложный пример: DSL миграций данных (18 операций)
GBNF_MIGRATION_DSL = r"""
root        ::= migration ws
migration   ::= "MIGRATION" ws "{" ws (operation ws)+ "}"
operation   ::= rename_op | move_op | transform_op | delete_op | add_op

rename_op   ::= "RENAME" ws "COLUMN" ws identifier ws "TO" ws identifier
move_op     ::= "MOVE" ws "TABLE" ws identifier ws "TO" ws "SCHEMA" ws identifier
transform_op ::= "TRANSFORM" ws identifier ws "USING" ws function_name ws "(" ws args? ws ")"
delete_op   ::= "DELETE" ws ("TABLE" | "COLUMN") ws identifier
add_op      ::= "ADD" ws "COLUMN" ws identifier ws datatype

identifier  ::= [a-zA-Z_][a-zA-Z0-9_]*
function_name ::= "to_upper" | "to_lower" | "trim" | "cast_int" | "cast_float"
                | "date_format" | "uuid_generate" | "hash_sha256"
datatype    ::= "TEXT" | "INTEGER" | "FLOAT" | "BOOLEAN" | "DATE" | "UUID"
args        ::= identifier ("," ws identifier)*
ws          ::= ([ \t\n])*
"""
```

## XGrammar: архитектура эффективного constrained decoding

```python
class XGrammarEngine:
    """
    XGrammar — дефолтный бэкенд structured generation в vLLM и TensorRT-LLM.

    Ключевое разделение токенов:
    1. Context-Independent (CI): токены допустимость которых
       не зависит от предыдущего контекста генерации
       → маски предвычисляются ОДИН РАЗ при компиляции грамматики
       → ~99% токенов попадают в этот класс

    2. Context-Dependent (CD): токены, допустимость которых
       зависит от состояния парсера (текущего положения в грамматике)
       → runtime проверка, но только для ~1% токенов

    Результат: 99% проверок логитов устранено предвычислением.
    Latency overhead constrained decoding: минимальный.
    """

    def compile_grammar(self, gbnf_grammar: str) -> dict:
        """
        Скомпилировать GBNF грамматику в маски токенов.

        Шаги:
        1. Парсинг GBNF → AST грамматики
        2. Устранение левой рекурсии (A → Aα | β → правая рекурсия)
        3. Построение PDA (Push-Down Automaton) состояний
        4. Для каждого состояния: вычислить допустимые следующие токены
        5. Разделить токены на CI (предвычислимые) и CD (runtime)
        6. Создать битовые маски для CI токенов

        Время компиляции: 10-100ms (одноразово).
        Runtime маскирование: ~0.1ms на шаг генерации.
        """
        pass

    def eliminate_left_recursion(self, grammar_rule: str) -> str:
        """
        Устранение левой рекурсии — обязательный шаг для LALR-парсеров.

        Проблема: A → Aα | β (левая рекурсия = бесконечный цикл при top-down parse)

        Преобразование:
        A → Aα | β
        ↓
        A  → β A'
        A' → α A' | ε  (ε = пустое слово)

        Пример для SQL EXPRESSION:
        expr → expr "+" term | term
        ↓
        expr  → term expr'
        expr' → "+" term expr' | ε
        """
        # Математическое преобразование левой рекурсии в правую
        pass


class DynamicGrammarBuilder:
    """
    Динамические грамматики: нетерминалы адаптируются к контексту.

    Проблема статической грамматики для SQL:
    Статическая: TABLE_NAME ::= [a-zA-Z_]+  (любое имя)
    → LLM может сгенерировать несуществующую таблицу "orders123"

    Динамическая: TABLE_NAME адаптируется к схеме конкретной БД
    → LLM может использовать ТОЛЬКО реальные таблицы из схемы

    Важно: грамматика перекомпилируется при каждом запросе
    с актуальным списком таблиц из БД.
    """

    def build_sql_grammar(self, schema: dict) -> str:
        """
        Построить GBNF грамматику SQL под конкретную схему БД.
        table_names и column_names берутся из реальной схемы.
        """
        table_names = " | ".join(f'"{t}"' for t in schema["tables"])
        # Генерируем grammar с динамическими нетерминалами
        return f"""
root        ::= select_stmt

select_stmt ::= "SELECT" ws columns ws "FROM" ws table_ref ws where_clause?

table_ref   ::= {table_names}

columns     ::= "*" | column_list
column_list ::= column_ref ("," ws column_ref)*

where_clause ::= "WHERE" ws condition
condition    ::= column_ref ws operator ws value

operator    ::= "=" | "!=" | "<" | ">" | "<=" | ">="
value       ::= string_val | number_val | null_val
string_val  ::= "'" [^']* "'"
number_val  ::= "-"? [0-9]+ ("." [0-9]+)?
null_val    ::= "NULL"

column_ref  ::= [a-zA-Z_][a-zA-Z0-9_.]*
ws          ::= [ \t\n]*
"""
```

## Интеграция с vLLM

```python
from langchain_openai import ChatOpenAI

class VLLMConstrainedGenerator:
    """
    Использование guided_grammar в vLLM через LangChain.
    XGrammar встроен как дефолтный бэкенд — не нужна доп. установка.
    """

    def __init__(self, vllm_url: str = "http://localhost:8000"):
        self.llm = ChatOpenAI(
            base_url=f"{vllm_url}/v1",
            api_key="token-abc123",
            model="Qwen2.5-7B-Instruct"
        )

    def generate_sql(self, natural_language: str, db_schema: dict) -> str:
        """
        Сгенерировать SQL строго по схеме БД.
        guided_grammar гарантирует синтаксически корректный SQL
        с реально существующими таблицами.
        """
        grammar = DynamicGrammarBuilder().build_sql_grammar(db_schema)

        response = self.llm.invoke(
            f"Convert to SQL: {natural_language}",
            extra_body={
                "guided_grammar": grammar,
                "guided_backend": "xgrammar"  # явно указать (по умолчанию и так)
            }
        )
        return response.content

    def generate_migration_dsl(self, description: str) -> str:
        """
        Сгенерировать DSL миграции данных по описанию на русском.
        GBNF_MIGRATION_DSL гарантирует только допустимые 18 операций.
        """
        response = self.llm.invoke(
            f"Создай план миграции данных: {description}",
            extra_body={"guided_grammar": GBNF_MIGRATION_DSL}
        )
        return response.content


PRODUCTION_CASES = {
    "case_1_sql_generation": {
        "проблема": "LLM галлюцинирует несуществующие таблицы и колонки",
        "решение": "Динамическая грамматика под реальную схему БД",
        "гарантия": "100% синтаксически + структурно корректный SQL"
    },
    "case_2_migration_dsl": {
        "операции": 18,
        "пример": "RENAME COLUMN user_id TO id; MOVE TABLE orders TO schema_v2",
        "гарантия": "Только допустимые операции, нет опечаток в синтаксисе"
    },
    "case_3_rag_fusion": {
        "задача": "Переформулировка запроса для RAG Fusion",
        "схема": '{"queries": ["query1", "query2", "query3"]}',
        "гарантия": "Всегда ровно 3 варианта запроса в правильном JSON"
    },
    "xgrammar_performance": {
        "CI_tokens": "~99% (предвычисляются при компиляции грамматики)",
        "CD_tokens": "~1% (runtime проверка)",
        "latency_overhead": "минимальный vs без грамматики",
        "интеграция": "дефолт в vLLM + TensorRT-LLM"
    }
}
```

## Применение к Lorenzo

```python
# Lorenzo: GBNF для структурированного вывода скриптов

class LorenzoStructuredOutput:
    """
    Safreliy паттерн для Lorenzo:
    GBNF-грамматика для gateaway.py /api/ask → структурированный ответ.
    Гарантировать формат ответа без retry:
    {"answer": str, "sources": list[str], "confidence": float}

    Для improve_llm_enrich.py: GBNF гарантирует что LLM вернёт
    ровно нужные поля карточки без галлюцинаций лишних ключей.
    """

    LORENZO_RESPONSE_GRAMMAR = r"""
root     ::= "{" ws
             "\"answer\"" ws ":" ws string ws "," ws
             "\"sources\"" ws ":" ws str_array ws "," ws
             "\"confidence\"" ws ":" ws number ws
             "}"

str_array ::= "[" ws (string ("," ws string)*)? ws "]"
string    ::= "\"" [^"]* "\""
number    ::= [0-9] ("." [0-9]+)?
ws        ::= [ \t\n]*
"""
```

## Возможные комбинации

| Комбинация | Новое свойство |
|------------|----------------|
| **GBNF + SAP Text2SQL (R49)** | Динамическая GBNF грамматика по схеме SAP → 100% корректный SAP SQL без галлюцинаций таблиц |
| **GBNF + LangGraph (R44)** | LangGraph узлы возвращают строго типизированные структуры через GBNF — нет ошибок парсинга |
| **GBNF + Agent Evaluation (R48)** | Golden Set оценивает не только ответ но и соответствие грамматике: структурная корректность tool calls |
| **GBNF + SENTINEL (R47)** | SENTINEL Layer 2 + GBNF: детектировать injection через нарушение грамматики входящего промпта |
| **GBNF + Lorenzo Gateway** | /api/ask всегда возвращает валидный JSON — нет retry при парсинге ответа |

## Контакт

- Статья: https://habr.com/ru/companies/postgrespro/articles/922260/ (июнь 2025)
- EN версия: https://habr.com/en/companies/postgrespro/articles/923866/
- Автор: Safreliy (Postgres Professional)
- XGrammar: xgrammar.mlc.ai (GitHub: mlc-ai/xgrammar)
- vLLM guided_grammar: docs.vllm.ai/en/latest/features/structured_outputs.html
- GBNF: github.com/ggerganov/llama.cpp/blob/master/grammars/README.md
- Иерархия Хомского: en.wikipedia.org/wiki/Chomsky_hierarchy
- Смежная (Structured output v2, R40): docs/06-discovery/round-40/
- Смежная (SAP Text2SQL, R49): docs/06-discovery/round-49/projects/gennadybanin-text2sql-sap-erp-schema-explorer.md

## Смотрите также
- [Главная](../../../README.md)
- [Метрики](../../../METRICS.md)
- [Здоровье](../../../HEALTH.md)
- [Глоссарий](../../../GLOSSARY.md)
- [Сущности](../../../ENTITIES.md)
- [Решения](../../../DECISIONS.md)
