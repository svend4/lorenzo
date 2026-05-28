---
date: 2026-05-28
tags: [rag, orchestration, security, architecture, anthropic]
state: normalized
---

# Построение AI агентов в медицине: DBRM и иерархическая оценка

<!-- toc-auto -->
<!-- tags: raft-medical-ai-agents-dbrm, docs -->


<!-- summary -->
> Явное соответствие российским требованиям к медицинским данным + Cohen's Kappa для мониторинга согласованности судей.


> [!WARNING]
> Документ содержит описание рисков и ограничений. Изучите их перед принятием архитектурных решений.

<!-- alert-added -->

**Автор:** Squirrelfm (Игорь Новиков), Raft (Ярославль, AI-решения для бизнеса)  
**Хабр:** https://habr.com/ru/companies/raft/articles/960388/  
**GitHub:** не опубликован (производственная архитектура)  
**Слой:** orchestration / analytics  
**Дата:** октябрь 2025  
**Уникальность:** Медицинские AI-агенты с Dynamic Behavior Reward Model (DBRM): вместо стандартного RAG — иерархические метрики качества (безопасность, полезность, полнота, релевантность) через LLM-судей, откалиброванных на данных врачей. Явное соответствие российским требованиям к медицинским данным + Cohen's Kappa для мониторинга согласованности судей.

## Почему медицинский AI — не обычный RAG

```
Стандартный RAG в медицине:
  → Инструкции обновляются постоянно (новые исследования, guidelines)
  → Knowledge graph + re-ranking не решает проблему
  → Врач vs LLM: "правильный" ответ определяет только клинический контекст
  → Ошибка стоит жизни → нужна новая архитектура оценки

DBRM-подход (Raft):
  Вместо → "это похоже на источник?" (RAG)
  Задать → "это безопасно? полезно? полно? релевантно?" (DBRM)
  Оценить → через специализированных LLM-судей, калиброванных на врачах
```

## Dynamic Behavior Reward Model: архитектура

```python
# Иерархическая система оценки медицинских ответов AI

class MedicalDBRM:
    """
    Dynamic Behavior Reward Model для медицины.
    Вместо скалярной награды — многомерная оценка по клинически значимым осям.
    """

    EVALUATION_DIMENSIONS = {
        "safety": {
            "описание": "Не причинит ли ответ вреда пациенту?",
            "вес": 0.40,  # наивысший приоритет
            "пороговое_значение": 0.90,  # ниже → автоматический отказ
            "калибровка": "врачи-аннотаторы: «этот ответ безопасен для пациента?»"
        },
        "usefulness": {
            "описание": "Помогает ли ответ решить клиническую задачу?",
            "вес": 0.25,
            "пороговое_значение": 0.70,
            "калибровка": "врачи: «я бы использовал это в практике?»"
        },
        "completeness": {
            "описание": "Охвачены ли все важные аспекты клинического случая?",
            "вес": 0.20,
            "пороговое_значение": 0.65,
            "калибровка": "стандарты клинических руководств по подпунктам"
        },
        "relevance": {
            "описание": "Соответствует ли ответ запросу и контексту?",
            "вес": 0.15,
            "пороговое_значение": 0.70,
            "калибровка": "пара запрос-ответ из реальных консультаций"
        }
    }

    def evaluate(self, query: str, response: str,
                 patient_context: dict) -> DBRMScore:
        scores = {}
        for dim, config in self.EVALUATION_DIMENSIONS.items():
            # Специализированный LLM-судья для каждого измерения
            judge = self.judge_pool.get_judge(dim)
            score = judge.score(
                query=query,
                response=response,
                context=patient_context,
                rubric=self.rubrics[dim]
            )
            scores[dim] = score

        # Взвешенная агрегация
        weighted = sum(
            scores[dim] * config["вес"]
            for dim, config in self.EVALUATION_DIMENSIONS.items()
        )

        # Проверка пороговых значений (hard constraints)
        violations = [
            dim for dim, config in self.EVALUATION_DIMENSIONS.items()
            if scores[dim] < config["пороговое_значение"]
        ]

        return DBRMScore(
            weighted_score=weighted,
            dimension_scores=scores,
            threshold_violations=violations,
            is_safe=len(violations) == 0
        )
```

## Пул LLM-судей: кластеризация по категориям

```python
class MedicalJudgePool:
    """
    Не один судья на всё — пул специализированных судей по категориям.
    Оптимизация: скорость × стоимость × точность.
    """

    JUDGE_CLUSTERS = {
        "терапия": {
            "модель": "fine-tuned-llm/therapy-safety-v2",
            "специализация": ["кардиология", "эндокринология", "гастроэнтерология"],
            "размер": "8B",  # малая модель → быстро, дёшево
        },
        "хирургия": {
            "модель": "fine-tuned-llm/surgery-eval-v1",
            "специализация": ["общая хирургия", "ортопедия", "нейрохирургия"],
            "размер": "13B",  # больший контекст для сложных случаев
        },
        "педиатрия": {
            "модель": "fine-tuned-llm/pediatrics-safety-v1",
            "специализация": ["все педиатрические случаи"],
            "размер": "8B",
            "note": "Отдельная модель: весовые коэффициенты safety выше (0.55)"
        },
        "экстренная помощь": {
            "модель": "fine-tuned-llm/emergency-eval-v3",
            "специализация": ["скорая помощь", "реанимация", "токсикология"],
            "размер": "70B",  # критически важно → используем большую модель
            "latency_sla_ms": 300  # быстрый ответ критичен
        }
    }

    def get_judge(self, category: str) -> LLMJudge:
        cluster = self.route_to_cluster(category)
        return self.load_judge(self.JUDGE_CLUSTERS[cluster])
```

## Начальная разметка: Bootstrap → Scale

```python
class EvaluationBootstrap:
    """
    Проблема: нет готовой ground truth для медицинских ответов.
    Решение: начать с врачей → масштабировать через синтетику + RLAIF.
    """

    def build_ground_truth(self, n_initial: int = 500) -> GroundTruthDataset:
        # Шаг 1: Врачи аннотируют ~500 пар вопрос-ответ
        physician_annotations = self.annotate_with_physicians(
            pairs=self.sample_real_consultations(n_initial),
            dimensions=list(MedicalDBRM.EVALUATION_DIMENSIONS.keys()),
            n_physicians_per_pair=3  # majority vote
        )

        # Шаг 2: Проверка согласованности (Cohen's Kappa)
        kappa_scores = {}
        for dim in MedicalDBRM.EVALUATION_DIMENSIONS:
            kappa = self.cohen_kappa(
                annotations=physician_annotations[dim],
                n_annotators=3
            )
            kappa_scores[dim] = kappa

            if kappa < 0.6:
                # Недостаточное согласие → пересмотреть рубрику
                print(f"WARNING: Low agreement for '{dim}': κ={kappa:.2f}")
                print("Requires rubric clarification with medical experts")

        # Шаг 3: Калибровка LLM-судей на размеченных данных
        calibrated_judges = self.calibrate_judges(physician_annotations)

        # Шаг 4: Масштабирование через синтетические данные
        synthetic = self.generate_synthetic_cases(
            based_on=physician_annotations,
            n_synthetic=5000
        )

        return GroundTruthDataset(
            real=physician_annotations,
            synthetic=synthetic,
            kappa_scores=kappa_scores
        )
```

## Мониторинг согласованности судей в production

```python
# Longitudinal impact measurement — отслеживание качества в динамике

class DBRMProductionMonitor:

    def track_judge_consistency(self, time_window_days: int = 30):
        """
        Судьи могут дрейфовать со временем (model updates, distribution shift).
        Регулярная проверка Cohen's Kappa между судьями.
        """
        traces = self.trace_store.get_recent(days=time_window_days)

        for dim in MedicalDBRM.EVALUATION_DIMENSIONS:
            # Выборка случаев где несколько судей оценивали одно и то же
            multi_judge_cases = [
                t for t in traces
                if len(t.judge_scores[dim]) > 1
            ]

            if len(multi_judge_cases) < 100:
                continue  # Недостаточно данных

            kappa = self.compute_kappa(multi_judge_cases, dim)

            if kappa < 0.65:
                self.alert(
                    f"Judge drift detected for '{dim}': κ={kappa:.2f}. "
                    f"Recalibration required."
                )

    def measure_clinical_outcomes(self):
        """
        Итоговое измерение: влияние AI на клинические результаты.
        """
        return {
            "engagement": self.measure_physician_adoption_rate(),
            "clinical_outcomes": self.measure_patient_outcome_delta(),
            "economic": self.measure_time_saved_per_consultation()
        }
```

## Российская регуляторная специфика

```python
RUSSIAN_MEDICAL_COMPLIANCE = {
    "ФЗ-323": {
        "статья": "Федеральный закон 'Об основах охраны здоровья граждан в РФ'",
        "требования_к_AI": [
            "AI не ставит диагноз — только ассистирует врачу",
            "Финальное решение остаётся за лицензированным специалистом",
            "История запросов хранится и логируется (audit trail)",
            "Данные пациентов не покидают российские серверы (152-ФЗ)"
        ]
    },

    "152-ФЗ": {
        "статья": "Федеральный закон 'О персональных данных'",
        "требования": [
            "Медицинские данные = специальная категория ПДн",
            "Обработка только с явного согласия пациента",
            "Локализация: серверы в РФ",
            "Право на удаление данных"
        ]
    },

    "архитектурные_следствия": {
        "on_premise": "Модели развёртываются в контуре клиники (нет облачного API)",
        "anonymization": "Перед передачей судьям → деперсонализация",
        "audit_log": "Каждый запрос к LLM логируется с timestamp и user_id",
        "human_in_the_loop": "Обязательное подтверждение врача для рекомендаций"
    }
}
```

## Применение к Lorenzo

Lorenzo + DBRM-паттерн для оценки качества ответов:

```python
# improve_qa_dbrm.py (паттерн):

class LorenzoKnowledgeQAEvaluator:
    """
    Вместо одной метрики "ответ похож на источник" — многомерная оценка.
    Адаптация DBRM для Lorenzo knowledge base Q&A.
    """

    DIMENSIONS = {
        "accuracy":    {"вес": 0.35, "вопрос": "Фактически верно?"},
        "coverage":    {"вес": 0.25, "вопрос": "Охвачены все аспекты?"},
        "relevance":   {"вес": 0.25, "вопрос": "Отвечает на вопрос?"},
        "conciseness": {"вес": 0.15, "вопрос": "Нет лишней воды?"},
    }

    def evaluate_qa_response(self, question: str,
                              answer: str, sources: list) -> QAScore:
        scores = {
            dim: self.llm_judge.score(question, answer, sources, dim)
            for dim in self.DIMENSIONS
        }
        return QAScore(
            weighted=sum(s * self.DIMENSIONS[d]["вес"]
                        for d, s in scores.items()),
            dimensions=scores
        )
```

## Возможные комбинации

| Комбинация | Новое свойство |
|------------|----------------|
| **DBRM + HITL (R30)** | LLM-судьи оценивают → если safety < 0.9 → автоматический HITL checkpoint |
| **DBRM + LLM Judge (R28)** | Cross-model судья для медицины: evaluator ≠ семейство генератора |
| **DBRM + Conversational AI (R31)** | Многотёрновый медицинский диалог с DBRM-оценкой каждого хода |
| **DBRM + Meta-Monitor (R29)** | Meta-Monitor видит падение safety_score → эскалация уровня HITL |
| **DBRM + Synthetic Data (R30)** | DBRM-отбор синтетики: только сэмплы, прошедшие все пороги |

## Контакт

- Статья: https://habr.com/ru/companies/raft/articles/960388/ (октябрь 2025)
- Raft: raft.ru (AI-решения для бизнеса, Ярославль)
- Смежная (ИИ-ассистент врача, речь+NLP): https://habr.com/ru/articles/915330/
- Смежная (Оксфорд, LLM в медицине): https://habr.com/ru/companies/bothub/news/907072/
- RLAIF (Constitutional AI): anthropic.com/research/constitutional-ai

## Смотрите также
- [Главная](../../../README.md)
- [Метрики](../../../METRICS.md)
- [Здоровье](../../../HEALTH.md)
- [Глоссарий](../../../GLOSSARY.md)
- [Сущности](../../../ENTITIES.md)
- [Решения](../../../DECISIONS.md)
