---
date: 2026-05-15
tags: [rag, orchestration, security, local-first, architecture]
state: normalized
---

# RPA + AI-агенты в Enterprise: не вместо, а вместе (RGS IT)

<!-- toc-auto -->
<!-- tags: rpa-llm-enterprise-rgs, docs -->


<!-- summary -->
> Контекст: зачем гибрид Архитектура оркестратора Пример: Tool Registry Принцип разделения ответственности
 
Архитектура оркестратора
 
Пример: Tool Registry
 
Принцип разделения ответственности
 
Изоляция и безопасность
 
Метрики RGS IT
 
Сравнение подходов
 
Применение к Lorenzo
Lorenzo имеет   и  .


> [!WARNING]
> Документ содержит описание рисков и ограничений. Изучите их перед принятием архитектурных решений.

<!-- alert-added -->

**Автор:** Сергей, руководитель технологий операций (RGS IT, Хабр)  
**Хабр:** https://habr.com/ru/companies/rgs_it/articles/1019918/  
**GitHub:** не опубликован (производственный кейс, паттерн описан)  
**Слой:** orchestration / automation  
**Дата:** апрель 2026  
**Уникальность:** Первый публичный российский production-кейс гибридной архитектуры RPA + AI-агент в enterprise: AI-агент = "мозг" (принимает решения), RPA-робот = "руки" (выполняет UI-действия в корпоративных системах). Ключевое: существующие RPA-сценарии становятся инструментами агента без переработки.

## Контекст: зачем гибрид

```
Проблема 1: Чистый RPA (без AI)
  Работает только для детерминированных задач: "нажать кнопку → заполнить поле"
  Ломается при: изменение UI, неструктурированный ввод, нестандартные кейсы

Проблема 2: Чистый AI-агент (без RPA)
  Умён, но не имеет доступа к корпоративным системам (SAP, 1С, legacy UI)
  Нет готовых интеграций с корпоративным ПО

Решение: гибрид
  AI-агент = планирование + reasoning + обработка неструктурированных данных
  RPA = выполнение действий в UI корпоративных систем
```

## Архитектура оркестратора

```
Запрос → AI-агент (LLM: GPT-4o / Claude Sonnet)
      ↓ reasoning + planning
Orchestrator
  → Tool Registry (каталог доступных RPA-сценариев)
  → выбирает нужный инструмент
  → передаёт параметры
      ↓
RPA-робот (UiPath / ROBIN / Sherpa RPA)
  → выполняет UI-действия в SAP / 1С / веб-системе
  → возвращает результат
      ↓
Orchestrator → AI-агент (анализирует результат → следующий шаг)
```

## Пример: Tool Registry

```python
# Существующие RPA-сценарии → описания для LLM
TOOL_REGISTRY = {
    "create_1c_invoice": {
        "description": "Создать счёт в 1С:Предприятие по параметрам",
        "parameters": {
            "client_name": "str",
            "amount": "float",
            "due_date": "str (YYYY-MM-DD)"
        },
        "rpa_script": "scripts/1c_create_invoice.robot"
    },
    "check_sap_order_status": {
        "description": "Проверить статус заказа в SAP ERP по номеру",
        "parameters": {"order_id": "str"},
        "rpa_script": "scripts/sap_order_status.robot"
    },
    "send_hr_notification": {
        "description": "Отправить уведомление в HR-систему",
        "parameters": {"employee_id": "str", "message": "str"},
        "rpa_script": "scripts/hr_notify.robot"
    }
}

# AI-агент вызывает инструмент как обычный LLM tool:
tools = [format_as_openai_tool(t) for t in TOOL_REGISTRY.values()]
response = llm.chat(messages, tools=tools)
# Агент выбирает нужный RPA-инструмент и параметры → Orchestrator исполняет
```

## Принцип разделения ответственности

```
AI-агент (интеллект):
  ✅ Понимает неструктурированный запрос на естественном языке
  ✅ Планирует последовательность шагов
  ✅ Обрабатывает исключения ("заказа нет → уведомить менеджера")
  ✅ Принимает решения при неоднозначности
  ❌ НЕ выполняет GUI-действия напрямую

RPA-робот (исполнение):
  ✅ Работает с любым корпоративным UI (SAP, 1С, legacy web)
  ✅ Надёжно воспроизводит клики, ввод данных
  ✅ Работает под service account (без передачи credentials агенту)
  ✅ Существующие сценарии без переработки
  ❌ НЕ принимает решения, НЕ обрабатывает неструктурированный ввод
```

## Изоляция и безопасность

```python
# Оркестратор обеспечивает изоляцию:
class RobotOrchestrator:
    def execute_rpa_tool(self, tool_name: str, params: dict, agent_id: str):
        # 1. Проверить права агента на инструмент
        if not self.acl.can_use(agent_id, tool_name):
            raise PermissionError(f"Agent {agent_id} cannot use {tool_name}")

        # 2. Запустить робота под его service account (не передаём credentials агенту)
        robot = RobotRunner(
            script=TOOL_REGISTRY[tool_name]["rpa_script"],
            service_account=self.robot_accounts[tool_name],  # изолированный аккаунт
            params=params
        )

        # 3. Аудит-лог
        self.audit.log(agent_id, tool_name, params, timestamp=now())

        return robot.run()
```

## Метрики RGS IT

```
До гибридной архитектуры:
  Время обработки типовой заявки: 2-3 часа (ручная обработка)
  Ошибки из-за человеческого фактора: ~8% заявок

После внедрения AI-агент + RPA:
  Время обработки: 12-20 минут (автоматически)
  Ошибки: ~1% (только нестандартные кейсы)
  Охват автоматизации: 70% входящих заявок

Преимущество vs чистого RPA:
  Нет "ломания" при изменении UI формулировок — агент переформулирует
  Нестандартный кейс → агент → эскалация человеку (не упал процесс)
```

## Сравнение подходов

```
Только RPA:
  ✅ Надёжно для детерминированных задач
  ✅ Дёшево в эксплуатации
  ❌ Ломается при UI-изменениях
  ❌ Не обрабатывает неструктурированный ввод

Только AI-агент:
  ✅ Понимает любой запрос
  ✅ Гибкий reasoning
  ❌ Нет доступа к корпоративным UI
  ❌ Нужен API/MCP для каждой системы

Гибрид AI + RPA:
  ✅ Понимание + выполнение
  ✅ Существующий RPA-парк → инструменты агента
  ✅ Изоляция credentials
  ⚠️ Сложнее отладка (2 слоя)
  ⚠️ Latency += время RPA-выполнения
```

## Применение к Lorenzo

Lorenzo имеет `improve_workflow_v2.py` и `improve_watcher.py`.  
RPA+AI паттерн = **Script-as-Tool**: Python скрипты Lorenzo становятся инструментами агента:

```python
# improve_script_agent.py (паттерн):
SCRIPT_REGISTRY = {
    "run_quality_check": {
        "description": "Запустить проверку качества документов в секции",
        "parameters": {"section": "str (e.g. 05-habr-projects)"},
        "script": "improve_run_all.py --group quality --section {section}"
    },
    "update_search_index": {
        "description": "Обновить поисковый индекс после изменения файлов",
        "parameters": {},
        "script": "improve_index_update.py"
    },
    "run_discovery_search": {
        "description": "Найти похожие проекты для файла",
        "parameters": {"file_path": "str"},
        "script": "improve_collab_finder.py --file {file_path} --top 5"
    }
}

# AI-агент выбирает нужный скрипт и запускает
# Аналог RPA — скрипт как "UI-автоматизация" над файловой системой
```

## Возможные комбинации

| Комбинация | Новое свойство |
|------------|----------------|
| **RPA+AI + A2A (R21)** | Разные AI-агенты управляют разными RPA-доменами через A2A |
| **RPA+AI + Durable State (R23)** | SessionContext для долгих RPA-процессов (reconnect, resume) |
| **RPA+AI + 3-Agent Case (R21)** | Discovery/Enricher/Monitor как RPA-инструменты AI-оркестратора |
| **RPA+AI + Langfuse (R13)** | Трейсинг: какой агент вызвал какой RPA-инструмент |
| **RPA+AI + n8n (R22)** | n8n = visual workflow для оркестрации AI-агент → RPA |

## Контакт

- Статья: https://habr.com/ru/companies/rgs_it/articles/1019918/ (апрель 2026)
- Смежная (От RPA к ИИ-агентам, эра): https://habr.com/ru/companies/sherpa_rpa/articles/847058/
- Смежная (LLM автоматизация рутины, SberDevices): https://habr.com/ru/companies/sberdevices/articles/806133/
- UiPath (RPA лидер): uipath.com
- ROBIN (RU RPA платформа): robin.company

## Смотрите также
- [Главная](../../../README.md)
- [Метрики](../../../METRICS.md)
- [Здоровье](../../../HEALTH.md)
- [Глоссарий](../../../GLOSSARY.md)
- [Сущности](../../../ENTITIES.md)
