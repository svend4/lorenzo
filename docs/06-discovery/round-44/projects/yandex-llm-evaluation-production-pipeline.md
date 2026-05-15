---
date: 2026-05-15
tags: [rag, knowledge, ingestion, architecture, self-improve]
state: normalized
---

# Yandex: production pipeline оценки LLM — от бенчмарков до LLM-as-judge

<!-- toc-auto -->
<!-- tags: yandex-llm-evaluation-production-pipeline, docs -->


<!-- summary -->
> `yandex-llm-evaluation-production-pipeline` — раздел документации проекта Lorenzo.


> [!WARNING]
> Документ содержит описание рисков и ограничений. Изучите их перед принятием архитектурных решений.

<!-- alert-added -->

**Автор:** ibarskaya (Яндекс)  
**Хабр:** https://habr.com/ru/companies/yandex/articles/861084/  
**GitHub:** нет (внутренняя система Яндекс)  
**Слой:** analytics  
**Дата:** ноябрь 2024  
**Уникальность:** Полное описание реальной production-системы оценки LLM (YandexGPT) на трёх уровнях: статические бенчмарки → Chatbot Arena → LLM-as-judge (GPT-4o). Ключевые находки: стилистическая предвзятость (пользователи предпочитают длинные структурированные ответы вне зависимости от качества) и утечка бенчмарков. Многоступенчатая воронка аннотации: предобучение → фильтрация оценщиков → разметка AI-тренерами → финальная разметка.

## Проблема: как измерить качество LLM в production

```
Задача: оценить YandexGPT и новые версии модели
  → Статические бенчмарки: быстро, но prone to leakage
  → Human evaluation: дорого, медленно, непоследовательно
  → A/B тесты: реальные пользователи, но долго + риск для метрик

Три уровня оценки в Яндекс:
  1. Статические бенчмарки — скрининг кандидатов (быстро)
  2. Chatbot Arena — сравнительная оценка (люди выбирают лучший ответ)
  3. LLM-as-judge — масштабируемая автоматическая оценка (GPT-4o)

Ключевые проблемы обнаруженные в процессе:
  → Стилистическая предвзятость: длинный + структурированный ≠ качественный
  → Утечка бенчмарков: модели обучаются на тестовых данных
  → Непоследовательность оценщиков: без калибровки ~ 60% agreement
```

## Многоступенчатая воронка оценки

```python
# Yandex: Production LLM Evaluation Pipeline
# habr.com/ru/companies/yandex/articles/861084

from dataclasses import dataclass, field
from typing import Optional
from enum import Enum

class EvaluationStage(Enum):
    STATIC_BENCHMARK = "static_benchmark"
    CHATBOT_ARENA = "chatbot_arena"
    LLM_AS_JUDGE = "llm_as_judge"
    HUMAN_EXPERT = "human_expert"


@dataclass
class EvaluationResult:
    model_name: str
    stage: EvaluationStage
    score: float
    metadata: dict = field(default_factory=dict)


class YandexLLMEvaluationPipeline:
    """
    Production-система оценки LLM в Яндекс.

    Воронка: бенчмарки → Arena → LLM-judge → решение о деплое.
    Каждый уровень фильтрует кандидатов для следующего.
    """

    # Статические бенчмарки для быстрого скрининга
    STATIC_BENCHMARKS = {
        "MERA": {
            "description": "Russian: 21 task benchmark (Сбер/MERA)",
            "cost": "low",
            "risk": "medium",  # leakage risk для RU датасетов
            "use_for": "Первичный скрининг новых чекпоинтов"
        },
        "MMLU": {
            "description": "English: 57 subject areas",
            "cost": "low",
            "risk": "high",  # широко известен, leakage вероятен
            "use_for": "Бейзлайн для сравнения с мировыми моделями"
        },
        "ruBQ": {
            "description": "Russian: question answering over Wikidata",
            "cost": "low",
            "risk": "low",
            "use_for": "Русскоязычные фактологические вопросы"
        },
        "Chatbot Arena Leaderboard": {
            "description": "ELO-рейтинг из реальных сравнений",
            "cost": "high",
            "risk": "low",
            "use_for": "Финальный benchmark для публичного позиционирования"
        }
    }

    def stage1_static_benchmark(self,
                                  model,
                                  benchmarks: list[str]) -> dict[str, float]:
        """
        Быстрый скрининг: прогнать модель на стандартных датасетах.
        Если модель не превосходит предыдущую версию → не двигаемся дальше.
        """
        results = {}
        for benchmark_name in benchmarks:
            score = self._run_benchmark(model, benchmark_name)
            results[benchmark_name] = score

            # Проверить на утечку: cosine similarity с train set
            leakage_score = self._check_benchmark_leakage(model, benchmark_name)
            if leakage_score > 0.8:
                results[f"{benchmark_name}_leakage_warning"] = leakage_score

        return results

    def stage2_chatbot_arena(self,
                              model_a,
                              model_b,
                              n_comparisons: int = 500) -> dict:
        """
        Chatbot Arena: пользователи выбирают лучший ответ из двух моделей (blind).
        Результат: ELO-рейтинг, win/loss/tie статистика.

        Ключевая находка: стилистическая предвзятость.
        Более длинный и структурированный ответ побеждает в 67% случаев
        вне зависимости от фактической точности.
        """
        comparisons = []
        for _ in range(n_comparisons):
            query = self._sample_query()

            response_a = model_a.generate(query)
            response_b = model_b.generate(query)

            # Blind comparison: пользователь не знает какая модель
            winner = self._human_judge(query, response_a, response_b)
            comparisons.append({
                "query": query,
                "winner": winner,
                "response_a_length": len(response_a),
                "response_b_length": len(response_b),
                "response_a_has_markdown": "##" in response_a or "- " in response_a,
                "response_b_has_markdown": "##" in response_b or "- " in response_b,
            })

        # Анализ предвзятости
        style_bias = self._analyze_style_bias(comparisons)
        elo = self._compute_elo(comparisons)

        return {
            "elo_model_a": elo["model_a"],
            "elo_model_b": elo["model_b"],
            "style_bias": style_bias,  # насколько длина/структура влияет на победу
            "comparisons": comparisons
        }

    def stage3_llm_as_judge(self,
                              model,
                              eval_set: list[dict],
                              judge_model: str = "gpt-4o") -> dict:
        """
        LLM-as-judge: GPT-4o оценивает ответы YandexGPT.
        Масштабируемая альтернатива human evaluation.

        Проблема: style bias переносится на LLM-judge!
        GPT-4o также предпочитает длинные структурированные ответы.
        Решение: explicit rubrics + calibration на human-annotated примерах.
        """
        scores = []
        for item in eval_set:
            query = item["query"]
            response = model.generate(query)
            reference = item.get("reference_answer")

            judge_prompt = self._build_judge_prompt(
                query, response, reference,
                rubrics=self.JUDGE_RUBRICS
            )

            judgment = self._call_judge(judge_model, judge_prompt)
            scores.append({
                "query": query,
                "score": judgment["score"],
                "reasoning": judgment["reasoning"],
                "criteria_scores": judgment["criteria_scores"]
            })

        return {
            "mean_score": sum(s["score"] for s in scores) / len(scores),
            "distribution": self._score_distribution(scores),
            "weak_criteria": self._find_weak_criteria(scores)
        }

    # Рубрики для LLM-judge (явные критерии вместо общей оценки)
    JUDGE_RUBRICS = {
        "factual_accuracy": {
            "weight": 0.35,
            "description": "Фактическая точность: проверяемые утверждения верны"
        },
        "completeness": {
            "weight": 0.25,
            "description": "Полнота: ответ покрывает ключевые аспекты запроса"
        },
        "relevance": {
            "weight": 0.20,
            "description": "Релевантность: ответ отвечает на заданный вопрос"
        },
        "clarity": {
            "weight": 0.20,
            "description": "Ясность: понятно, без лишней воды"
            # NOTE: clarity ≠ длина; длинный ≠ ясный
        }
    }
```

## Многоступенчатая аннотация данных

```python
class MultiStageAnnotationPipeline:
    """
    Воронка создания обучающих данных для оценки.

    Этапы:
    1. Предобучение оценщиков: калибровка на gold-примерах
    2. Фильтрация: оставить оценщиков с agreement > 75%
    3. AI-тренеры: профессиональные аннотаторы с LLM-помощью
    4. Финальная разметка: эксперты проверяют спорные случаи
    """

    ANNOTATION_STAGES = [
        {
            "stage": "calibration",
            "description": "Оценщики размечают 50 gold-примеров с известным ответом",
            "filter": "inter_annotator_agreement > 0.75",
            "output": "Откалиброванный пул оценщиков"
        },
        {
            "stage": "ai_assisted_annotation",
            "description": "AI-тренеры + LLM для первичного предложения оценки",
            "tools": ["GigaChat черновик оценки", "Интерфейс подтверждения/отклонения"],
            "output": "Быстрая разметка с контролем качества"
        },
        {
            "stage": "expert_review",
            "description": "Эксперты проверяют случаи с низким agreement",
            "threshold": "agreement < 0.6 → expert review",
            "output": "Финальная разметка"
        }
    ]

    def filter_assessors(self, assessors: list,
                          calibration_set: list[dict]) -> list:
        """
        Оставить только оценщиков с inter-annotator agreement > 75%.
        Без калибровки → agreement ~60% → высокий шум в данных.
        """
        qualified = []
        for assessor in assessors:
            assessor_scores = assessor.annotate(calibration_set)
            agreement = self._compute_agreement(assessor_scores,
                                                  calibration_set)
            if agreement > 0.75:
                qualified.append(assessor)
        return qualified

    def detect_style_bias_in_annotations(self,
                                          annotations: list[dict]) -> dict:
        """
        Проверить: не оценивают ли аннотаторы стиль вместо качества.
        Признаки: корреляция оценки с длиной или наличием markdown.
        """
        length_correlation = self._pearson_correlation(
            [a["response_length"] for a in annotations],
            [a["score"] for a in annotations]
        )

        markdown_bias = self._point_biserial(
            [a["has_markdown"] for a in annotations],
            [a["score"] for a in annotations]
        )

        return {
            "length_correlation": length_correlation,
            "markdown_bias": markdown_bias,
            "bias_detected": length_correlation > 0.3 or markdown_bias > 0.2,
            "recommendation": (
                "Добавить explicit rubric 'краткость ценится'"
                if length_correlation > 0.3 else "OK"
            )
        }


BENCHMARK_LEAKAGE_ANALYSIS = {
    "проблема": "Модели могут быть обучены на тестовых данных бенчмарков",
    "признаки": [
        "Резкий рост на конкретном бенчмарке без роста на других",
        "Высокое сходство промптов бенчмарка с обучающим корпусом",
        "Ответы содержат шаблоны специфичные для датасета"
    ],
    "метрики_детекции": {
        "embedding_similarity": "cosine(train_set, benchmark) > 0.8",
        "perplexity_drop": "PPL на бенчмарке << PPL на похожих данных",
        "n_gram_overlap": "4-gram overlap train/test > 15%"
    },
    "решение": [
        "Динамические бенчмарки (SWE-MERA, обновляются ежемесячно)",
        "Hold-out тестовые сеты не публикуемые до финальной оценки",
        "Мониторинг аномальных скачков метрик"
    ]
}
```

## Ключевые выводы

```python
EVALUATION_FINDINGS = {
    "стилистическая_предвзятость": {
        "факт": "Длинные структурированные ответы побеждают в Arena в 67% случаев",
        "причина": "Пользователи воспринимают структуру как признак качества",
        "следствие": "Модели могут оптимизировать стиль, а не содержание",
        "решение": [
            "Blind evaluation скрывающая длину",
            "Separate rubrics: стиль отдельно от точности",
            "A/B тесты с контролем длины"
        ]
    },

    "утечка_бенчмарков": {
        "факт": "Рост на MERA не всегда коррелирует с реальным улучшением",
        "масштаб": "До 20% скора может быть от memorization",
        "решение": "Ротация тестовых датасетов + динамические бенчмарки"
    },

    "llm_as_judge_ограничения": {
        "gpt4o_также_предвзят": "GPT-4o предпочитает длинные ответы (style bias)",
        "self_enhancement": "Модели семейства GPT предпочитают GPT-стиль ответов",
        "решение": "Calibration на human-labeled примерах + explicit rubrics"
    },

    "production_рекомендации": [
        "Не полагаться на один бенчмарк",
        "Всегда проверять на leakage перед публикацией",
        "LLM-as-judge: добавлять рубрики явно, калибровать на human data",
        "Arena: размечать предвзятость оценщиков перед запуском"
    ]
}

SYSTEM_PROFILE = {
    "организация": "Яндекс (YandexGPT team)",
    "статус": "Production (внутренняя система, не open-source)",
    "модель": "YandexGPT (все версии)",
    "judge_модель": "GPT-4o (внешний)",

    "воронка_этапов": [
        "Статические бенчмарки → скрининг (дни)",
        "Chatbot Arena → сравнительная оценка (недели)",
        "LLM-as-judge → масштабирование (часы)",
        "Human expert → финальное решение о деплое"
    ],

    "инфраструктура_аннотации": {
        "оценщики": "Пул с калибровкой (agreement > 75%)",
        "инструменты": "AI-assisted annotation (LLM черновик + human подтверждение)",
        "размер": "Тысячи размеченных примеров на задачу"
    }
}
```

## Применение к Lorenzo

```python
# Lorenzo: Yandex evaluation паттерн для оценки качества docs/

class LorenzoDocEvaluationPipeline:
    """
    Yandex паттерн для Lorenzo:
    Трёхуровневая оценка качества базы знаний.
    Вместо YandexGPT → docs/; вместо Arena → review_queue.py.
    """

    def stage1_static_metrics(self, doc_path: str) -> dict:
        """
        Статические метрики: readability, completeness, broken links.
        Аналог статических бенчмарков.
        """
        return {
            "readability": self._flesch_kincaid(doc_path),
            "completeness": self._check_required_sections(doc_path),
            "link_health": self._check_links(doc_path)
        }

    def stage2_review_queue(self, doc_path: str) -> dict:
        """
        Review Queue UI (review_queue.py):
        Пользователь сравнивает два варианта карточки → выбирает лучший.
        Аналог Chatbot Arena.
        """
        return self._load_from_review_queue(doc_path)

    def stage3_llm_judge(self, doc_path: str) -> dict:
        """
        improve_llm_qa.py с рубриками:
        LLM оценивает документ по явным критериям.
        Аналог LLM-as-judge.
        """
        rubrics = {
            "technical_accuracy": 0.40,
            "actionability": 0.30,    # можно ли воспроизвести
            "uniqueness": 0.30        # не дублирует ли другие docs/
        }
        return self._llm_evaluate(doc_path, rubrics)
```

## Возможные комбинации

| Комбинация | Новое свойство |
|------------|----------------|
| **Yandex Eval + LOCK-R (R43)** | Blind Judge архитектура + рубрики для устранения style bias в Arena |
| **Yandex Eval + LangFuse (R38)** | Трейсинг каждой оценки: какой промпт дал консистентный результат |
| **Yandex Eval + SWE-MERA (R41)** | Динамический бенчмарк + style-bias-free оценка = честный рейтинг |
| **Yandex Eval + RAG чанкинг (R43)** | RAGAS метрики + Yandex-стиль LLM-judge = полный RAG evaluation stack |
| **Yandex Eval + Lorenzo Gateway** | /api/ask с self-evaluation: каждый ответ автоматически оценивается |

## Контакт

- Статья: https://habr.com/ru/companies/yandex/articles/861084/ (ноябрь 2024)
- Автор: ibarskaya (Яндекс, команда YandexGPT)
- Chatbot Arena: lmarena.ai (LMSYS)
- Смежная (LOCK-R CoT парадокс, R43): docs/06-discovery/round-43/projects/lockr-cot-paradox-bayesian-reasoning-benchmark.md
- Смежная (LangFuse наблюдаемость, R38): docs/06-discovery/round-38/
- MERA benchmark: mera.a-ai.ru

## Смотрите также
- [Главная](../../../README.md)
- [Метрики](../../../METRICS.md)
- [Здоровье](../../../HEALTH.md)
- [Глоссарий](../../../GLOSSARY.md)
- [Сущности](../../../ENTITIES.md)
- [Решения](../../../DECISIONS.md)
