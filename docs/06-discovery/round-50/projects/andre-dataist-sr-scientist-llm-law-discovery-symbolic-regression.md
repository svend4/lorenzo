---
date: 2026-05-15
tags: [rag, orchestration, knowledge, ingestion, architecture]
state: normalized
---

# SR-Scientist: LLM-агент открывает законы природы через символическую регрессию и RL

<!-- toc-auto -->
<!-- tags: andre-dataist-sr-scientist-llm-law-discovery-symbolic-regression, docs -->


<!-- summary -->
> `andre-dataist-sr-scientist-llm-law-discovery-symbolic-regression` — раздел документации проекта Lorenzo.


> [!TIP]
> Документ содержит практические рекомендации и лучшие практики.

<!-- alert-added -->

**Автор:** andre_dataist  
**Хабр:** https://habr.com/ru/articles/957620/  
**GitHub:** github.com/GAIR-NLP/SR-Scientist  
**Слой:** analytics / orchestration  
**Дата:** октябрь 2025  
**Уникальность:** LLM-агент в стиле ReAct автономно открывает математические законы из экспериментальных данных через символическую регрессию — без участия человека. Буфер опыта хранит лучшие уравнения между сессиями. Обучение через GRPO (Group Relative Policy Optimization) с непрерывной наградой. Точность: +6-35% над базовыми SR-методами; 7-8 точных уравнений vs 4-5 у конкурентов. Тестирование на GPT-OSS-120B, Qwen3-Coder-30B, Qwen3-Coder-480B.

## Проблема: символическая регрессия требует экспертизы

```
Символическая регрессия (Symbolic Regression, SR):
  → Задача: найти математическое уравнение, объясняющее данные
  → Вход: (x1, x2, ..., xn) → y таблица измерений
  → Выход: аналитическое выражение f(x1...xn) = y

Традиционные SR-методы:
  → Genetic Programming (GP): перебор деревьев выражений
  → Ограничение: нет понимания физического смысла
  → Пример провала: x1*x2 + x3 (верно численно, но бессмысленно физически)

Физик vs GP:
  → GP: минимизирует MSE → любое уравнение
  → Физик: ищет уравнение со смыслом (размерность, симметрия, сохранение)

SR-Scientist решение:
  → LLM знает физику/химию/биологию из pretraining
  → LLM предлагает структуру уравнения (гипотеза)
  → Инструменты проверяют гипотезу на данных
  → GRPO обучает LLM находить лучшие уравнения
```

## Архитектура SR-Scientist

```python
# andre_dataist: SR-Scientist — LLM агент для открытия законов
# habr.com/ru/articles/957620/
# github.com/GAIR-NLP/SR-Scientist

from dataclasses import dataclass, field
from typing import Optional
import numpy as np
import json

@dataclass
class Equation:
    """Математическое уравнение — гипотеза агента."""
    expression: str          # "F = G * m1 * m2 / r**2" (символьная форма)
    variables: list[str]     # ["G", "m1", "m2", "r"]
    nmse: float             # Normalized Mean Squared Error (ниже = лучше)
    mape: float             # Mean Absolute Percentage Error
    is_exact: bool          # точное совпадение с истинным законом
    iteration: int          # на каком шаге найдено

@dataclass
class ExperienceBuffer:
    """
    Буфер опыта: хранит лучшие уравнения между сессиями.

    Ключевой компонент SR-Scientist:
    Обычный ReAct: каждый запуск с нуля
    SR-Scientist: лучшие гипотезы предыдущих запусков → seed для следующих

    Аналог "научной памяти": не повторять уже проверенные тупики.
    """
    best_equations: list[Equation] = field(default_factory=list)
    failed_hypotheses: list[str] = field(default_factory=list)
    domain_knowledge: dict = field(default_factory=dict)
    max_size: int = 50

    def add(self, eq: Equation):
        """Добавить уравнение, сохраняя только лучшие."""
        self.best_equations.append(eq)
        self.best_equations.sort(key=lambda x: x.nmse)
        if len(self.best_equations) > self.max_size:
            self.best_equations = self.best_equations[:self.max_size]


class SRScientistAgent:
    """
    LLM-агент для открытия математических законов.

    Архитектура ReAct:
    Reason: сформулировать гипотезу об уравнении
    Act: проверить гипотезу инструментами
    Observe: измерить качество уравнения на данных
    → повторить до нахождения точного закона или max_steps

    Два инструмента:
    1. data_analyst: анализировать данные, строить корреляции, предобработка
    2. equation_evaluator: вычислить NMSE/MAPE для предложенного уравнения

    Оптимальная длина: ~25 шагов на итерацию.
    """

    def __init__(self, llm, experience_buffer: ExperienceBuffer):
        self.llm = llm
        self.buffer = experience_buffer

    async def discover_law(self,
                            data: np.ndarray,
                            variable_names: list[str],
                            domain: str = "physics") -> Equation:
        """
        Автономное открытие закона из экспериментальных данных.

        data: матрица [n_samples, n_variables + 1]
              последний столбец = целевая переменная y
        variable_names: ["m1", "m2", "r", "G"]
        domain: "physics" | "chemistry" | "biology" | "materials"
        """
        # Начальный контекст: данные + лучшие прошлые гипотезы
        context = self._build_context(data, variable_names, domain)

        messages = [
            {"role": "system", "content": self._system_prompt(domain)},
            {"role": "user", "content": context}
        ]

        best_equation = None

        for step in range(25):  # оптимально ~25 шагов
            # ReAct: Reason → Act
            action = await self._react_step(messages)

            if action["type"] == "data_analyst":
                # Анализировать данные: корреляции, размерности, паттерны
                result = self._data_analyst(data, variable_names,
                                             action["analysis_request"])

            elif action["type"] == "equation_evaluator":
                # Проверить уравнение на данных
                eq = action["equation"]
                nmse, mape = self._evaluate_equation(eq, data, variable_names)

                equation = Equation(
                    expression=eq,
                    variables=variable_names,
                    nmse=nmse, mape=mape,
                    is_exact=nmse < 1e-6,
                    iteration=step
                )

                if best_equation is None or nmse < best_equation.nmse:
                    best_equation = equation
                    self.buffer.add(equation)

                if equation.is_exact:
                    return equation

                result = json.dumps({"nmse": nmse, "mape": mape,
                                      "is_exact": equation.is_exact})

            elif action["type"] == "final_answer":
                return best_equation or self._best_from_buffer()

            messages.append({"role": "tool", "content": result})

        return best_equation

    def _build_context(self, data, variables, domain) -> str:
        """
        Контекст из данных + буфера опыта.
        Буфер опыта — ключевое отличие от обычного ReAct.
        """
        stats = self._compute_stats(data, variables)

        prior_knowledge = ""
        if self.buffer.best_equations:
            top_3 = self.buffer.best_equations[:3]
            prior_knowledge = "\nЛучшие предыдущие гипотезы:\n" + \
                              "\n".join(f"- {eq.expression} (NMSE={eq.nmse:.6f})"
                                        for eq in top_3)

        return f"""Домен: {domain}
Переменные: {variables}
Статистика данных: {stats}
{prior_knowledge}

Задача: найти аналитическое уравнение, которое точно объясняет данные."""

    def _evaluate_equation(self, expr: str,
                             data: np.ndarray,
                             variables: list[str]) -> tuple[float, float]:
        """
        Вычислить NMSE и MAPE для символьного выражения.
        Использует sympy для парсинга + numpy для вычисления.
        """
        import sympy as sp

        # Парсить выражение
        syms = {v: sp.Symbol(v) for v in variables}
        expr_parsed = sp.sympify(expr, locals=syms)
        expr_func = sp.lambdify(list(syms.values()), expr_parsed, "numpy")

        # Вычислить предсказания
        X = data[:, :-1]
        y_true = data[:, -1]
        y_pred = expr_func(*[X[:, i] for i in range(X.shape[1])])

        # NMSE
        nmse = np.mean((y_true - y_pred) ** 2) / np.var(y_true)
        # MAPE
        mape = np.mean(np.abs((y_true - y_pred) / (y_true + 1e-8)))

        return float(nmse), float(mape)
```

## GRPO-обучение агента

```python
class SRScientistTrainer:
    """
    Обучение SR-Scientist через GRPO (Group Relative Policy Optimization).

    GRPO — вариант RLHF без отдельной reward-модели:
    - Генерировать G вариантов ответа на один промпт
    - Вычислить награды для каждого варианта
    - Обновить политику: повысить prob для лучших вариантов

    Непрерывная награда (ключевое отличие от бинарной):
    r = 1 - min(NMSE, 1)  → диапазон [0, 1]
    При точном совпадении (NMSE < 1e-6) r = 1.0 (максимум)
    При плохой гипотезе (NMSE = 1) r = 0.0

    Это лучше бинарного "правильно/неправильно":
    Агент получает сигнал даже при частично верных гипотезах.
    """

    CONTINUOUS_REWARD = "r = 1 - min(NMSE(predicted, true), 1.0)"

    def compute_reward(self, equation: Equation) -> float:
        """Непрерывная награда для GRPO."""
        if equation.is_exact:
            return 1.0
        return max(0.0, 1.0 - min(equation.nmse, 1.0))


BENCHMARK_RESULTS = {
    "датасет": "LSR-Synth: физика, химия, биология, материаловедение",
    "модели_тестирования": [
        "GPT-OSS-120B",
        "Qwen3-Coder-30B",
        "Qwen3-Coder-480B"
    ],
    "метрики": {
        "MAPE": "cross-domain",
        "NMSE": "normalized MSE",
        "symbolic_accuracy": "точное совпадение уравнения"
    },
    "результаты": {
        "точных_уравнений_SR_Scientist": "7-8 из N (vs 4-5 у конкурентов)",
        "прирост_точности": "6-35% над базовыми SR-методами",
        "оптимальная_длина_сценария": "~25 шагов"
    },
    "arxiv": "https://arxiv.org/abs/2510.11661"
}
```

## Применение к Lorenzo

```python
# Lorenzo: SR-Scientist паттерн для поиска закономерностей в базе знаний

class LorenzoPatternDiscovery:
    """
    andre_dataist паттерн для Lorenzo:
    Агент-исследователь для поиска закономерностей в docs/:
    "Какие темы коррелируют между раундами?"
    "Какой паттерн у проектов с высоким collab_score?"

    Адаптация SR-Scientist:
    data = матрица метрик проектов (wc, tags, collab_score, round)
    variables = ["wc", "tags_count", "round_num", "collab_score"]
    цель = найти формулу: collab_score ≈ f(wc, tags, round)

    Буфер опыта = SUMMARIES.md Lorenzo — накапливать лучшие
    корреляции между раундами.
    """
    pass
```

## Возможные комбинации

| Комбинация | Новое свойство |
|------------|----------------|
| **SR-Scientist + Temporal KG (R47)** | Темпоральный граф научных законов: как SR-агент обновляет уравнения при новых данных |
| **SR-Scientist + Agent Evaluation (R48)** | Golden Set для SR-агента: эталонные трассы открытия закона Ньютона/Хука |
| **SR-Scientist + LangGraph (R44)** | LangGraph: reason_node → data_analyst_node → evaluate_node → refine или finalize |
| **SR-Scientist + LLM Observability (R45)** | Трейсинг: как меняется качество гипотез за 25 шагов → визуализация convergence |
| **SR-Scientist + Coordination Harness (R46)** | Несколько SR-агентов ищут законы параллельно → coordination harness измеряет fidelity передачи гипотез |

## Контакт

- Статья: https://habr.com/ru/articles/957620/ (октябрь 2025)
- Автор: andre_dataist (Хабр)
- GitHub: github.com/GAIR-NLP/SR-Scientist
- arXiv: https://arxiv.org/abs/2510.11661
- GRPO: Group Relative Policy Optimization (DeepSeek-R1 оригинал)
- SymPy: sympy.org (символьные вычисления в Python)
- Смежная (LLM для науки v1, R36): docs/06-discovery/round-36/
- Смежная (Reasoning models, R20): docs/06-discovery/round-20/

## Смотрите также
- [Главная](../../../README.md)
- [Метрики](../../../METRICS.md)
- [Здоровье](../../../HEALTH.md)
- [Глоссарий](../../../GLOSSARY.md)
- [Сущности](../../../ENTITIES.md)
- [Решения](../../../DECISIONS.md)
