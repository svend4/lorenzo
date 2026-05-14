# Мультиагентная разработка в Cursor: субагенты для больших проектов

**Автор:** rdudov (Хабр, ноябрь 2025)  
**Хабр:** https://habr.com/ru/articles/971620/  
**GitHub:** https://github.com/rdudov/agents  
**Слой:** orchestration  
**Дата:** ноябрь 2025  
**Уникальность:** Практическая оркестрация в Cursor без нативной поддержки мультиагентов: координатор → субагенты (аналитик/архитектор/планировщик/разработчик/ревьюер) через cursor-agent CLI. Маршрутизация моделей: Opus 4.5 для анализа, Composer-1 для реализации. Изоляция контекста каждого субагента. GitHub с рабочими промптами.

## Проблема: параллельные агенты на большом коде = хаос

```
Наивный подход (один агент на весь проект):
  → Контекст 100K+ токенов → галлюцинации
  → Агент теряет нить в середине большого рефакторинга
  → Timeout, OOM, незавершённые изменения

Наивный мультиагентный подход (без оркестрации):
  → Агент А пишет класс User
  → Агент Б параллельно пишет класс User иначе
  → Конфликт → merge hell

Правильный подход (rdudov):
  → Сначала skeleton (framework) сверху вниз
  → Только потом параллельная реализация
  → Каждый агент видит только свой контекст
```

## Архитектура: Orchestrator → Specialist Agents

```bash
# cursor-agent CLI: запуск субагента из командной строки
# GitHub: github.com/rdudov/agents

# Оркестратор: центральный агент, координирует субагентов

ORCHESTRATOR_PROMPT = """
Ты — старший инженер. Управляй командой субагентов.
Твои инструменты: cursor-agent <role> <task> <context_file>

Роли субагентов:
- analyst:    анализирует требования, создаёт tech spec
- architect:  проектирует структуру кода, интерфейсы
- planner:    декомпозирует задачу на файлы/модули
- developer:  реализует конкретный файл/функцию
- reviewer:   проверяет результат, находит баги

Последовательность:
1. analyst → spec.md
2. architect → architecture.md + interfaces.py
3. planner → tasks.json (список файлов)
4. developer × N (параллельно по файлам из tasks.json)
5. reviewer → review.md + патчи

Правило: каждый субагент получает ТОЛЬКО свои входные данные.
"""

# Запуск субагента
import subprocess

def run_subagent(role: str, task: str, context_file: str) -> str:
    result = subprocess.run(
        ["cursor-agent", role, "--task", task, "--context", context_file],
        capture_output=True, text=True, timeout=300
    )
    return result.stdout
```

## Маршрутизация моделей по задаче

```python
# Ключевой insight: разные задачи требуют разных моделей

MODEL_ROUTING = {
    "analyst": {
        "model": "claude-opus-4-5",   # мощная модель для глубокого анализа
        "задача": "понять требования, найти неочевидные проблемы",
        "cost_per_task": "высокая, но важно не ошибиться"
    },
    "architect": {
        "model": "claude-opus-4-5",   # архитектура = критичное решение
        "задача": "спроектировать интерфейсы, избежать coupling",
        "cost_per_task": "высокая"
    },
    "planner": {
        "model": "claude-sonnet-4-6", # средняя задача: декомпозиция
        "задача": "разбить на файлы, порядок реализации"
    },
    "developer": {
        "model": "composer-1",        # специализирован на коде, дешевле
        "задача": "реализовать конкретный файл по спецификации",
        "cost_per_task": "низкая, запускается N раз"
    },
    "reviewer": {
        "model": "claude-sonnet-4-6", # достаточно для code review
        "задача": "найти баги, нарушения стиля, несоответствия spec"
    }
}

# Суммарная стоимость vs один Opus на всё:
# Orchestration cost ≈ 0.4× от "Opus на всё"
# При этом качество выше (каждый агент фокусирован)
```

## Изоляция контекста: каждый агент видит только своё

```python
class ContextIsolator:
    """
    Ключевой паттерн: не давать агентам "видеть" лишнее.
    Это предотвращает hallucination и token bloat.
    """

    def prepare_developer_context(self,
                                   file_to_implement: str,
                                   architecture: dict,
                                   spec: dict) -> str:
        """
        Developer видит только:
        - Свой файл и его интерфейс
        - Зависимости (импорты)
        - Релевантную часть спецификации
        НЕ видит: другие файлы, общую архитектуру, бизнес-требования
        """
        file_spec = architecture["files"][file_to_implement]
        relevant_deps = [
            architecture["files"][dep]
            for dep in file_spec["dependencies"]
        ]

        return f"""
# Твоя задача: реализовать {file_to_implement}

## Интерфейс (что должно быть в файле):
{file_spec["interface"]}

## Зависимости (уже реализованы):
{self._summarize_deps(relevant_deps)}

## Требования к реализации:
{spec["requirements"][file_to_implement]}

## Стиль кода:
{spec["code_style"]}

Реализуй ТОЛЬКО этот файл. Не меняй другие файлы.
"""

    def prepare_reviewer_context(self, file: str,
                                  implementation: str,
                                  spec: dict) -> str:
        """
        Reviewer видит: файл + spec.
        НЕ видит: другие файлы, решения других субагентов.
        """
        return f"""
Проверь реализацию файла {file}.

Спецификация:
{spec["requirements"][file]}

Реализация:
{implementation}

Проверь: корректность логики, edge cases, стиль, типы.
"""
```

## Top-Down стратегия: skeleton первый

```python
class TopDownOrchestration:
    """
    Антипаттерн: дать 5 агентам реализовывать параллельно сразу.
    → Агент А делает class User(id, name)
    → Агент Б делает class User(user_id, username)
    → Конфликт при интеграции

    Правильно: skeleton → реализация
    """

    async def orchestrate(self, spec: Spec) -> CodeBase:
        # Шаг 1: Architect создаёт скелет (все файлы с заглушками)
        skeleton = await self.run_agent("architect",
            task="Создай скелет всех файлов с заглушками (pass/NotImplemented)",
            context=spec.architecture
        )

        # Шаг 2: Сохранить скелет в файловую систему
        # Теперь все интерфейсы согласованы ДО реализации
        self.write_skeleton(skeleton)

        # Шаг 3: Planner декомпозирует на независимые задачи
        tasks = await self.run_agent("planner",
            task="Составь список файлов для параллельной реализации",
            context=skeleton
        )

        # Шаг 4: Developer-ы реализуют параллельно (уже нет конфликтов)
        implementations = await asyncio.gather(*[
            self.run_agent("developer",
                task=f"Реализуй {file}",
                context=self.prepare_developer_context(file, skeleton, spec)
            )
            for file in tasks.files
        ])

        # Шаг 5: Reviewer проверяет каждый файл
        reviews = await asyncio.gather(*[
            self.run_agent("reviewer", task=f"Проверь {file}", context=impl)
            for file, impl in zip(tasks.files, implementations)
        ])

        return self.merge(implementations, reviews)
```

## Применение к Lorenzo

```python
# improve_multiagent_codegen.py (паттерн):

class LorenzoMultiAgentCodgen:
    """
    Lorenzo пишет скрипты improve_*.py.
    Мультиагентный паттерн rdudov для генерации новых скриптов.
    """

    async def generate_script(self, requirement: str) -> str:
        # Analyst: понять требование
        spec = await self.analyst.analyze(requirement)

        # Architect: спроектировать структуру скрипта
        structure = await self.architect.design(spec)

        # Developer: реализовать (один файл = один разработчик)
        code = await self.developer.implement(structure)

        # Reviewer: проверить соответствие стандартам Lorenzo
        reviewed = await self.reviewer.check(code,
            standards="scripts/improve_*.py должен иметь --dry-run флаг")

        return reviewed
```

## Возможные комбинации

| Комбинация | Новое свойство |
|------------|----------------|
| **Multi-Agent + Orchestrator (R27)** | 5-фазный оркестратор + cursor-agent CLI = production-grade coding agent |
| **Multi-Agent + HITL (R30)** | Reviewer агент → HITL checkpoint перед применением изменений |
| **Multi-Agent + RAG тесты (R27)** | Автогенерация тестов → Agent Driven Development loop |
| **Multi-Agent + Coreness Flow (R30)** | Hot-reload для агентных ролей: смена роли без перезапуска |
| **Multi-Agent + MCP (R04)** | MCP-first: каждый субагент через MCP-инструменты, не CLI |

## Контакт

- Статья: https://habr.com/ru/articles/971620/ (ноябрь 2025)
- GitHub промпты: https://github.com/rdudov/agents
- Смежная (Agent Driven Development, тесты): https://habr.com/ru/articles/1010148/
- Смежная (мультиагентная разработка до продакшена): https://habr.com/ru/articles/993470/
- cursor-agent CLI: cursor.sh (встроен в Cursor IDE)
