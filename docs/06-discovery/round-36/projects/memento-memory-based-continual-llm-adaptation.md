# AgentFly/Memento: память вместо файнтюнинга для LLM continuous adaptation

**Автор:** andre_dataist  
**Хабр:** https://habr.com/ru/articles/940824/  
**GitHub:** https://github.com/Agent-on-the-Fly/Memento  
**Слой:** memory / orchestration  
**Дата:** август 2025  
**Уникальность:** Полное решение проблемы catastrophic forgetting без обновления весов: замороженная LLM + case-based reasoning memory + soft Q-learning для оценки полезности случаев (M-MDP). Continuous online adaptation без alignment degradation. Zero gradient updates = zero риска разрушения alignment. Развёртываемый open-source фреймворк.

## Проблема: файнтюнинг убивает alignment

```
Catastrophic forgetting (катастрофическое забывание):
  Нейросеть обучена на задаче A.
  → Дообучить на задаче B
  → Забывает задачу A

Проблема для LLM в production:
  → Нужно добавить новые знания (новые продукты, политики)
  → Full fine-tuning: дорого ($$$), долго, рискованно
  → Incremental fine-tuning: catastrophic forgetting + alignment degradation
  → LoRA адаптеры: лучше, но всё равно меняют поведение

Классические решения:
  EWC (Elastic Weight Consolidation) → замедляет forgetting, но не останавливает
  ROME/MEMIT → точечное редактирование весов → риск side effects
  Replay Buffer → храним старые данные → privacy issues

AgentFly/Memento решение:
  → НЕ менять веса вообще
  → Новые знания → в memory store
  → Memory retrieval вместо weight updates
  → Soft Q-learning: умный выбор что помнить, что забыть
```

## Архитектура: Planner + Executor + Memory

```python
# AgentFly/Memento: github.com/Agent-on-the-Fly/Memento

from memento import MementoAgent, CaseMemory, SoftQLearner

class MementoFramework:
    """
    Три компонента:

    1. Frozen LLM (Planner)
       → Базовая модель, веса НЕ меняются никогда
       → Принимает: запрос + retrieved cases из памяти
       → Выдаёт: ответ + reflection (что узнал нового)

    2. Case Memory
       → Хранилище прошлых взаимодействий
       → Каждый case: {context, action, outcome, utility}
       → Retrieval: semantic similarity OR Q-value

    3. Soft Q-Learner
       → Оценивает utility каждого case
       → Обновляет Q-values без touching LLM weights
       → Pruning: удалять неполезные cases
    """

    def __init__(self, base_llm, memory_capacity: int = 10000):
        self.llm = base_llm             # замороженная модель
        self.memory = CaseMemory(capacity=memory_capacity)
        self.q_learner = SoftQLearner(
            temperature=0.1,             # softmax temperature
            discount=0.95,               # gamma
            lr=0.01                      # Q-value learning rate
        )

    def adapt(self, context: str, query: str) -> str:
        # 1. Найти релевантные cases из памяти
        retrieved = self.memory.retrieve(
            query=query,
            method="hybrid",  # semantic similarity + Q-value
            top_k=5
        )

        # 2. Augment промпт с retrieved cases
        augmented_prompt = self._build_prompt(query, retrieved)

        # 3. LLM генерирует ответ (веса не меняются!)
        response = self.llm.generate(augmented_prompt)

        # 4. Reflection: оценить качество ответа
        outcome = self._evaluate_outcome(query, response)

        # 5. Сохранить новый case в память
        new_case = {
            "context": context,
            "query": query,
            "response": response,
            "outcome": outcome,
            "utility": outcome.score  # initial utility = outcome quality
        }
        self.memory.add(new_case)

        # 6. Обновить Q-values через soft Q-learning
        self.q_learner.update(
            cases=retrieved,
            reward=outcome.score,
            next_state_cases=self.memory.retrieve(query, top_k=5)
        )

        return response
```

## Soft Q-Learning для оценки utility кейсов

```python
import torch
import torch.nn.functional as F

class SoftQLearner:
    """
    Soft Q-Learning (Haarnoja et al., 2018) адаптированный для memory utility.

    Стандартный Q-learning: Q(s,a) = r + γ * max Q(s',a')
    Soft Q-learning: учитывает энтропию → exploration

    State s: embedding запроса
    Action a: выбрать этот case для retrieval
    Reward r: насколько помог этот case в генерации ответа
    """

    def __init__(self, temperature: float = 0.1,
                 discount: float = 0.95, lr: float = 0.01):
        self.temperature = temperature  # α в soft Q-learning
        self.discount = discount        # γ
        self.lr = lr
        # Q-table: case_id → Q-value
        self.q_values: dict[str, float] = {}

    def update(self, cases: list[dict], reward: float,
               next_state_cases: list[dict]):
        """
        Bellman backup для soft Q-learning:
        Q(s,a) ← Q(s,a) + lr * [r + γ * soft_V(s') - Q(s,a)]

        Где soft_V(s') = temperature * log(Σ exp(Q(s',a')/temperature))
        """
        # Soft value function (entropy-regularized)
        next_q_values = [self.q_values.get(c["id"], 0.0)
                         for c in next_state_cases]
        if next_q_values:
            next_q_tensor = torch.tensor(next_q_values)
            # Softmax normalization с температурой
            soft_v = self.temperature * torch.logsumexp(
                next_q_tensor / self.temperature, dim=0
            ).item()
        else:
            soft_v = 0.0

        # Обновить Q-values использованных cases
        for case in cases:
            old_q = self.q_values.get(case["id"], 0.0)
            td_error = reward + self.discount * soft_v - old_q
            self.q_values[case["id"]] = old_q + self.lr * td_error

    def prune_memory(self, memory: "CaseMemory",
                     threshold: float = -0.5):
        """Удалить cases с низкой utility."""
        to_remove = [
            case_id for case_id, q in self.q_values.items()
            if q < threshold
        ]
        for case_id in to_remove:
            memory.remove(case_id)
            del self.q_values[case_id]
```

## M-MDP: Markovian Decision Process для памяти

```python
class MemoryMDP:
    """
    M-MDP (Memory-augmented MDP) формализация:

    State s_t = (запрос, текущие K cases в памяти)
    Action a_t = какой case добавить/обновить/удалить
    Reward r_t = качество ответа LLM с этой конфигурацией памяти
    Transition: обновление памяти согласно action

    Цель: научиться управлять памятью так, чтобы
    LLM давала лучшие ответы с минимумом cases.
    """

    def __init__(self, memory_capacity: int = 1000):
        self.capacity = memory_capacity
        self.states = {}   # embeddings

    def compute_state(self, query: str, memory_snapshot: list) -> torch.Tensor:
        """State = concat(query_embedding, mean(case_embeddings))"""
        query_emb = self.embed(query)
        if memory_snapshot:
            case_emb = torch.mean(
                torch.stack([self.embed(c["query"]) for c in memory_snapshot]),
                dim=0
            )
        else:
            case_emb = torch.zeros_like(query_emb)
        return torch.cat([query_emb, case_emb])

# Ключевые свойства M-MDP:
M_MDP_PROPERTIES = {
    "no_weight_updates": "LLM веса никогда не меняются",
    "online_learning": "система обучается в реальном времени на каждом запросе",
    "privacy_safe": "старые данные не нужно хранить (Q-values достаточно)",
    "scalable": "O(log N) поиск по памяти через ANN",
    "interpretable": "Q-values показывают какие cases полезны"
}
```

## Сравнение с альтернативами

```python
ADAPTATION_COMPARISON = {
    "Full Fine-tuning": {
        "catastrophic_forgetting": "★ (высокий риск)",
        "стоимость": "$$$$",
        "скорость_адаптации": "дни/недели",
        "alignment_risk": "высокий",
        "privacy": "требует сохранения данных"
    },
    "LoRA / QLoRA": {
        "catastrophic_forgetting": "★★★ (снижен)",
        "стоимость": "$$",
        "скорость_адаптации": "часы",
        "alignment_risk": "умеренный",
        "privacy": "требует сохранения данных"
    },
    "ROME / MEMIT": {
        "catastrophic_forgetting": "★★★★ (точечное редактирование)",
        "стоимость": "$",
        "скорость_адаптации": "минуты",
        "alignment_risk": "умеренный (side effects)",
        "privacy": "не требует"
    },
    "RAG (retrieval только)": {
        "catastrophic_forgetting": "★★★★★ (нет weights)",
        "стоимость": "$",
        "alignment_risk": "нет",
        "ограничение": "не обучается на прошлых ошибках"
    },
    "Memento (M-MDP)": {
        "catastrophic_forgetting": "★★★★★ (нет weights)",
        "стоимость": "$",
        "скорость_адаптации": "реальное время",
        "alignment_risk": "нет (веса заморожены)",
        "ключевое_преимущество": "Q-learning учит memory management"
    }
}
```

## Применение к Lorenzo

```python
# Lorenzo накапливает знания итерационно (раунды R01-R36).
# Memento паттерн: адаптивная LLM без переобучения

class LorenzoMementoAdapter:
    """
    Каждый раунд discovery добавляет новые проекты.
    Memento: новые знания → в case memory, не в fine-tuning.
    improve_llm_qa.py улучшается без обновления модели.
    """

    def add_new_round(self, round_projects: list[dict]):
        for project in round_projects:
            case = {
                "query": f"Расскажи о {project['name']}",
                "response": project["description"],
                "outcome": {"score": 1.0},  # новые данные = полезны
                "utility": 1.0
            }
            self.memory.add(case)
            # Q-learning обновит utility на основе реальных запросов
```

## Возможные комбинации

| Комбинация | Новое свойство |
|------------|----------------|
| **Memento + Cognitive Memory (R31)** | Episodic/semantic nodes + Q-learning управление utility = полноценная когнитивная память |
| **Memento + agent-memory-mcp (R01)** | MCP интерфейс к Memento memory → стандартный доступ для любых агентов |
| **Memento + HITL (R30)** | HITL feedback → reward signal для Q-learning обновления utility кейсов |
| **Memento + LangGraph (R35)** | MemorySaver в LangGraph → Memento M-MDP для умного управления историей |
| **Memento + Meta-Monitor (R29)** | Meta-Monitor оценивает качество ответов → reward для Memento Q-learner |

## Контакт

- Статья: https://habr.com/ru/articles/940824/ (август 2025)
- GitHub: https://github.com/Agent-on-the-Fly/Memento
- Soft Q-Learning: arxiv.org/abs/1702.08165 (Haarnoja et al.)
- Case-Based Reasoning: классический AI метод (Kolodner, 1993)
- Смежная (catastrophic forgetting для новичков): https://habr.com/ru/articles/846434/
- Смежная (инерция весов и subliminal learning): https://habr.com/ru/articles/987130/
