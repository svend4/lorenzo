---
date: 2026-05-28
tags: [rag, orchestration, architecture, roadmap, self-improve]
state: normalized
---

# Внутри оркестратора: 5-фазная структура воркеров, meta-agent-v3, Skills Library

<!-- toc-auto -->
<!-- tags: orchestrator-5phase-multiagent, docs -->


<!-- summary -->
> Автор: AI Dev Team (aidevteam.ru), Хабр, декабрь 2025 Хабр: https://habr.com/ru/articles/975376/
Хабр: https://habr.com/ru/articles/975376/  
GitHub: github.com/kissrosecicd-hub (AI Dev Team)  
Слой: orchestration  
Дата: декабрь 2025  
Уникальность: Production мультиагентный оркестратор с


> [!WARNING]
> Документ содержит описание рисков и ограничений. Изучите их перед принятием архитектурных решений.

<!-- alert-added -->

**Автор:** AI Dev Team (aidevteam.ru), Хабр, декабрь 2025  
**Хабр:** https://habr.com/ru/articles/975376/  
**GitHub:** github.com/kissrosecicd-hub (AI Dev Team)  
**Слой:** orchestration  
**Дата:** декабрь 2025  
**Уникальность:** Production мультиагентный оркестратор с 33 специализированными агентами. Ключевое: каждый воркер работает в полной изоляции контекста (только JSON-план, без chat history) и следует строгому 5-фазному жизненному циклу. meta-agent-v3 генерирует новых агентов из 500-строчного шаблона за 2–3 минуты. Откат (backtracking) встроен структурно — валидация на фазе 3 возвращает управление оркестратору.

## Проблема с наивными мультиагентными системами

```
Наивный подход (CrewAI/AutoGen из коробки):
  Агент 1 → Агент 2 → Агент 3 → FAIL

Проблемы:
  ❌ Накопление ошибок: каждый агент наследует ошибки предыдущего
  ❌ Context pollution: chat history растёт → агенты путаются
  ❌ Нет rollback: если Агент 3 провалился → перезапуск с нуля
  ❌ Нет стандартизации: каждый агент делает всё по-своему
  ❌ Добавить нового агента = переписать систему

Production подход (AI Dev Team):
  Оркестратор ↔ Воркеры (изолированные, стандартизированные)
```

## 5-фазный жизненный цикл воркера

```python
class Worker:
    """
    Каждый специализированный агент следует одному жизненному циклу.
    Контекст: только JSON-план от оркестратора, НЕ chat history.
    """

    def execute(self, plan: WorkPlan) -> WorkReport:
        # ФАЗА 1: Читать план
        task = self.read_plan(plan)
        # Input: JSON с задачей, параметрами, ожидаемым результатом
        # Никакого chat history → чистый контекст

        # ФАЗА 2: Выполнить работу
        result = self.do_work(task)
        # Специализированная логика: код, анализ, поиск, генерация...

        # ФАЗА 3: Валидировать результат
        validation = self.validate(result, task.acceptance_criteria)
        if not validation.passed:
            # ОТКАТ: вернуть оркестратору с объяснением
            return WorkReport(
                status="failed",
                reason=validation.error,
                partial_result=result,
                retry_hints=validation.suggestions
            )

        # ФАЗА 4: Сгенерировать отчёт
        report = self.generate_report(task, result)
        # Структурированный JSON: что сделано, метрики, артефакты

        # ФАЗА 5: Вернуть управление
        return WorkReport(status="success", report=report)
```

## Оркестратор: планирование и откаты

```python
class Orchestrator:
    """Master-агент: декомпозирует задачи, распределяет, обрабатывает откаты"""

    def execute_task(self, goal: str, max_retries: int = 3) -> Result:
        # Декомпозиция цели в подзадачи
        plan = self.decompose(goal)
        # → [Task("analyze_repo"), Task("write_tests"), Task("fix_bugs"), ...]

        results = {}
        for task in plan.tasks:
            worker = self.registry.get_worker(task.type)

            for attempt in range(max_retries):
                report = worker.execute(WorkPlan(
                    task=task,
                    context=results,  # артефакты предыдущих воркеров
                    acceptance_criteria=task.success_criteria
                ))

                if report.status == "success":
                    results[task.id] = report.result
                    break
                else:
                    # Откат: оркестратор перепланирует
                    plan = self.replan(
                        original_plan=plan,
                        failed_task=task,
                        failure_reason=report.reason,
                        retry_hints=report.retry_hints
                    )
            else:
                # После max_retries → эскалация
                return Result(status="needs_human", failed_task=task)

        return Result(status="success", artifacts=results)
```

## meta-agent-v3: самогенерация агентов

```python
# Ключевое: оркестратор может создавать новых специалистов на лету

WORKER_TEMPLATE = """
# Шаблон воркера (500 строк, заполняется meta-agent-v3)

class {AgentName}Worker(BaseWorker):
    SPECIALIZATION = "{description}"
    TOOLS = {tools}           # из Skills Library
    ACCEPTANCE_CRITERIA = {   # что значит "успех"
        "primary": "{primary_metric}",
        "secondary": {secondary_metrics}
    }

    def do_work(self, task: WorkTask) -> WorkResult:
        # Специализированная логика (генерируется meta-agent-v3)
        {implementation}
"""

class MetaAgentV3:
    """Генерирует нового воркера из описания задачи"""

    def create_worker(self, need: str) -> type[Worker]:
        # "Нужен агент который умеет анализировать производительность SQL-запросов"
        spec = self.llm.design_worker(
            need=need,
            available_tools=self.skills_library.list_tools(),
            template=WORKER_TEMPLATE
        )
        worker_code = self.llm.implement(spec)
        # 2-3 минуты → новый Worker готов к использованию
        return compile_worker(worker_code)
```

## Skills Library: переиспользуемые инструменты

```python
# Аналог Tool Registry из RPA+AI (R23), но для агентов

SKILLS_LIBRARY = {
    # Файловые операции
    "read_file":    Skill(fn=read_file,    cost="low",  safety="safe"),
    "write_file":   Skill(fn=write_file,   cost="low",  safety="requires_approval"),
    "git_commit":   Skill(fn=git_commit,   cost="low",  safety="requires_approval"),

    # Анализ кода
    "run_tests":    Skill(fn=run_tests,    cost="medium", safety="safe"),
    "run_linter":   Skill(fn=run_linter,   cost="low",    safety="safe"),
    "check_types":  Skill(fn=check_types,  cost="low",    safety="safe"),

    # Веб и данные
    "web_search":   Skill(fn=web_search,   cost="medium", safety="safe"),
    "fetch_url":    Skill(fn=fetch_url,    cost="low",    safety="safe"),
    "query_db":     Skill(fn=query_db,     cost="medium", safety="safe"),

    # LLM-специфичные
    "summarize":    Skill(fn=summarize,    cost="high",   safety="safe"),
    "embed_text":   Skill(fn=embed_text,   cost="medium", safety="safe"),
    "classify":     Skill(fn=classify,     cost="medium", safety="safe"),
}

# Воркеры не вызывают инструменты напрямую → только через Skills Library
# → аудит, rate limiting, cost tracking централизованы
```

## Production опыт: 33 агента

```
Реальная система AI Dev Team (декабрь 2025):

33 специализированных агента:
  Анализаторы (8):   code_analyzer, dependency_analyzer, security_scanner...
  Генераторы (7):    test_writer, doc_writer, migration_writer...
  Валидаторы (6):    syntax_checker, logic_verifier, coverage_checker...
  Исправители (5):   bug_fixer, refactorer, optimizer...
  Репортеры (4):     report_writer, metrics_collector...
  Мета (3):         orchestrator, meta-agent-v3, skills_registry

Цикл health-check/fix/verify:
  Оркестратор → находит проблемы → запускает fixers → верифицирует
  → автоматически без человеческого участия

Ключевая метрика:
  Валидация на фазе 3 → откат до re-plan в 23% задач
  После re-plan: 94% успешно завершаются
```

## Применение к Lorenzo

Lorenzo имеет `improve_run_all.py` — оркестратор. Паттерн 5-фаз:

```python
# improve_workflow_v3.py (паттерн):
# Каждый скрипт Lorenzo = воркер с 5-фазным циклом

class LorenzoWorkerV3:
    """Обёртка для любого improve_*.py в 5-фазный цикл"""

    def execute(self, script: str, plan: dict) -> WorkReport:
        # Фаза 1: Читать план (что ожидается от скрипта)
        task = plan[script]

        # Фаза 2: Выполнить
        result = run_script(script, task.args)

        # Фаза 3: Валидировать (есть ли ожидаемые артефакты)
        if not self.validate_output(result, task.expected_outputs):
            return WorkReport(status="failed", reason=result.stderr)

        # Фаза 4: Отчёт
        report = {"script": script, "duration": result.time, "lines": result.output_lines}

        # Фаза 5: Вернуть
        return WorkReport(status="success", report=report)

class LorenzoOrchestrator:
    """improve_run_all.py v3: с откатами и перепланированием"""

    def run(self, goal: str) -> None:
        plan = self.decompose_goal(goal)
        for task in plan:
            report = LorenzoWorkerV3().execute(task.script, plan)
            if report.status == "failed":
                plan = self.replan(plan, failed=task)
```

## Возможные комбинации

| Комбинация | Новое свойство |
|------------|----------------|
| **Orchestrator + CAVM (R26)** | CAVM-переменные = артефакты между воркерами (общее пространство состояния) |
| **Orchestrator + Durable State (R23)** | SessionContext = состояние оркестратора между перезапусками |
| **Orchestrator + RPA+AI (R23)** | Skills Library = Tool Registry: воркеры вызывают RPA-скрипты |
| **Orchestrator + AIOps (R24)** | Оркестратор инцидентов: Anomaly → IncidentPredictor → AutoFixer |
| **Orchestrator + LLM Router (R20)** | Роутинг по воркерам: простые задачи → Haiku-воркер, сложные → Opus-воркер |

## Контакт

- Статья: https://habr.com/ru/articles/975376/ (декабрь 2025)
- GitHub: github.com/kissrosecicd-hub
- Смежная (архитектуры multi-agent Just AI): https://habr.com/ru/companies/just_ai/articles/1000896/
- Смежная (9 агентов на open-source): https://habr.com/ru/articles/1009608/
- Смежная (мультиагентный хаос): https://habr.com/ru/articles/1026856/

## Смотрите также
- [Главная](../../../README.md)
- [Метрики](../../../METRICS.md)
- [Здоровье](../../../HEALTH.md)
- [Глоссарий](../../../GLOSSARY.md)
- [Сущности](../../../ENTITIES.md)
