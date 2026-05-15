# Глухой телефон для ИИ: физика LLM-графов и почему добавление агентов всё ломает

> [!WARNING]
> Документ содержит описание рисков и ограничений. Изучите их перед принятием архитектурных решений.

<!-- alert-added -->

**Автор:** aak204  
**Хабр:** https://habr.com/ru/articles/1019490/  
**GitHub:** https://github.com/aak204/llm-coordination-harness  
**Слой:** analytics / orchestration  
**Дата:** апрель 2026  
**Уникальность:** Единственная русскоязычная статья, рассматривающая мультиагентные LLM-системы как задачу физики коммуникации. LLM Coordination Harness: 4 оригинальных метрики (F — fidelity, ρ — error correlation, B — propagation balance, C — fan-in pressure). Экспериментальное измерение деградации информации в star vs tree топологиях на 144 циклах и ~2000 API-вызовах. Тот же автор, что LOCK-R (R43), — новое направление исследований.

## Проблема: добавление агентов ухудшает результат

```
Интуиция: больше агентов = лучший результат
Реальность: "глухой телефон" — информация деградирует на каждом хопе

Ключевые вопросы:
  → Сколько % критической информации теряется при передаче между агентами?
  → Агенты ошибаются независимо или коррелированно?
  → Равномерно ли распределяется сигнал по сети?
  → Насколько перегружены узлы с большим fan-in?

Текущее состояние:
  → Стандартные метрики (accuracy, token count) не отвечают на эти вопросы
  → Нет инструментов измерения "здоровья" координации
  → Архитекторы выбирают топологию интуитивно
```

## 4 метрики координации: математика

```python
# aak204: LLM Coordination Harness
# habr.com/ru/articles/1019490
# github.com/aak204/llm-coordination-harness

import numpy as np
from dataclasses import dataclass
from typing import Optional

@dataclass
class CoordinationMetrics:
    """
    4 оригинальных метрики здоровья мультиагентной системы.
    Измеряют разные аспекты коммуникационной физики LLM-графа.
    """
    F: float   # Fidelity — сохранность информации
    rho: float  # Error Correlation — независимость ошибок агентов
    B: float   # Propagation Balance — равномерность сигнала
    C: float   # Fan-in Pressure — нагрузка на входящие узлы


def compute_fidelity(
    source_facts: list[str],
    received_facts: list[str],
    critical_subset: Optional[list[str]] = None
) -> float:
    """
    F (Fidelity): доля критической информации, пережившей передачу.

    Диапазон: [0, 1]. F=1 — вся информация сохранена. F=0 — потеря всего.

    Ключевое отличие от accuracy:
    Accuracy измеряет правильность конечного ответа.
    Fidelity измеряет сохранность фактов на каждом хопе — можно найти
    где именно произошла потеря.
    """
    if critical_subset is not None:
        # Оценивать только критические факты (не весь контекст)
        source_critical = set(critical_subset) & set(source_facts)
        received_critical = set(critical_subset) & set(received_facts)
    else:
        source_critical = set(source_facts)
        received_critical = set(received_facts)

    if not source_critical:
        return 1.0

    preserved = source_critical & received_critical
    return len(preserved) / len(source_critical)


def compute_error_correlation(
    agent_errors: list[list[bool]]
) -> float:
    """
    ρ (Error Correlation): насколько агенты ошибаются совместно.

    ρ ≈ 0: ошибки независимы (коллективная мудрость работает — можно голосовать)
    ρ ≈ 1: ошибки коррелированы (коллективная глупость — все ошибаются вместе)

    Формула: среднее попарное phi-correlation между ошибками агентов.
    """
    n_agents = len(agent_errors)
    if n_agents < 2:
        return 0.0

    correlations = []
    for i in range(n_agents):
        for j in range(i + 1, n_agents):
            errors_i = np.array(agent_errors[i], dtype=float)
            errors_j = np.array(agent_errors[j], dtype=float)

            # Phi-correlation (Matthews Correlation Coefficient для binary)
            if errors_i.std() > 0 and errors_j.std() > 0:
                phi = np.corrcoef(errors_i, errors_j)[0, 1]
                correlations.append(phi)

    return float(np.mean(correlations)) if correlations else 0.0


def compute_propagation_balance(
    message_sizes: dict[str, list[int]]
) -> float:
    """
    B (Propagation Balance): насколько равномерно сигнал распределяется.

    Используется коэффициент Джини (Gini coefficient):
    B=1: идеальное равномерное распределение
    B=0: весь сигнал концентрируется в одном узле

    message_sizes: {agent_id: [размеры сообщений]}
    """
    total_per_agent = [sum(sizes) for sizes in message_sizes.values()]
    if not total_per_agent or sum(total_per_agent) == 0:
        return 1.0

    total = sum(total_per_agent)
    proportions = sorted([x / total for x in total_per_agent])
    n = len(proportions)

    # Коэффициент Джини
    gini_numerator = sum(
        abs(proportions[i] - proportions[j])
        for i in range(n)
        for j in range(n)
    )
    gini = gini_numerator / (2 * n * sum(proportions))

    return 1.0 - gini  # 1 - Gini → высокое B = равномерность


def compute_fan_in_pressure(
    context_window_size: int,
    incoming_messages: list[str]
) -> float:
    """
    C (Fan-in Pressure): насколько переполнен контекст получателя.

    C ∈ [0, 1]. C=1 → полное насыщение контекстного окна.
    Высокое C → агент работает в условиях context overflow → потеря фактов.
    """
    total_incoming_tokens = sum(
        len(msg.split()) * 1.3  # грубая оценка: 1.3 токена на слово
        for msg in incoming_messages
    )
    return min(1.0, total_incoming_tokens / context_window_size)
```

## Экспериментальное измерение: Star vs Tree

```python
class TopologyExperiment:
    """
    Сравнение двух топологий:
    - Star (flat): один координатор + N агентов-исполнителей
    - Balanced Tree: иерархия глубиной 2 (средний уровень агрегирует)

    Датасеты:
    - CRAFT-mini: задачи с асимметричным распределением информации
    - AgentsNet-mini: многошаговые reasoning tasks
    """

    EXPERIMENT_CONFIG = {
        "topologies": ["star", "balanced_tree"],
        "message_budgets": [0, 32, 96],    # токены на хоп
        "models": ["Qwen 3.5 Plus", "Gemini 3.1 Flash Lite"],
        "api": "OpenRouter",
        "total_cycles": 144,
        "total_api_calls": "~2000",
        "datasets": ["CRAFT-mini", "AgentsNet-mini"]
    }

    KEY_FINDINGS = {
        "fact_loss_in_tree": {
            "value": "~25% потеря фактов при иерархической передаче",
            "reason": "Каждый агрегирующий узел сжимает информацию → потери",
            "analogy": "Классический 'глухой телефон': искажение нарастает"
        },

        "adversarial_resilience": {
            "finding": "Tree топология устойчивее к adversarial injection чем Star",
            "reason": (
                "Инъекция ложного факта в одну ветку иерархии "
                "изолируется на уровне агрегации. "
                "В Star-топологии ложный факт напрямую достигает координатора."
            ),
            "paradox": "Та же иерархия, которая теряет факты, защищает от атак"
        },

        "message_budget_effect": {
            "finding": "Бюджет 32 токена: значительная потеря. 96 токенов: резкое улучшение F",
            "sweet_spot": "96 токенов на хоп — хороший баланс cost vs fidelity",
            "zero_budget": "0 токенов: только структурная координация, без контента"
        },

        "standard_metrics_failure": {
            "finding": (
                "Метрики volume и accuracy переоценивают quality координации. "
                "Можно иметь высокий accuracy финального ответа при низком F — "
                "модель 'угадала' не сохранив промежуточные факты."
            )
        }
    }

    def run_experiment(self,
                        topology: str,
                        budget: int,
                        model: str,
                        dataset: str) -> CoordinationMetrics:
        """
        Один экспериментальный цикл: запустить агентную систему,
        измерить 4 метрики координации.
        """
        # Инициализировать граф агентов
        graph = self._build_topology(topology, model)

        # Запустить на датасете
        results = graph.run(dataset, message_budget=budget)

        # Измерить метрики
        return CoordinationMetrics(
            F=compute_fidelity(
                results["source_facts"],
                results["final_facts"],
                results["critical_facts"]
            ),
            rho=compute_error_correlation(results["agent_error_vectors"]),
            B=compute_propagation_balance(results["message_sizes"]),
            C=compute_fan_in_pressure(
                graph.context_window,
                results["coordinator_inputs"]
            )
        )


DESIGN_GUIDELINES = {
    "когда_star": [
        "Задачи с малым числом критических фактов",
        "Нет угрозы adversarial injection",
        "Нужна максимальная fidelity (F)",
        "Агенты ошибаются независимо (низкое ρ)"
    ],
    "когда_tree": [
        "Adversarial environment: ненадёжные источники данных",
        "Много агентов (fan-in > 5 у координатора)",
        "Допустима некоторая потеря фактов",
        "Нужна устойчивость к инъекциям"
    ],
    "message_budget": {
        "0_токенов": "Только структурная координация (маршрутизация)",
        "32_токена": "Базовый уровень, значительные потери",
        "96_токенов": "Рекомендуемый минимум для сохранения качества"
    }
}
```

## Применение к Lorenzo

```python
# Lorenzo: Coordination Harness для оценки мультиагентных пайплайнов

class LorenzoCoordinationAudit:
    """
    aak204 паттерн для Lorenzo:
    Измерить F, ρ, B, C для improve_run_all.py пайплайна.
    Каждая группа скриптов = агент; вывод одной = вход другой.
    Найти где именно информация теряется между группами.
    """

    def audit_pipeline(self, groups: list[str]) -> dict[str, CoordinationMetrics]:
        """
        Запустить пайплайн групп и измерить метрики координации.
        Например: reports → quality → analytics → export.
        """
        metrics = {}
        prev_output = None

        for group in groups:
            result = self._run_group(group, input_data=prev_output)
            if prev_output is not None:
                metrics[group] = CoordinationMetrics(
                    F=compute_fidelity(
                        prev_output["key_facts"],
                        result["key_facts"]
                    ),
                    rho=0.0,   # нет параллельных агентов в линейном пайплайне
                    B=1.0,     # один поток
                    C=compute_fan_in_pressure(4096, result["input_texts"])
                )
            prev_output = result

        return metrics
```

## Возможные комбинации

| Комбинация | Новое свойство |
|------------|----------------|
| **Coordination Harness + LOCK-R (R43)** | Тот же автор: Bayesian Regret как F-метрика на детективных задачах мультиагентного reasoning |
| **Coordination Harness + LangGraph (R44)** | Измерять F/ρ/B/C для LangGraph графов: когда добавление узлов помогает, а когда вредит |
| **Coordination Harness + SherlockOps (R42)** | Измерить fan-in pressure SherlockOps: насколько перегружен координирующий агент |
| **Coordination Harness + Sequential (R38)** | MAESTRO sequential координация: tree или star для медицинских DAG? |
| **Coordination Harness + Yandex LLM Eval (R44)** | Метрики координации как новый тип evaluation: F = fidelity benchmark |

## Контакт

- Статья: https://habr.com/ru/articles/1019490/ (апрель 2026)
- GitHub: https://github.com/aak204/llm-coordination-harness
- Автор: aak204 (тот же автор LOCK-R, R43)
- Датасеты: CRAFT-mini, AgentsNet-mini
- API: OpenRouter (Qwen 3.5 Plus + Gemini 3.1 Flash Lite)
- Смежная (LOCK-R CoT парадокс, R43): docs/06-discovery/round-43/projects/lockr-cot-paradox-bayesian-reasoning-benchmark.md
- Смежная (A2A протокол, R21): docs/06-discovery/round-21/
