---
date: 2026-06-05
tags: [rag, orchestration, security, ingestion, architecture]
state: normalized
---

# Paper2Agent: научные статьи → интерактивные AI агенты через MCP

<!-- toc-auto -->
<!-- tags: paper2agent-scientific-papers-mcp-tools, docs -->


<!-- summary -->
> `paper2agent-scientific-papers-mcp-tools` — раздел документации проекта Lorenzo.


> [!NOTE]
> Документ создан на основе исследования. Ссылки ведут на связанные материалы.

<!-- alert-added -->

**Автор:** andre_dataist  
**Хабр:** https://habr.com/ru/articles/945582/  
**GitHub:** https://github.com/jmiao24/Paper2Agent  
**Слой:** orchestration  
**Дата:** сентябрь 2025  
**Уникальность:** Первый фреймворк конвертации статических научных PDF в интерактивные AI агенты через MCP: 4 специализированных субагента (environment/tutorial/function/testing) собрали 22 геномных инструмента из статьи AlphaGenome за 3 часа без ручной работы. Уникальная метрика: success rate конвертации как прокси качества публикации (плохо задокументированная статья = агент не соберётся).

## Проблема: научные статьи — мёртвые артефакты

```
Типичная научная статья:
  → PDF с кодом в виде текста
  → GitHub репо с README из трёх строк
  → "Воспроизведи результаты" = 2-3 дня работы

Исследователь хочет:
  → Использовать метод из статьи: "можешь ли ты проанализировать мои данные
    методом из этой статьи?"
  → Интерактивно: задать вопросы к данным из статьи
  → Автоматически: взять 100 статей, извлечь все методы

Paper2Agent решение:
  → PDF → MCP server с инструментами за часы
  → LLM может ВЫЗВАТЬ функции из статьи как tools
  → Reproducibility failure = quality signal
```

## Архитектура: 4 специализированных субагента

```python
# github.com/jmiao24/Paper2Agent

from paper2agent import Paper2AgentPipeline

class Paper2AgentSystem:
    """
    4 субагента выполняются последовательно:

    SubAgent 1: EnvironmentSetup
      → Парсит README, requirements.txt, Dockerfile
      → Создаёт conda/venv окружение
      → Устанавливает зависимости

    SubAgent 2: TutorialExtractor
      → Находит примеры использования в тексте статьи
      → Запускает tutorial notebooks
      → Валидирует что базовый pipeline работает

    SubAgent 3: FunctionExtractor
      → Идентифицирует ключевые функции/классы
      → Оборачивает их в MCP tools
      → Генерирует JSON Schema для каждого инструмента

    SubAgent 4: IterativeTester
      → Тестирует каждый MCP tool
      → Исправляет ошибки через LLM
      → Документирует edge cases
    """

    def convert_paper_to_agent(self, paper_pdf: str,
                                github_url: str) -> MCPServer:
        pipeline = Paper2AgentPipeline(
            llm="claude-sonnet-4-6",  # для всех субагентов
            timeout_per_agent=45 * 60   # 45 мин на субагента
        )

        # Шаг 1: Настроить окружение
        env = pipeline.setup_environment(
            repo_url=github_url,
            paper_pdf=paper_pdf
        )

        # Шаг 2: Запустить туториалы
        tutorials = pipeline.extract_and_run_tutorials(env)

        # Шаг 3: Извлечь функции → MCP tools
        mcp_tools = pipeline.extract_functions_as_tools(
            repo=env.repo,
            paper_pdf=paper_pdf,
            validated_examples=tutorials.examples
        )

        # Шаг 4: Протестировать tools
        tested_server = pipeline.test_and_fix_tools(
            tools=mcp_tools,
            max_iterations=5   # итеративное исправление ошибок
        )

        return tested_server
```

## SubAgent 3: Извлечение функций в MCP инструменты

```python
from anthropic import Anthropic
import inspect
import json

class FunctionExtractor:
    """
    Ключевой субагент: читает код + статью → создаёт MCP tools.
    """

    EXTRACTION_PROMPT = """
Проанализируй следующую функцию из научной статьи.

Код функции:
{function_code}

Контекст из статьи:
{paper_context}

Создай MCP tool definition:
{{
  "name": "snake_case_tool_name",
  "description": "Что делает функция (1 предложение для исследователя)",
  "inputSchema": {{
    "type": "object",
    "properties": {{
      "param_name": {{
        "type": "string|number|array",
        "description": "Что означает параметр"
      }}
    }},
    "required": ["обязательные параметры"]
  }},
  "example_usage": "mcp_client.call('tool_name', param=value)",
  "scientific_context": "Уравнение/метод из статьи, который реализует функция"
}}
"""

    def extract_tools_from_repo(self, repo_path: str,
                                 paper_pdf: str) -> list[dict]:
        # Найти ключевые функции через AST анализ
        functions = self._find_public_functions(repo_path)

        # Найти соответствующий контекст в статье
        paper_text = self._extract_paper_text(paper_pdf)

        tools = []
        for func in functions:
            # LLM создаёт MCP tool definition
            tool_def = self.llm.complete(
                self.EXTRACTION_PROMPT.format(
                    function_code=inspect.getsource(func),
                    paper_context=self._find_relevant_section(
                        paper_text, func.__name__
                    )
                )
            )
            tools.append(json.loads(tool_def))

        return tools
```

## Кейс: AlphaGenome → 22 геномных инструмента за 3 часа

```python
# Из статьи: конвертация AlphaGenome в Paper2Agent

ALPHAGENOME_CASE_STUDY = {
    "статья": "AlphaGenome: genomic foundation model",
    "репозиторий": "github.com/google-deepmind/alphagenome",
    "время_конвертации": "3 часа (автоматически, без ручной работы)",
    "результат": "22 MCP инструмента",

    "созданные_инструменты": [
        "predict_gene_expression(sequence: str, tissue: str) → float",
        "find_regulatory_elements(sequence: str) → list[dict]",
        "compute_variant_effect(ref: str, alt: str, position: int) → dict",
        "annotate_chromatin_accessibility(sequence: str) → np.ndarray",
        # ... ещё 18 инструментов
    ],

    "пример_использования": """
# До Paper2Agent (2-3 дня работы):
import alphagenome
model = alphagenome.load_model(...)
# читать документацию, разбираться с API, отлаживать...

# После Paper2Agent (сразу):
result = mcp_client.call(
    'predict_gene_expression',
    sequence="ATCGATCG...",
    tissue="liver"
)
# → {"expression_level": 7.3, "confidence": 0.89, "tissue": "liver"}
""",

    "качество_конвертации": {
        "tool_success_rate": "19/22 (86%)",
        "failed_tools": "3 инструмента с нестандартными GPU зависимостями"
    }
}
```

## Reproducibility как метрика качества публикации

```python
class ReproducibilityQualityMetric:
    """
    Ключевая идея статьи:
    Paper2Agent success rate = прокси метрика качества публикации.

    Если статья хорошо задокументирована:
      → Чёткие инструкции установки → SubAgent 1 успешен
      → Понятные туториалы → SubAgent 2 успешен
      → Документированные функции → SubAgent 3 успешен
      → Тесты проходят → SubAgent 4 успешен
      → success rate: 80-95%

    Если статья плохо задокументирована:
      → "pip install requirements.txt" → ошибки версий
      → Туториал не запускается
      → Функции без docstring → неверные MCP schemas
      → success rate: 20-40%
    """

    def compute_paper_quality_score(self, conversion_results: dict) -> float:
        weights = {
            "env_setup": 0.2,      # базовое окружение
            "tutorial_run": 0.3,   # воспроизводимость примеров
            "tool_extraction": 0.3, # документированность API
            "test_pass_rate": 0.2  # корректность реализации
        }

        score = sum(
            conversion_results[step]["success_rate"] * weight
            for step, weight in weights.items()
        )
        return score  # 0.0 - 1.0

# Применение: автоматический скоринг paper submissions
# "Этот preprint набрал 0.31 — рекомендуем улучшить документацию перед сабмишном"
```

## MCP интерфейс: стандартный доступ к инструментам

```python
# MCP server сгенерированный Paper2Agent

import mcp.server as mcp

class GeneratedMCPServer:
    """
    После конвертации: любой LLM клиент может использовать
    инструменты из научной статьи через стандартный MCP протокол.
    """

    @mcp.tool()
    def predict_gene_expression(self, sequence: str, tissue: str) -> dict:
        """
        Предсказать уровень экспрессии гена.
        Из AlphaGenome (DeepMind, 2024): модель предсказывает
        экспрессию по последовательности ДНК.

        Args:
            sequence: нуклеотидная последовательность (A/T/C/G)
            tissue: ткань (liver/heart/brain/kidney/...)
        Returns:
            {"expression_level": float, "confidence": float, "tissue": str}
        """
        # Реальный вызов AlphaGenome модели
        return self.alphagenome_model.predict(sequence, tissue=tissue)

# Использование через Claude:
# "Предскажи экспрессию этого гена в печени: ATCGATCG..."
# → Claude вызывает predict_gene_expression tool → реальный результат
```

## Применение к Lorenzo

```python
# Lorenzo собирает проекты с Хабра.
# Paper2Agent паттерн: превратить проекты Lorenzo в MCP инструменты

class LorenzoProjectToMCP:
    """
    Каждый проект Lorenzo (improve_*.py скрипт)
    → MCP tool через Paper2Agent паттерн.

    Вместо: "запусти python scripts/improve_llm_qa.py --question X"
    Станет: mcp_client.call("llm_qa", question="X")
    """

    def auto_wrap_scripts_as_tools(self):
        for script in self.list_scripts("scripts/improve_*.py"):
            tool_def = self.function_extractor.extract(
                code=script.source,
                context=f"Lorenzo скрипт: {script.description}"
            )
            self.mcp_server.register(tool_def)
```

## Возможные комбинации

| Комбинация | Новое свойство |
|------------|----------------|
| **Paper2Agent + MCP (R04)** | Paper2Agent генерирует MCP серверы → автоматическое расширение экосистемы |
| **Paper2Agent + LLAMATOR (R33)** | Red-team сгенерированных MCP инструментов: безопасны ли научные методы? |
| **Paper2Agent + Cursor Multi-Agent (R33)** | Researcher agent читает статью → developer agent реализует → Paper2Agent валидирует |
| **Paper2Agent + ai-review (R34)** | ai-review проверяет код сгенерированных MCP инструментов |
| **Paper2Agent + RAG tests (R27)** | Автогенерация тестов для каждого MCP tool через Agent Driven Development |

## Контакт

- Статья: https://habr.com/ru/articles/945582/ (сентябрь 2025)
- GitHub: https://github.com/jmiao24/Paper2Agent
- AlphaGenome (DeepMind): github.com/google-deepmind/alphagenome
- MCP Protocol: modelcontextprotocol.io
- Смежная (агрегатор научных статей, Python API): https://habr.com/ru/articles/846704/
- Смежная (LLM в науке, анализ экспериментов): https://habr.com/ru/companies/timeweb/articles/967672/

## Смотрите также
- [Главная](../../../README.md)
- [Метрики](../../../METRICS.md)
- [Здоровье](../../../HEALTH.md)
- [Глоссарий](../../../GLOSSARY.md)
- [Сущности](../../../ENTITIES.md)
- [Решения](../../../DECISIONS.md)
