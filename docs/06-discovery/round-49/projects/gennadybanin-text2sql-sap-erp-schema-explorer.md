# Сапёр в эпоху LLM: Text-to-SQL агент для SAP ERP с итеративной разведкой схемы

**Автор:** gennadybanin (Геннадий Банин, GitHub: GunS82)  
**Хабр:** https://habr.com/ru/articles/954712/  
**GitHub:** есть (Text to SQL SAP Agent)  
**Слой:** orchestration / knowledge  
**Дата:** октябрь 2025  
**Уникальность:** Schema-agnostic Text2SQL агент для SAP ERP: не генерация SQL по известной схеме, а итеративная разведка неизвестной схемы из тысяч SAP-таблиц через цикл гипотез и инструментальных проверок. 4 инструмента (are_tables_present, get_table_fields, run_sap_sql_query, get_domain_texts), 4 типа JSON-действий, confidence scoring. Точность: 15% → 85% (2/13 → 11/13 вопросов), ключевое улучшение — добавление get_domain_texts для справочных значений.

## Проблема: тысячи таблиц SAP без документации

```
SAP ERP и Text2SQL:
  → SAP содержит тысячи таблиц: VBAK (заказы), EDIDS (IDoc), BTCJOB (фоновые задания)...
  → Нет единой документации на схему
  → Имена таблиц — аббревиатуры без очевидного смысла
  → LLM "знает" SAP общо, но не конкретную конфигурацию инсталляции

Стандартный Text2SQL подход:
  → Дать LLM полную схему в промпте → генерировать SQL
  → Проблема: тысячи таблиц → контекст переполнен
  → LLM галлюцинирует: SELECT * FROM ORDERS (не существует!)
  → Корректное имя: VBAK + VBAP (header + positions)

Паттерн "Сапёр":
  → Агент не знает схему заранее
  → Агент исследует схему через инструменты перед написанием SQL
  → Гипотеза → проверка → уточнение → финальный запрос
  → Точность: 15% → 85% (с 2 до 11 из 13 вопросов)
```

## Архитектура Schema Explorer Agent

```python
# gennadybanin (GunS82): Text-to-SQL агент для SAP ERP
# habr.com/ru/articles/954712/

from dataclasses import dataclass
from typing import Literal, Optional
import json

ActionType = Literal[
    "select_tables",      # Сформировать гипотезу: какие таблицы нужны
    "explore_and_probe",  # Исследовать таблицы: поля, примеры значений
    "execute_final_query", # Выполнить финальный SQL
    "provide_final_answer" # Вернуть ответ пользователю
]

@dataclass
class AgentAction:
    """
    Структурированное действие агента (JSON output от LLM).
    Constrained decoding через JSON schema гарантирует валидность.
    """
    action_type: ActionType
    tables: Optional[list[str]] = None     # для select_tables
    sql_query: Optional[str] = None        # для execute_final_query
    answer: Optional[str] = None          # для provide_final_answer
    confidence: Optional[float] = None    # 0-1, только для final
    reasoning: Optional[str] = None       # CoT: почему выбрал эти таблицы


class SAPSchemaExplorerAgent:
    """
    Text-to-SQL агент с итеративной разведкой схемы SAP ERP.

    Паттерн: Сапёр (проверяет прежде чем наступить)
    LLM не пишет SQL сразу → сначала исследует схему → потом пишет SQL.

    Инструменты (4 штуки):
    1. are_tables_present(table_names) → exists: bool для каждой
    2. get_table_fields(table_name) → список полей с типами
    3. run_sap_sql_query(sql) → первые 10 строк результата (с LIMIT)
    4. get_domain_texts(field_name, domain_name) → расшифровка кодов (MARA→MTART)

    4 типа действий:
    select_tables → explore_and_probe → execute_final_query → provide_final_answer
    """

    def __init__(self, sap_client, llm_client):
        self.sap = sap_client
        self.llm = llm_client
        self.exploration_log = []

    async def answer_question(self, question: str) -> dict:
        """
        Полный цикл: вопрос → исследование схемы → SQL → ответ.

        Максимум 10 шагов исследования (Circuit Breaker).
        """
        messages = [
            {"role": "system", "content": self._build_system_prompt()},
            {"role": "user", "content": question}
        ]

        for step in range(10):
            # LLM генерирует следующее действие
            action = await self._get_next_action(messages)
            self.exploration_log.append(action)

            if action.action_type == "select_tables":
                # Агент сформулировал гипотезу о нужных таблицах
                existence = await self.are_tables_present(action.tables)
                tool_result = json.dumps(existence)

            elif action.action_type == "explore_and_probe":
                # Исследовать поля таблиц + попробовать выборку
                fields = {}
                for table in action.tables:
                    fields[table] = await self.get_table_fields(table)
                # Зонд: SELECT * FROM table LIMIT 3
                probe_results = {}
                for table in action.tables[:3]:  # не более 3 за шаг
                    probe_results[table] = await self.run_sap_sql_query(
                        f"SELECT TOP 3 * FROM {table}"
                    )
                tool_result = json.dumps({"fields": fields, "probes": probe_results})

            elif action.action_type == "execute_final_query":
                # Финальный SQL — выполнить
                result = await self.run_sap_sql_query(action.sql_query)
                tool_result = json.dumps(result)

            elif action.action_type == "provide_final_answer":
                # Агент готов ответить
                return {
                    "answer": action.answer,
                    "confidence": action.confidence,
                    "steps": step + 1,
                    "tables_explored": list({
                        t for a in self.exploration_log
                        if a.tables for t in a.tables
                    })
                }

            # Добавить результат инструмента в контекст
            messages.append({"role": "assistant",
                              "content": json.dumps({"action": action.__dict__})})
            messages.append({"role": "tool",
                              "content": tool_result})

        return {"error": "max_steps_exceeded", "steps": 10}

    async def are_tables_present(self, table_names: list[str]) -> dict:
        """
        Проверить существуют ли таблицы в схеме SAP.
        Критично: SAP-таблицы меняются от версии к версии.
        """
        result = {}
        for table in table_names:
            exists = await self.sap.execute(
                f"SELECT COUNT(*) FROM DD02L WHERE TABNAME = '{table}'"
            )
            result[table] = exists[0][0] > 0
        return result

    async def get_domain_texts(self,
                                field_name: str,
                                domain_name: str) -> dict:
        """
        Получить расшифровку кодовых значений из SAP Domain.

        Ключевое улучшение (15% → 85%):
        SAP хранит коды: MTART='FERT' (готовая продукция), 'HALB' (полуфабрикат)
        Без domain_texts: WHERE MTART = 'finished_goods' → ошибка
        С domain_texts: LLM знает что "готовая продукция" = MTART = 'FERT'

        Пример ответа:
        {"FERT": "Готовая продукция", "HALB": "Полуфабрикат", "ROH": "Сырьё"}
        """
        domain_values = await self.sap.execute(f"""
            SELECT DOMVALUE_L, DDTEXT
            FROM DD07T
            WHERE DOMNAME = '{domain_name}'
              AND DDLANGUAGE = 'R'
        """)
        return {row[0].strip(): row[1].strip() for row in domain_values}
```

## Результаты и анализ ошибок

```python
BENCHMARK_RESULTS = {
    "задача": "13 вопросов разной сложности по SAP ERP (IDoc, демо-данные, задания, метаданные)",
    "модель_LLM": "ChatGPT 4.1",
    "результаты": {
        "baseline_без_агента": {
            "correct": 2,
            "total": 13,
            "accuracy": 0.154,
            "проблема": "LLM галлюцинирует таблицы: SELECT FROM ORDERS вместо VBAK"
        },
        "с_schema_explorer": {
            "correct": 11,
            "total": 13,
            "accuracy": 0.846,
            "улучшение": "15% → 85%"
        }
    },

    "анализ_ошибок": {
        "до_domain_texts": {
            "correct": "7/13 (54%)",
            "проблема": "WHERE material_type = 'finished' → ошибка (нужно 'FERT')"
        },
        "после_domain_texts": {
            "correct": "11/13 (85%)",
            "исправлено": "Теперь агент знает: 'готовая продукция' = MTART = 'FERT'"
        },
        "оставшиеся_2_ошибки": (
            "SAP-специфические JOIN паттерны (client-dependent таблицы MANDT поле) "
            "и кастомные Z-таблицы без описания в стандартных DD02L/DD07T"
        )
    },

    "типы_вопросов": [
        "Интеграция IDoc: статусы входящих/исходящих сообщений",
        "Демо-данные: заказы по конкретному клиенту",
        "Фоновые задания: BTCJOB + BTCTIME + BTCSTAT",
        "Метаданные: описания полей из DD03T"
    ]
}


SYSTEM_PROMPT_PATTERN = """
Ты — SAP эксперт, помогающий найти данные в системе SAP через SQL.

Действуй методично:
1. Сформируй гипотезу о нужных таблицах (select_tables)
2. Исследуй поля и примеры данных (explore_and_probe)
3. При необходимости — получи справочники значений (через get_domain_texts)
4. Напиши финальный SQL (execute_final_query)
5. Предоставь ответ с оценкой уверенности (provide_final_answer)

Важно:
- Всегда проверяй существование таблиц перед использованием
- SAP хранит коды (FERT, HALB), не текстовые значения — всегда проверяй domain
- Используй TOP N вместо LIMIT (SAP HANA/ABAP SQL диалект)
- Для client-dependent таблиц всегда добавляй WHERE MANDT = '100'

Отвечай ТОЛЬКО в JSON формате:
{"action_type": "...", "tables": [...], "reasoning": "..."}
"""
```

## Применение к Lorenzo

```python
# Lorenzo: Schema Explorer для поиска по неизвестной структуре docs/

class LorenzoSchemaExplorer:
    """
    gennadybanin паттерн для Lorenzo:
    Адаптировать SAP Schema Explorer для docs/ структуры.

    Аналог "тысяч SAP таблиц" = "сотни docs/ файлов неизвестной структуры".
    Новый пользователь не знает что есть в docs/ — агент исследует сам.

    Инструменты для Lorenzo:
    1. list_docs(section) → файлы в разделе
    2. read_headings(file) → структура файла
    3. search_content(query) → BM25 поиск
    4. get_related(file) → связанные файлы
    """

    async def explore_and_answer(self, question: str) -> dict:
        """Итеративно исследовать docs/ → ответить."""
        # Аналог Schema Explorer, но для Markdown базы знаний
        pass
```

## Возможные комбинации

| Комбинация | Новое свойство |
|------------|----------------|
| **SAP Text2SQL + GBNF (R49)** | Динамическая GBNF грамматика по исследованной схеме SAP → 100% корректный SQL без галлюцинаций |
| **SAP Text2SQL + LangGraph (R44)** | LangGraph граф: select_tables → explore → execute → check → retry (каждое действие = узел с checkpoint) |
| **SAP Text2SQL + Agent Evaluation (R48)** | Golden Set для Text2SQL агентов: эталонные трассы исследования схемы + ожидаемые инструменты |
| **SAP Text2SQL + Temporal KG (R47)** | История запросов к схеме → темпоральный граф: как менялась схема SAP при апгрейдах |
| **SAP Text2SQL + LLM Observability (R45)** | Трейсинг каждого шага разведки: где агент ошибается в гипотезах о таблицах |

## Контакт

- Статья: https://habr.com/ru/articles/954712/ (октябрь 2025)
- Автор: gennadybanin (Геннадий Банин), GitHub: GunS82
- SAP HANA SQL: help.sap.com/docs/SAP_HANA_PLATFORM
- DD02L/DD07T: SAP Data Dictionary tables (schema + domain metadata)
- VBAK/VBAP: SAP Sales Order tables (standard)
- Смежная (Text2SQL v1, R16): docs/06-discovery/round-16/
- Смежная (Text2SQL X5 ретейл, R29): docs/06-discovery/round-29/
- Смежная (GBNF constrained decoding, R49): docs/06-discovery/round-49/projects/safreliy-gbnf-xgrammar-constrained-decoding.md
