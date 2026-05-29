---
date: 2026-05-29
tags: [rag, orchestration, security, knowledge, ingestion]
state: normalized
---

# Готовим AI-агента к production: HITL-фреймворк и трёхуровневая классификация действий

<!-- toc-auto -->
<!-- tags: llmstart-hitl-agent-production, docs -->


<!-- summary -->
> Готовим AI-агента к production: HITL-фреймворк и трёхуровневая классификация действий
 
 
 
>   — раздел документации проекта Lorenzo.


> [!IMPORTANT]
> Ключевой документ для понимания архитектуры. Рекомендуется прочитать в первую очередь.

<!-- alert-added -->

**Автор:** smirnoff_ai (Сергей Смирнов), LLMStart.ru (Хабр, март 2025)  
**Хабр:** https://habr.com/ru/companies/llmstart/articles/1015508/  
**GitHub:** не применимо (практическое руководство)  
**Слой:** orchestration  
**Дата:** март 2025  
**Уникальность:** Производственный гайд с полным HITL-фреймворком: трёхуровневая классификация действий агента (обязательный HITL / контекстный HITL / автономный) по критерию обратимости. Слоёная архитектура защиты: content filters, tool call limits, rate limiters. Последовательный пайплайн валидации: User → Agent → HITL-checkpoint → Tool execution. ReAct+MCP с LangSmith/Langfuse для калибровки порогов.

## Ключевой вопрос: когда агент должен спросить человека?

```
Без HITL-стратегии:
  Агент делает всё сам → ошибка = необратимые последствия
  "Удали все файлы старше 30 дней" → удалил нужные
  "Отправь письмо клиентам" → отправил всем 10K клиентов

Наивный HITL (спрашивать всегда):
  Агент → "Подтвердить чтение файла?" → Да
  Агент → "Подтвердить поиск?" → Да
  Агент → "Подтвердить анализ?" → Да
  → Usability = 0, агент бесполезен

Правильный HITL (LLMStart подход):
  Классифицировать действия по обратимости → спрашивать только когда нужно
```

## Трёхуровневая классификация действий

```python
from enum import Enum

class HITLRequirement(Enum):
    MANDATORY = "mandatory"    # всегда требует подтверждения
    CONTEXTUAL = "contextual"  # зависит от контекста
    AUTONOMOUS  = "autonomous" # агент решает сам

# Классификация по обратимости и масштабу последствий

ACTION_CLASSIFICATION = {
    # MANDATORY HITL: необратимые + высокие ставки
    HITLRequirement.MANDATORY: {
        "examples": [
            "Финансовые транзакции (переводы, платежи)",
            "Отправка email / Slack сообщений внешним получателям",
            "Удаление данных (файлы, записи БД)",
            "Изменение прав доступа (IAM, ACL)",
            "Публикация в production (деплой, release)",
            "Изменение конфигурации инфраструктуры"
        ],
        "critical_property": "Необратимо + влияет на внешние системы/людей",
        "validation": "Требует явного подтверждения + причины"
    },

    # CONTEXTUAL HITL: зависит от инициатора и контекста
    HITLRequirement.CONTEXTUAL: {
        "examples": [
            "Создание встречи в календаре (инициирует пользователь → ок)",
            "Изменение файла в рабочей директории (если пользователь попросил → ок)",
            "Запрос к внешнему API (в зависимости от данных и стоимости)",
            "Создание issue/PR (если это часть задачи → ок)"
        ],
        "critical_property": "Обратимо ИЛИ инициировано пользователем",
        "validation": "Проверить: это явно запрошено пользователем?"
    },

    # AUTONOMOUS: читающие операции, низкий риск
    HITLRequirement.AUTONOMOUS: {
        "examples": [
            "Чтение файлов, поиск по коду",
            "Веб-поиск (только чтение)",
            "Выполнение аналитических запросов к БД (SELECT)",
            "Проверка статуса (git status, health check)",
            "Генерация текста/кода для ревью"
        ],
        "critical_property": "Только чтение / легко обратимо",
        "validation": "Не требует подтверждения"
    }
}
```

## Архитектура HITL-пайплайна

```python
class HITLValidationPipeline:
    """
    Последовательная валидация: User → Agent → HITL → Tool
    """

    def execute_action(self, action: AgentAction,
                        context: ExecutionContext) -> ActionResult:
        # Слой 1: Content Filter (всегда)
        if self.content_filter.is_harmful(action):
            return ActionResult(
                status="blocked",
                reason="Content policy violation"
            )

        # Слой 2: Tool Call Limits
        if self.rate_limiter.is_exceeded(tool=action.tool,
                                          user=context.user_id):
            return ActionResult(
                status="rate_limited",
                reason=f"Tool {action.tool} limit exceeded for today"
            )

        # Слой 3: HITL Classification
        hitl_level = self.classify_action(action)

        if hitl_level == HITLRequirement.MANDATORY:
            # Создать запрос на подтверждение
            approval = self.hitl_gateway.request_approval(
                action=action,
                reason=self.explain_why_asking(action),
                timeout_sec=300,
                risk_level="HIGH"
            )
            if not approval.granted:
                return ActionResult(status="rejected_by_human",
                                    feedback=approval.reason)

        elif hitl_level == HITLRequirement.CONTEXTUAL:
            # Проверить контекст
            if not self.is_explicitly_requested(action, context):
                approval = self.hitl_gateway.request_approval(
                    action=action,
                    reason="Агент собирается выполнить действие вне явного запроса",
                    timeout_sec=60,
                    risk_level="MEDIUM"
                )
                if not approval.granted:
                    return ActionResult(status="rejected_by_human")

        # AUTONOMOUS: выполнить без подтверждения
        return self.tool_executor.execute(action)
```

## Confidence Thresholds: когда агент должен признать незнание

```python
class ConfidenceBasedHITL:
    """
    Дополнение к классификации по действиям:
    агент оценивает собственную уверенность → принимает решение о HITL
    """

    CONFIDENCE_THRESHOLDS = {
        "autonomous":   0.90,  # агент уверен на 90%+ → действует
        "ask_for_info": 0.70,  # агент уверен на 70-90% → уточняет у пользователя
        "escalate":     0.50,  # менее 70% → обязательная консультация
    }

    def should_escalate(self, action: AgentAction,
                         reasoning: AgentReasoning) -> HITLDecision:
        confidence = reasoning.confidence_score

        if confidence >= self.CONFIDENCE_THRESHOLDS["autonomous"]:
            return HITLDecision.AUTONOMOUS

        elif confidence >= self.CONFIDENCE_THRESHOLDS["ask_for_info"]:
            return HITLDecision.ASK_CLARIFICATION(
                question=self.generate_clarification_question(
                    action, reasoning.uncertain_aspects
                )
            )
        else:
            return HITLDecision.ESCALATE(
                reason=f"Низкая уверенность ({confidence:.0%}). "
                       f"Требуется человеческая экспертиза.",
                context=reasoning.decision_context
            )

    def generate_clarification_question(self, action: AgentAction,
                                         uncertain: list[str]) -> str:
        return (
            f"Прежде чем выполнить '{action.description}', "
            f"уточните: {', '.join(uncertain)}"
        )
```

## Guard Rails: защитные слои

```python
# LiteLLM Proxy как центральный rate limiter

GUARD_RAILS_CONFIG = {
    "content_filters": {
        "personal_data_detector": {
            "patterns": ["ИНН", "паспорт", "СНИЛС", r"\d{3}-\d{3}-\d{3} \d{2}"],
            "action": "redact_and_flag"
        },
        "harmful_instruction_detector": {
            "model": "classifier/harmful_content_ru",
            "threshold": 0.85,
            "action": "block"
        }
    },

    "tool_limits": {
        # Per user, per day
        "send_email":     {"limit": 10,    "window": "1d"},
        "delete_file":    {"limit": 5,     "window": "1d"},
        "api_call":       {"limit": 1000,  "window": "1h"},
        "web_search":     {"limit": 100,   "window": "1h"},
    },

    "rate_limits": {
        # Token budgets via LiteLLM Proxy
        "per_user_per_day": 500_000,   # токенов
        "per_session":      50_000,    # токенов
        "max_context":      100_000,   # токенов в одном запросе
    }
}

# LangSmith/Langfuse: калибровка порогов
class ThresholdCalibrator:
    """Анализ продакшн данных → корректировка HITL порогов"""

    def calibrate(self, trace_history: list[Trace]) -> dict:
        # Найти случаи где агент ошибся без HITL
        false_autonomous = [
            t for t in trace_history
            if t.hitl_level == "autonomous" and t.outcome == "error"
        ]
        # Найти случаи где HITL был лишним
        false_mandatory = [
            t for t in trace_history
            if t.hitl_level == "mandatory" and t.human_always_approved
        ]

        return {
            "recommendation": {
                "lower_threshold": len(false_mandatory) / len(trace_history),
                "raise_threshold": len(false_autonomous) / len(trace_history)
            }
        }
```

## ReAct + MCP интеграция

```python
# Стандартная ReAct архитектура с HITL-checkpoint

class HITLReActAgent:
    def run(self, task: str) -> str:
        thoughts = []
        for step in range(self.max_steps):
            # Thought: агент думает что делать
            thought = self.llm.think(task, thoughts, self.available_tools)

            # Action: агент выбирает действие
            action = self.parse_action(thought)

            # HITL CHECKPOINT (встроен в ReAct loop)
            result = self.hitl_pipeline.execute_action(
                action=action,
                context=ExecutionContext(
                    task=task,
                    thought_history=thoughts,
                    user_id=self.user_id
                )
            )

            if result.status == "rejected_by_human":
                # Человек отказал → агент перепланирует
                thoughts.append(Thought(
                    content=f"Действие {action.name} отклонено: {result.feedback}",
                    type="rejection"
                ))
                continue

            # Observation: результат выполнения
            thoughts.append(Thought(content=result.output, type="observation"))

            if self.is_task_complete(thoughts):
                break

        return self.synthesize_answer(thoughts)
```

## Применение к Lorenzo

Lorenzo `improve_watcher.py` + HITL паттерн:

```python
# improve_workflow_hitl.py (паттерн):

class LorenzoHITLWorkflow:
    """
    Lorenzo автономно запускает скрипты.
    HITL: для деструктивных операций — запросить подтверждение.
    """

    MANDATORY_SCRIPTS = {
        "improve_summaries.py": "Перезаписывает файлы без dry-run",
        "improve_readmes.py":   "Перезаписывает README без dry-run",
        "improve_apply*.py":    "Применяет изменения к документам"
    }

    def run_script(self, script: str, args: list) -> RunResult:
        # Обязательный HITL для деструктивных скриптов
        if any(pattern in script for pattern in self.MANDATORY_SCRIPTS):
            reason = self.MANDATORY_SCRIPTS.get(script, "Изменяет файлы")
            if not self.ask_user_confirmation(script, reason):
                return RunResult(status="skipped_by_user")

        return run_python_script(script, args)

    def ask_user_confirmation(self, script: str, reason: str) -> bool:
        print(f"\n⚠️  {script}: {reason}")
        print("Запустить? [y/N]: ", end="")
        return input().strip().lower() == "y"
```

## Возможные комбинации

| Комбинация | Новое свойство |
|------------|----------------|
| **HITL + Durable State (R23)** | ApprovalQueue = stateful HITL: агент ждёт одобрения между сессиями |
| **HITL + Orchestrator (R27)** | Оркестратор с HITL: воркер создаёт approval request при рискованных действиях |
| **HITL + AIOps (R24)** | AIOps авто-ремедиация: только после HITL для production-систем |
| **HITL + Meta-Monitor (R29)** | Meta-Monitor видит agent anomaly → автоматически повышает HITL-уровень |
| **HITL + RPA+AI (R23)** | Tool Registry с HITL: RPA-действия на prod всегда через HITL |

## Контакт

- Статья: https://habr.com/ru/companies/llmstart/articles/1015508/ (март 2025)
- Смежная (Durable State + ApprovalQueue R23): https://habr.com/ru/articles/1031440/
- Смежная (Top 10 угроз Agentic AI): https://habr.com/ru/companies/bastion/articles/963800/
- LiteLLM Proxy: github.com/BerriAI/litellm (MIT)
- LangSmith: smith.langchain.com
- Langfuse: langfuse.com

## Смотрите также
- [Главная](../../../README.md)
- [Метрики](../../../METRICS.md)
- [Здоровье](../../../HEALTH.md)
- [Глоссарий](../../../GLOSSARY.md)
- [Сущности](../../../ENTITIES.md)
- [Решения](../../../DECISIONS.md)
