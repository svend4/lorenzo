---
date: 2026-05-15
tags: [rag, orchestration, knowledge, ingestion, local-first]
state: normalized
---

# Инженерия оценки агентов: Golden Set с CoT-трассами и RAGAS + Knowledge Graph на русском

<!-- toc-auto -->
<!-- tags: kobets87-agent-evaluation-golden-set-ragas, docs -->


<!-- summary -->
> `kobets87-agent-evaluation-golden-set-ragas` — раздел документации проекта Lorenzo.


> [!WARNING]
> Документ содержит описание рисков и ограничений. Изучите их перед принятием архитектурных решений.

<!-- alert-added -->

**Автор:** kobets87  
**Хабр:** https://habr.com/ru/articles/1034050/  
**GitHub:** нет (код в статье, LM_Studio для локального запуска)  
**Слой:** orchestration / analytics  
**Дата:** май 2025  
**Уникальность:** Практическое руководство по построению системы оценки агентов с нуля: Golden Set с эталонными цепочками CoT + примеры function calling, RAGAS + Knowledge Graph для генерации single-hop и multi-hop вопросов на русском языке, Python + локальная LLM (LM_Studio). Закрывает угол, не покрытый R41(SWE-MERA)/R44(Yandex 3-stage)/R47(CLEV): не готовый бенчмарк, а инженерная инфраструктура построения Golden Set с reasoning traces.

## Проблема: агент "вроде работает" — но как это измерить?

```
Типичная ситуация разработчика агента:
  → Запускаешь агент на 10 запросов → 8 правильных → "неплохо"
  → Через неделю делаешь правку промпта → 7 правильных → регрессия?
  → Или случайность? Выборка из 10 не показательна.
  → Агент недетерминирован: один запрос → разные ответы

Три пласта проблемы:
  1. Финальный ответ правильный, но путь к нему неверный
     ("угадал" через другую цепочку рассуждений → нестабильно)
  2. Tool calls: правильный инструмент, неправильные параметры
     → не поймать по final answer
  3. Multi-hop рассуждения: ошибка на шаге 2 → финал может быть верным
     (компенсаторные рассуждения) → ложное ощущение качества

Решение: Golden Set с CoT-трассами + автогенерация тестов через RAGAS
```

## Golden Set: эталонные цепочки рассуждений

```python
# kobets87: инженерия оценки LLM-агентов
# habr.com/ru/articles/1034050/

from dataclasses import dataclass, field
from typing import Optional
import json

@dataclass
class ToolCall:
    """Эталонный вызов инструмента в Golden Set."""
    tool_name: str
    parameters: dict
    expected_result_type: str  # "text" | "list" | "dict" | "number"


@dataclass
class ReasoningStep:
    """Один шаг в эталонной цепочке рассуждений (CoT)."""
    step_id: int
    thought: str           # что агент должен подумать
    action: Optional[ToolCall]  # если шаг требует вызова инструмента
    observation: Optional[str]  # что наблюдает после tool call
    is_critical: bool      # критический шаг — ошибка здесь = провал теста


@dataclass
class GoldenSetExample:
    """
    Эталонный пример для Golden Set.

    Содержит не только вопрос/ответ, но и:
    - Эталонную цепочку CoT (шаги рассуждений)
    - Ожидаемые вызовы инструментов с параметрами
    - Критические шаги (обязательные для правильного ответа)

    Это позволяет оценивать ПРОЦЕСС, а не только финальный ответ.
    """
    example_id: str
    question: str
    expected_answer: str
    reasoning_chain: list[ReasoningStep]
    expected_tool_calls: list[ToolCall]
    question_type: str     # "single_hop" | "multi_hop" | "conditional"
    difficulty: str        # "easy" | "medium" | "hard"
    domain: str            # тематическая область


# Пример Golden Set для агента с поиском
GOLDEN_EXAMPLE = GoldenSetExample(
    example_id="gs_001",
    question="Какой был штраф за нарушение ПДД в России в 2022 году?",
    expected_answer="Штраф за превышение скорости на 20-40 км/ч составлял 500 рублей",
    reasoning_chain=[
        ReasoningStep(
            step_id=1,
            thought="Нужно найти информацию о штрафах ПДД на 2022 год",
            action=ToolCall(
                tool_name="search_documents",
                parameters={"query": "штраф ПДД 2022", "date_filter": "2022-01-01"},
                expected_result_type="list"
            ),
            observation="Найдено 3 документа о ПДД",
            is_critical=True  # если не вызвал search → ошибка
        ),
        ReasoningStep(
            step_id=2,
            thought="Из найденных документов нужно извлечь конкретный штраф",
            action=None,  # рассуждение без tool call
            observation=None,
            is_critical=True
        )
    ],
    expected_tool_calls=[
        ToolCall("search_documents",
                  {"query": "штраф ПДД", "date_filter": "2022-01-01"},
                  "list")
    ],
    question_type="single_hop",
    difficulty="easy",
    domain="legal"
)
```

## RAGAS + Knowledge Graph: автогенерация тестовых вопросов

```python
class RAGASKnowledgeGraphGenerator:
    """
    Генерация тестовых вопросов через RAGAS + Knowledge Graph.

    RAGAS TestSet Generator:
    - Берёт корпус документов
    - Строит Knowledge Graph (концепты + связи)
    - Генерирует вопросы по паттернам: simple, reasoning, multi_hop

    Ключевое для русского языка:
    - По умолчанию RAGAS оптимизирован для EN
    - Нужна адаптация: русскоязычная LLM для генерации вопросов
    - LM_Studio позволяет запустить локально (без облака)
    """

    def __init__(self, local_llm_url: str = "http://localhost:1234"):
        """
        local_llm_url: LM_Studio API endpoint (OpenAI-compatible)
        Используемая модель: Qwen2.5-7B или Mistral-7B-Instruct на русском
        """
        self.llm_url = local_llm_url

    def generate_test_set(self,
                           documents: list[str],
                           n_questions: int = 50,
                           language: str = "ru") -> list[GoldenSetExample]:
        """
        Автоматически сгенерировать тестовые вопросы из корпуса документов.

        Распределение по типам (рекомендуется):
        - single_hop: 40% (проверяет базовое извлечение фактов)
        - multi_hop: 40% (проверяет reasoning через несколько документов)
        - conditional: 20% (проверяет понимание условий "если...то...")
        """
        # Шаг 1: построить Knowledge Graph из документов
        kg = self._build_knowledge_graph(documents)

        # Шаг 2: RAGAS TestSet Generator с локальной LLM
        from ragas.testset.generator import TestsetGenerator
        from ragas.testset.evolutions import simple, reasoning, multi_context

        # Адаптация для русского языка
        generator = TestsetGenerator.from_langchain(
            generator_llm=self._get_local_llm(),
            critic_llm=self._get_local_llm(),
            embeddings=self._get_local_embeddings()
        )

        testset = generator.generate_with_langchain_docs(
            documents=self._to_langchain_docs(documents),
            test_size=n_questions,
            distributions={
                simple: 0.4,
                reasoning: 0.4,
                multi_context: 0.2
            }
        )

        return self._convert_to_golden_set(testset, kg)

    def _build_knowledge_graph(self, documents: list[str]) -> dict:
        """
        Построить Knowledge Graph из корпуса.
        Узлы: концепты (законы, нормы, организации)
        Рёбра: отношения (РЕГУЛИРУЕТ, СОДЕРЖИТ, ИЗМЕНЯЕТ)

        Используется для multi-hop генерации:
        "Закон А → регулирует → Норму Б → применяется к → Случаю В"
        → вопрос: "Как Закон А применяется к Случаю В?"
        """
        # NER + relation extraction из корпуса
        entities = self._extract_entities(documents)
        relations = self._extract_relations(documents, entities)

        return {
            "nodes": entities,
            "edges": relations,
            "multi_hop_paths": self._find_multi_hop_paths(entities, relations)
        }

    def _get_local_llm(self):
        """OpenAI-compatible LM_Studio LLM для RAGAS."""
        from langchain_openai import ChatOpenAI
        return ChatOpenAI(
            base_url=f"{self.llm_url}/v1",
            api_key="lm-studio",
            model="local-model"
        )
```

## Метрики оценки агентских трасс

```python
class AgentTraceEvaluator:
    """
    Оценка агентских трасс по трём измерениям (kucev R48-подход):

    1. Tool-Use Eval: правильный инструмент + правильные параметры
    2. Workflow Eval: полный агентный пайплайн
    3. Reasoning Chain Eval: когерентность цепочки рассуждений

    Но kobets87 добавляет четвёртое: Process Eval через Golden Set —
    сравнение реальной трассы с эталонной шаг за шагом.
    """

    def evaluate_against_golden(self,
                                  actual_trace: list[dict],
                                  golden: GoldenSetExample) -> dict:
        """
        Сравнить реальную трассу агента с эталонной Golden Set.

        Три компонента оценки:
        1. Critical steps coverage: прошёл ли агент все is_critical=True шаги?
        2. Tool call accuracy: правильные инструменты + параметры?
        3. Final answer correctness: правильный финальный ответ?
        """
        # 1. Critical steps: обязательные шаги должны быть выполнены
        critical_steps = [s for s in golden.reasoning_chain if s.is_critical]
        covered_critical = sum(
            1 for step in critical_steps
            if self._step_covered(step, actual_trace)
        )
        critical_coverage = covered_critical / len(critical_steps)

        # 2. Tool calls: инструмент + параметры
        tool_scores = []
        for expected_call in golden.expected_tool_calls:
            actual_call = self._find_matching_call(expected_call, actual_trace)
            if actual_call:
                param_score = self._score_parameters(
                    expected_call.parameters,
                    actual_call.get("parameters", {})
                )
                tool_scores.append(param_score)
            else:
                tool_scores.append(0.0)  # инструмент не вызван

        tool_accuracy = sum(tool_scores) / len(tool_scores) if tool_scores else 0

        # 3. Final answer
        answer_correct = self._check_answer(
            actual_trace[-1].get("output", ""),
            golden.expected_answer
        )

        return {
            "critical_coverage": critical_coverage,
            "tool_accuracy": tool_accuracy,
            "answer_correct": answer_correct,
            "overall_score": (
                0.4 * critical_coverage +
                0.3 * tool_accuracy +
                0.3 * float(answer_correct)
            ),
            "passed": critical_coverage >= 1.0 and answer_correct
        }

    def pass_at_k(self, agent_fn, question: str, k: int = 5) -> float:
        """
        pass@k: запустить агент K раз, считать долю правильных.
        Учитывает недетерминизм LLM.

        pass@1 = 0.6 означает: агент правильно отвечает в 60% запусков.
        Для production нужен pass@3 > 0.8.
        """
        correct = sum(
            1 for _ in range(k)
            if self._run_and_check(agent_fn, question)
        )
        return correct / k
```

## Circuit Breaker для бесконечных рассуждений

```python
class ReasoningCircuitBreaker:
    """
    Агенты иногда зацикливаются в CoT — думают бесконечно, не достигая ответа.
    Circuit Breaker: принудительная остановка через N шагов.

    Признаки зацикливания:
    - Одинаковые tool calls с теми же параметрами (повтор)
    - Растущая энтропия рассуждений (нет сходимости)
    - Отсутствие финального ответа за max_steps шагов
    """

    def __init__(self, max_steps: int = 15, max_tool_repeats: int = 3):
        self.max_steps = max_steps
        self.max_tool_repeats = max_tool_repeats

    def check(self, trace: list[dict]) -> tuple[bool, str]:
        """
        Проверить нужно ли остановить агент.
        Возвращает (should_stop, reason).
        """
        if len(trace) >= self.max_steps:
            return True, "max_steps_exceeded"

        # Проверить повторяющиеся tool calls
        tool_calls = [t for t in trace if t.get("type") == "tool_call"]
        if self._has_repeated_calls(tool_calls, self.max_tool_repeats):
            return True, "tool_call_loop_detected"

        return False, "ok"

    def _has_repeated_calls(self, calls: list[dict], threshold: int) -> bool:
        """Обнаружить повтор одинаковых вызовов инструментов."""
        from collections import Counter
        call_signatures = [
            f"{c['tool']}:{json.dumps(c.get('params', {}), sort_keys=True)}"
            for c in calls
        ]
        return any(count >= threshold for count in Counter(call_signatures).values())


BENCHMARK_SETUP = {
    "локальная_инфраструктура": {
        "llm": "LM_Studio (OpenAI-compatible API, localhost:1234)",
        "модели_для_теста": ["Qwen2.5-7B", "Mistral-7B-Instruct"],
        "стоимость": "$0 (полностью локально)",
        "требования": "16GB RAM + 8GB VRAM (или CPU-only медленнее)"
    },
    "ragas_версия": "0.1.x (TestsetGenerator API)",
    "генерация_тестов": {
        "single_hop": "40% — прямые вопросы из одного документа",
        "multi_hop": "40% — вопросы через 2-3 документа и KG",
        "conditional": "20% — условные вопросы ('если X, то Y?')"
    },
    "golden_set_размер": {
        "минимум": 50,
        "рекомендуется": 200,
        "для_production": 500
    }
}
```

## Применение к Lorenzo

```python
# Lorenzo: Golden Set для оценки MCP-инструментов

class LorenzoAgentEvaluation:
    """
    kobets87 паттерн для Lorenzo:
    Golden Set для оценки поведения агентов с Lorenzo MCP-инструментами.

    Вопрос: "Какой проект использует BM25 для поиска?"
    Эталон: search_docs(query="BM25") → find_similar(project_id=X) → ответ
    Критический шаг: search_docs ДОЛЖЕН быть вызван

    RAGAS + Lorenzo docs/ → автогенерация тестовых вопросов
    о проектах Svyazi из базы знаний.
    """

    LORENZO_GOLDEN_EXAMPLES = [
        {
            "question": "Какой проект из базы Lorenzo использует BM25 для поиска?",
            "expected_tools": ["search_docs", "bm25_passages"],
            "expected_answer_contains": ["BM25", "improve_passage_retrieval"]
        },
        {
            "question": "Назови авторов проектов из раунда R38",
            "expected_tools": ["search_docs"],
            "answer_type": "list_of_authors"
        }
    ]

    def build_golden_set_from_docs(self, docs_path: str) -> list[GoldenSetExample]:
        """
        Построить Golden Set из docs/ Lorenzo через RAGAS.
        Генерирует 50 вопросов о проектах Svyazi + правильные трассы.
        """
        generator = RAGASKnowledgeGraphGenerator()
        docs = self._load_docs(docs_path)
        return generator.generate_test_set(docs, n_questions=50, language="ru")
```

## Возможные комбинации

| Комбинация | Новое свойство |
|------------|----------------|
| **Agent Eval + LangGraph (R44)** | LangGraph граф трассируется → Golden Set проверяет каждый узел, а не только финальный ответ |
| **Agent Eval + LLM Observability (R45)** | Semantic span трассировка + Golden Set: автоматически находить шаги где агент отклоняется от эталона |
| **Agent Eval + CLEV (R47)** | CLEV-консенсус судей для оценки качества CoT-трасс: три модели голосуют был ли reasoning верным |
| **Agent Eval + Coordination Harness (R46)** | Golden Set для мультиагентных систем: эталонная трасса включает межагентные сообщения |
| **Agent Eval + Lorenzo MCP** | Регрессионное тестирование MCP-инструментов Lorenzo: Golden Set из 50 вопросов о базе знаний |

## Контакт

- Статья: https://habr.com/ru/articles/1034050/ (май 2025)
- Автор: kobets87 (Хабр)
- RAGAS: docs.ragas.io (TestsetGenerator)
- LM_Studio: lmstudio.ai (локальный OpenAI-compatible сервер)
- DeepEval: deepeval.ai (альтернатива: kucev R48, ToolCorrectnessMetric)
- Смежная (SWE-MERA benchmark, R41): docs/06-discovery/round-41/
- Смежная (Yandex LLM eval, R44): docs/06-discovery/round-44/projects/yandex-llm-evaluation-production-pipeline.md
- Смежная (CLEV LLM Judge, R47): docs/06-discovery/round-47/projects/maslennikov-llm-judge-educational-content-clev.md

## Смотрите также
- [Главная](../../../README.md)
- [Метрики](../../../METRICS.md)
- [Здоровье](../../../HEALTH.md)
- [Глоссарий](../../../GLOSSARY.md)
- [Сущности](../../../ENTITIES.md)
- [Решения](../../../DECISIONS.md)
