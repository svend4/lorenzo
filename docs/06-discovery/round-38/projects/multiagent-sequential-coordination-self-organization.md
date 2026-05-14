# Долой иерархию: LLM-агенты самоорганизуются лучше, чем мы их проектируем

**Автор:** dochkinavika (Вика Дочкина, исследователь Сбер, диссертация по автономным AI-системам)  
**Хабр:** https://habr.com/ru/articles/1017200/  
**GitHub:** нет  
**Слой:** orchestration  
**Дата:** март 2025  
**Уникальность:** Контролируемый эксперимент на 25 000+ задачах и >1 млрд токенов, сравнивающий 4 протокола координации. Главный результат: Sequential (агенты видят результаты друг друга, без ролей) Q=0.724 vs Coordinator (центральный агент раздаёт задачи) Q=0.640, p<0.001. Феномен «добровольного самоотказа» — 38/60 неактивных агентов сами отказываются участвовать. Система автоматически углубляет иерархию при росте сложности (1.22→1.56 уровня).

## Проблема: мы усложняем то, что работает проще

```
Стандартный подход к мультиагентным системам:
  → Назначить роли (Аналитик, Разработчик, Критик...)
  → Центральный Coordinator раздаёт задачи
  → Агенты "не знают" о работе других

Интуиция подсказывает: структура → лучше.
Эксперимент показывает: НЕТ.

Sequential без ролей:
  → Агент 1 пишет → Агент 2 видит + добавляет → ...
  → Агенты сами решают когда "молчать"
  → Качество выше на 14%

Почему: LLM обучены на человеческом тексте где ответы строятся
последовательно с учётом контекста — это их естественная среда.
```

## 4 протокола координации: экспериментальное сравнение

```python
# Четыре протокола — разные способы организовать одну задачу

from dataclasses import dataclass
from enum import Enum

class CoordinationProtocol(Enum):
    COORDINATOR = "coordinator"  # Q=0.640 — центральный агент раздаёт задачи
    SEQUENTIAL  = "sequential"   # Q=0.724 — агенты видят результаты друг друга
    BROADCAST   = "broadcast"    # Q=0.510 — все видят задачу, отвечают параллельно
    SHARED      = "shared"       # Q=0.503 — общее пространство без явной координации

@dataclass
class ExperimentSetup:
    """
    Из статьи dochkinavika: экспериментальная установка.
    """
    tasks: int = 25_000          # задач в экспериментах
    tokens: str = ">1 млрд"      # суммарный расход
    models_tested: list = None   # 8 моделей
    agent_counts: list = None    # 4, 8, 16, 32, 64, 128, 256 агентов

    def __post_init__(self):
        self.models_tested = [
            "Claude",            # лучшее качество
            "GPT-5.4",
            "GPT-4o",
            "DeepSeek v3.2",     # 95% качества Claude при 1/24 стоимости
            "GLM-5",
            "Gemini-3-flash",
            "GigaChat 2 Max",
            "Llama-3-70B"
        ]
        self.agent_counts = [4, 8, 16, 32, 64, 128, 256]


class SequentialProtocol:
    """
    Победивший протокол: ~50 строк кода, без role-assignment промптов.

    Агент N получает:
    1. Оригинальную задачу
    2. Все предыдущие ответы агентов 1..N-1
    3. Может добавить что-то новое ИЛИ заявить что "пас"
    """

    async def run(self, task: str, agents: list, n_rounds: int = 1) -> str:
        context = {"task": task, "responses": []}

        for round_num in range(n_rounds):
            for i, agent in enumerate(agents):
                prompt = self._build_prompt(context, agent_index=i)
                response = await agent.generate(prompt)

                # Феномен самоотказа: агент сам решает "мне нечего добавить"
                if self._is_withdrawal(response):
                    context["withdrawals"] = context.get("withdrawals", 0) + 1
                    continue

                context["responses"].append({
                    "agent": agent.name,
                    "content": response,
                    "round": round_num
                })

        return self._synthesize(context)

    def _build_prompt(self, context: dict, agent_index: int) -> str:
        prev_responses = "\n\n".join([
            f"Агент {i+1}: {r['content']}"
            for i, r in enumerate(context["responses"])
        ])

        return f"""Задача: {context["task"]}

Предыдущие ответы:
{prev_responses if prev_responses else "(ты первый)"}

Твоя задача: добавь что-то ценное, что ещё не было сказано.
Если все важные аспекты уже покрыты — скажи "Согласен, добавить нечего."
НЕ повторяй то, что уже сказано."""

    def _is_withdrawal(self, response: str) -> bool:
        """Детектор феномена самоотказа."""
        withdrawal_phrases = [
            "добавить нечего", "согласен с предыдущими",
            "все аспекты покрыты", "не могу добавить ценность",
            "предыдущие ответы исчерпывающие"
        ]
        return any(p in response.lower() for p in withdrawal_phrases)
```

## Феномен самоотказа и адаптивная иерархия

```python
EXPERIMENT_FINDINGS = {
    "withdrawal_phenomenon": {
        "описание": "Феномен добровольного самоотказа",
        "данные": "38 из 60 'неактивных' агентов в Sequential",
        "поведение": "Агент самостоятельно заявляет что не добавит ценности",
        "вывод": "LLM natural pruning: агенты 'знают' когда говорить"
    },

    "adaptive_hierarchy": {
        "описание": "Автоматическое углубление иерархии при сложности",
        "простые_задачи": 1.22,   # средняя глубина иерархии
        "сложные_задачи": 1.56,   # глубже без внешней инструкции
        "механизм": "Агенты сами начинают организовывать подзадачи"
    },

    "scaling": {
        "4_агента":   {"Q": 0.68, "cost_relative": 1.0},
        "16_агентов": {"Q": 0.79, "cost_relative": 2.3},
        "64_агента":  {"Q": 0.89, "cost_relative": 5.7},
        "256_агентов": {"Q": 0.95, "cost_relative": 11.8},
        "вывод": "Закон убывающей отдачи, но Q≈0.95 устойчиво при 256 агентах"
    },

    "role_specialization": {
        "уникальных_ролей": 5006,
        "использованы_ровно_раз": "54%",
        "вывод": "LLM создают одноразовые специализации под задачу"
    },

    "cost_efficiency": {
        "DeepSeek_v3_2": {
            "quality_vs_claude": "95%",
            "cost_vs_claude": "1/24",
            "практический_вывод": "Для большинства задач DeepSeek оптимален"
        }
    }
}
```

## Метрика Q: multi-criterion model-judge

```python
class QualityMetricQ:
    """
    Q — независимая оценка качества ответа от model-judge.
    5 критериев, каждый 0-1.
    """

    CRITERIA = {
        "accuracy":      "Точность фактических утверждений",
        "completeness":  "Охват всех аспектов задачи",
        "coherence":     "Логическая связность рассуждений",
        "applicability": "Практическая применимость ответа",
        "alignment":     "Соответствие исходной задаче/миссии"
    }

    def evaluate(self, response: str, task: str) -> float:
        """Возвращает Q ∈ [0, 1]."""
        scores = {}
        for criterion, description in self.CRITERIA.items():
            prompt = f"""Оцени от 0 до 1: {description}

Задача: {task}
Ответ: {response}

Верни только число."""
            scores[criterion] = float(self.judge_llm.generate(prompt))

        return sum(scores.values()) / len(scores)


BENCHMARK_RESULTS = {
    "protocol_comparison": {
        "Sequential":  {"Q": 0.724, "code_lines": "~50", "role_prompts": False},
        "Coordinator": {"Q": 0.640, "code_lines": "~200", "role_prompts": True},
        "Broadcast":   {"Q": 0.510, "code_lines": "~30", "role_prompts": False},
        "Shared":      {"Q": 0.503, "code_lines": "~40", "role_prompts": False},
    },
    "statistical_significance": "p < 0.001 (Sequential vs all others)",
    "dataset": "25,000+ diverse tasks",
    "judge": "независимая model-judge (не та что генерирует ответы)"
}
```

## Практические выводы

```python
PRACTICAL_GUIDELINES = {
    "когда_Sequential": [
        "Задачи требующие итеративного уточнения",
        "Когда нужно критическое peer-review",
        "Когда нельзя заранее определить какие роли нужны",
        "Исследовательские/творческие задачи"
    ],

    "когда_Coordinator": [
        "Строго параллельные независимые подзадачи",
        "Когда порядок выполнения критичен",
        "Когда нужна явная ответственность за компонент"
    ],

    "реализация_Sequential": """
# Sequential протокол — ~50 строк без role-assignment:
async def sequential_multi_agent(task, agents, n=1):
    context = [task]
    for _ in range(n):
        for agent in agents:
            response = await agent.chat(
                [task] + context,
                system="Добавь что-то ценное или скажи 'нечего добавить'"
            )
            if "нечего добавить" not in response.lower():
                context.append(response)
    return context[-1]  # последний ответ как финальный
    """
}
```

## Применение к Lorenzo

```python
# Lorenzo собирает знания от нескольких агентов-обогатителей.
# Sequential паттерн: каждый скрипт видит результаты предыдущих.

class LorenzoSequentialEnrichment:
    """
    Вместо параллельного запуска независимых improve_*.py скриптов —
    Sequential: каждый следующий скрипт видит вывод предыдущего.

    Например: textrank → abstract → gap_filler
    каждый следующий использует результат предыдущего как контекст.
    """

    ENRICHMENT_SEQUENCE = [
        "improve_textrank.py",     # резюме
        "improve_abstract.py",     # абстракт на основе резюме
        "improve_gap_filler.py",   # заполнение пробелов с учётом абстракта
        "improve_crosslink_all.py" # ссылки с учётом заполненных пробелов
    ]
```

## Возможные комбинации

| Комбинация | Новое свойство |
|------------|----------------|
| **Sequential + LangGraph (R35)** | Sequential как StateGraph: каждый узел видит предыдущий state |
| **Sequential + Cognitive Memory (R31)** | Агенты накапливают рабочую память через Sequential rounds |
| **Sequential + LLM Judge (R28)** | Q-метрика как реальный judge в цикле Lorenzo enrichment |
| **Sequential + MAESTRO CARL (R38)** | CARL DAG для параллельных шагов + Sequential для peer-review фазы |
| **Sequential + AgentFS (R01)** | Файловая система как shared context для Sequential агентов |

## Контакт

- Статья: https://habr.com/ru/articles/1017200/ (март 2025)
- Автор: Вика Дочкина (Сбер), диссертация по автономным AI-системам
- Смежная (Agent Federation MQTT+HNSW): https://habr.com/ru/articles/951248/
- Смежная (ACI формализованный интерфейс агентов): https://habr.com/ru/articles/945472/
- Смежная (оркестрация Domclick, BPMN+LLM): https://habr.com/ru/companies/domclick/articles/966066/
