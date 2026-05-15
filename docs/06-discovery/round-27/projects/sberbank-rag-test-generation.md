---
date: 2026-05-15
tags: [rag, orchestration, ingestion, architecture, self-improve]
state: normalized
---

# Автогенерация тестов в IDE: RAG + LLM превращают ручные сценарии в код

<!-- toc-auto -->
<!-- tags: sberbank-rag-test-generation, docs -->


<!-- summary -->
> Автогенерация тестов в IDE: RAG + LLM превращают ручные сценарии в код — раздел документации проекта Lorenzo.
 
 
 
>   — раздел документации проекта Lorenzo.


> [!WARNING]
> Документ содержит описание рисков и ограничений. Изучите их перед принятием архитектурных решений.

<!-- alert-added -->

**Автор:** Sergo_01 (Александр Поляков), Сбербанк, март 2025  
**Хабр:** https://habr.com/ru/companies/sberbank/articles/1011830/  
**GitHub:** не опубликован (внутренний плагин JetBrains)  
**Слой:** orchestration / analytics  
**Дата:** март 2025  
**Уникальность:** JetBrains IDE плагин использует PSI (Program Structure Interface) для обхода Java AST вместо работы с кодом как текстом — извлекает `@Step` аннотации и `@TmsLink` идентификаторы. RAG-пайплайн встраивает описания тест-шагов в векторное хранилище для few-shot retrieval в стиле проекта. Двойная валидация: LLM self-check + PSI-верификация синтаксиса. Результат: 68% тестов требуют минимальных правок.

## Проблема: LLM не знает ваш тест-фреймворк

```
Наивный подход:
  "Напиши тест для метода LoginService.authenticate()"
  → GPT выдаёт generic JUnit тест, не знающий:
    - ваши @Step/@TmsLink аннотации
    - стиль именования в проекте
    - набор utils и helper-классов
    - конкретные шаги из TestRail/Allure
  → 90% кода нужно переписывать

Подход Сбербанка:
  PSI понимает структуру → RAG знает стиль → LLM пишет как команда
```

## PSI: работа с AST, а не текстом

```java
// PSI (Program Structure Interface) — JetBrains API для работы с AST

class TestContextExtractor {
    /**
     * Извлекает @Step аннотации вместо regex по тексту
     * PSI гарантирует корректность даже при рефакторинге
     */
    List<StepInfo> extractSteps(PsiClass testClass) {
        List<StepInfo> steps = new ArrayList<>();

        // Обходим методы класса через AST
        for (PsiMethod method : testClass.getMethods()) {
            PsiAnnotation stepAnnotation = method.getAnnotation("io.qameta.allure.Step");
            PsiAnnotation tmsAnnotation = method.getAnnotation("io.qameta.allure.TmsLink");

            if (stepAnnotation != null) {
                steps.add(new StepInfo(
                    id: extractTmsId(tmsAnnotation),
                    description: extractValue(stepAnnotation),
                    parameters: extractParameters(method),
                    returnType: method.getReturnType().getPresentableText()
                ));
            }
        }
        return steps;
    }

    // PSI vs plain text:
    // ❌ Текст: regex('@Step\s*\("([^"]+)"\)') → сломается при переносе строки
    // ✅ PSI:   method.getAnnotation("...") → работает всегда
}
```

## RAG-пайплайн: few-shot в стиле проекта

```python
# Архитектура RAG для генерации тестов

class TestRAGPipeline:
    def __init__(self, project_path: str):
        # Индексируем все существующие тесты проекта
        self.vector_store = VectorStore()
        self._index_project_tests(project_path)

    def _index_project_tests(self, path: str) -> None:
        """Строим corpus из реальных тестов команды"""
        for test_file in find_test_files(path):
            # Извлекаем через PSI
            steps = psi_extractor.extractSteps(parse_java(test_file))
            for step in steps:
                self.vector_store.add(
                    text=step.description,
                    metadata={
                        "method_name": step.method_name,
                        "full_code": step.source_code,
                        "tms_id": step.tms_id,
                        "imports": step.required_imports
                    }
                )

    def build_few_shot_prompt(self, target_steps: list[str]) -> str:
        """Few-shot примеры из того же проекта"""
        examples = []
        for step_desc in target_steps:
            # Ищем похожие шаги в базе (cosine similarity)
            similar = self.vector_store.search(
                query=step_desc,
                top_k=3,
                min_score=0.75
            )
            examples.extend(similar)

        return GENERATION_PROMPT.format(
            examples=format_examples(examples),
            target_steps=target_steps,
            project_style=self.infer_style(examples)
        )
```

## Генерация с двойной валидацией

```python
GENERATION_PROMPT = """
Ты — senior QA инженер в команде. Пишешь тест в точном стиле команды.

Примеры из вашего проекта:
{examples}

Задача: сгенерировать тест для шагов:
{target_steps}

Требования:
1. Использовать ТОЛЬКО аннотации из примеров выше
2. Именование: точно как в примерах (camelCase, глагол+существительное)
3. @TmsLink: заглушка TMS-XXXX (заменить вручную)
4. Импорты: только те что нужны

Сгенерируй java-класс:
"""

class TestGenerationService:
    def generate(self, steps: list[str]) -> GenerationResult:
        # Шаг 1: RAG few-shot prompt
        prompt = rag_pipeline.build_few_shot_prompt(steps)

        # Шаг 2: Генерация
        raw_code = llm.generate(prompt)

        # Шаг 3: Валидация 1 — LLM self-check
        validation_prompt = f"Проверь код на соответствие стилю:\n{raw_code}"
        self_check = llm.validate(validation_prompt)

        if not self_check.passed:
            raw_code = llm.fix(raw_code, self_check.issues)

        # Шаг 4: Валидация 2 — PSI синтаксическая проверка
        psi_result = psi_validator.check_syntax(raw_code)

        if not psi_result.valid:
            # Исправляем синтаксически некорректный код
            raw_code = self.fix_syntax(raw_code, psi_result.errors)

        return GenerationResult(
            code=raw_code,
            imports=extract_imports(raw_code),
            requires_manual_review=psi_result.has_warnings
        )
```

## Результаты

```
Метрики (20 проектов Сбербанка, март 2025):

  Без RAG (zero-shot GPT):
    → 12% тестов используются без правок
    → Средние правки: 45 минут на тест

  С RAG few-shot (Сбербанк плагин):
    → 68% тестов используются без правок (или с мелкими правками)
    → Средние правки: 8 минут на тест
    → Ускорение: 5.6× по времени на написание теста

  Где помогает больше всего:
    ✅ Стандартные CRUD-операции (92% без правок)
    ✅ UI-шаги (87% без правок)
    
  Где нужна помощь человека:
    ⚠️ Сложная бизнес-логика (43% без правок)
    ⚠️ Интеграционные тесты с нестандартным стеком
```

## Интеграция в IDE

```
JetBrains Plugin (IntelliJ/Goland/PyCharm):

  Пользователь → Shift+Ctrl+T (или меню Generate)
  ↓
  Plugin PSI: сканирует открытый класс/метод
  ↓
  Plugin: показывает список найденных @Step-ов
  ↓
  Пользователь: выбирает нужные шаги для теста
  ↓
  RAG Pipeline: строит few-shot промпт из похожих тестов проекта
  ↓
  LLM: генерирует тест-метод
  ↓
  PSI Validator: проверяет синтаксис
  ↓
  Plugin: вставляет готовый код в нужное место
  ↓
  Пользователь: правит @TmsLink + edge cases
```

## Применение к Lorenzo

Lorenzo + PSI паттерн → **Структурная индексация скриптов**:

```python
# improve_script_psi.py (паттерн):
# Вместо работы со скриптами как текстом → AST-анализ через ast модуль Python

import ast

class ScriptPSI:
    """PSI для Python-скриптов Lorenzo: понимает структуру, не regex"""

    def extract_functions(self, script_path: str) -> list[FunctionInfo]:
        tree = ast.parse(open(script_path).read())
        functions = []
        for node in ast.walk(tree):
            if isinstance(node, ast.FunctionDef):
                functions.append(FunctionInfo(
                    name=node.name,
                    docstring=ast.get_docstring(node),
                    args=[a.arg for a in node.args.args],
                    decorators=[d.id for d in node.decorator_list
                                if hasattr(d, 'id')]
                ))
        return functions

    def find_similar_scripts(self, query: str) -> list[str]:
        """RAG по описаниям функций — как RAG по @Step аннотациям"""
        return rag_search(
            query=query,
            corpus=self.index_all_scripts()
        )
```

## Возможные комбинации

| Комбинация | Новое свойство |
|------------|----------------|
| **RAG TestGen + DerAI (R27)** | SAST находит уязвимость → TestGen пишет security-тест для неё автоматически |
| **RAG TestGen + LLM unit tests (R20)** | Mutation testing: LLM тесты → мутации → проверка покрытия |
| **RAG TestGen + Code Review AI (R15)** | Code review видит изменение → автоматически генерирует тест для него |
| **RAG TestGen + CAVM (R26)** | CAVM пайплайн: изменения → тесты → запуск → отчёт автоматически |
| **RAG TestGen + Orchestrator (R27)** | Воркер-специалист по тестам в 5-фазном оркестраторе |

## Контакт

- Статья: https://habr.com/ru/companies/sberbank/articles/1011830/ (март 2025)
- Смежная (VK юнит-тесты с LLM): https://habr.com/ru/companies/vk/articles/921410/
- Смежная (AI тесты которые ничего не тестируют): https://habr.com/ru/articles/1023532/
- PSI API (JetBrains): plugins.jetbrains.com/docs/intellij/psi.html
- Allure TestOps: qameta.io/allure

## Смотрите также
- [Главная](../../../README.md)
- [Метрики](../../../METRICS.md)
- [Здоровье](../../../HEALTH.md)
- [Глоссарий](../../../GLOSSARY.md)
- [Сущности](../../../ENTITIES.md)
