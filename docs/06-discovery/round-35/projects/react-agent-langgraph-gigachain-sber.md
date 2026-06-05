# Современный ReAct-агент с LangGraph: от текстового парсинга к function calling

> [!WARNING]
> Документ содержит описание рисков и ограничений. Изучите их перед принятием архитектурных решений.

<!-- alert-added -->

**Автор:** trashchenkov (GigaChain / Сбер AI)  
**Хабр:** https://habr.com/ru/companies/sberbank/articles/934938/  
**GitHub:** https://github.com/ai-forever/gigachain  
**Слой:** orchestration  
**Дата:** август 2025  
**Уникальность:** Документирует переход от оригинального text-parsing ReAct (arXiv 2022) к современному structured function calling — с объяснением где старый подход ломается в production. LangGraph как циклический state machine с checkpoint-based persistence (StateSnapshot + MemorySaver) для multi-turn памяти. Полный рабочий код с GigaChat-2-Max (российская LLM), не OpenAI.

## Проблема: оригинальный ReAct ломается в production

```
ReAct (2022, arXiv:2210.03629):
  Thought: нужно узнать погоду в Москве
  Action: search[погода Москва]
  Observation: +15°C, облачно
  → ответ: "В Москве сейчас +15°C"

Проблема: LLM парсит текстовые метки "Thought/Action/Observation"
  → Модель "придумывает" Observation (галлюцинирует инструменты)
  → Нет гарантии формата → парсинг ломается
  → Нет памяти между сессиями
  → Параллельный вызов инструментов невозможен

Современный ReAct (2025):
  → function calling: структурированный JSON, не текст
  → LangGraph: явный state machine с персистентностью
  → MemorySaver: multi-turn память через checkpoints
  → Параллельные tool calls из коробки
```

## LangGraph: циклический граф вместо DAG

```python
# gigachain: github.com/ai-forever/gigachain
# LangGraph = LangChain для агентов с циклами

from langgraph.graph import StateGraph, END
from langgraph.checkpoint.memory import MemorySaver
from langchain_core.messages import HumanMessage, AIMessage, ToolMessage
from typing import TypedDict, Annotated
import operator

# State: что хранится между шагами агента
class AgentState(TypedDict):
    messages: Annotated[list, operator.add]  # история сообщений

# Граф агента
def build_react_agent(tools: list, llm) -> StateGraph:
    """
    LangChain цепочки = DAG (направленный ациклический граф)
    LangGraph = позволяет циклы: agent → tools → agent → tools → ...

    Принципиальная разница:
    DAG: A → B → C (нельзя вернуться назад)
    LangGraph: agent ⟷ tools (цикл до финального ответа)
    """

    workflow = StateGraph(AgentState)

    # Узел 1: Агент (LLM)
    def call_agent(state: AgentState) -> dict:
        response = llm.invoke(state["messages"])
        return {"messages": [response]}

    # Узел 2: Инструменты
    def call_tools(state: AgentState) -> dict:
        last_message = state["messages"][-1]
        results = []
        for tool_call in last_message.tool_calls:
            tool = next(t for t in tools if t.name == tool_call["name"])
            result = tool.invoke(tool_call["args"])
            results.append(ToolMessage(
                content=str(result),
                tool_call_id=tool_call["id"]
            ))
        return {"messages": results}

    # Роутер: продолжать или завершить?
    def should_continue(state: AgentState) -> str:
        last = state["messages"][-1]
        if hasattr(last, "tool_calls") and last.tool_calls:
            return "tools"  # есть tool calls → идём в инструменты
        return END          # нет tool calls → финальный ответ

    # Собрать граф
    workflow.add_node("agent", call_agent)
    workflow.add_node("tools", call_tools)
    workflow.set_entry_point("agent")
    workflow.add_conditional_edges("agent", should_continue)
    workflow.add_edge("tools", "agent")  # ← ключевой цикл

    return workflow
```

## MemorySaver: персистентная память между сессиями

```python
from langgraph.checkpoint.memory import MemorySaver
from gigachain import GigaChat

# Создать агент с персистентной памятью
memory = MemorySaver()  # in-memory (или SqliteSaver для prod)

llm = GigaChat(
    model="GigaChat-2-Max",
    credentials=os.environ["GIGACHAT_CREDENTIALS"],
    scope="GIGACHAT_API_CORP"
)

# Зарегистрировать инструменты
tools = [web_search_tool, write_file_tool]
llm_with_tools = llm.bind_tools(tools)

# Собрать агент с памятью
graph = build_react_agent(tools, llm_with_tools)
app = graph.compile(checkpointer=memory)

# Первый вызов
config = {"configurable": {"thread_id": "user_123"}}  # ID сессии
result_1 = app.invoke(
    {"messages": [HumanMessage("Как дела у Сбера в 2025?")]},
    config=config
)

# Второй вызов — помнит предыдущий контекст
result_2 = app.invoke(
    {"messages": [HumanMessage("А что насчёт их AI продуктов?")]},
    config=config  # тот же thread_id → та же память
)

# StateSnapshot: можно посмотреть состояние в любой момент
snapshot = app.get_state(config)
print(snapshot.values["messages"])  # вся история

# Вернуться к предыдущей точке (time-travel debugging)
history = list(app.get_state_history(config))
past_state = history[2]  # 3-й checkpoint
app.invoke(None, config=past_state.config)  # перемотать назад
```

## Function Calling vs Text Parsing

```python
# Почему text parsing ломается:

# ❌ Старый ReAct (text parsing):
OLD_REACT_PROMPT = """
Используй следующие инструменты:
- search: поиск в интернете. Формат: search[запрос]
- calculate: калькулятор. Формат: calculate[выражение]

Thought: {thought}
Action: {action}
Observation: {observation}
"""
# Проблемы:
# 1. Модель может написать: "Action: search[Москва погода" (нет закрывающей скобки)
# 2. Модель "галлюцинирует" Observation до реального вызова инструмента
# 3. Нет типизации аргументов (строка vs число)

# ✅ Новый ReAct (function calling):
from langchain_core.tools import tool
from pydantic import BaseModel

class SearchInput(BaseModel):
    query: str
    max_results: int = 5

@tool(args_schema=SearchInput)
def web_search(query: str, max_results: int = 5) -> str:
    """Поиск информации в интернете."""
    # GigaChat передаёт структурированный JSON:
    # {"name": "web_search", "args": {"query": "Москва погода", "max_results": 3}}
    return search_api.search(query, limit=max_results)

# LangGraph гарантирует:
# → JSON невалидный → исключение на уровне pydantic, не парсинга текста
# → Нет галлюцинаций инструментов (LLM видит только реальные результаты)
# → Параллельные вызовы: LLM может вернуть несколько tool_calls за раз
```

## GigaChat-2-Max: российская LLM в production

```python
# GigaChain: адаптация LangChain для GigaChat API

from gigachain import GigaChat
from gigachain_community.tools import GigaSearchTool

# Аутентификация через Сбер OAuth
llm = GigaChat(
    credentials=os.environ["GIGACHAT_CREDENTIALS"],
    model="GigaChat-2-Max",  # самая мощная модель GigaChat
    scope="GIGACHAT_API_CORP",  # корпоративный доступ
    verify_ssl_certs=False   # корпоративная инфраструктура
)

# GigaSearch: российский поиск (не Google/Bing)
search_tool = GigaSearchTool()

# Полный агент (из кода статьи):
from langgraph.prebuilt import create_react_agent

agent = create_react_agent(
    model=llm,
    tools=[search_tool, write_file_tool],
    checkpointer=MemorySaver()
)

# Запуск:
events = agent.stream(
    {"messages": [HumanMessage("Найди последние новости о GigaChat")]},
    config={"configurable": {"thread_id": "demo"}},
    stream_mode="values"
)

for event in events:
    last_message = event["messages"][-1]
    last_message.pretty_print()

# Преимущества GigaChat vs OpenAI для RU:
GIGACHAT_ADVANTAGES = {
    "законодательство": "Данные обрабатываются в РФ (152-ФЗ)",
    "русский_язык": "Лучше понимает юридические/бизнес тексты на RU",
    "интеграция": "Сбер экосистема (BI.ZONE, СберБизнес, etc.)",
    "цена": "Корпоративный тариф ниже OpenAI при больших объёмах"
}
```

## Time-Travel Debugging: откат к прошлому состоянию

```python
# Уникальная фича LangGraph: можно откатиться к любому checkpoint

class AgentDebugger:
    """
    LangGraph сохраняет StateSnapshot для каждого шага.
    Это позволяет:
    1. Посмотреть что думал агент на каждом шаге
    2. Откатиться к нужной точке и продолжить
    3. Испытать другую ветку решений
    """

    def debug_session(self, thread_id: str):
        config = {"configurable": {"thread_id": thread_id}}

        # Посмотреть всю историю checkpoints
        for snapshot in self.app.get_state_history(config):
            print(f"Step {snapshot.config['configurable']['checkpoint_id']}")
            print(f"Messages: {len(snapshot.values['messages'])}")
            print(f"Next: {snapshot.next}")

    def rollback_and_retry(self, thread_id: str, step: int):
        """Откатиться на N шагов назад и попробовать снова."""
        config = {"configurable": {"thread_id": thread_id}}
        history = list(self.app.get_state_history(config))
        past_config = history[step].config

        # Изменить сообщение и продолжить с этой точки
        self.app.update_state(
            past_config,
            {"messages": [HumanMessage("Попробуй другой подход")]},
            as_node="agent"
        )
        return self.app.invoke(None, config=past_config)
```

## Применение к Lorenzo

```python
# Паттерн: LangGraph агент для оркестрации Lorenzo скриптов

from langgraph.prebuilt import create_react_agent
from langchain_core.tools import tool

@tool
def run_lorenzo_script(script_name: str, args: str = "") -> str:
    """Запустить скрипт Lorenzo из scripts/improve_*.py"""
    result = subprocess.run(
        ["python", f"scripts/{script_name}", *args.split()],
        capture_output=True, text=True
    )
    return result.stdout[:1000]

@tool
def search_knowledge_base(query: str) -> str:
    """Поиск по базе знаний Lorenzo"""
    # Вызов improve_llm_qa.py
    pass

# Агент-оркестратор Lorenzo с памятью сессии
lorenzo_agent = create_react_agent(
    model=llm,
    tools=[run_lorenzo_script, search_knowledge_base],
    checkpointer=MemorySaver()
)
```

## Возможные комбинации

| Комбинация | Новое свойство |
|------------|----------------|
| **LangGraph + Cursor Multi-Agent (R33)** | LangGraph state machine как backend для cursor-agent оркестратора |
| **LangGraph + HITL (R30)** | LangGraph interrupt() → HITL checkpoint перед критичными действиями |
| **LangGraph + Cognitive Memory (R31)** | MemorySaver → SQLite cognitive memory (episodic + semantic) |
| **LangGraph + 5-phase Orchestrator (R27)** | LangGraph реализует 5-фазный оркестратор с явными состояниями |
| **LangGraph + Meta-Monitor (R29)** | Meta-Monitor детектирует аномалии → LangGraph агент принимает решение |

## Контакт

- Статья: https://habr.com/ru/companies/sberbank/articles/934938/ (август 2025)
- GitHub GigaChain: https://github.com/ai-forever/gigachain
- GitVerse (mirror): gitverse.ru/GigaTeam/gigachain
- LangGraph: python.langchain.com/docs/langgraph
- GigaChat API: developers.sber.ru/portal/products/gigachat
- Оригинальный ReAct: arxiv.org/abs/2210.03629
- Смежная (Production-ready AI агент ReAct + Advanced RAG): https://habr.com/ru/articles/981100/
