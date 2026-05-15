---
date: 2026-05-15
tags: [memory, rag, orchestration, ingestion, local-first]
state: normalized
---

# Multi-Agent LLM Customer Support: 92% автоматизации без эскалации на живых операторов

<!-- toc-auto -->
<!-- tags: ivan-zhirnov-multiagent-customer-support-92pct-automation, docs -->


<!-- summary -->
> `ivan-zhirnov-multiagent-customer-support-92pct-automation` — раздел документации проекта Lorenzo.


> [!WARNING]
> Документ содержит описание рисков и ограничений. Изучите их перед принятием архитектурных решений.

<!-- alert-added -->

**Автор:** ivan_zhirnov (Иван Жирнов, Передовые Платежные Решения)  
**Хабр:** https://habr.com/ru/articles/976782/  
**GitHub:** нет (production кейс)  
**Слой:** orchestration  
**Дата:** декабрь 2025  
**Уникальность:** Production-кейс миграции с rule-based chatbot на supervisor-pattern multi-agent LLM: 73,000+ текстовых диалогов/месяц, 92%+ решаются без участия человека. Конкретный разбор почему бизнес-логика вернулась из промптов в код (борьба с галлюцинациями). Два специализированных агента (транзакции vs FAQ) + детерминированный supervisor. FAISS+TF-IDF гибридный retrieval (победил Chroma). Голосовой канал: 15,000+ звонков/месяц, 20-30% автоматизация.

## Проблема: скриптовый chatbot не масштабируется

```
Финтех компания: платёжные решения для бизнеса
Каналы поддержки: 73,000+ текстовых диалогов + 15,000+ звонков/месяц

Версия 1: скриптовый чат-бот (decision tree)
  → Работает для топ-20 сценариев
  → Остальные 80% → немедленно оператор
  → Не масштабируется: каждый новый сценарий = неделя разработки
  → Ошибки: изменение одного узла ломает другие сценарии

Версия 2 (первая попытка LLM): всё в промпт
  → "Ты умный ассистент банка. Отвечай на все вопросы."
  → Проблема: галлюцинации в числах (комиссии, лимиты)
  → "Комиссия 0.5%" → может ответить "0.8%" (выдумал)
  → Нельзя доверить транзакционные данные промпту

  Урок: бизнес-логика с точными числами → В КОД, не в промпт.
  Промпт = понять намерение + объяснить. Код = достать точные данные.

Версия 3 (production): supervisor multi-agent
  Результат: 92%+ диалогов без эскалации на человека
```

## Архитектура: supervisor-pattern multi-agent

```python
# ivan_zhirnov (Передовые Платежные Решения): Multi-Agent Support Bot
# habr.com/ru/articles/976782/

from dataclasses import dataclass
from typing import Literal, Optional
from enum import Enum

class DialogIntent(Enum):
    """Намерения пользователя — определяются supervisor."""
    TRANSACTION_STATUS = "transaction"     # статус платежа, история
    ACCOUNT_QUESTION = "account"           # лимиты, тарифы, настройки
    PRODUCT_FAQ = "faq"                    # общие вопросы о продуктах
    COMPLAINT = "complaint"                # жалоба → приоритетная эскалация
    UNCLEAR = "unclear"                    # уточнить у пользователя
    ESCALATE = "escalate"                  # передать живому оператору


@dataclass
class DialogContext:
    """Контекст текущего диалога."""
    session_id: str
    messages: list[dict]
    intent: DialogIntent
    confidence: float        # уверенность supervisor в роутинге
    user_id: str
    escalation_trigger: Optional[str] = None


class DeterministicSupervisor:
    """
    Supervisor-агент: роутинг без LLM-неопределённости.

    Ключевое архитектурное решение: supervisor НЕ использует LLM
    для принятия решения об эскалации.
    → Детерминированный threshold-based роутинг
    → Эскалация = явное правило, не "LLM решил что нужен оператор"

    Почему не LLM supervisor:
    LLM может "передумать" между идентичными запросами (temperature > 0).
    Для customer support нужна предсказуемость: одинаковые условия = одинаковое решение.
    """

    ESCALATION_TRIGGERS = [
        "хочу жалобу",
        "требую возврат",
        "подать в суд",
        "руководство",
        "это безобразие"
    ]

    CONFIDENCE_THRESHOLD = 0.75  # ниже → уточняющий вопрос

    def route(self, context: DialogContext) -> str:
        """
        Детерминированный роутинг: правила + keyword matching.
        Возвращает: имя агента-обработчика.
        """
        last_message = context.messages[-1]["content"].lower()

        # Явная эскалация по ключевым словам (не LLM!)
        if any(trigger in last_message for trigger in self.ESCALATION_TRIGGERS):
            context.escalation_trigger = "keyword_match"
            return "human_agent"

        # Низкая уверенность → уточнить
        if context.confidence < self.CONFIDENCE_THRESHOLD:
            return "clarification_agent"

        # Роутинг по намерению
        routing = {
            DialogIntent.TRANSACTION_STATUS: "transaction_agent",
            DialogIntent.ACCOUNT_QUESTION: "account_agent",
            DialogIntent.PRODUCT_FAQ: "faq_agent",
            DialogIntent.COMPLAINT: "human_agent",  # всегда к человеку
            DialogIntent.UNCLEAR: "clarification_agent",
            DialogIntent.ESCALATE: "human_agent"
        }

        return routing.get(context.intent, "faq_agent")


class TransactionAgent:
    """
    Специализированный агент для транзакционных запросов.

    КЛЮЧЕВОЕ: бизнес-логика в коде, не в промпте!
    LLM понимает вопрос → код достаёт точные данные → LLM объясняет.

    Пример:
    Пользователь: "Почему списано 150 руб 15 января?"
    → LLM classifies: transaction inquiry
    → Код: SELECT * FROM transactions WHERE date='2025-01-15' AND user_id=X
    → Код: resolve commission_rule(transaction.type, transaction.amount)
    → LLM: объясняет результат на русском языке

    НЕ: "LLM, вычисли комиссию по правилам..." → галлюцинации!
    """

    async def handle(self, context: DialogContext) -> str:
        """
        Транзакционный запрос: данные из БД → LLM для объяснения.
        """
        # Шаг 1: LLM извлекает параметры из сообщения пользователя
        params = await self._extract_query_params(context)

        # Шаг 2: КОД достаёт точные данные из БД (не LLM!)
        transaction_data = await self.db.get_transactions(
            user_id=context.user_id,
            date_filter=params.get("date"),
            amount_filter=params.get("amount")
        )

        # Шаг 3: КОД применяет бизнес-правила (не LLM!)
        explanation_data = self._apply_business_rules(transaction_data)

        # Шаг 4: LLM формулирует понятный ответ по данным из кода
        response = await self._explain_to_user(context, explanation_data)

        return response


class HybridRetriever:
    """
    FAISS + TF-IDF гибридный retriever для FAQ базы.

    Выбор FAISS vs Chroma:
    Тестировали оба на корпусе документов поддержки.
    FAISS выиграл по:
    1. Скорость: FAISS (C++) vs Chroma (Python) → 3× быстрее
    2. Память: FAISS compact format vs Chroma overhead
    3. Простота деплоя: один файл vs embedded DB

    Гибрид FAISS + TF-IDF:
    TF-IDF хорошо находит точные фразы ("статья 161 ФЗ")
    FAISS хорошо находит семантически похожее ("как вернуть деньги")
    → Объединить через RRF (Reciprocal Rank Fusion)
    """

    def search(self, query: str, top_k: int = 5) -> list[dict]:
        """Гибридный поиск: FAISS semantic + TF-IDF lexical."""
        faiss_results = self._faiss_search(query, top_k * 2)
        tfidf_results = self._tfidf_search(query, top_k * 2)

        # RRF fusion
        combined = self._reciprocal_rank_fusion(
            faiss_results, tfidf_results, k=60
        )
        return combined[:top_k]


class EscalationManager:
    """
    Управление эскалацией на живых операторов.

    Три триггера эскалации:
    1. Keyword match (детерминированный, мгновенный)
    2. Low confidence (supervisor < threshold после 2 попыток уточнения)
    3. Explicit user request ("хочу говорить с оператором")

    При эскалации: полная история диалога → живой оператор.
    Оператор видит: что спрашивал пользователь + что отвечал бот.
    → Seamless handoff без повторных объяснений.
    """

    async def escalate(self, context: DialogContext) -> dict:
        """Передать диалог живому оператору с полным контекстом."""
        # Сформировать summary для оператора
        summary = await self._summarize_dialog(context)

        return {
            "action": "transfer_to_human",
            "priority": "HIGH" if context.intent == DialogIntent.COMPLAINT else "NORMAL",
            "dialog_summary": summary,
            "trigger": context.escalation_trigger,
            "full_history": context.messages
        }


PRODUCTION_RESULTS = {
    "объём": {
        "текст": "73,000+ диалогов/месяц",
        "голос": "15,000+ звонков/месяц"
    },
    "автоматизация": {
        "текст": "92%+ без участия человека",
        "голос": "20-30% (сложнее: распознавание речи + шум)"
    },
    "архитектурные_решения": {
        "supervisor": "детерминированный (не LLM) → предсказуемость",
        "retrieval": "FAISS + TF-IDF гибрид (победил Chroma по скорости)",
        "бизнес_логика": "в коде, не в промптах → нет галлюцинаций в числах",
        "время_ответа": "1-несколько секунд"
    },
    "модель": "ChatGPT-4o-mini (баланс качество/стоимость для 73K диалогов)"
}
```

## Применение к Lorenzo

```python
# Lorenzo: supervisor multi-agent для /api/ask

class LorenzoSupervisorGateway:
    """
    ivan_zhirnov паттерн для Lorenzo:
    Supervisor-роутинг запросов к /api/ask по типу запроса.

    Типы запросов Lorenzo:
    "найди проект про X" → SearchAgent (BM25/TF-IDF)
    "сравни подход A и B" → CompareAgent (2 поиска + синтез)
    "расскажи об авторе X" → ContactAgent (contacts/ + CONTACTS.md)
    "что нового в раунде N" → RoundAgent (round-N/session-log.md)

    Детерминированный supervisor: regex patterns для роутинга,
    LLM только для финального ответа с данными из кода.
    """
    pass
```

## Возможные комбинации

| Комбинация | Новое свойство |
|------------|----------------|
| **Multi-Agent Support + Behavioral Profiles (R50)** | Профили "нетерпеливый клиент" vs "детальный вопрос" → разные стратегии ответа |
| **Multi-Agent Support + LangGraph (R44)** | LangGraph: supervisor_node → transaction_node/faq_node + interrupt_before эскалация |
| **Multi-Agent Support + LLM Observability (R45)** | Трейсинг: где бот уходит в эскалацию, какие вопросы чаще всего не решаются |
| **Multi-Agent Support + Qwen3Guard (R50)** | Qwen3Guard для фильтрации токсичных запросов в поддержку до передачи агентам |
| **Multi-Agent Support + Agent Evaluation (R48)** | Golden Set: эталонные трассы "правильного" роутинга для 10 типовых сценариев поддержки |

## Контакт

- Статья: https://habr.com/ru/articles/976782/ (декабрь 2025)
- Автор: ivan_zhirnov (Иван Жирнов, Передовые Платежные Решения)
- FAISS: github.com/facebookresearch/faiss
- RRF: Reciprocal Rank Fusion (Cormack et al., 2009)
- Смежная (Robovoice голосовая поддержка, R41): docs/06-discovery/round-41/
- Смежная (5-фазный оркестратор, R27): docs/06-discovery/round-27/
- Смежная (Multi-agent coordination, R38): docs/06-discovery/round-38/

## Смотрите также
- [Главная](../../../README.md)
- [Метрики](../../../METRICS.md)
- [Здоровье](../../../HEALTH.md)
- [Глоссарий](../../../GLOSSARY.md)
- [Сущности](../../../ENTITIES.md)
- [Решения](../../../DECISIONS.md)
