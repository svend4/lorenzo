---
date: 2026-05-29
tags: [rag, orchestration, ingestion, architecture, roadmap]
state: normalized
---

# Agent Driven Development: LLM + Stryker мутационное тестирование

<!-- toc-auto -->
<!-- tags: agent-driven-testing-stryker-mutation-pipeline, docs -->


<!-- summary -->
> `agent-driven-testing-stryker-mutation-pipeline` — раздел документации проекта Lorenzo.


> [!NOTE]
> Документ создан на основе исследования. Ссылки ведут на связанные материалы.

<!-- alert-added -->

**Автор:** rurikovich  
**Хабр:** https://habr.com/ru/articles/1010148/  
**GitHub:** нет  
**Слой:** orchestration  
**Дата:** март 2025  
**Уникальность:** Единственная статья на Хабре с реальным применением мутационного тестирования (Stryker4s) в LLM-пайплайне. 6-gate pipeline: компиляция → зелёные тесты → стабильность → мутационное тестирование → smell-анализ → семантическое ревью. Дифференцированные пороги по типу кода (pure functions 50%, business services 40%, I/O 30%). Двухагентная архитектура: Writer Agent + Reviewer Agent с 12-пунктным чеклистом. 86.8% тестов приняты ревью (68 файлов).

## Проблема: LLM генерирует тесты которые "зелёные", но бесполезные

```
Наивная генерация тестов LLM:
  → "Напиши тест для функции calculate()" → тест написан
  → Тест проходит → покрытие растёт
  → Но: тест не проверяет граничные случаи

Мутационное тестирование обнаруживает это:
  → Stryker меняет ">" на ">=" в строке 42
  → Тест продолжает проходить → МУТАНТ ВЫЖИЛ
  → Значит: тест не проверяет этот граничный случай

6-gate pipeline с мутациями:
  → Gate 4: мутационное тестирование с порогами
  → При выживании мутанта → агент получает фидбек
  → Агент добавляет граничные тесты → перезапуск
```

## Двухагентная архитектура

```python
# rurikovich: Agent Driven Development (habr 1010148)

from dataclasses import dataclass
from typing import Literal

@dataclass
class TestGenerationRequest:
    source_code: str
    class_name: str
    code_type: Literal["pure_function", "business_service", "io_operation"]
    existing_tests: list[str] = None
    mutation_feedback: list[str] = None  # выжившие мутанты

class WriterAgent:
    """
    Агент 1: генерирует тесты на основе кода и фидбека.
    Получает информацию о выживших мутантах для улучшения.
    """

    WRITER_SYSTEM = """Ты — опытный Scala разработчик.
Генерируй ScalaTest тесты с ScalaMock.

Правила:
1. Тестируй граничные случаи (null, пустые коллекции, переполнение)
2. Используй property-based testing для бизнес-логики
3. Mockи только внешние зависимости, не внутренние
4. Каждый тест: arrange → act → assert
5. Если есть информация о выживших мутантах — добавь тесты для них"""

    async def generate(self, request: TestGenerationRequest) -> str:
        mutation_context = ""
        if request.mutation_feedback:
            mutation_context = "\n\nВЫЖИВШИЕ МУТАНТЫ (нужно покрыть):\n"
            mutation_context += "\n".join(
                f"- {m}" for m in request.mutation_feedback
            )

        prompt = f"""Код для тестирования:
```scala
{request.source_code}
```
{mutation_context}

Тип кода: {request.code_type}
Существующие тесты: {len(request.existing_tests or [])} штук.

Сгенерируй ScalaTest тесты."""

        return await self.llm.generate(
            system=self.WRITER_SYSTEM,
            user=prompt
        )


class ReviewerAgent:
    """
    Агент 2: 12-пунктный чеклист ревью сгенерированных тестов.
    Экономия токенов 30-50% (ревьюер отклоняет плохие тесты рано).
    """

    REVIEW_CHECKLIST = [
        "Тест компилируется без ошибок",
        "Нет хардкода внешних ресурсов (URL, файловые пути)",
        "Mock настроен до act-фазы",
        "assert проверяет бизнес-результат, не имплементацию",
        "Тест изолирован (нет зависимости от других тестов)",
        "Название теста описывает сценарий",
        "Граничные случаи покрыты (null, empty, max)",
        "Нет Thread.sleep() или реальных задержек",
        "Используется правильный тип assertion (shouldBe vs shouldEqual)",
        "Тест стабилен (не flaky при параллельном запуске)",
        "Нет дублирования существующих тестов",
        "Мутации покрыты (если был фидбек)"
    ]

    async def review(self, tests_code: str,
                      source_code: str) -> dict:
        checklist_str = "\n".join(
            f"{i+1}. {item}"
            for i, item in enumerate(self.REVIEW_CHECKLIST)
        )

        prompt = f"""Проверь тесты по чеклисту.

Исходный код:
```scala
{source_code}
```

Тесты:
```scala
{tests_code}
```

Чеклист:
{checklist_str}

Для каждого пункта: PASS/FAIL + краткое объяснение при FAIL.
Финальный вердикт: APPROVE/REJECT."""

        result = await self.llm.generate(user=prompt)
        return self._parse_review(result)
```

## 6-Gate Pipeline

```python
import subprocess
from pathlib import Path

class SixGatePipeline:
    """
    6 последовательных гейтов.
    Провал любого → фидбек агенту → перегенерация.
    """

    MUTATION_THRESHOLDS = {
        "pure_function":     50,  # % мутантов должно быть убито
        "business_service":  40,
        "io_operation":      30,  # I/O сложнее мутировать
        "default":           35
    }

    async def run(self, request: TestGenerationRequest,
                   max_iterations: int = 3) -> dict:
        writer = WriterAgent()
        reviewer = ReviewerAgent()

        for iteration in range(max_iterations):
            print(f"=== Итерация {iteration + 1}/{max_iterations} ===")

            # Генерация (с фидбеком от предыдущей итерации)
            tests = await writer.generate(request)

            # Gate 1: Компиляция
            if not await self._compile(tests):
                request.mutation_feedback = ["КОМПИЛЯЦИЯ FAILED: проверь синтаксис"]
                continue

            # Gate 2: Зелёные тесты
            test_results = await self._run_tests(tests)
            if not test_results["all_pass"]:
                request.mutation_feedback = [
                    f"ТЕСТ FAILED: {t}" for t in test_results["failures"]
                ]
                continue

            # Gate 3: Стабильность (3 прогона)
            if not await self._check_stability(tests, runs=3):
                request.mutation_feedback = ["FLAKY тест: нестабильный результат"]
                continue

            # Gate 4: Мутационное тестирование (Stryker4s)
            threshold = self.MUTATION_THRESHOLDS.get(
                request.code_type, self.MUTATION_THRESHOLDS["default"]
            )
            mutation_result = await self._run_stryker(tests, threshold)
            if not mutation_result["passed"]:
                # Конкретный фидбек: какие мутанты выжили
                request.mutation_feedback = mutation_result["survived_mutants"]
                print(f"  Мутантов выжило: {len(mutation_result['survived_mutants'])}")
                continue

            # Gate 5: Smell-анализ (scalafix)
            if not await self._check_smell(tests):
                request.mutation_feedback = ["CODE SMELL: проверь через scalafix"]
                continue

            # Gate 6: Семантическое ревью (Reviewer Agent)
            review = await reviewer.review(tests, request.source_code)
            if review["verdict"] == "REJECT":
                request.mutation_feedback = review["issues"]
                continue

            # Все 6 гейтов пройдены!
            return {
                "status": "APPROVED",
                "tests": tests,
                "iterations": iteration + 1,
                "mutation_score": mutation_result["score"]
            }

        return {"status": "FAILED", "iterations": max_iterations}

    async def _run_stryker(self, tests: str,
                            threshold: int) -> dict:
        """
        Stryker4s: инъекция мутаций и запуск тестов.
        Возвращает список выживших мутантов для фидбека агенту.
        """
        # sbt "stryker" → отчёт в target/stryker-reports/
        result = subprocess.run(
            ["sbt", f"set stryker / mutationScoreThreshold := {threshold}",
             "stryker"],
            capture_output=True, text=True, cwd=self.project_dir
        )

        # Парсинг отчёта Stryker
        report = self._parse_stryker_report(
            Path("target/stryker-reports/report.json")
        )

        survived = [
            f"Мутант выжил: {m['location']} ({m['mutation']}: {m['original']} → {m['mutated']})"
            for m in report["survived_mutants"]
        ]

        return {
            "passed": report["mutation_score"] >= threshold,
            "score": report["mutation_score"],
            "survived_mutants": survived
        }
```

## Результаты на реальном Scala/Akka монолите

```python
PRODUCTION_RESULTS = {
    "стек": {
        "язык": "Scala + Akka",
        "build": "SBT",
        "test_framework": "ScalaTest + ScalaMock",
        "mutation_tool": "Stryker4s",
        "coverage": "Scoverage",
        "db_testing": "PostgreSQL + Testcontainers",
        "llm": "Claude (через API)"
    },

    "метрики": {
        "файлов_сгенерировано": 68,
        "принято_ревью": "86.8%",
        "branch_coverage_delta": "+6%",
        "экономия_токенов": "30-50% (ревьюер отклоняет рано)",
        "ускорение_компиляции": "90с → 60с (JVM 3GB + параллельный backend)"
    },

    "sprint_driven_vs_coverage_driven": {
        "sprint_driven": "286 тестов за 45 спринтов (стабильно)",
        "coverage_driven": "~170-65 тестов за раунд (убывает по мере насыщения)"
    },

    "дифференцированные_пороги": {
        "чистые_функции": "50% (детерминированная логика)",
        "бизнес_сервисы": "40% (сложная логика)",
        "IO_операции":    "30% (внешние зависимости трудно мутировать)"
    }
}
```

## Применение к Lorenzo

```python
# Lorenzo: применить 6-gate pipeline к generate_*.py скриптам

class LorenzoTestPipeline:
    """
    Генерация тестов для improve_*.py скриптов через 6-gate pipeline.
    Мутационный инструмент: mutmut (Python аналог Stryker4s).
    """

    PYTHON_MUTATION_THRESHOLDS = {
        "pure_function": 60,   # утилиты без side effects
        "io_script":     30,   # скрипты с файловым I/O
        "llm_script":    20    # LLM-скрипты (внешние зависимости)
    }

    async def generate_for_script(self, script_path: str) -> dict:
        source = Path(script_path).read_text()
        request = TestGenerationRequest(
            source_code=source,
            class_name=Path(script_path).stem,
            code_type="io_script"
        )

        # Адаптация: pytest вместо ScalaTest, mutmut вместо Stryker4s
        pipeline = SixGatePipeline(
            compile_cmd=["python", "-m", "py_compile"],
            test_cmd=["pytest", "--tb=short"],
            mutation_cmd=["mutmut", "run"]
        )

        return await pipeline.run(request)
```

## Возможные комбинации

| Комбинация | Новое свойство |
|------------|----------------|
| **Stryker Pipeline + AI-review (R34)** | ai-review локальный Ollama → Reviewer Agent в 6-gate pipeline |
| **Stryker Pipeline + LangGraph (R35)** | LangGraph StateGraph: 6 гейтов как state transitions с retry |
| **Stryker Pipeline + LLAMATOR (R33)** | LLAMATOR атаки → мутации в промптах агента = тестирование robustness |
| **Stryker Pipeline + LangFuse (R38)** | Трейсы Writer/Reviewer Agent в LangFuse: latency и token cost по итерациям |
| **Stryker Pipeline + Sequential (R38)** | Sequential: Writer → Reviewer → Writer... без центрального оркестратора |

## Контакт

- Статья: https://habr.com/ru/articles/1010148/ (март 2025)
- Автор: rurikovich (Хабр)
- Stryker4s: https://stryker-mutator.io/docs/stryker4s/
- ScalaTest: scalatestplus.org
- Смежная (11-агентный QA пайплайн): https://habr.com/ru/articles/1019656/
- Смежная (VK AST-based unit test gen): https://habr.com/ru/companies/vk/articles/921410/
- Смежная (Яндекс VLM для E2E тестов): https://habr.com/ru/companies/yandex/articles/970428/

## Смотрите также
- [Главная](../../../README.md)
- [Метрики](../../../METRICS.md)
- [Здоровье](../../../HEALTH.md)
- [Глоссарий](../../../GLOSSARY.md)
- [Сущности](../../../ENTITIES.md)
- [Решения](../../../DECISIONS.md)
