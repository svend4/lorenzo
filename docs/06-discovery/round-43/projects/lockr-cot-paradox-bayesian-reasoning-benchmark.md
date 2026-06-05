# LOCK-R: CoT-парадокс и слепой судья для LLM-рассуждений

> [!NOTE]
> Документ создан на основе исследования. Ссылки ведут на связанные материалы.

<!-- alert-added -->

**Автор:** aak204  
**Хабр:** https://habr.com/ru/articles/1020016/  
**GitHub:** https://github.com/aak204/LOCK-R  
**Слой:** analytics  
**Дата:** апрель 2025  
**Уникальность:** Детективный бенчмарк LOCK-R с байесовскими метриками для измерения качества рассуждений агентов (не только финального ответа). Ключевое открытие: CoT-парадокс — включение Chain-of-Thought улучшает исследование гипотез, но в 2 раза увеличивает байесовскую ошибку при верификации (агент рационализирует первоначальную гипотезу). Решение: разделить роли на «думающего исследователя» и «слепого судью» (blind judge без thinking) — regret падает с 1.47 до 0.09. Воспроизведено на Qwen3.5-9B и GPT-5.4, подтверждено на реальном production кейсе.

## Проблема: CoT делает суждение хуже, не лучше

```
Стандартное убеждение:
  → Chain-of-Thought prompting улучшает reasoning
  → "Думай шаг за шагом" → лучший ответ
  → GPT-4 с CoT лучше GPT-4 без CoT

LOCK-R эксперимент показал иное:
  → CoT (thinking mode): хорошо ИССЛЕДУЕТ гипотезы
  → CoT при ВЕРИФИКАЦИИ: генерирует текст который РАЦИОНАЛИЗИРУЕТ
    уже выбранную гипотезу вместо честного взвешивания
  → Байесовская ошибка удваивается!

Аналогия: детектив который "думает вслух":
  → Хорошо: собирает улики широко
  → Плохо: когда надо голосовать — объясняет почему уже выбранный
    подозреваемый всё равно виноват (confirmation bias в тексте)

Решение: разделить thinking explorer и blind judge
  → Explorer (с CoT): ищет улики, задаёт вопросы
  → Judge (без CoT): видит только факты, выносит вердикт
  → regret: 1.47 → 0.09 (16-кратное улучшение)
```

## LOCK-R Benchmark: детективная игра с байесовскими метриками

```python
# LOCK-R: Logical Operations and Chain-of-thought Killing in Reasoning
# github.com/aak204/LOCK-R

from dataclasses import dataclass
import math
from typing import Optional

@dataclass
class Hypothesis:
    """Одна из трёх взаимоисключающих гипотез."""
    id: str
    description: str
    true_likelihood: float     # истинная вероятность (скрыта от агента)
    initial_prior: float       # начальный prior агента


@dataclass
class Evidence:
    """Улика, которую агент может получить через инструмент."""
    tool_name: str
    result: str
    likelihood_updates: dict   # как эта улика обновляет posteriors


class LOCKRBenchmark:
    """
    Детективная игра с управляемыми вероятностями.
    Три взаимоисключающих гипотезы → агент расследует → вердикт.

    Метрики:
    - Bayesian Regret: отклонение от идеального байесовского агента
    - Asymmetry Coefficient (Kc): реакция на подтверждающие vs опровергающие улики
    """

    def __init__(self,
                 hypotheses: list[Hypothesis],
                 available_evidence: list[Evidence],
                 tool_budget: int = 4):
        self.hypotheses = hypotheses
        self.available_evidence = available_evidence
        self.tool_budget = tool_budget  # 4 вызова инструментов максимум

    def run_agent(self, agent, scenario_id: str) -> dict:
        """
        Запустить агента на сценарии.
        Агент вызывает инструменты → получает улики → выносит вердикт.
        """
        tool_calls = []
        agent_state = {"posteriors": {h.id: h.initial_prior
                                       for h in self.hypotheses}}

        # Агент расследует (до tool_budget вызовов)
        for _ in range(self.tool_budget):
            tool_name, args = agent.choose_tool(agent_state, self.available_evidence)
            if tool_name is None:
                break

            evidence = self._get_evidence(tool_name)
            tool_calls.append(tool_name)
            agent_state["evidence_seen"] = agent_state.get("evidence_seen", [])
            agent_state["evidence_seen"].append(evidence)

        # Вердикт агента
        verdict = agent.judge(agent_state)

        # Расчёт метрик
        return {
            "verdict": verdict,
            "tool_calls": tool_calls,
            "bayesian_regret": self._compute_regret(verdict, agent_state),
            "asymmetry_kc": self._compute_asymmetry(agent_state),
            "true_answer": self._true_hypothesis()
        }

    def _compute_regret(self, verdict: str, agent_state: dict) -> float:
        """
        Bayesian Regret = KL(agent_posteriors || ideal_posteriors).
        Идеальный агент: обновляет posteriors строго по Байесу.
        Реальный агент: байесовская ошибка при рационализации.
        """
        ideal = self._compute_ideal_bayesian(agent_state["evidence_seen"])
        agent_post = agent_state["posteriors"]

        kl = sum(
            ideal[h] * math.log(ideal[h] / agent_post.get(h, 1e-10))
            for h in ideal if ideal[h] > 0
        )
        return kl

    def _compute_asymmetry(self, agent_state: dict) -> float:
        """
        Asymmetry Coefficient Kc:
        Kc > 1: агент больше реагирует на подтверждающие улики
        Kc < 1: агент больше реагирует на опровергающие
        Kc = 1: идеально симметричная байесовская обработка

        Высокий Kc при CoT: рационализация первоначальной гипотезы.
        """
        confirming_updates = []
        disconfirming_updates = []

        for evidence in agent_state.get("evidence_seen", []):
            for h, update in evidence.likelihood_updates.items():
                if update > 0:
                    confirming_updates.append(update)
                else:
                    disconfirming_updates.append(abs(update))

        if not disconfirming_updates:
            return float("inf")

        return (sum(confirming_updates) / max(len(confirming_updates), 1)) / \
               (sum(disconfirming_updates) / max(len(disconfirming_updates), 1))
```

## CoT-парадокс: экспериментальное доказательство

```python
COT_PARADOX_RESULTS = {
    "эксперимент": "LOCK-R детективная игра, 4 инструмента, 3 гипотезы",
    "модели": ["Qwen3.5-9B", "GPT-5.4"],

    "результаты": {
        "без_CoT": {
            "bayesian_regret": 0.89,
            "asymmetry_kc": 1.12,
            "описание": "Агент не думает → случайная ошибка"
        },
        "с_CoT_единый_агент": {
            "bayesian_regret": 1.47,
            "asymmetry_kc": 2.31,
            "описание": "CoT УХУДШАЕТ верификацию: рационализация гипотезы"
        },
        "thinking_explorer_plus_blind_judge": {
            "bayesian_regret": 0.09,
            "asymmetry_kc": 1.03,
            "описание": "Разделение ролей: 16x улучшение regret"
        }
    },

    "производственный_кейс": {
        "задача": "Расследование сбоя Payment API",
        "single_agent_accuracy": "40%",
        "blind_judge_accuracy": "100%",
        "описание": "Реальный production debugging подтвердил результаты"
    },

    "объяснение_парадокса": """
    CoT при верификации:
    - Агент выбрал гипотезу H1 (возможно ошибочно)
    - Начинает "думать": "H1 потому что A, и потому что B, и..."
    - Генерация текста в пользу H1 усиливает её вес в attention
    - Опровергающие улики для H1 получают меньший вес
    - Результат: confirmation bias закодирован в самом процессе мышления
    """
}


class BlindJudgeArchitecture:
    """
    Решение CoT-парадокса: разделить thinking и judging.
    """

    def solve(self, task: str) -> str:
        # Агент 1: Thinking Explorer (с extended thinking)
        # Задача: собрать все релевантные факты, не делать выводов
        exploration = self.explorer.explore(
            task=task,
            instruction="Собери ТОЛЬКО факты. НЕ делай выводов. "
                        "НЕ выбирай гипотезу. Просто перечисли наблюдения.",
            thinking_enabled=True  # CoT разрешён для исследования
        )

        # Агент 2: Blind Judge (без thinking)
        # Видит только факты, не видит рассуждений Explorer
        verdict = self.judge.decide(
            facts_only=exploration["facts"],  # только факты, без CoT-текста
            instruction="На основе ТОЛЬКО этих фактов: какая гипотеза верна?",
            thinking_enabled=False  # CoT ЗАПРЕЩЁН для суждения
        )

        return verdict

    # Ключевой принцип: Judge не видит thinking Explorer
    # → нет рационализации → симметричная байесовская обработка
```

## Практические рекомендации

```python
PRACTICAL_RECOMMENDATIONS = {
    "когда_использовать_CoT": [
        "Исследование пространства решений (exploration)",
        "Генерация кода (пошаговое рассуждение)",
        "Математические вычисления",
        "Декомпозиция задачи на шаги"
    ],

    "когда_НЕ_использовать_CoT": [
        "Финальное суждение между гипотезами",
        "Оценка вероятностей (adversarial reasoning)",
        "Classification задачи с множеством классов",
        "Когда нужна симметричная обработка за и против"
    ],

    "архитектурный_паттерн": {
        "thinking_explorer": "extended thinking включён",
        "blind_judge": "thinking ВЫКЛЮЧЕН, видит только факты",
        "разделение": "Judge НЕ видит CoT Explorer'а",
        "применение": "Multi-agent debugging, диагностика, расследования"
    },

    "метрики_для_мониторинга": {
        "bayesian_regret": "Отклонение от идеального байесовского агента",
        "asymmetry_kc": "Симметричность обработки за и против (цель: ~1.0)",
        "tool_efficiency": "Качество выбора инструментов (не случайность)"
    }
}
```

## Применение к Lorenzo

```python
# Lorenzo: blind-judge паттерн для Q&A качества

class LorenzoBlindJudgeQA:
    """
    LOCK-R паттерн для Lorenzo improve_llm_qa.py:
    При неоднозначных вопросах разделить exploration и judgment.
    """

    def ask(self, question: str, docs: list[str]) -> dict:
        # Explorer: найти все релевантные факты (thinking=True)
        facts = self.explorer.extract_facts(
            question=question,
            docs=docs,
            thinking=True  # CoT для широкого поиска
        )

        # Judge: вынести ответ только по фактам (thinking=False)
        answer = self.judge.answer(
            question=question,
            facts_only=facts,  # без CoT explorer'а
            thinking=False     # без рационализации
        )

        return {
            "answer": answer,
            "facts_used": facts,
            "confidence": self._compute_confidence(facts, answer)
        }
```

## Возможные комбинации

| Комбинация | Новое свойство |
|------------|----------------|
| **LOCK-R + SherlockOps (R42)** | Blind judge для RCA: Explorer собирает данные алерта, Judge выносит вердикт |
| **LOCK-R + Sequential (R38)** | Sequential панель агентов: каждый — blind judge своей гипотезы |
| **LOCK-R + LangFuse (R38)** | Трейсинг asymmetry Kc в реальных запросах: мониторинг CoT-парадокса |
| **LOCK-R + Contract SGR (R39)** | Blind judge для анализа рисков договора: Explorer читает, Judge оценивает |
| **LOCK-R + MAESTRO (R38)** | CARL DAG: отдельный шаг blind-judge для финального медицинского решения |

## Контакт

- Статья: https://habr.com/ru/articles/1020016/ (апрель 2025)
- GitHub: https://github.com/aak204/LOCK-R
- Смежная (Reasoning LLMs обзор 4 подхода, Kual): https://habr.com/ru/articles/894688/
- Смежная (TinyZero RL reasoning): https://github.com/Jiayi-Pan/TinyZero/
