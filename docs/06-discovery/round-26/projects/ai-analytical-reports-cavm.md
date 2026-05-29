---
date: 2026-05-29
tags: [memory, rag, orchestration, ingestion, architecture]
state: normalized
---

# AI-агенты пишут аналитические отчёты: CAVM framework

<!-- toc-auto -->
<!-- tags: ai-analytical-reports-cavm, docs -->


<!-- summary -->
> Проблема: аналитический отчёт = многошаговый процесс CAVM: Code Agent with Variable Memory
 
CAVM: Code Agent with Variable Memory
 
Архитектура мультиагентной аналитики
 
Верификация через специализированные агенты
 
Применение в финансовой аналитике
 
Применение к Lorenzo
Lorenzo имеет


> [!NOTE]
> Документ создан на основе исследования. Ссылки ведут на связанные материалы.

<!-- alert-added -->

**Автор:** независимый разработчик (Хабр, октябрь 2025)  
**Хабр:** https://habr.com/ru/articles/960338/  
**GitHub:** не опубликован (паттерн и архитектура описаны в статье)  
**Слой:** orchestration / analytics / knowledge  
**Дата:** октябрь 2025  
**Уникальность:** Code Agent with Variable Memory (CAVM) — фреймворк для написания аналитических отчётов командой агентов: каждый шаг = рассуждение + генерация кода + исполнение + обновление переменных. Общее пространство переменных устраняет разрывы между поиском, анализом и финальным текстом. Специализированные vision-агенты проверяют качество графиков и таблиц.

## Проблема: аналитический отчёт = многошаговый процесс

```
Традиционный аналитик:
  1. Сбор данных (Excel, SQL, API) — 2-3 часа
  2. Очистка и агрегация — 1-2 часа
  3. Анализ + выводы — 3-4 часа
  4. Написание текста — 2-3 часа
  5. Визуализация (графики, таблицы) — 1-2 часа
  Итого: 8-14 часов на один отчёт

Почему один LLM не справляется:
  → Контекст заполняется промежуточными данными
  → Нет персистентности между шагами (пересчитывает всё заново)
  → Смешивает данные из разных источников (галлюцинации)
  → Не верифицирует вычисления
```

## CAVM: Code Agent with Variable Memory

```python
# Ключевая идея: всё через исполняемый код + общий стейт

class CAVMAgent:
    def __init__(self):
        # Общее пространство переменных — персистентно между шагами
        self.variables = {}

        # История действий — для reasoning следующего агента
        self.history = []

    def step(self, task: str) -> None:
        # Агент рассуждает → генерирует код → исполняет → сохраняет
        code = self.llm.generate_code(
            task=task,
            current_variables=self.variables,
            history=self.history
        )

        # Исполнение кода (Python sandbox)
        result = self.executor.run(code)

        # Обновить переменные (результат доступен следующим агентам)
        self.variables.update(result.new_variables)
        self.history.append({
            "task": task, "code": code, "result": result.summary
        })
```

## Архитектура мультиагентной аналитики

```
Pipeline для аналитического отчёта:

Агент 1: Data Collector
  task: "Загрузи квартальные данные из Q3_sales.xlsx"
  code: pd.read_excel("Q3_sales.xlsx") → df_sales
  → variables["df_sales"] = DataFrame(...)

Агент 2: Data Cleaner
  task: "Очисти df_sales: убери дубли, заполни пропуски"
  code: df_clean = df_sales.dropna().drop_duplicates()...
  → variables["df_clean"] = ...

Агент 3: Analyzer
  task: "Найди топ-10 продуктов, тренды, аномалии"
  code: top10 = df_clean.groupby("product")...
        anomalies = detect_outliers(df_clean)...
  → variables["top10"] = ..., variables["anomalies"] = ...

Агент 4: Visualizer
  task: "Построй 3 ключевых графика"
  code: plt.bar(top10), plt.line(trends), plt.scatter(anomalies)
  → variables["charts"] = [fig1, fig2, fig3]

Агент 5: Visual Checker (VLM)
  task: "Проверь что графики читаемы, оси подписаны, нет артефактов"
  → approves/requests fixes for each chart

Агент 6: Writer
  task: "Напиши executive summary на основе анализа"
  context: variables["top10"] + variables["anomalies"] + charts
  → final_report.md
```

## Верификация через специализированные агенты

```python
# Критически важно: отдельный агент проверяет расчёты

class VerificationAgent:
    """Независимая проверка ключевых цифр в отчёте"""

    def verify_numbers(self, report: str, variables: dict) -> list[Issue]:
        # Извлечь все числа из отчёта
        numbers_in_report = extract_numbers(report)

        # Проверить каждое число через код
        issues = []
        for num in numbers_in_report:
            verification_code = f"""
            # Проверить: {num.context}
            actual = {num.recompute_expression}
            assert abs(actual - {num.value}) < 0.01, f"Mismatch: {{actual}} != {num.value}"
            """
            result = self.executor.run(verification_code)
            if not result.success:
                issues.append(Issue(num, result.error))
        return issues
    # Предотвращает "галлюцинацию цифр" в финансовых отчётах
```

## Применение в финансовой аналитике

```python
# Пример: еженедельный отчёт по продажам

weekly_report_pipeline = [
    DataCollectorAgent(sources=["CRM", "ERP", "GA4"]),
    DataCleanerAgent(rules=["deduplicate", "fill_nulls", "normalize_dates"]),
    AnalyzerAgent(metrics=["revenue", "conversion", "churn", "LTV"]),
    AnomalyDetectorAgent(method="isolation_forest"),
    VisualizerAgent(charts=["revenue_trend", "funnel", "geo_heatmap"]),
    VisualCheckerAgent(model="claude-sonnet-4-6"),  # VLM проверяет
    WriterAgent(style="executive_summary", length=500),
    VerificationAgent(),   # двойная проверка цифр
]

report = CAVMPipeline(weekly_report_pipeline).run(
    date_range="last_7_days",
    output_format="pdf"
)
# Результат: PDF-отчёт за 12-18 минут вместо 8-14 часов
```

## Применение к Lorenzo

Lorenzo имеет `improve_metrics.py`, `improve_kpi.py`, `improve_report.py`.  
CAVM паттерн = **Multi-Agent Report Pipeline**:

```python
# improve_cavm_report.py (паттерн):
# Вместо одного скрипта "сгенерируй отчёт" — пайплайн агентов

class LorenzoReportPipeline:
    def run(self) -> str:
        state = {}

        # Агент 1: собрать данные
        state["metrics"] = MetricCollector.run(state)
        # → из METRICS.md, KPI.md, audit.db

        # Агент 2: анализ трендов
        state["trends"] = TrendAnalyzer.run(state)
        # → сравнить с прошлой неделей

        # Агент 3: выявить аномалии
        state["issues"] = AnomalyDetector.run(state)
        # → что ухудшилось, что требует внимания

        # Агент 4: написать отчёт
        return ReportWriter.run(state)
        # → структурированный DIGEST.md с цифрами и рекомендациями
```

## Возможные комбинации

| Комбинация | Новое свойство |
|------------|----------------|
| **CAVM + AIOps (R24)** | CAVM пишет incident report: данные мониторинга → анализ → рекомендации |
| **CAVM + LLM Router (R20)** | Haiku для data collection, Sonnet для analysis, Opus для final narrative |
| **CAVM + Langfuse (R13)** | Трейсинг каждого агента-шага: какой код сгенерирован, сколько времени |
| **CAVM + Graph RAG (R22)** | Агент-аналитик дополняет данные через Neo4j knowledge graph |
| **CAVM + Durable State (R23)** | SessionContext: прерванный отчёт восстанавливается с последнего checkpoint |

## Контакт

- Статья: https://habr.com/ru/articles/960338/ (октябрь 2025)
- Смежная (AI-агенты в аналитике, 2 production проекта): https://habr.com/ru/articles/970790/
- Смежная (как аналитики используют ИИ, Яндекс Практикум): https://habr.com/ru/companies/yandex_praktikum/articles/1004550/
- Code Interpreter / Jupyter-style execution: jupyter.org

## Смотрите также
- [Главная](../../../README.md)
- [Метрики](../../../METRICS.md)
- [Здоровье](../../../HEALTH.md)
- [Глоссарий](../../../GLOSSARY.md)
- [Сущности](../../../ENTITIES.md)
