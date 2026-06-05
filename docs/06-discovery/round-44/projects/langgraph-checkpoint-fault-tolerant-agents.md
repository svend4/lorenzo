# LangGraph: checkpoint, fault tolerance и state management для агентов

> [!TIP]
> Этот документ описывает MVP-подход. Начните с него для быстрого прототипа.

<!-- alert-added -->

**Автор:** antipov_dmitry  
**Хабр:** https://habr.com/ru/articles/956940/  
**GitHub:** нет (примеры в статье, 15+ Python сниппетов)  
**Слой:** orchestration  
**Дата:** октябрь 2025  
**Уникальность:** Глубокое сравнение LangChain vs LangGraph с 15+ рабочими Python-примерами и акцентом на production-паттерны: три бэкенда чекпоинтинга (MemorySaver/SqliteSaver/PostgresSaver), fault tolerance через `.with_retry()` + fallback цепочки, time-travel rollback, interrupt_before/after для human-in-the-loop. Единственная русскоязычная статья на Хабре с полным разбором LangGraph state management для отказоустойчивых production-агентов.

## Проблема: агенты падают и теряют состояние

```
LangChain проблемы в production:
  → Цепочки: нет состояния между вызовами
  → Агент упал на шаге 7 из 10 → начинай сначала
  → Нет контроля: нельзя остановить агента на шаге
  → Нет откатов: агент принял неверное решение → нет undo

LangGraph решение:
  → Граф с явным состоянием (State TypedDict)
  → Чекпоинты: сохранять состояние после каждого узла
  → Прерывания: interrupt_before/after любого узла
  → Time-travel: откат к любому предыдущему чекпоинту
  → Fault tolerance: retry + fallback на уровне узлов
```

## LangChain vs LangGraph: ключевые различия

```python
# antipov_dmitry: LangGraph production patterns
# habr.com/ru/articles/956940

from typing import TypedDict, Annotated
from langgraph.graph import StateGraph, END
from langgraph.checkpoint.memory import MemorySaver
from langgraph.checkpoint.sqlite import SqliteSaver
from langgraph.checkpoint.postgres import PostgresSaver
import operator

# --- LangChain: stateless цепочка ---
from langchain.chains import LLMChain
from langchain.prompts import PromptTemplate

def langchain_approach(llm):
    """LangChain: простая цепочка без состояния."""
    chain = (
        PromptTemplate.from_template("Ответь на вопрос: {question}")
        | llm
        | StrOutputParser()
    )
    # Нет состояния между вызовами
    # Нет чекпоинтов
    # Нет rollback
    return chain

# --- LangGraph: stateful граф ---
class AgentState(TypedDict):
    """Явное состояние агента — основа LangGraph."""
    messages: Annotated[list, operator.add]  # аккумулируется через узлы
    current_step: str
    tool_results: dict
    error_count: int
    final_answer: str | None


def langgraph_approach():
    """LangGraph: граф с явным состоянием и чекпоинтами."""

    def research_node(state: AgentState) -> AgentState:
        """Узел исследования: ищет информацию."""
        return {
            "current_step": "research",
            "tool_results": {"search": "...результаты поиска..."}
        }

    def reasoning_node(state: AgentState) -> AgentState:
        """Узел рассуждения: анализирует результаты."""
        return {
            "current_step": "reasoning",
            "final_answer": "...синтезированный ответ..."
        }

    def should_continue(state: AgentState) -> str:
        """Условный переход: продолжить или завершить."""
        if state["error_count"] > 3:
            return "error_handler"
        if state["final_answer"]:
            return END
        return "research"

    # Построить граф
    workflow = StateGraph(AgentState)
    workflow.add_node("research", research_node)
    workflow.add_node("reasoning", reasoning_node)
    workflow.add_conditional_edges("research", should_continue)
    workflow.add_edge("reasoning", END)
    workflow.set_entry_point("research")

    return workflow
```

## Три бэкенда чекпоинтинга

```python
class CheckpointBackends:
    """
    Три уровня чекпоинтинга для разных сред.
    Выбор бэкенда = выбор trade-off: простота vs надёжность.
    """

    @staticmethod
    def development_setup():
        """
        MemorySaver: разработка и отладка.
        Хранит состояние в RAM — теряется при перезапуске.
        """
        checkpointer = MemorySaver()

        workflow = StateGraph(AgentState)
        # ... добавить узлы ...
        app = workflow.compile(checkpointer=checkpointer)

        config = {"configurable": {"thread_id": "debug-session-1"}}
        result = app.invoke({"messages": ["Вопрос"]}, config)
        return result

    @staticmethod
    def local_production_setup(db_path: str = "agent_state.db"):
        """
        SqliteSaver: локальный production (один инстанс).
        Персистентность через SQLite — выживает перезапуск.
        Thread ID = идентификатор сессии пользователя.
        """
        with SqliteSaver.from_conn_string(db_path) as checkpointer:
            workflow = StateGraph(AgentState)
            # ... добавить узлы ...
            app = workflow.compile(checkpointer=checkpointer)

            # Возобновить прерванный сеанс
            config = {"configurable": {"thread_id": "user-42-session"}}

            # Если агент упал — продолжить с последнего чекпоинта
            result = app.invoke(
                None,  # None = возобновить с последнего чекпоинта
                config
            )
            return result

    @staticmethod
    def distributed_production_setup(connection_string: str):
        """
        PostgresSaver: распределённый production (горизонтальное масштабирование).
        Несколько инстансов агента разделяют состояние через PostgreSQL.

        Применение: LangSmith Deployment — managed LangGraph deployment.
        """
        with PostgresSaver.from_conn_string(connection_string) as checkpointer:
            checkpointer.setup()  # создать таблицы при первом запуске

            workflow = StateGraph(AgentState)
            # ... добавить узлы ...
            app = workflow.compile(checkpointer=checkpointer)

            # thread_id = session, user_id = partition key
            config = {
                "configurable": {
                    "thread_id": "enterprise-task-12345",
                    "checkpoint_ns": "production-v2"
                }
            }
            return app.invoke({"messages": ["Задача"]}, config)


CHECKPOINT_COMPARISON = {
    "MemorySaver": {
        "персистентность": "❌ Только в RAM",
        "масштабирование": "❌ Один процесс",
        "применение": "Разработка, юнит-тесты",
        "pip": "langgraph"
    },
    "SqliteSaver": {
        "персистентность": "✅ SQLite файл",
        "масштабирование": "⚠️ Один инстанс",
        "применение": "Локальный production, MVP",
        "pip": "langgraph[sqlite]"
    },
    "PostgresSaver": {
        "персистентность": "✅ PostgreSQL",
        "масштабирование": "✅ Горизонтальное",
        "применение": "Enterprise production",
        "pip": "langgraph[postgres]"
    }
}
```

## Fault Tolerance: retry и fallback

```python
from langchain_core.runnables import RunnableLambda
from tenacity import retry, stop_after_attempt, wait_exponential

class FaultTolerantAgentPatterns:
    """
    Production-паттерны для отказоустойчивых агентов.
    """

    def node_with_retry(self, llm):
        """
        .with_retry(): автоматический повтор при сбое узла.
        Применяется на уровне Runnable.
        """
        unreliable_llm = llm.with_retry(
            stop_after_attempt=3,
            wait_exponential_jitter=True,   # jitter избегает thundering herd
            retry_if_exception_type=(       # только для retryable ошибок
                ConnectionError,
                TimeoutError,
            )
        )

        def research_node(state: AgentState) -> AgentState:
            # unreliable_llm автоматически повторит 3 раза при сбое
            response = unreliable_llm.invoke(state["messages"])
            return {"messages": [response]}

        return research_node

    def node_with_fallback(self, primary_llm, fallback_llm):
        """
        .with_fallbacks(): если primary модель недоступна → fallback.
        Паттерн: дорогая модель → дешевая модель → hard error.
        """
        robust_llm = primary_llm.with_fallbacks([
            fallback_llm,
            RunnableLambda(lambda x: {"content": "Сервис временно недоступен"})
        ])

        def reasoning_node(state: AgentState) -> AgentState:
            response = robust_llm.invoke(state["messages"])
            return {"messages": [response]}

        return reasoning_node

    def error_recovery_node(self, state: AgentState) -> AgentState:
        """
        Специальный узел восстановления ошибок.
        Граф направляет сюда при error_count > threshold.
        """
        error_count = state.get("error_count", 0) + 1

        if error_count >= 3:
            # Слишком много ошибок → graceful degradation
            return {
                "final_answer": "Не удалось выполнить задачу. Обратитесь к оператору.",
                "error_count": error_count
            }

        # Попробовать упрощённый путь
        return {
            "current_step": "simplified_research",
            "error_count": error_count
        }
```

## Human-in-the-Loop: прерывания и time-travel

```python
class HumanInTheLoopPatterns:
    """
    Паттерны для вовлечения человека в процесс агента.
    """

    def setup_with_interrupts(self, workflow: StateGraph, checkpointer):
        """
        interrupt_before/after: остановить агент перед/после узла.
        Человек проверяет/корректирует состояние → агент продолжает.
        """
        app = workflow.compile(
            checkpointer=checkpointer,
            interrupt_before=["action_node"],  # остановить ДО действия
            interrupt_after=["research_node"]  # остановить ПОСЛЕ исследования
        )
        return app

    def time_travel_rollback(self, app, config: dict, thread_id: str):
        """
        Time-travel: откат к любому предыдущему чекпоинту.
        Использование: агент принял неверное решение → вернуться на шаг N.
        """
        # Получить историю чекпоинтов
        history = list(app.get_state_history(config))

        print("История состояний агента:")
        for i, state_snapshot in enumerate(history):
            print(f"  [{i}] Step: {state_snapshot.values.get('current_step')}")
            print(f"       Checkpoint ID: {state_snapshot.config['configurable']['checkpoint_id']}")

        # Откатиться к конкретному чекпоинту
        target_checkpoint = history[2]  # например, шаг 3 назад
        rollback_config = {
            "configurable": {
                "thread_id": thread_id,
                "checkpoint_id": target_checkpoint.config["configurable"]["checkpoint_id"]
            }
        }

        # Продолжить с этого чекпоинта (возможно с изменёнными данными)
        corrected_state = {
            "current_step": "research",  # переопределить шаг
            "error_count": 0             # сбросить счётчик ошибок
        }

        result = app.invoke(corrected_state, rollback_config)
        return result

    def human_approval_loop(self, app, config: dict):
        """
        Паттерн: агент предлагает действие → человек одобряет → агент выполняет.
        """
        # Запустить агент до прерывания
        state = app.invoke({"messages": ["Задача"]}, config)

        # Агент остановился для проверки
        current_state = app.get_state(config)
        proposed_action = current_state.values.get("proposed_action")

        print(f"Агент предлагает: {proposed_action}")
        human_decision = input("Одобрить? (y/n): ")

        if human_decision.lower() == "y":
            # Продолжить с одобренным действием
            app.update_state(config, {"approved": True})
            final_result = app.invoke(None, config)  # None = продолжить
        else:
            # Отменить и откатить
            app.update_state(config, {"approved": False, "final_answer": "Отменено пользователем"})
            final_result = app.invoke(None, config)

        return final_result
```

## Сравнение LangChain vs LangGraph

```python
COMPARISON_TABLE = {
    "Состояние": {
        "LangChain": "Нет встроенного состояния (каждый вызов независим)",
        "LangGraph": "TypedDict State, аккумулируется через граф"
    },
    "Персистентность": {
        "LangChain": "Только через внешние хранилища вручную",
        "LangGraph": "Встроенный checkpointer (Memory/SQLite/Postgres)"
    },
    "Fault Tolerance": {
        "LangChain": ".with_retry() на цепочках",
        "LangGraph": ".with_retry() + fallback + error recovery узлы"
    },
    "Прерывания": {
        "LangChain": "Нет",
        "LangGraph": "interrupt_before/after любого узла"
    },
    "Time-travel": {
        "LangChain": "Нет",
        "LangGraph": "get_state_history() + откат к любому чекпоинту"
    },
    "HITL": {
        "LangChain": "Ручная реализация",
        "LangGraph": "Встроенный паттерн через прерывания"
    },
    "Параллелизм": {
        "LangChain": "LCEL parallel (ограниченный)",
        "LangGraph": "fan-out/fan-in узлы нативно"
    },
    "Применение": {
        "LangChain": "Простые цепочки, RAG без состояния",
        "LangGraph": "Долгосрочные агенты, multi-step workflows"
    }
}

SYSTEM_PROFILE = {
    "библиотека": "LangGraph (LangChain Inc.)",
    "версия": "≥ 0.2 (с checkpointing)",
    "pip": "pip install langgraph langgraph[sqlite] langgraph[postgres]",
    "managed": "LangSmith Deployment (horizontal scaling)",
    "лицензия": "MIT",

    "когда_LangGraph_не_нужен": [
        "Простые RAG-пайплайны без состояния",
        "Однократные запросы без retry-логики",
        "Прототипы где fault tolerance не критична"
    ],

    "когда_LangGraph_обязателен": [
        "Агенты выполняющие задачи > 10 минут",
        "Multi-agent системы с разделённым состоянием",
        "Задачи требующие human approval на шагах",
        "Критические workloads где нельзя начинать сначала"
    ]
}
```

## Применение к Lorenzo

```python
# Lorenzo: LangGraph checkpoint для долгосрочных задач

class LorenzoAgentWithCheckpointing:
    """
    LangGraph паттерн для Lorenzo:
    improve_run_all.py как LangGraph граф с чекпоинтами.
    Если пайплайн упал на скрипте 45 из 159 → продолжить с 45, не с 1.
    """

    def build_improve_pipeline(self):
        """
        improve_run_all.py → LangGraph граф.
        Каждая группа скриптов = узел графа.
        Чекпоинт после каждой группы.
        """
        from langgraph.graph import StateGraph
        from langgraph.checkpoint.sqlite import SqliteSaver

        class PipelineState(TypedDict):
            completed_groups: list[str]
            current_group: str
            errors: dict
            metrics: dict

        workflow = StateGraph(PipelineState)

        for group in ["reports", "quality", "analytics", "export"]:
            workflow.add_node(group, self._make_group_node(group))

        workflow.set_entry_point("reports")
        workflow.add_edge("reports", "quality")
        workflow.add_edge("quality", "analytics")
        workflow.add_edge("analytics", "export")
        workflow.add_edge("export", END)

        with SqliteSaver.from_conn_string("./pipeline_state.db") as checkpointer:
            app = workflow.compile(checkpointer=checkpointer)

        return app

    def resume_after_failure(self, app, session_id: str):
        """
        Возобновить пайплайн после падения.
        SQLite чекпоинт помнит где остановились.
        """
        config = {"configurable": {"thread_id": session_id}}
        return app.invoke(None, config)  # продолжить с чекпоинта
```

## Возможные комбинации

| Комбинация | Новое свойство |
|------------|----------------|
| **LangGraph + MAESTRO (R38)** | CARL DAG → LangGraph граф: клиническая логика с персистентным состоянием между сессиями |
| **LangGraph + SherlockOps (R42)** | SherlockOps расследование как LangGraph: чекпоинт после каждого инструмента + HITL для критических решений |
| **LangGraph + LangFuse (R38)** | Трейсинг каждого чекпоинта: полная история решений агента в production |
| **LangGraph + Cognitive Memory (R31)** | SQLite чекпоинт + SQLite memory = агент помнит AND восстанавливается после падения |
| **LangGraph + Privacy Gateway (R41)** | HITL interrupt: остановиться перед отправкой PII в облако, запросить одобрение |

## Контакт

- Статья: https://habr.com/ru/articles/956940/ (октябрь 2025)
- Автор: antipov_dmitry (Habr)
- LangGraph docs: python.langchain.com/docs/langgraph
- LangSmith Deployment: smith.langchain.com
- Смежная (SherlockOps Go-агент, R42): docs/06-discovery/round-42/projects/sherlockops-llm-alert-investigation-devops.md
- Смежная (Cognitive Memory SQLite, R31): docs/06-discovery/round-31/
