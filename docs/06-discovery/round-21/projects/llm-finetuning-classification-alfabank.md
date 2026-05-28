---
date: 2026-05-28
tags: [memory, rag, orchestration, ingestion, architecture]
state: normalized
---

# LLM для текстовой классификации — лабораторная работа Альфа-Банка

<!-- toc-auto -->
<!-- tags: llm-finetuning-classification-alfabank, docs -->


<!-- summary -->
> Автор: команда Альфа-Банк (ML-инженеры) Хабр: https://habr.com/ru/companies/alfa/articles/968176/
Хабр: https://habr.com/ru/companies/alfa/articles/968176/  
GitHub: не опубликован (внутренняя разработка, методика описана полностью)  
Слой: knowledge / ingestion / orchestration  
Дата: 2025  
Уникальность


> [!WARNING]
> Документ содержит описание рисков и ограничений. Изучите их перед принятием архитектурных решений.

<!-- alert-added -->

**Автор:** команда Альфа-Банк (ML-инженеры)  
**Хабр:** https://habr.com/ru/companies/alfa/articles/968176/  
**GitHub:** не опубликован (внутренняя разработка, методика описана полностью)  
**Слой:** knowledge / ingestion / orchestration  
**Дата:** 2025  
**Уникальность:** Практическая «лабораторная работа» от ML-команды крупного банка: fine-tuning LLM для нестандартных задач классификации на русскоязычных данных. Включает: выбор базовой модели (Qwen vs LLaMA vs BERT), оценку данных для fine-tuning (500–10K примеров в зависимости от сложности), метрики оценки. Прямой ответ на вопрос «когда LLM лучше BERT для классификации?»

## Задача: нестандартная классификация

```
Стандартная классификация:
  «Определи тональность отзыва» → BERT справляется отлично

Нестандартная (Альфа-Банк):
  «Определи: жалоба ли это на обслуживание ИЛИ вопрос о продукте ИЛИ техническая проблема»
  + учёт контекста: предыдущие сообщения, канал (чат/звонок/email)
  + русский язык со сленгом и опечатками
  + новые категории появляются каждый квартал
        ↓
BERT: переобучать при каждой новой категории
LLM: описать новую категорию в промпте → работает сразу (few-shot)
```

## Когда LLM > BERT для классификации

```
BERT выигрывает:
  ✅ Данных много (>10K примеров)
  ✅ Категории стабильные
  ✅ Нужна скорость (<50ms)
  ✅ Нет GPU → BERT на CPU нормально

LLM выигрывает:
  ✅ Данных мало (<500 примеров)
  ✅ Категории меняются часто
  ✅ Сложный контекст (многоходовой диалог)
  ✅ Нужны объяснения классификации
  ✅ Нестандартные классы ("намерение клиента", "эмоциональный тон")
```

## Выбор базовой модели (эксперимент Альфа-Банка)

```
Тест на русскоязычном корпусе банка (нестандартная классификация):

Qwen 2.5 7B (fine-tuned):
  F1: 0.89 | Скорость: 120ms | RAM: 14GB | 🏆

LLaMA 3.1 8B (fine-tuned):
  F1: 0.87 | Скорость: 135ms | RAM: 16GB

ruBERT-large (fine-tuned):
  F1: 0.84 | Скорость: 45ms  | RAM: 1.2GB (но меньше гибкость)

GigaChat (API, few-shot):
  F1: 0.82 | Скорость: 2000ms | RAM: 0 (API)

GPT-4o (API, few-shot):
  F1: 0.91 | Скорость: 3000ms | RAM: 0 (но дорого + ПД уходят)

Победитель: Qwen 2.5 7B fine-tuned
  = лучший баланс quality/speed/cost для локального деплоя
```

## Данные для fine-tuning: сколько нужно

```
Тип задачи                    Минимум    Оптимум    Примечание
─────────────────────────────────────────────────────────────
Простая классификация          500       1 000      2-5 категорий
Сложная классификация         1 000      3 000      5-15 категорий
Domain adaptation             2 000      5 000      специфичный язык
Instruction following         3 000     10 000      точное следование
Нестандартные задачи          1 500      5 000      банковский случай
```

**Ключевой вывод**: 500-1000 качественных примеров дают 80-90% от полного датасета.

## Pipeline fine-tuning Альфа-Банка

```python
# 1. Подготовка данных
dataset = [
    {
        "instruction": "Классифицируй обращение клиента.",
        "input": "Почему у меня списали 500 рублей без объяснений?",
        "output": "ЖАЛОБА | Тема: списание | Срочность: высокая"
    },
    ...  # 2000 размеченных примеров
]

# 2. Fine-tuning через Unsloth (из R15)
from unsloth import FastLanguageModel
model, tokenizer = FastLanguageModel.from_pretrained(
    model_name="Qwen/Qwen2.5-7B-Instruct",
    max_seq_length=2048,
    load_in_4bit=True,  # QLoRA
)
model = FastLanguageModel.get_peft_model(model, r=16, lora_alpha=32)

# 3. Training (< 3 часа на RTX 3090)
trainer = SFTTrainer(model=model, dataset=dataset, ...)
trainer.train()

# 4. Inference
result = model.generate("Классифицируй: " + customer_text)
# → "ЖАЛОБА | Тема: списание | Срочность: высокая"
```

## Structured Output для классификации

```python
# Проблема: LLM иногда генерирует неправильный формат категории
# Решение: structured output (паттерн из SGLang R19)

from pydantic import BaseModel
from enum import Enum

class Category(str, Enum):
    COMPLAINT = "ЖАЛОБА"
    QUESTION = "ВОПРОС"
    TECHNICAL = "ТЕХНИЧЕСКАЯ_ПРОБЛЕМА"

class ClassificationResult(BaseModel):
    category: Category
    topic: str
    urgency: int  # 1-5
    reasoning: str  # объяснение (для аудита)

# С structured output: всегда валидный JSON, можно парсить автоматически
```

## Метрики оценки

```
Не только accuracy:
  F1 micro/macro — баланс по классам
  Cohen's kappa  — согласие с человеком-разметчиком
  Confusion matrix — где путается (важно для банка)
  Latency p95     — 95-й перцентиль (критично для SLA)
  
A/B тест:
  Контрольная группа: старые правила → ошибок 12%
  Экспериментальная: LLM → ошибок 6%
  Улучшение: -50% ошибок классификации
```

## Применение к Lorenzo

Lorenzo использует `improve_reclassify.py` (TF-IDF рубрикация).  
Fine-tuned LLM = следующий уровень:

```python
# improve_reclassify_llm.py (не существует, паттерн):
# Размечаем 1000 правильных классификаций из существующих docs/
# Fine-tune Qwen2.5-7B на этих примерах
# Результат: классификация учитывает Svyazi-контекст, не только TF-IDF

# Benefit:
# - новые секции (round-XX) → автоматически правильно рубрицируются
# - понимает "агент + память" → class orchestration (не keyword matching)
```

## Возможные комбинации

| Комбинация | Новое свойство |
|------------|----------------|
| **Alfa Classification + Fine-tuning (R15)** | Unsloth QLoRA pipeline → Lorenzo-специфичная классификация |
| **Alfa Classification + Synthetic Data (R18)** | Distilabel генерирует 2000+ обучающих примеров автоматически |
| **Alfa Classification + Jay Guard (R21)** | ПД в клиентских текстах → анонимизация → классификация |
| **Alfa Classification + FRIDA (R18)** | FRIDA embeddings как features для классификатора |
| **Alfa Classification + RAG Eval (R16)** | RAGAS оценивает: точность классификации в CI |

## Контакт

- Статья: https://habr.com/ru/companies/alfa/articles/968176/ (2025)
- Смежная (Desmond doc review, тот же банк): https://habr.com/ru/companies/alfa/articles/932058/
- Unsloth (fast fine-tuning): github.com/unslothai/unsloth (Apache 2.0)
- Qwen2.5: github.com/QwenLM/Qwen2.5 (Apache 2.0)
- ruBERT: huggingface.co/ai-forever/ruBERT-large

## Смотрите также
- [Главная](../../../README.md)
- [Метрики](../../../METRICS.md)
- [Здоровье](../../../HEALTH.md)
- [Глоссарий](../../../GLOSSARY.md)
- [Сущности](../../../ENTITIES.md)
