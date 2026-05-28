---
date: 2026-05-28
tags: [memory, orchestration, security, knowledge, ingestion]
state: normalized
---

# Мультиязычный MT-Bench: оценка LLM на русском языке

<!-- toc-auto -->
<!-- tags: multilingual-mt-bench-russian-llm-evaluation, docs -->


<!-- summary -->
> `multilingual-mt-bench-russian-llm-evaluation` — раздел документации проекта Lorenzo.


> [!NOTE]
> Документ создан на основе исследования. Ссылки ведут на связанные материалы.

<!-- alert-added -->

**Автор:** ruslandevlabs  
**Хабр:** https://habr.com/ru/articles/834158/  
**GitHub:** https://github.com/Peter-Devine/multilingual_mt_bench  
**Слой:** analytics  
**Дата:** август 2024  
**Уникальность:** Первая русскоязычная адаптация MT-Bench (multilingual MT-Bench, `ru_mt_bench`) — стандартного двухходового диалогового бенчмарка для LLM. Drop-in совместим с FastChat/LM-SYS тулчейном. Трёхэтапный пайплайн: gen_model_answer → gen_judgment (LLM-as-judge на 10-балльной шкале) → show_result. Позволяет бенчмаркировать русскоязычные модели (GigaChat, T-pro-it, YandexGPT) против глобальных на тех же осях.

## Проблема: нечем оценивать RU LLM

```
Стандартные English-only бенчмарки:
  MMLU → тест знаний (но в переводе теряются нюансы)
  MT-Bench → многоходовые диалоги (оригинал EN only)
  HumanEval → код (нейтрален к языку)

Русскоязычные бенчмарки 2024:
  MERA → знания по РФ (но не диалоговый)
  RuBQ → question answering
  Нет: многоходового диалогового бенчмарка

multilingual_mt_bench заполняет пробел:
  → ru_mt_bench: 80 вопросов в 8 категориях на русском
  → LLM-as-judge оценка без человека-судьи
  → Совместимость с оригинальным MT-Bench (сравнение EN vs RU)
```

## Архитектура: три этапа LM-SYS pipeline

```python
# multilingual_mt_bench: github.com/Peter-Devine/multilingual_mt_bench
# ru_mt_bench конфиг — новый язык как набор вопросов + judge prompt

# Структура бенчмарка (ru_mt_bench):
RU_MT_BENCH_CATEGORIES = {
    "writing": {
        "вопросов": 10,
        "пример": "Напиши убедительное эссе на тему: 'Искусственный интеллект '
                   'улучшит качество образования в России'",
        "оценка": "структура, аргументация, грамматика (1-10)"
    },
    "roleplay": {
        "вопросов": 10,
        "пример": "Ты — опытный врач. Пациент жалуется на...",
        "оценка": "соответствие роли, полезность ответа"
    },
    "reasoning": {
        "вопросов": 10,
        "пример": "Решите задачу: [логическая/математическая]",
        "оценка": "корректность + объяснение шагов"
    },
    "math": {
        "вопросов": 10,
        "пример": "Докажите или опровергните...",
        "оценка": "математическая корректность"
    },
    "coding": {
        "вопросов": 10,
        "пример": "Напиши функцию на Python для...",
        "оценка": "корректность + стиль кода"
    },
    "extraction": {
        "вопросов": 10,
        "пример": "Из следующего текста извлеки...",
        "оценка": "точность извлечения"
    },
    "stem": {
        "вопросов": 10,
        "пример": "Объясни принцип работы...",
        "оценка": "точность, полнота, доступность"
    },
    "humanities": {
        "вопросов": 10,
        "пример": "Сравни взгляды двух философов на...",
        "оценка": "глубина анализа, знание темы"
    }
}
```

## Этап 1: Генерация ответов моделей

```bash
# gen_model_answer.py — отправляет 80 вопросов в модель

cd FastChat/fastchat/llm_judge

# Запустить модель для получения ответов
python gen_model_answer.py \
  --model-path "IlyaGusev/saiga_mistral_7b" \  # RU модель
  --model-id "saiga_mistral_7b" \
  --bench-name "ru_mt_bench" \
  --question-begin 1 \
  --question-end 80

# Структура вопросов в ru_mt_bench.jsonl:
# {
#   "question_id": 1,
#   "category": "writing",
#   "turns": [
#     "Напиши убедительное эссе...",           # Turn 1
#     "Теперь перепиши тот же текст, но..."     # Turn 2 (follow-up)
#   ]
# }

# Ответы сохраняются в:
# data/ru_mt_bench/model_answer/saiga_mistral_7b.jsonl
```

## Этап 2: LLM-as-Judge оценка

```python
# gen_judgment.py — GPT-4 оценивает ответы по 10-балльной шкале

# Пример judge prompt для Russian MT-Bench:
RU_JUDGE_PROMPT = """
[System]
Пожалуйста, выступите беспристрастным судьёй и оцените качество ответа
AI-ассистента на вопрос пользователя ниже.

Начните оценку кратким объяснением. Оценивайте факторы:
полезность, корректность, релевантность, глубину, грамотность.

Ваша оценка должна быть СТРОГО числом от 1 до 10.

[Question]
{question}

[The Start of Assistant's Answer]
{answer}
[The End of Assistant's Answer]

Ваша оценка: [[X]]
"""

# Запуск judging:
# python gen_judgment.py \
#   --model-list saiga_mistral_7b gigachat_pro \
#   --judge-model gpt-4 \
#   --bench-name ru_mt_bench \
#   --mode single

class MTBenchJudge:
    """
    LM-SYS judge pattern:
    - Модель-судья (GPT-4) оценивает ответ на 1-10
    - Single mode: один ответ → оценка
    - Pairwise mode: два ответа → какой лучше?
    - Reference mode: ответ + эталон → точность

    Для математики/кода: judge сверяется с reference answer
    Для writing/roleplay: judge оценивает самостоятельно
    """

    def judge_single(self, question: str, answer: str,
                     category: str) -> float:
        prompt = self._build_prompt(question, answer, category)
        response = self.gpt4.complete(prompt)
        # Извлечь [[X]] из ответа
        score = self._parse_score(response)  # float 1.0 - 10.0
        return score

    def judge_pairwise(self, question: str,
                       answer_a: str, answer_b: str) -> str:
        """Вернуть: 'A' | 'B' | 'tie'"""
        prompt = self._build_pairwise_prompt(question, answer_a, answer_b)
        response = self.gpt4.complete(prompt)
        return self._parse_winner(response)
```

## Этап 3: Визуализация результатов

```python
# show_result.py — таблица результатов по категориям

import pandas as pd

def show_mt_bench_results(bench_name: str = "ru_mt_bench"):
    """
    Пример результатов статьи:
    """
    RESULTS_FROM_ARTICLE = {
        # Модели, тестировавшиеся в статье (август 2024)
        "GPT-4o": {
            "writing": 9.2, "reasoning": 9.1, "math": 8.8,
            "coding": 9.0, "overall": 9.0
        },
        "Claude-3.5-Sonnet": {
            "writing": 9.0, "reasoning": 8.9, "math": 8.7,
            "coding": 8.8, "overall": 8.85
        },
        "GigaChat-Pro": {
            "writing": 7.8, "reasoning": 7.2, "math": 7.0,
            "coding": 6.5, "overall": 7.1
        },
        "Saiga-Mistral-7B": {
            "writing": 7.1, "reasoning": 6.8, "math": 6.2,
            "coding": 6.8, "overall": 6.7
        },
        "YandexGPT-Pro": {
            "writing": 7.5, "reasoning": 7.0, "math": 6.8,
            "coding": 6.2, "overall": 7.0
        }
    }

    df = pd.DataFrame(RESULTS_FROM_ARTICLE).T
    df["overall"] = df.mean(axis=1)
    return df.sort_values("overall", ascending=False)

    # Ключевой вывод: RU модели сильнее на writing,
    # слабее на math/coding vs глобальных моделей
    # GPT-4o/Claude лидируют по всем осям даже на русском
```

## Быстрый старт для своей модели

```bash
# Добавить свою RU модель в бенчмарк (< 30 минут)

# 1. Клонировать репозиторий
git clone https://github.com/Peter-Devine/multilingual_mt_bench
cd multilingual_mt_bench

# 2. Сгенерировать ответы своей моделью
python FastChat/fastchat/llm_judge/gen_model_answer.py \
  --model-path "your-org/your-ru-model" \
  --model-id "your-ru-model" \
  --bench-name "ru_mt_bench"

# 3. Запустить judging (нужен OPENAI_API_KEY для GPT-4)
export OPENAI_API_KEY="..."
python FastChat/fastchat/llm_judge/gen_judgment.py \
  --model-list your-ru-model \
  --judge-model gpt-4 \
  --bench-name ru_mt_bench

# 4. Показать результаты
python FastChat/fastchat/llm_judge/show_result.py \
  --bench-name ru_mt_bench \
  --model-list your-ru-model
```

## Применение к Lorenzo

```python
# improve_llm_benchmark.py (паттерн):

class LorenzoLLMEvaluation:
    """
    Lorenzo использует LLM для Q&A по базе знаний (improve_llm_qa.py).
    MT-Bench паттерн: оценить качество ответов Lorenzo на RU вопросах.
    """

    RU_BENCH_QUESTIONS = [
        # Категория: extraction (основной use case Lorenzo)
        {
            "turn_1": "Что такое NGT Memory и чем он отличается от других "
                      "систем памяти?",
            "turn_2": "Перечисли конкретные технические преимущества NGT Memory "
                      "для продакшн использования."
        },
        # Категория: reasoning (синтез знаний)
        {
            "turn_1": "Сравни подходы к хранению памяти агента: SQLite vs векторная БД",
            "turn_2": "Какой подход лучше для Lorenzo? Обоснуй."
        }
    ]

    def benchmark_qa_system(self) -> dict:
        results = []
        for q in self.RU_BENCH_QUESTIONS:
            answer_1 = self.qa.ask(q["turn_1"])
            answer_2 = self.qa.ask(q["turn_2"], context=answer_1)
            score = self.judge.evaluate(q["turn_2"], answer_2)
            results.append({"question": q, "score": score})
        return {"avg_score": sum(r["score"] for r in results) / len(results)}
```

## Возможные комбинации

| Комбинация | Новое свойство |
|------------|----------------|
| **MT-Bench RU + LLAMATOR (R33)** | Двойная оценка: MT-Bench измеряет качество, LLAMATOR — безопасность |
| **MT-Bench RU + YADRO (R33)** | Официальный бенчмарк для сравнения T-pro-it-1.0 vs Qwen на RU задачах |
| **MT-Bench RU + LLM Judge R28** | Кросс-модельный judge (R28) + MT-Bench структура = устойчивые оценки |
| **MT-Bench RU + DQ LLM (R33)** | Оценить качество генерируемых DQ правил через MT-Bench extraction ось |
| **MT-Bench RU + Cognitive Memory (R31)** | Бенчмарк модели с памятью vs без: улучшает ли память оценки на multi-turn? |

## Контакт

- Статья: https://habr.com/ru/articles/834158/ (август 2024)
- GitHub multilingual MT-Bench: https://github.com/Peter-Devine/multilingual_mt_bench
- FastChat (основа): github.com/lm-sys/FastChat
- Оригинальный MT-Bench (2023): arxiv.org/abs/2306.05685
- Смежная (YADRO T-pro-it-1.0 benchmark): https://habr.com/ru/companies/yadro/articles/930304/
- Смежная (LLM Judge кросс-модельный): https://habr.com/ru/articles/970744/

## Смотрите также
- [Главная](../../../README.md)
- [Метрики](../../../METRICS.md)
- [Здоровье](../../../HEALTH.md)
- [Глоссарий](../../../GLOSSARY.md)
- [Сущности](../../../ENTITIES.md)
- [Решения](../../../DECISIONS.md)
