---
date: 2026-05-28
tags: [memory, rag, orchestration, knowledge, ingestion]
state: normalized
---

# FREED++: Ускорение де ново генерации молекул через исправление багов RL-фреймворка

<!-- toc-auto -->
<!-- tags: alexandertelepov-freed-plus-plus-drug-discovery-rl-gnn, docs -->


<!-- summary -->
> `alexandertelepov-freed-plus-plus-drug-discovery-rl-gnn` — раздел документации проекта Lorenzo.


> [!WARNING]
> Документ содержит описание рисков и ограничений. Изучите их перед принятием архитектурных решений.

<!-- alert-added -->

**Автор:** AlexanderTelepov (Александр Телепов, AIRI — AI Research Institute)  
**Хабр:** https://habr.com/ru/companies/airi/articles/842534/  
**GitHub:** github.com/AIRI-Institute/FFREED  
**Слой:** analytics / knowledge  
**Дата:** сентябрь 2024  
**Уникальность:** Оригинальное исследование AIRI: автор нашёл и исправил критические баги в NeurIPS 2021 FREED фреймворке (critic получал распределения вероятностей вместо embeddings точек присоединения → сломанное обучение), создал два улучшения: FFREED (только фиксы) и FREED++ (упрощённая архитектура). GNN + actor-critic RL для de novo генерации молекул-лекарств: автоматическое построение молекулы шаг за шагом через выбор фрагментов и точек присоединения. 8.5× speedup, 22× снижение памяти. Тестирование на 6 белках-мишенях vs 3 в оригинале.

## Проблема: de novo генерация молекул с гарантированным связыванием

```
Drug Discovery традиционный путь:
  → Скрининг 10^6-10^9 молекул из библиотек
  → Годы + миллиарды долларов
  → Большинство кандидатов не связываются с мишенью

De Novo молекулярная генерация:
  → Генерировать молекулы "с нуля" под конкретную мишень
  → Оптимизировать docking score (прокси связывания с белком)
  → Автоматически находить кандидаты без ручного скрининга

FREED (NeurIPS 2021):
  → Actor-critic RL + GNN для генерации молекул
  → Строит молекулу шаг за шагом: выбор фрагмента + точки присоединения
  → Проблема: три критических бага → плохое обучение

FREED++ (AlexanderTelepov, AIRI):
  → Нашёл баги через тщательный анализ кода
  → Исправил + упростил архитектуру
  → 8.5× speedup, 22× меньше памяти
  → Тестирование на 6 белках-мишенях (vs 3 в оригинале)
```

## Архитектура FREED++ и найденные баги

```python
# AlexanderTelepov (AIRI): FREED++ — de novo drug discovery
# habr.com/ru/companies/airi/articles/842534/
# github.com/AIRI-Institute/FFREED

from dataclasses import dataclass
from typing import Optional
import numpy as np

@dataclass
class Molecule:
    """
    Молекула в процессе построения.

    FREED строит молекулы инкрементально:
    1. Начать с seed-атома/фрагмента
    2. Выбрать точку присоединения (attachment point)
    3. Выбрать фрагмент для присоединения
    4. Выбрать конфигурацию (bond type, 3D geometry)
    5. Повторить до готовности
    """
    smiles: str                      # SMILES нотация молекулы
    attachment_points: list[int]     # индексы атомов для расширения
    graph_embedding: np.ndarray      # GNN embedding текущей молекулы
    docking_score: Optional[float]   # связывание с белком (ниже = лучше)
    is_complete: bool = False


@dataclass
class ProteinTarget:
    """Белок-мишень для drug discovery."""
    pdb_id: str           # PDB база данных (структура белка)
    binding_site: dict    # координаты и размеры кармана связывания
    docking_engine: str   # "gnina" | "vina" | "rdock"


# ===== КРИТИЧЕСКИЕ БАГИ ОРИГИНАЛЬНОГО FREED =====

class FREEDBug1_CriticInput:
    """
    Баг #1 (самый критический): Critic получает не то что должен.

    Оригинальный FREED:
      Actor выбирает action = (attachment_point_idx, fragment_idx)
      Critic должен оценивать: насколько хорош этот выбор?

    Что должен получать Critic:
      embedding точки присоединения (реальный вектор признаков атома)

    Что реально получал Critic в оригинальном коде:
      probability distribution над attachment points (softmax output)
      → Critic видел вероятности ВЫБОРА, а не характеристики ТОЧКИ
      → Critic не мог научиться оценивать химическую осмысленность
      → Обучение было фундаментально сломано

    FREED++ fix:
      critic_input = attachment_point_embedding  # реальный embedding
      # вместо: critic_input = action_probabilities
    """

    @staticmethod
    def broken_original(action_probs: np.ndarray) -> float:
        """Оригинал: critic получает вероятности (НЕПРАВИЛЬНО)."""
        # critic(softmax_output) → бессмысленная оценка
        return critic_network(action_probs)  # BUG: probs != embeddings

    @staticmethod
    def fixed_freed_plus_plus(attachment_point_embedding: np.ndarray) -> float:
        """FREED++: critic получает embedding точки (ПРАВИЛЬНО)."""
        return critic_network(attachment_point_embedding)


class FREEDBug2_EmbeddingDim:
    """
    Баг #2 + архитектурное упрощение FREED++.

    Оригинальный FREED:
      Объединял embeddings через мультипликативное взаимодействие
      → Embedding dimension взрывался до 1024
      → Огромная память, медленное обучение

    FREED++ решение:
      Заменить мультипликацию на конкатенацию + линейный слой
      dim: 1024 → ~128 (зависит от конфига)
      → 22× меньше памяти
      → Сопоставимое или лучшее качество (меньше переобучение)
    """

    ORIGINAL_DIM = 1024  # multiplicative interaction → взрыв размерности
    FREED_PLUS_PLUS_DIM = 128  # concatenation + linear → компактно


class FREEDPlusPlusAgent:
    """
    FREED++ actor-critic агент для генерации молекул.

    GNN обрабатывает текущую молекулу как граф:
    → Узлы = атомы (тип, заряд, гибридизация)
    → Рёбра = связи (одиночная, двойная, ароматическая)

    На каждом шаге агент выбирает:
    1. Attachment point: какой атом молекулы расширять
    2. Fragment: какой химический фрагмент добавить
    3. Configuration: bond type + 3D конфигурация

    Actor: выбирает действие (жадно или sampling)
    Critic: оценивает ценность состояния для обновления actor
    """

    def select_action(self, molecule: Molecule,
                       fragment_library: list[str]) -> dict:
        """
        Выбрать следующее действие по построению молекулы.

        Returns:
            {
              "attachment_point": int,  # индекс атома-якоря
              "fragment": str,           # SMILES фрагмента
              "bond_type": str,          # "SINGLE" | "DOUBLE" | "AROMATIC"
            }
        """
        # GNN → embedding текущей молекулы
        mol_embedding = self.gnn.encode(molecule)

        # Actor head: вероятности над точками присоединения
        attachment_probs = self.actor_attachment(mol_embedding)
        attachment_idx = attachment_probs.argmax()

        # FREED++ FIX: embedding точки присоединения (не probs!)
        attachment_embedding = mol_embedding[attachment_idx]  # ПРАВИЛЬНО

        # Critic оценивает embedding точки
        value = self.critic(attachment_embedding)

        # Actor head: вероятности над фрагментами
        fragment_probs = self.actor_fragment(
            mol_embedding,
            attachment_embedding
        )
        fragment_idx = fragment_probs.argmax()

        return {
            "attachment_point": attachment_idx.item(),
            "fragment": fragment_library[fragment_idx],
            "value_estimate": value.item()
        }

    def compute_reward(self, molecule: Molecule,
                        target: ProteinTarget) -> float:
        """
        Награда = docking score (proxy для связывания с белком).

        Docking score < 0 → молекула связывается (лучше = меньше)
        Нормализуем в [0, 1] для стабильного RL обучения.

        Валидация на PDBbind/DUD-E: Spearman r > 0.7 с экспериментальными данными.
        """
        docking = self._run_docking(molecule, target)  # gnina/vina
        # Нормализация: типичный диапазон [-12, -4] kcal/mol
        normalized_reward = (docking - (-4)) / ((-12) - (-4))
        return float(np.clip(normalized_reward, 0, 1))


BENCHMARK_RESULTS = {
    "датасет": "6 белков-мишеней (vs 3 в оригинальном FREED)",
    "белки_мишени": [
        "CDK2 (киназа клеточного цикла)",
        "EGFR (онкология)",
        "GSK3β",
        "JNK3",
        "p38α",
        "VEGFR2"
    ],
    "baseline_сравнение": [
        "REINVENT (Рекуррентная сеть + RL)",
        "MolDQN (Q-learning на молекулах)",
        "Pocket2Mol (E(3)-equivariant GNN)"
    ],
    "метрики": {
        "docking_score": "FREED++ лучше REINVENT/MolDQN на всех 6 мишенях",
        "spearman_correlation": "> 0.7 с экспериментальными данными (PDBbind/DUD-E)",
        "arxiv": "https://arxiv.org/abs/2401.09840v1",
        "journal": "Submitted to TMLR (Transactions on ML Research)"
    },
    "инженерные_улучшения": {
        "speedup": "8.5× vs оригинальный FFREED",
        "memory_reduction": "22× (embedding dim 1024→128)",
        "time_per_step": "~0.3-0.4s (batch=100) vs ~2.5s у FFREED"
    }
}

FOUND_BUGS = [
    {
        "bug": "Critic получал probability distributions вместо attachment point embeddings",
        "severity": "КРИТИЧЕСКИЙ — фундаментально сломанное обучение critic",
        "fix": "Передавать реальный embedding точки присоединения"
    },
    {
        "bug": "Multiplicative interaction → embedding dim 1024",
        "severity": "PERFORMANCE — избыточная память",
        "fix": "Concatenation + linear layer → dim 128, 22× меньше памяти"
    },
    {
        "bug": "Тестирование только на 3 белках (FREED оригинал)",
        "severity": "ОЦЕНКА — ограниченный бенчмарк",
        "fix": "Расширен до 6 белков-мишеней для более надёжных выводов"
    }
]
```

## Применение к Lorenzo

```python
# Lorenzo: FREED++ паттерн для поиска оптимальных комбинаций проектов

class LorenzoMolecularAnalogy:
    """
    AlexanderTelepov паттерн для Lorenzo:
    Аналогия: de novo генерация "молекул знания".

    Вместо молекулы → комбинация проектов Lorenzo
    Вместо белка-мишени → целевая задача ("агент с памятью")
    Вместо docking score → collab_score (насколько хорошо проекты сочетаются)

    Actor-critic для поиска комбинаций:
    Attachment point = место соединения двух проектов
    Fragment = новый проект для добавления в ансамбль
    Reward = collab_score ансамбля из improve_collab_finder.py

    Но в первую очередь: бенчмарк FREED++ полезен для Lorenzo
    как пример "найти и исправить баги в чужом коде через тщательный анализ"
    — то же что debug cycle в скриптах Lorenzo.
    """
    pass
```

## Возможные комбинации

| Комбинация | Новое свойство |
|------------|----------------|
| **FREED++ + SR-Scientist (R50)** | SR-Scientist открывает законы связывания молекул; FREED++ генерирует молекулы по этим законам — полный цикл drug discovery |
| **FREED++ + Agent Evaluation (R48)** | Golden Set для drug discovery агента: эталонные трассы генерации известных одобренных препаратов |
| **FREED++ + Temporal KG (R47)** | Темпоральный граф: как меняется docking score молекулы при итеративном добавлении фрагментов |
| **FREED++ + LLM Observability (R45)** | Трейсинг: visualize actor-critic convergence curves + какие фрагменты агент выбирает чаще |
| **FREED++ + Coordination Harness (R46)** | Несколько FREED++-агентов ищут молекулы параллельно → coordination harness собирает лучших кандидатов |

## Контакт

- Статья: https://habr.com/ru/companies/airi/articles/842534/ (сентябрь 2024)
- Автор: AlexanderTelepov (Александр Телепов, AIRI — AI Research Institute)
- GitHub: github.com/AIRI-Institute/FFREED
- arXiv: https://arxiv.org/abs/2401.09840v1
- FREED оригинал (NeurIPS 2021): github.com/AITRICS/FREED
- AIRI: airi.net (российский AI исследовательский институт)
- Docking engine: gnina (gnina.github.io) / AutoDock Vina
- Смежная (SR-Scientist законы, R50): docs/06-discovery/round-50/projects/andre-dataist-sr-scientist-llm-law-discovery-symbolic-regression.md
- Смежная (LLM для науки, R36): docs/06-discovery/round-36/

## Смотрите также
- [Главная](../../../README.md)
- [Метрики](../../../METRICS.md)
- [Здоровье](../../../HEALTH.md)
- [Глоссарий](../../../GLOSSARY.md)
- [Сущности](../../../ENTITIES.md)
- [Решения](../../../DECISIONS.md)
