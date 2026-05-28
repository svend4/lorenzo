---
date: 2026-05-28
tags: [memory, rag, orchestration, knowledge, ingestion]
state: normalized
---

# Robovoice: LLM + RAG для омниканальной службы поддержки

<!-- toc-auto -->
<!-- tags: robovoice-llm-rag-omnichannel-customer-support, docs -->


<!-- summary -->
> `robovoice-llm-rag-omnichannel-customer-support` — раздел документации проекта Lorenzo.


> [!NOTE]
> Документ создан на основе исследования. Ссылки ведут на связанные материалы.

<!-- alert-added -->

**Автор:** mmikeles (Михаил Крюков, технический директор Robovoice / SL Soft)  
**Хабр:** https://habr.com/ru/companies/slsoft/articles/877914/  
**GitHub:** нет (production-платформа), используется LangChain  
**Слой:** orchestration / analytics  
**Дата:** январь 2025  
**Уникальность:** Production омниканальный бот-оркестратор с двухагентной маршрутизацией: простые запросы (статус заявки, FAQ) минуют LLM и обрабатываются детерминированными конечными автоматами, сложные мультиходовые — через LLM + RAG с извлечением сущностей. Сравнительный бенчмарк 5 LLM для русскоязычной поддержки (GigaChat MAX, GPT-4o, LLaMA 3.1 70B, YandexGPT 4, Gemma 2 9B). Результат: автоматизация с 20% до 90%, время обработки с 10 минут до 8-15 секунд.

## Проблема: один пайплайн не работает для всех типов запросов

```
Типичная служба поддержки:
  → "Где моя заявка №12345?" — детерминированный запрос к БД
  → "Объясните разницу между тарифами" — нужен RAG по документам
  → "Почему вчера не работало?" — мультиходовой + контекст диалога
  → "Соедините с менеджером" — эскалация к человеку

Наивный монолитный подход:
  → Всё через LLM → дорого + медленно на простых запросах
  → Только FAQ-поиск → не справляется с мультиходовыми
  → Нет маршрутизации → оператор получает всё

Robovoice двухагентная архитектура:
  → Rule-based FSM: FAQ, статусы, стандартные действия (быстро, дёшево)
  → LLM + RAG: сложные запросы, контекст диалога, неструктурированные
  → Маршрутизатор-сущностей: решает кто обрабатывает запрос
  → Эскалация: когда оба агента не уверены → человек
```

## Двухагентная архитектура

```python
# Robovoice: dual-agent omnichannel routing
# Оркестратор: LangChain + Dagster ETL

from enum import Enum
from dataclasses import dataclass
from typing import Optional

class RouteDecision(Enum):
    RULE_BASED = "rule_based"    # FSM: быстро, детерминированно
    LLM_RAG = "llm_rag"         # RAG + LLM: мультиходовое, сложное
    ESCALATE = "escalate"        # Человек-оператор

@dataclass
class DialogContext:
    """Состояние диалога через все каналы (телефон, чат, email, мессенджер)."""
    session_id: str
    channel: str               # "phone" / "chat" / "email" / "telegram"
    history: list[dict]        # последние 10 ходов (~8K токенов)
    extracted_entities: dict   # ticket_id, equipment_model, branch_address
    turn_count: int


class OmnichannelRouter:
    """
    Маршрутизатор запросов: rule-based FSM vs LLM+RAG.
    Ключевой принцип: LLM задействуется только когда нужно.
    """

    # Паттерны для rule-based обработки
    RULE_PATTERNS = {
        "ticket_status": r"заявк[аи]?\s+(?:№|номер)?\s*(\d+)",
        "working_hours": ["режим работы", "часы работы", "когда открыто"],
        "contact_info":  ["телефон", "адрес", "email", "написать"],
        "cancel_request": ["отмени", "отменить заявку", "удали заявку"]
    }

    def route(self, message: str,
               context: DialogContext) -> tuple[RouteDecision, dict]:
        """
        Маршрутизация по трём критериям:
        1. Есть ли паттерн rule-based? → FSM
        2. Извлечены ли сущности для точного поиска? → LLM+RAG
        3. Неопределённость высокая? → Эскалация
        """
        # Шаг 1: Извлечение сущностей (быстрый NER)
        entities = self._extract_entities(message)

        # Шаг 2: Проверка rule-based паттернов
        for rule_name, pattern in self.RULE_PATTERNS.items():
            if self._matches(message, pattern):
                return RouteDecision.RULE_BASED, {
                    "rule": rule_name,
                    "entities": entities
                }

        # Шаг 3: Есть ли контекст для RAG?
        if len(context.history) > 0 or entities:
            return RouteDecision.LLM_RAG, {"entities": entities}

        # Шаг 4: Если полная неопределённость → эскалация
        if self._is_uncertain(message, context):
            return RouteDecision.ESCALATE, {"reason": "low_confidence"}

        return RouteDecision.LLM_RAG, {"entities": entities}

    def _extract_entities(self, message: str) -> dict:
        """
        Извлечение ключевых сущностей перед маршрутизацией.
        Интеграция с CRM/ITSM: ticket_id → реальные данные из системы.
        """
        import re
        entities = {}

        # Номер заявки
        ticket_match = re.search(r"(?:заявк[аи]?\s*(?:№|номер)?\s*)(\d+)", message)
        if ticket_match:
            entities["ticket_id"] = ticket_match.group(1)

        # Модель оборудования (зависит от домена)
        # Адрес филиала
        # ...

        return entities


class RAGSupportAgent:
    """
    LLM + RAG агент для сложных запросов.
    Dagster ETL загружает и индексирует базу знаний из 6 источников.
    """

    # Индексированные источники знаний
    KNOWLEDGE_SOURCES = [
        "1C",           # данные о заявках, клиентах
        "Bitrix24",     # CRM: история взаимодействий
        "Jira",         # задачи и инциденты
        "Zendesk",      # тикеты поддержки
        "Confluence",   # база знаний и регламенты
        "SharePoint"    # документы и инструкции
    ]

    def answer(self, message: str,
                context: DialogContext,
                entities: dict) -> dict:
        """
        RAG + LLM: поиск релевантных документов → генерация ответа.
        Контекст диалога: последние 10 ходов (~8K токенов).
        """
        # Обогащение запроса сущностями
        enriched_query = self._enrich_with_entities(message, entities)

        # RAG: поиск по базе знаний (LangChain + custom vector DB)
        docs = self.retriever.retrieve(enriched_query, top_k=5)

        # Данные из CRM по ticket_id если есть
        crm_data = self._fetch_crm_data(entities.get("ticket_id"))

        # LLM: генерация ответа с контекстом
        response = self.llm.generate(
            query=enriched_query,
            docs=docs,
            crm_data=crm_data,
            history=context.history[-10:]  # последние 10 ходов
        )

        return {
            "answer": response,
            "sources": [d["source"] for d in docs],
            "confidence": response.get("confidence", 0.0)
        }
```

## Бенчмарк 5 LLM для русскоязычной поддержки

```python
LLM_BENCHMARK = {
    "задача": "Русскоязычная служба поддержки B2B",
    "метрики": ["accuracy_%", "latency_s"],

    "результаты": [
        {
            "model": "GigaChat MAX",
            "accuracy": 92,
            "latency_s": 1.2,
            "особенность": "Лучший баланс скорость/качество для RU"
        },
        {
            "model": "GPT-4o",
            "accuracy": 96,
            "latency_s": 2.0,
            "особенность": "Лучшее качество, но дороже и медленнее"
        },
        {
            "model": "LLaMA 3.1 70B",
            "accuracy": 85,
            "latency_s": 0.8,
            "особенность": "Open-source, самый быстрый из сравниваемых"
        },
        {
            "model": "YandexGPT 4",
            "accuracy": 83,
            "latency_s": None,
            "особенность": "Российская модель, не лучшая точность"
        },
        {
            "model": "Gemma 2 9B",
            "accuracy": 89,
            "latency_s": None,
            "особенность": "Компактная, достойная точность"
        }
    ],

    "победитель_production": "GigaChat MAX (баланс точность/скорость/стоимость для RU)",
    "победитель_качество": "GPT-4o (96% но дороже)"
}

PRODUCTION_METRICS = {
    "автоматизация_до": "20%",
    "автоматизация_после": "90%",
    "время_обработки_до": "10+ минут",
    "время_обработки_после": "8-15 секунд",
    "контекст_диалога": "10 ходов (~8K токенов)",
    "интеграции": ["1C", "Bitrix24", "Jira", "Zendesk", "Confluence", "SharePoint"],
    "протоколы": ["OAuth 2.0", "TLS 1.3"]
}
```

## Логика эскалации

```python
class EscalationLogic:
    """
    Когда передавать разговор человеку-оператору.
    Эскалация = признание системы в своих ограничениях.
    """

    ESCALATION_TRIGGERS = {
        "low_confidence": 0.5,      # LLM не уверен в ответе
        "no_match_rag": True,        # RAG не нашёл релевантных документов
        "complaint_detected": True,  # Негативный тон + жалоба
        "explicit_request": [        # Явная просьба к оператору
            "соедините с менеджером",
            "хочу говорить с человеком",
            "оператор"
        ],
        "max_turns_no_resolution": 5 # 5 ходов без решения
    }

    def should_escalate(self, response: dict,
                         context: DialogContext,
                         sentiment: float) -> bool:
        """
        Многофакторное решение об эскалации.
        sentiment < 0: негативный тон → повышает приоритет эскалации.
        """
        if response["confidence"] < self.ESCALATION_TRIGGERS["low_confidence"]:
            return True
        if not response.get("sources"):  # RAG не нашёл ничего
            return True
        if sentiment < -0.3:  # Раздражённый пользователь
            return True
        if context.turn_count >= self.ESCALATION_TRIGGERS["max_turns_no_resolution"]:
            return True
        for phrase in self.ESCALATION_TRIGGERS["explicit_request"]:
            if phrase in context.history[-1].get("user", "").lower():
                return True
        return False
```

## Применение к Lorenzo

```python
# Lorenzo: dual-agent routing паттерн для Q&A

class LorenzoSupportRouter:
    """
    Robovoice паттерн для Lorenzo /api/ask:
    Простые запросы → BM25 без LLM (быстро, бесплатно)
    Сложные мультиходовые → LLM + RAG
    Неопределённые → предложить уточнить
    """

    def route_query(self, query: str, context: list) -> str:
        # Простой факт-вопрос: прямой BM25
        if self._is_factual(query) and not context:
            return "bm25_direct"

        # Мультиходовой или сложный: LLM + RAG
        if context or self._is_complex(query):
            return "llm_rag"

        # По умолчанию: гибридный поиск
        return "hybrid_search"
```

## Возможные комбинации

| Комбинация | Новое свойство |
|------------|----------------|
| **Robovoice + Академия РАНХиГС (R40)** | Два LangGraph StateGraph: поддержка + образование → единая платформа ботов |
| **Robovoice + Cognitive Memory (R31)** | SQLite память: Robovoice помнит историю клиента между сессиями |
| **Robovoice + LangFuse (R38)** | Трейсинг каждого маршрута: rule-based vs LLM, время эскалации |
| **Robovoice + Sequential (R38)** | Ансамбль агентов-специалистов обсуждает сложные кейсы без координатора |
| **Robovoice + AISecurity (R37)** | FLAME guard перед Robovoice: защита от prompt injection в поддержке |

## Контакт

- Статья: https://habr.com/ru/companies/slsoft/articles/877914/ (январь 2025)
- SL Soft: slsoft.ru
- Robovoice: robovoice.ru
- RagFlow: github.com/infiniflow/ragflow
- LangChain: langchain.com
- Смежная (LLM для колл-центра аналитика, codementor): https://habr.com/ru/articles/963364/
- Смежная (T-Bank LLM поддержка, ira_step): https://habr.com/ru/companies/tbank/articles/879128/

## Смотрите также
- [Главная](../../../README.md)
- [Метрики](../../../METRICS.md)
- [Здоровье](../../../HEALTH.md)
- [Глоссарий](../../../GLOSSARY.md)
- [Сущности](../../../ENTITIES.md)
- [Решения](../../../DECISIONS.md)
