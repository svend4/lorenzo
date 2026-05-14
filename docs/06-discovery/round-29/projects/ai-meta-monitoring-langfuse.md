# Как научить AI анализировать AI: meta-monitoring агентов с Langfuse

**Автор:** rkazmin (Хабр, январь 2026)  
**Хабр:** https://habr.com/ru/articles/987230/  
**GitHub:** не опубликован (личный проект, архитектура в статье)  
**Слой:** orchestration / analytics  
**Дата:** январь 2026  
**Уникальность:** Трёхкомпонентная система: Go backend с встроенным LLM автоматически анализирует телеметрию других AI-агентов. Определяет 5 классов аномалий: bottleneck производительности, cost spike, логический цикл, ошибки, нормальная работа. Cursor Hooks захватывают IDE-level трейсы → Langfuse → LLM-классификатор. Реальный "AI наблюдает за AI".

## Проблема: кто следит за агентами?

```
Классический мониторинг (инфраструктура):
  CPU → alert  |  Memory → alert  |  Error rate → alert
  → Хорошо для сервисов, плохо для AI агентов

Проблемы AI-агентов:
  ❌ Агент "работает" (нет exception), но делает не то
  ❌ Агент застрял в цикле (повторяет одно действие)
  ❌ Агент принимает дорогие решения (Opus вместо Haiku)
  ❌ Reasoning деградирует при длинном контексте
  ❌ Инструменты вызываются не в том порядке

Нужен: семантический мониторинг
  → Понять ЧТО делает агент, не только КАК
  → Классифицировать поведение как нормальное/аномальное
  → Обнаруживать паттерны за сессию, не только в один момент
```

## Архитектура: три компонента

```
┌─────────────────────────────────────────────────────────┐
│  КОМПОНЕНТ 1: Сбор трейсов                              │
│                                                          │
│  IDE агент (Cursor)                                      │
│    ↓ Cursor Hooks (каждый tool call, completion)         │
│  Chrome Extension                                        │
│    ↓ UI событий → POST /traces                          │
│  Go Backend                                              │
│    ↓ принять, нормализовать, записать                    │
│  Langfuse                                                │
│    ↓ spans, traces, scores хранятся                     │
└─────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────┐
│  КОМПОНЕНТ 2: LLM-классификатор аномалий                │
│                                                          │
│  Langfuse → batch трейсов → Go Backend                   │
│    ↓ встроенный LLM анализирует                          │
│  5 классов аномалий:                                     │
│    1. performance_bottleneck                             │
│    2. cost_spike                                         │
│    3. logical_loop                                       │
│    4. error_pattern                                      │
│    5. healthy_operation                                  │
│    ↓ классифицирует + объясняет                          │
│  Alert → Slack/Email/PagerDuty                           │
└─────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────┐
│  КОМПОНЕНТ 3: Dashboard                                  │
│                                                          │
│  Агрегация по агентам, задачам, времени                  │
│  Cost per agent / Cost per task type                     │
│  Anomaly timeline                                        │
│  Drill-down до отдельного span                           │
└─────────────────────────────────────────────────────────┘
```

## Go backend: нормализация и отправка в Langfuse

```go
// Принимаем трейсы от разных агентов

type AgentTrace struct {
    AgentID    string      `json:"agent_id"`
    SessionID  string      `json:"session_id"`
    Timestamp  time.Time   `json:"timestamp"`
    EventType  string      `json:"event_type"` // "tool_call"|"completion"|"error"
    Duration   int64       `json:"duration_ms"`
    InputTokens  int       `json:"input_tokens"`
    OutputTokens int       `json:"output_tokens"`
    Model      string      `json:"model"`
    ToolName   string      `json:"tool_name,omitempty"`
    Success    bool        `json:"success"`
    Metadata   map[string]interface{} `json:"metadata"`
}

func (s *Server) HandleTrace(w http.ResponseWriter, r *http.Request) {
    var trace AgentTrace
    json.NewDecoder(r.Body).Decode(&trace)

    // Нормализовать и отправить в Langfuse
    langfuseSpan := langfuse.Span{
        TraceID:   trace.SessionID,
        Name:      trace.EventType,
        StartTime: trace.Timestamp,
        EndTime:   trace.Timestamp.Add(time.Duration(trace.Duration) * time.Millisecond),
        Input:     map[string]interface{}{"tokens": trace.InputTokens},
        Output:    map[string]interface{}{"tokens": trace.OutputTokens},
        Metadata: map[string]interface{}{
            "model":     trace.Model,
            "tool":      trace.ToolName,
            "cost_usd":  calculateCost(trace),
            "success":   trace.Success,
        },
    }
    s.langfuse.CreateSpan(langfuseSpan)

    // Добавить в очередь для LLM-анализа
    s.analysisQueue.Push(trace)
}
```

## LLM-классификатор: 5 классов аномалий

```python
ANOMALY_CLASSIFICATION_PROMPT = """
Ты — система мониторинга AI-агентов.
Проанализируй телеметрию сессии и классифицируй поведение.

Телеметрия сессии (последние 20 событий):
{traces_json}

Метрики:
  - Общее время: {total_duration_ms}ms
  - Токены потрачено: {total_tokens}
  - Стоимость: ${total_cost_usd}
  - Количество tool_calls: {tool_call_count}
  - Количество ошибок: {error_count}

Классифицируй как ОДИН из:
1. PERFORMANCE_BOTTLENECK — один инструмент занимает >50% времени
2. COST_SPIKE — стоимость >3× среднего за похожие задачи
3. LOGICAL_LOOP — одно и то же действие повторяется >3 раз
4. ERROR_PATTERN — ошибки с нарастающей частотой
5. HEALTHY_OPERATION — всё в норме

Формат ответа:
{{
  "class": "LOGICAL_LOOP",
  "confidence": 0.89,
  "evidence": ["tool 'read_file' вызван 7 раз", "одинаковый path каждый раз"],
  "recommendation": "Агент застрял в петле. Проверить условие выхода."
}}
"""

class MetaMonitoringAgent:
    """LLM анализирует поведение других LLM-агентов"""

    def analyze_session(self, session_id: str) -> AnomalyReport:
        # Получить все трейсы сессии из Langfuse
        traces = self.langfuse.get_traces(session_id=session_id)

        # Агрегировать метрики
        metrics = self.aggregate_metrics(traces)

        # LLM-классификация
        response = self.classifier_llm.generate(
            ANOMALY_CLASSIFICATION_PROMPT.format(
                traces_json=json.dumps(traces[-20:], indent=2),
                total_duration_ms=metrics.duration,
                total_tokens=metrics.tokens,
                total_cost_usd=metrics.cost,
                tool_call_count=metrics.tool_calls,
                error_count=metrics.errors
            )
        )

        result = parse_json(response)

        # Алерт если аномалия
        if result["class"] != "HEALTHY_OPERATION":
            self.alert_manager.send(
                severity="warning" if result["confidence"] > 0.7 else "info",
                agent_id=traces[0].agent_id,
                anomaly=result["class"],
                evidence=result["evidence"]
            )

        return AnomalyReport(**result)
```

## Cursor Hooks: захват IDE-level событий

```python
# .cursor/hooks.py (запускается при каждом tool call)

def on_tool_call(tool_name: str, args: dict, result: dict,
                 duration_ms: int) -> None:
    """Cursor вызывает этот хук после каждого tool call агента"""
    import requests

    requests.post("http://localhost:8080/traces", json={
        "agent_id": os.environ.get("CURSOR_AGENT_ID"),
        "session_id": os.environ.get("CURSOR_SESSION_ID"),
        "timestamp": datetime.utcnow().isoformat(),
        "event_type": "tool_call",
        "tool_name": tool_name,
        "duration_ms": duration_ms,
        "success": result.get("success", True),
        "metadata": {
            "args_summary": str(args)[:200],  # не логируем секреты
            "result_size": len(str(result))
        }
    })

# Chrome Extension: аналогично для browser-based агентов
# → фиксирует DOM манипуляции, навигацию, формы
```

## Паттерны обнаруженных аномалий

```python
# Реальные паттерны из production (анонимизировано)

DISCOVERED_ANOMALY_PATTERNS = {
    "read_file_loop": {
        "симптом": "read_file вызывается >5 раз с одним путём",
        "причина": "агент не кешировал результат → читает каждый шаг",
        "решение": "добавить memory layer (R01 паттерн)"
    },
    "model_escalation": {
        "симптом": "задача начата Haiku → переключилась на Opus без явной причины",
        "причина": "ошибки в дешёвой модели → роутер выбирает дорогую",
        "решение": "LLM Router (R20) с явными правилами эскалации"
    },
    "context_overflow": {
        "симптом": "latency растёт нелинейно → деградация качества",
        "причина": "context window заполнен → модель теряет начало",
        "решение": "summarization при достижении 70% context"
    },
    "tool_misorder": {
        "симптом": "write_file вызван до read_file для того же файла",
        "причина": "агент перезаписывает файл не прочитав",
        "решение": "pre-condition checks в tool definitions"
    }
}
```

## Применение к Lorenzo

Lorenzo `improve_watcher.py` + meta-monitoring паттерн:

```python
# improve_meta_monitor.py (паттерн):

class LorenzoMetaMonitor:
    """
    Lorenzo запускает скрипты → meta-monitor анализирует их поведение
    Аналог: скрипты = "агенты", meta-monitor = LLM-классификатор
    """

    def analyze_run(self, run_log: RunLog) -> AnomalyReport:
        # Собрать метрики запуска
        traces = [
            {"script": step.script,
             "duration_ms": step.duration,
             "exit_code": step.exit_code,
             "output_lines": step.output_count}
            for step in run_log.steps
        ]

        # LLM анализирует паттерн запуска
        analysis = self.llm.analyze(
            traces=traces,
            question="Есть ли аномалии в этом запуске? Какие скрипты работают дольше нормы?"
        )

        # Алерт если нашёл что-то необычное
        if analysis.has_anomalies:
            self.notify(analysis.anomalies)
        return analysis

    def detect_regressions(self, current: RunLog,
                            baseline: RunLog) -> list[Regression]:
        """Сравнить с предыдущим запуском — benchmark.json паттерн"""
        return compare_runs(current, baseline)
```

## Возможные комбинации

| Комбинация | Новое свойство |
|------------|----------------|
| **Meta-Monitor + Langfuse (R13)** | Langfuse = backend для трейсов; Meta-Monitor добавляет LLM-семантику |
| **Meta-Monitor + AIOps (R24)** | AIOps предсказывает инциденты → Meta-Monitor ловит аномалии агентов = полный стек |
| **Meta-Monitor + Orchestrator (R27)** | Оркестратор видит аномалии воркеров через Meta-Monitor → перепланирует |
| **Meta-Monitor + Durable State (R23)** | Состояние агента в Redis → Meta-Monitor видит историю между сессиями |
| **Meta-Monitor + LLM Judge (R28)** | Meta-Monitor ловит поведенческие аномалии; LLM Judge оценивает качество output |

## Контакт

- Статья: https://habr.com/ru/articles/987230/ (январь 2026)
- Langfuse: langfuse.com, github.com/langfuse/langfuse (MIT)
- Смежная (LLM Observability большой гайд): https://habr.com/ru/articles/972480/
- Смежная (Cloud.ru агентные сбои): https://habr.com/ru/companies/cloud_ru/articles/1008714/
- OpenTelemetry для LLM: opentelemetry.io/docs/specs/semconv/gen-ai/
