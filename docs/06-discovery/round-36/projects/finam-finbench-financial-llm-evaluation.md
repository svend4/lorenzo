---
date: 2026-06-05
tags: [memory, rag, orchestration, security, knowledge]
state: normalized
---

# FinBench: финансовые бенчмарки для LLM от Финама

<!-- toc-auto -->
<!-- tags: finam-finbench-financial-llm-evaluation, docs -->


<!-- summary -->
> `finam-finbench-financial-llm-evaluation` — раздел документации проекта Lorenzo.


> [!WARNING]
> Документ содержит описание рисков и ограничений. Изучите их перед принятием архитектурных решений.

<!-- alert-added -->

**Автор:** Finam_Broker (Лаборатории ИИ «Финама»)  
**Хабр:** https://habr.com/ru/companies/finam_broker/articles/989842/  
**GitHub:** https://github.com/FinamAILab/Finam-FinBench_public  
**Слой:** analytics  
**Дата:** январь 2025  
**Уникальность:** Первые domain-specific финансовые бенчмарки для LLM на русском языке: вопросы из профессиональных экзаменов CFA L1-3, CMT L2 и российских финансовых олимпиад. LLM-as-Judge методология с агрегацией рангов. Выявлен ключевой gap: модели, специализированные на практических задачах, уступают на классических финансовых бенчмарках. Открытый датасет + код оценки на GitHub.

## Проблема: общие бенчмарки не измеряют финансовые навыки

```
Стандартные LLM бенчмарки:
  MMLU → академические знания (есть финансовые вопросы, но мало)
  MT-Bench → диалоговые задачи
  HumanEval → код

Результат: хорошая модель по MMLU ≠ хорошая модель для трейдинга

Реальные задачи финансового аналитика:
  → Анализ 10-K / МСФО отчётов
  → CFA-уровень рассуждений о рисках
  → Понимание деривативов и структурных продуктов
  → Регуляторные вопросы (ЦБ РФ, ФСФР)

FinBench заполняет пробел:
  → CFA L1-3 вопросы: portfolio theory, fixed income, derivatives
  → CMT L2: technical analysis, market microstructure
  → RU финансовые олимпиады: российская специфика
  → LLM-as-Judge: не просто right/wrong, а качество объяснения
```

## Структура бенчмарка: три источника вопросов

```python
# github.com/FinamAILab/Finam-FinBench_public
# Структура датасета

FINBENCH_STRUCTURE = {
    "CFA_Level_1": {
        "количество_вопросов": 450,
        "темы": [
            "Ethical and Professional Standards",
            "Quantitative Methods",
            "Economics",
            "Financial Reporting and Analysis",
            "Corporate Finance",
            "Equity Investments",
            "Fixed Income",
            "Derivatives",
            "Alternative Investments",
            "Portfolio Management"
        ],
        "тип": "multiple choice (4 варианта)",
        "язык": "EN → адаптированные на RU"
    },
    "CFA_Level_2": {
        "количество_вопросов": 180,
        "формат": "vignette-based (кейс + вопросы)",
        "сложность": "применение концепций к реальным сценариям"
    },
    "CFA_Level_3": {
        "количество_вопросов": 90,
        "формат": "essay-style + constructed response",
        "сложность": "portfolio management, risk assessment"
    },
    "CMT_Level_2": {
        "количество_вопросов": 150,
        "темы": ["Technical Analysis", "Market Microstructure",
                 "Quantitative Methods for Trading"],
        "уникальность": "технический анализ — редко в LLM бенчмарках"
    },
    "RU_Financial_Olympiad": {
        "количество_вопросов": 200,
        "источник": "Всероссийская олимпиада по финансам и экономике",
        "покрытие": ["налоговое право РФ", "банковское регулирование ЦБ РФ",
                     "российский фондовый рынок (MOEX)"]
    }
}
```

## LLM-as-Judge: оценка качества объяснений

```python
import pandas as pd
from openai import OpenAI

class FinancialLLMJudge:
    """
    Трёхэтапная оценка: правильность + качество объяснения + уверенность.
    NaN фильтрация + агрегация рангов по доменам.
    """

    JUDGE_PROMPT = """
Ты — опытный финансовый аналитик с квалификацией CFA.
Оцени ответ модели на финансовый вопрос.

Вопрос: {question}
Правильный ответ: {correct_answer}
Ответ модели: {model_answer}

Оцени по 5 критериям (каждый 1-10):
1. Корректность: правильный ли ответ?
2. Объяснение: понимает ли модель ЧТО и ПОЧЕМУ?
3. Глубина: использует ли финансовые концепции правильно?
4. Практичность: применимо ли в реальной торговле/анализе?
5. Регуляторная точность: соответствует ли нормативной базе?

Верни JSON:
{{"correctness": X, "explanation": X, "depth": X,
  "practicality": X, "regulatory": X, "comment": "..."}}
"""

    def evaluate_model(self, model_name: str,
                       benchmark: pd.DataFrame) -> pd.DataFrame:
        results = []
        for _, row in benchmark.iterrows():
            # Получить ответ оцениваемой модели
            model_answer = self.query_model(model_name, row["question"])

            # Judge оценивает
            scores = self._judge(
                question=row["question"],
                correct_answer=row["answer"],
                model_answer=model_answer
            )

            results.append({
                "model": model_name,
                "domain": row["domain"],
                "question_id": row["id"],
                **scores
            })

        return pd.DataFrame(results)

    def aggregate_rankings(self, all_results: pd.DataFrame) -> pd.DataFrame:
        """
        Агрегация рангов по доменам:
        1. Фильтрация NaN (модель отказалась отвечать)
        2. Ранжирование внутри каждого домена
        3. Средний ранг как итоговая метрика
        """
        # Фильтр NaN — важно! Некоторые модели отказываются от финансовых вопросов
        clean = all_results.dropna(subset=["correctness", "explanation"])

        # Ранжирование по доменам
        rankings = []
        for domain in clean["domain"].unique():
            domain_data = clean[clean["domain"] == domain]
            domain_scores = domain_data.groupby("model")["correctness"].mean()
            domain_ranks = domain_scores.rank(ascending=False)
            rankings.append(domain_ranks.rename(domain))

        return pd.concat(rankings, axis=1)
```

## Результаты: gap между общими и специализированными моделями

```python
# Ключевые находки из статьи (январь 2025):

FINBENCH_RESULTS = {
    "общий_рейтинг": {
        # модели, которые хорошо на общих бенчмарках
        "GPT-4o":            {"cfa_avg": 7.8, "cmt": 6.9, "ru_olympiad": 7.2},
        "Claude-3.5-Sonnet": {"cfa_avg": 7.6, "cmt": 7.1, "ru_olympiad": 6.8},
        "Gemini-1.5-Pro":    {"cfa_avg": 7.3, "cmt": 6.7, "ru_olympiad": 6.5},
    },

    "финансово_специализированные": {
        # Модели, дообученные на финансовых данных
        "FinGPT-v3.3":       {"cfa_avg": 6.2, "cmt": 6.8, "ru_olympiad": 5.1},
        # ← парадокс: специализированная модель ХУЖЕ на классическом CFA
    },

    "российские_модели": {
        "GigaChat-Pro":      {"cfa_avg": 6.1, "cmt": 5.8, "ru_olympiad": 7.4},
        # ← лидер на RU олимпиаде, но отстаёт на EN-based CFA
        "YandexGPT-Pro":     {"cfa_avg": 5.9, "cmt": 5.5, "ru_olympiad": 7.0},
    },

    "ключевой_вывод": (
        "1. GPT-4o / Claude лидируют даже на финансовых задачах "
        "без специализации. "
        "2. FinGPT (fine-tuned on финансовые новости) ХУЖЕ GPT-4o на CFA "
        "— знание новостей ≠ понимание финансовой теории. "
        "3. GigaChat лучший на RU-специфике (российские реалии). "
        "4. CMT (технический анализ) — самая сложная категория для всех."
    )
}
```

## Как добавить свою модель в бенчмарк

```bash
# github.com/FinamAILab/Finam-FinBench_public

git clone https://github.com/FinamAILab/Finam-FinBench_public
cd Finam-FinBench_public

# Структура:
# data/
#   cfa_level1.jsonl    # вопросы CFA L1
#   cfa_level2.jsonl    # вопросы CFA L2
#   cmt_level2.jsonl    # вопросы CMT L2
#   ru_olympiad.jsonl   # RU олимпиада
# evaluation/
#   judge.py            # LLM-as-Judge
#   aggregate.py        # агрегация рангов
#   run_benchmark.py    # основной скрипт

# Запустить оценку своей модели:
python evaluation/run_benchmark.py \
  --model "your-model-name" \
  --api-url "http://localhost:8000/v1" \
  --domains cfa_level1 cfa_level2 ru_olympiad \
  --judge-model "gpt-4o"

# Результат: ваша модель в сравнении с лидербордом
```

## Применение к Lorenzo

```python
# Lorenzo базируется на технических документах Хабра.
# FinBench паттерн: бенчмарк качества ответов Lorenzo QA системы

class LorenzoQABenchmark:
    """
    Аналог FinBench для Lorenzo:
    Проверить improve_llm_qa.py на специализированных вопросах
    о проектах из базы знаний.
    """

    BENCHMARK_QUESTIONS = [
        {"q": "Что такое NGT Memory и как работает HNSW индекс?",
         "expected_concepts": ["HNSW", "NGT", "approximate nearest neighbor"]},
        {"q": "Сравни Yodoca и agent-memory-mcp по архитектуре памяти",
         "expected_concepts": ["episodic", "semantic", "MCP", "SQLite"]},
    ]

    def evaluate_qa_system(self) -> float:
        correct = 0
        for q in self.BENCHMARK_QUESTIONS:
            answer = self.qa.ask(q["q"])
            coverage = sum(1 for c in q["expected_concepts"] if c in answer)
            correct += coverage / len(q["expected_concepts"])
        return correct / len(self.BENCHMARK_QUESTIONS)
```

## Возможные комбинации

| Комбинация | Новое свойство |
|------------|----------------|
| **FinBench + MT-Bench RU (R34)** | Финансовая ось в MT-Bench: специализированный evaluation pipeline |
| **FinBench + LLAMATOR (R33)** | Red-teaming финансовых моделей: безопасность + качество в одном фреймворке |
| **FinBench + FinPDF pipeline (R32)** | Тестировать FinPDF LLM анализ через FinBench вопросы по извлечённым данным |
| **FinBench + LLM Judge R28** | Кросс-модельный judge для финансовых вопросов: устранение self-preference |
| **FinBench + DBRM (R31)** | DBRM паттерн: иерархические метрики для финансовых LLM (точность + объяснение) |

## Контакт

- Статья: https://habr.com/ru/companies/finam_broker/articles/989842/ (январь 2025)
- GitHub: https://github.com/FinamAILab/Finam-FinBench_public
- Finam AI Lab: finam.ru
- CFA Institute: cfainstitute.org
- Смежная (Finam LLM трейдинг, торговые сигналы): https://habr.com/ru/companies/finam_broker/ (R26)
- Смежная (AML риски CatBoost, ЦБ РФ): https://habr.com/ru/companies/t2/articles/875286/

## Смотрите также
- [Главная](../../../README.md)
- [Метрики](../../../METRICS.md)
- [Здоровье](../../../HEALTH.md)
- [Глоссарий](../../../GLOSSARY.md)
- [Сущности](../../../ENTITIES.md)
- [Решения](../../../DECISIONS.md)
