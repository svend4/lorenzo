# LLM + MCP + OpenSearch: анализ логов безопасности через codegen

**Автор:** Ins4n3 (Kaspersky)  
**Хабр:** https://habr.com/ru/companies/kaspersky/articles/953780/  
**GitHub:** https://github.com/ins4n333/aidemo  
**Слой:** orchestration / analytics  
**Дата:** октябрь 2025  
**Уникальность:** 5-фазный pipeline для ad-hoc анализа логов безопасности через LLM без написания парсеров вручную. Ключевой паттерн: LLM анализирует структуру 1 примера лога → генерирует Python-скрипт → скрипт выгружает данные через Scroll API и обрабатывает вне контекстного окна. Обходит ограничение в 128K токенов при работе с миллионами строк логов. Стек: Roo Code + кастомный MCP-сервер для OpenSearch.

## Проблема: логи безопасности не помещаются в контекстное окно

```
Задача SOC-аналитика:
  "Найди все хосты с подозрительными DNS-запросами за последнюю неделю"

Наивный подход — засунуть логи в LLM:
  → Неделя логов = 50+ GB = миллионы строк
  → LLM контекст: 128K токенов ≈ ~100K слов ≈ ~500 строк логов
  → Проблема: 99.99% логов не влезет

Деградация контекста:
  → При заполнении >70-80% контекста LLM теряет точность
  → Анализировать 500 из миллиона строк = бесполезно

Codegen паттерн решает:
  → LLM видит 1 пример лога → понимает структуру
  → LLM генерирует Python скрипт для выгрузки через Scroll API
  → Скрипт работает ВНЕ LLM с полным объёмом данных
  → LLM анализирует только итоговую агрегацию (маленький вывод)
```

## 5-фазный Pipeline

```python
# Kaspersky: LLM + MCP + OpenSearch log analysis
# github.com/ins4n333/aidemo

import json
from pathlib import Path

class SecurityLogAnalyzer:
    """
    5 фаз анализа логов через LLM + MCP + OpenSearch.
    Роль "PythonDeveloper" в .roomodes для кодогенерации.
    """

    def analyze(self, analyst_task: str) -> dict:
        """
        analyst_task: "Найди все хосты с подозрительными DNS за неделю"
        """
        # Фаза 1: Schema Detection (1 лог пример)
        sample_log = self.mcp.get_sample_log(n=1)
        schema = self.llm.analyze_schema(sample_log, analyst_task)

        # Фаза 2: Bulk Download через Scroll API (вне LLM)
        scroll_script = self.llm.generate_scroll_script(schema, analyst_task)
        raw_data = self.execute_script(scroll_script)  # ВНЕ контекста LLM

        # Фаза 3: Codegen — Python скрипт обработки данных
        analysis_script = self.llm.generate_analysis_script(
            schema=schema,
            task=analyst_task,
            sample_output=raw_data[:100]  # только первые 100 строк
        )
        analysis_result = self.execute_script(analysis_script)  # ВНЕ LLM

        # Фаза 4: Local Execution — агрегация (маленький вывод → LLM)
        final_answer = self.llm.synthesize(
            task=analyst_task,
            analysis_result=analysis_result  # агрегат, не сырые логи
        )

        # Фаза 5: Orchestration — декомпозиция сложных задач
        return {
            "answer": final_answer,
            "script_used": analysis_script,
            "records_analyzed": raw_data.get("total_hits", 0)
        }
```

## MCP-сервер для OpenSearch

```python
# opensearch.py — кастомный MCP-сервер (github.com/ins4n333/aidemo)

import mcp.server as mcp
import json
from opensearchpy import OpenSearch, helpers

class OpenSearchMCPServer:
    """
    MCP интерфейс к OpenSearch/Kibana для LLM-агентов.
    LLM вызывает tools, не знает об OpenSearch под капотом.
    """

    def __init__(self, host: str, index_pattern: str):
        self.client = OpenSearch(hosts=[{"host": host, "port": 9200}])
        self.index = index_pattern

    @mcp.tool()
    def get_sample_log(self, n: int = 1) -> dict:
        """
        Получить N примеров логов для анализа схемы.
        LLM использует для понимания структуры данных.
        """
        result = self.client.search(
            index=self.index,
            body={"query": {"match_all": {}}, "size": n}
        )
        return result["hits"]["hits"]

    @mcp.tool()
    def get_index_mapping(self) -> dict:
        """
        Получить маппинг полей индекса OpenSearch.
        Нужен LLM чтобы генерировать корректные запросы.
        """
        return self.client.indices.get_mapping(index=self.index)

    @mcp.tool()
    def execute_query(self, query: dict,
                       time_range_hours: int = 168) -> dict:
        """
        Выполнить DSL-запрос к OpenSearch (для небольших результатов).
        Для больших данных LLM должна использовать scroll_query.
        """
        query["query"] = {
            "bool": {
                "must": [query.get("query", {"match_all": {}})],
                "filter": [{
                    "range": {
                        "@timestamp": {
                            "gte": f"now-{time_range_hours}h",
                            "lte": "now"
                        }
                    }
                }]
            }
        }
        return self.client.search(index=self.index, body=query, size=100)

    @mcp.tool()
    def count_matching(self, query: dict) -> int:
        """Посчитать количество событий без загрузки данных."""
        return self.client.count(index=self.index, body=query)["count"]
```

## Codegen паттерн: обход ограничения контекста

```python
class CodegenAnalysisPattern:
    """
    Ключевой паттерн: LLM генерирует код, код работает вне LLM.

    Почему это работает:
    - LLM хорошо пишет Python (навык из обучения)
    - Python Scroll API обрабатывает ГБ данных
    - LLM видит только агрегат (сотни строк, не миллионы)
    """

    SCROLL_SCRIPT_PROMPT = """
Ты — PythonDeveloper (роль из .roomodes).
Напиши МИНИМАЛЬНЫЙ Python скрипт для выгрузки логов из OpenSearch.

Схема лога:
{schema}

Задача аналитика:
{analyst_task}

Требования к скрипту:
1. Используй Scroll API для больших объёмов (>10K записей)
2. Фильтруй только нужные поля (не грузи всё)
3. Выводи в stdout как JSON (одна запись = одна строка)
4. Добавь прогресс-вывод в stderr
5. Обработай ошибки соединения

Скрипт должен читать JSON и выводить в stdout.
Только код, без объяснений."""

    ANALYSIS_SCRIPT_PROMPT = """
Ты — PythonDeveloper.
Напиши скрипт для анализа загруженных логов.

Задача: {analyst_task}
Пример данных (первые 5 строк):
{sample_data}

Скрипт:
- Читает JSON из stdin (одна запись в строке)
- Выполняет агрегацию/фильтрацию по задаче
- Выводит КРАТКУЮ сводку в stdout (не более 200 строк)
- Включает топ-N результатов и статистику

Только код, без объяснений."""

    def execute_script(self, script: str,
                        input_data: str = None) -> str:
        """
        Выполнить сгенерированный Python скрипт в sandbox.
        Изоляция: subprocess + timeout + ограничение памяти.
        """
        import subprocess
        result = subprocess.run(
            ["python", "-c", script],
            input=input_data,
            capture_output=True,
            text=True,
            timeout=60,  # timeout для длинных скриптов
            # В production: Docker sandbox для изоляции
        )
        if result.returncode != 0:
            raise RuntimeError(f"Script failed: {result.stderr}")
        return result.stdout


# Конфигурация .roomodes (Roo Code): роль PythonDeveloper
ROOMODE_CONFIG = {
    "customModes": [{
        "slug": "python-developer",
        "name": "PythonDeveloper",
        "roleDefinition": """Ты — Python разработчик для анализа данных.
Пишешь минимальные, понятные скрипты.
Читаешь данные из stdin/файла, выводишь в stdout.
Никогда не используй интерактивные компоненты.
При анализе логов: всегда используй агрегацию, не выводи сырые данные.""",
        "groups": ["read", "command"]
    }]
}
```

## Практические результаты и ограничения

```python
SYSTEM_PROFILE = {
    "организация": "Kaspersky (внутренняя разработка)",
    "github": "https://github.com/ins4n333/aidemo",
    "файлы": ["opensearch.py", "mcp.json", ".roomodes"],

    "стек": {
        "orchestrator": "Roo Code (AI-агент с поддержкой MCP)",
        "mcp_server": "Кастомный OpenSearch MCP (opensearch.py)",
        "llm": "Внутренняя модель Kaspersky (OpenAI-совместимый API)",
        "context_window": "128K токенов",
        "index": "OpenSearch / Kibana"
    },

    "паттерн_codegen": {
        "почему": "Логи не влезают в контекст",
        "как": "LLM пишет Python → Python обрабатывает данные вне LLM",
        "результат": "Обработка ГБ данных при 128K контексте"
    },

    "деградация_контекста": {
        "порог": ">70-80% заполнения",
        "следствие": "Снижение точности LLM",
        "решение": "Codegen + локальное выполнение"
    },

    "типичные_задачи": [
        "Найти хосты с аномальными DNS-запросами",
        "Выявить lateral movement паттерны",
        "Корреляция событий авторизации с сетевой активностью",
        "Статистика по типам угроз за период"
    ],

    "ограничения": [
        "Нет метрик точности/скорости (демонстрационная статья)",
        "Sandbox для codegen execution нужен отдельно",
        "Не заменяет SIEM-корреляцию, дополняет ad-hoc анализ"
    ]
}
```

## Применение к Lorenzo

```python
# Lorenzo: codegen паттерн для анализа больших корпусов документов

class LorenzoCodegenAnalysis:
    """
    Kaspersky паттерн для Lorenzo:
    При вопросах о больших корпусах (все 160 проектов)
    LLM генерирует Python скрипт анализа вместо загрузки в контекст.
    """

    async def analyze_corpus(self, question: str) -> dict:
        # Шаг 1: LLM видит структуру 1 документа
        sample = self.read_sample_doc()
        schema = await self.llm.analyze_schema(sample)

        # Шаг 2: LLM генерирует анализирующий скрипт
        script = await self.llm.generate(f"""
Напиши Python скрипт для анализа docs/ директории.
Задача: {question}
Схема документа: {schema}
Выводи результат как JSON в stdout.
""")
        # Шаг 3: Запустить скрипт вне LLM
        result = self.executor.run(script, cwd="/home/user/lorenzo/docs")

        # Шаг 4: LLM синтезирует финальный ответ из агрегата
        return await self.llm.synthesize(question, result)
```

## Возможные комбинации

| Комбинация | Новое свойство |
|------------|----------------|
| **Kaspersky MCP + AISecurity (R37)** | AISecurity фильтрует запросы → Kaspersky MCP анализирует логи атак |
| **Kaspersky MCP + IoT-MCP (R37)** | IoT метрики + SIEM логи → единый MCP interface для SOC |
| **Kaspersky MCP + Meta-Monitor (R29)** | Meta-Monitor видит аномалии → LLM codegen для глубокого анализа |
| **Kaspersky MCP + LangFuse (R38)** | Трейсинг codegen pipeline: время генерации vs выполнения скрипта |
| **Kaspersky MCP + Lorenzo Gateway** | /api/ask → codegen анализ docs/ без загрузки всех файлов в контекст |

## Контакт

- Статья: https://habr.com/ru/companies/kaspersky/articles/953780/ (октябрь 2025)
- GitHub: https://github.com/ins4n333/aidemo (Python, 3 файла)
- Roo Code: roocode.com
- OpenSearch: opensearch.org
- Смежная (Agentic SOC архитектура): https://habr.com/ru/articles/1015052/
- Смежная (MaxPatrol SIEM ML, Positive Technologies): https://habr.com/ru/companies/pt/articles/852784/
