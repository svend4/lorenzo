---
date: 2026-05-15
tags: [memory, rag, orchestration, knowledge, ingestion]
state: normalized
---

# Resume Ranking в Росатоме: SmartAdaptPrecision@K, обнаружение bias, 78% vs 84% рекрутер

<!-- toc-auto -->
<!-- tags: ksidorov-rosatom-resume-ranking-smartadaptprecision-bias, docs -->


<!-- summary -->
> `ksidorov-rosatom-resume-ranking-smartadaptprecision-bias` — раздел документации проекта Lorenzo.


> [!WARNING]
> Документ содержит описание рисков и ограничений. Изучите их перед принятием архитектурных решений.

<!-- alert-added -->

**Автор:** ksidorov (Кирилл Сидоров, GreenAtom / Росатом)  
**Хабр:** https://habr.com/ru/companies/greenatom/articles/917546/  
**GitHub:** нет (production ML кейс)  
**Слой:** orchestration / analytics  
**Дата:** июнь 2025  
**Уникальность:** Production ML-кейс найма в Росатоме: путь от TF-IDF+XGBoost через BERT (E5/TinyBERT/BGE-M3/Siamese+Triplet Loss) до Tiny Sentence BERT + MLP + ONNX. Уникальная метрика SmartAdaptPrecision@K для fair ранжирования при ничьих исторических оценок. Задокументированные training biases: семейное положение завышало ранг, знание английского парадоксально снижало, "ОГУРЕЦ" получил неправильный вес. 78% accuracy vs 84% у рекрутеров домена и 70% у общих рекрутеров.

## Проблема: O(n) сложность и bias в историческом ранжировании

```
Росатом / GreenAtom: крупная госкорпорация, тысячи вакансий

Проблема масштаба:
  HR-специалист: просматривает N резюме для позиции
  Сложность: O(n) — каждое резюме требует полного просмотра
  При росте кандидатского потока → рекрутер перегружен

Проблема данных:
  Исторические данные = решения прошлых рекрутеров
  → Субъективность, неравномерное качество
  → Некоторые рекрутеры ставили одинаковую оценку разным кандидатам
  → Ничьи в исторических оценках → как обучать модель?

Проблема bias:
  Обнаружено при анализе обученных моделей:
  1. Семейное положение → завышало ранг (юридически нейтральный фактор)
  2. Знание английского → снижало ранг (парадокс: IT-позиции требуют английского!)
  3. "ОГУРЕЦ" (случайное слово) → получил значимый вес
  → Модель выучила noise из исторических данных
```

## Эволюция архитектур и кастомная метрика

```python
# ksidorov (GreenAtom/Росатом): Resume Ranking с fairness метрикой
# habr.com/ru/companies/greenatom/articles/917546/

from dataclasses import dataclass
from typing import Optional
import numpy as np

@dataclass
class Resume:
    """Резюме кандидата."""
    candidate_id: str
    raw_text: str          # исходный текст (может включать авиабилеты!)
    skills: list[str]
    experience_years: float
    education: str
    languages: list[str]
    family_status: str     # поле которое НЕЛЬЗЯ использовать для ранжирования


@dataclass
class Vacancy:
    """Вакансия."""
    position: str
    required_skills: list[str]
    description: str
    domain: str  # nuclear_physics | it | management | engineering


@dataclass
class RankingResult:
    """Результат ранжирования одного резюме."""
    candidate_id: str
    score: float           # 0-1 релевантность
    rank: int
    confidence: float
    unexpected_flag: bool  # модель неуверена → "неожиданный кандидат"


class SmartAdaptPrecision:
    """
    Кастомная метрика для fair оценки при ничьях.

    Проблема стандартного Precision@K:
    Если у 5 кандидатов одинаковая историческая оценка "4",
    то порядок между ними произвольный.
    При вычислении Precision@K: зависит от случайного порядка ничьих
    → Метрика нестабильна при обучении.

    SmartAdaptPrecision@K:
    Для каждого кандидата с ничьей → вычислить ВЕРОЯТНОСТЬ
    что он попадёт в топ-K при случайном порядке.
    Суммировать вероятности → аналитическое значение без случайности.

    Нормализовано в [0, 1] → интерпретируемо как precision.
    """

    def compute(self,
                 ranked_list: list[RankingResult],
                 relevance_scores: list[float],
                 k: int) -> float:
        """
        SmartAdaptPrecision@K: аналитический расчёт без случайности.

        ranked_list: предсказанный порядок модели
        relevance_scores: исторические оценки рекрутеров (могут быть ничьи)
        k: топ-K позиций
        """
        n = len(ranked_list)
        precision_sum = 0.0

        for i in range(k):
            candidate = ranked_list[i]
            candidate_score = relevance_scores[candidate.candidate_id]

            # Сколько кандидатов с такой же оценкой?
            tied_count = sum(1 for s in relevance_scores.values()
                              if s == candidate_score)

            # Сколько кандидатов с ЛУЧШЕЙ оценкой?
            better_count = sum(1 for s in relevance_scores.values()
                                if s > candidate_score)

            # Вероятность что этот кандидат попадёт в топ-K
            # при случайном разрешении ничьих
            remaining_slots = k - better_count
            if remaining_slots <= 0:
                p_in_top_k = 0.0
            elif remaining_slots >= tied_count:
                p_in_top_k = 1.0
            else:
                p_in_top_k = remaining_slots / tied_count

            precision_sum += p_in_top_k

        return precision_sum / k  # нормализация в [0, 1]


class ResumeRankingPipeline:
    """
    Эволюция архитектур от TF-IDF до Tiny Sentence BERT + MLP.

    Итерация 1: TF-IDF + XGBoost
      Быстро, интерпретируемо, но плохо понимает семантику.
      "Backend developer" ≠ "Python разработчик" для TF-IDF.

    Итерация 2: BERT-based (E5, TinyBERT, BGE-M3)
      Семантическое понимание → лучше.
      Проблема: тяжёлые модели → медленно для 1000+ резюме в день.

    Итерация 3: Siamese Networks + Triplet Loss
      Обучить: [vacancy, relevant_resume] > [vacancy, irrelevant_resume]
      Triplet Loss: d(anchor, pos) < d(anchor, neg) + margin
      Лучший precision для похожих вакансий.

    Итерация 4 (production): Tiny Sentence BERT + MLP + ONNX
      Маленький и быстрый (Tiny → CPU inference)
      MLP поверх embeddings для domain calibration
      ONNX export → deployment без PyTorch зависимости
    """

    # ONNX deployment: нет PyTorch в production
    INFERENCE_ENGINE = "ONNX Runtime"
    MONITORING = "ClearML"
    LOAD_TEST = "Locust"


class BiasDetector:
    """
    Обнаружение тренировочных bias в ранжировании.

    Метод: permutation feature importance на валидационном сете.
    Перемешать значения поля → если accuracy падает → поле важно.

    Три обнаруженных bias в Росатоме:
    """

    DISCOVERED_BIASES = [
        {
            "feature": "family_status",
            "problem": "Семейное положение завышало ранг некоторых кандидатов",
            "cause": "Исторический рекрутер предпочитал определённые статусы",
            "fix": "Удалить feature из модели; невалидный критерий найма"
        },
        {
            "feature": "english_language",
            "problem": "Знание английского СНИЖАЛО ранг → парадокс для IT",
            "cause": "В исторических данных: вакансии без требования EN + кандидаты с EN → не нанимали",
            "fix": "Включить уровень вакансии в контекст; сегментация по типу позиции"
        },
        {
            "feature": "random_tokens",
            "example": '"ОГУРЕЦ" получил значимый вес в feature importance',
            "cause": "Шум в исторических данных; несколько кандидатов с этим словом → нанятые",
            "fix": "Threshold на feature importance; min frequency filter"
        }
    ]

    def audit_features(self,
                        model,
                        validation_data,
                        sensitive_features: list[str]) -> dict:
        """
        Аудит модели на наличие bias.

        sensitive_features: поля нейтральные для найма
        (семейное положение, национальность, возраст)
        → должны иметь нулевую importance
        """
        importances = {}
        baseline_score = model.evaluate(validation_data)

        for feature in sensitive_features:
            # Перемешать значения поля → измерить падение accuracy
            permuted_data = self._permute_feature(validation_data, feature)
            permuted_score = model.evaluate(permuted_data)

            # Высокая разница → feature влияет → потенциальный bias
            importances[feature] = baseline_score - permuted_score

        bias_flags = {f: imp for f, imp in importances.items()
                       if abs(imp) > 0.02}  # threshold 2%
        return bias_flags


class UnexpectedCandidateFlag:
    """
    "Неожиданный кандидат": флаг неуверенности модели.

    Если модель даёт высокий score но confidence < threshold:
    → Флаг для HR: "Модель оценила высоко, но неуверена — проверьте вручную"

    Используется для:
    1. Нестандартный бэкграунд (смена отрасли)
    2. Нетипичный набор скиллов (редкая комбинация)
    3. Мало примеров в тренировочных данных (new job family)
    """

    THRESHOLD = 0.65  # confidence ниже → флаг "unexpected"

    def flag(self, result: RankingResult) -> bool:
        return result.score > 0.7 and result.confidence < self.THRESHOLD


BENCHMARK_RESULTS = {
    "датасет": "Реальные кандидаты Росатома (Skillaz, ~20 NoSQL таблиц)",
    "проблемы_данных": [
        "Неструктурированные резюме",
        "Прикреплённые авиабилеты вместо документов",
        "Исторические ничьи в оценках рекрутеров"
    ],
    "accuracy": {
        "модель": "78%",
        "рекрутер_домена": "84%",
        "рекрутер_общий": "70%",
        "вывод": "Модель превосходит среднего рекрутера на незнакомых вакансиях"
    },
    "стек": {
        "tracking": "ClearML",
        "inference": "ONNX Runtime",
        "load_test": "Locust",
        "data_source": "Skillaz (ATS)"
    },
    "модели_протестированы": [
        "TF-IDF + XGBoost",
        "multilingual-e5 (E5-large)",
        "TinyBERT",
        "BGE-M3",
        "Siamese Network + Triplet Loss",
        "Tiny Sentence BERT + MLP [ВЫБРАНА]"
    ]
}
```

## Применение к Lorenzo

```python
# Lorenzo: SmartAdaptPrecision для ранжирования карточек

class LorenzoFairRanking:
    """
    ksidorov паттерн для Lorenzo:
    SmartAdaptPrecision@K для ранжирования карточек с одинаковым collab_score.

    Проблема аналогична ничьям в резюме:
    Несколько карточек с collab_score=0.7 → какой порядок?
    Стандартный Recall@K нестабилен при ничьях.

    SmartAdaptPrecision@K:
    Аналитически вычислить вероятность что карточка
    с tied score попадёт в топ-K → стабильная метрика.

    Bias audit для Lorenzo:
    Проверить: не ли перекос в пользу карточек из последних раундов?
    (аналог временного bias в hiring)
    """
    pass
```

## Возможные комбинации

| Комбинация | Новое свойство |
|------------|----------------|
| **Resume Ranking + RAG Embedder Fine-Tuning (R50)** | Fine-tuned embedder для HR domain: deepvk/USER-bge-m3 + LoRA на корпусе резюме = лучше чем BGE-M3 general |
| **Resume Ranking + Behavioral Profiles (R50)** | Профиль рекрутера (строгий vs мягкий) → разный SmartAdaptPrecision@K threshold |
| **Resume Ranking + Agent Evaluation (R48)** | Golden Set для HR ranking: эталонные решения рекрутеров-экспертов для bias-free оценки модели |
| **Resume Ranking + LLM Observability (R45)** | Трейсинг: feature importance drifts over time → ранняя детекция новых bias при переобучении |
| **Resume Ranking + ЕГЭ репетитор (R51)** | Общий паттерн: оба проекта оценивают людей (кандидаты/студенты) с fairness ограничениями |

## Контакт

- Статья: https://habr.com/ru/companies/greenatom/articles/917546/ (июнь 2025)
- Автор: ksidorov (Кирилл Сидоров, GreenAtom / Росатом)
- Skillaz: skillaz.ru (ATS система)
- ClearML: clear.ml (ML experiment tracking)
- Siamese Networks + Triplet Loss: оригинальная статья (Schroff et al., 2015)
- BGE-M3: huggingface.co/BAAI/bge-m3
- Смежная (HR AI, R23): docs/06-discovery/round-23/
- Смежная (RAG Embedder Fine-Tuning, R50): docs/06-discovery/round-50/projects/huraligne-pgk-rag-embedder-finetuning-hard-negatives.md

## Смотрите также
- [Главная](../../../README.md)
- [Метрики](../../../METRICS.md)
- [Здоровье](../../../HEALTH.md)
- [Глоссарий](../../../GLOSSARY.md)
- [Сущности](../../../ENTITIES.md)
- [Решения](../../../DECISIONS.md)
