---
date: 2026-05-29
tags: [memory, rag, knowledge, ingestion, architecture]
state: normalized
---

# EduLLM-RU: дообучение LLM для задач российских учителей за $400

<!-- toc-auto -->
<!-- tags: edullm-ru-finetuning-teachers-craft, docs -->


<!-- summary -->
> EduLLM-RU: дообучение LLM для задач российских учителей за $400 — раздел документации проекта Lorenzo.
 
 
 
>   — раздел документации проекта Lorenzo.


> [!NOTE]
> Документ создан на основе исследования. Ссылки ведут на связанные материалы.

<!-- alert-added -->

**Автор:** daniel_ivanov  
**Хабр:** https://habr.com/ru/articles/1026516/  
**GitHub:** https://github.com/csylabs-org/edubench-ru  
**Слой:** analytics  
**Дата:** апрель 2025  
**Уникальность:** End-to-end pipeline fine-tuning Qwen3.5-27B через QLoRA+Unsloth по методологии CRAFT (ACL 2025): 30 000 синтетических QA пар из реальных педагогических seed данных (MMLU-RU, MERA, gsm8k-ru, планы уроков) через Claude и Gemini Batch API. EduLLM-RU: rank #9 из 30 моделей, на уровне GPT-5.4 на образовательных задачах. Стоимость: $400 за 6 часов на H200. 152-ФЗ compliance: данные студентов не покидают инфраструктуру.

## Проблема: глобальные LLM не знают российскую педагогику

```
Задачи российских учителей:
  → Генерация вариантов контрольных (разного уровня сложности)
  → Адаптация учебных материалов под уровень класса
  → Подготовка к ОГЭ/ЕГЭ (российские стандарты)
  → Отчёты в формате ФГОС (Федеральный государственный стандарт)

Проблема с глобальными моделями:
  OpenAI/Anthropic → данные учеников уходят за рубеж → 152-ФЗ нарушение
  GPT-4 → не знает ФГОС, ОГЭ/ЕГЭ специфику
  → Нужна локальная суверенная модель, обученная на RU педагогике

Решение:
  QLoRA fine-tuning Qwen3.5-27B → EduLLM-RU
  Стоимость: ~30 000 руб ($400) за 6 часов обучения на H200
  Результат: rank #9/30, на уровне GPT-5.4 на педагогических задачах
```

## CRAFT методология: синтетические данные из реальных

```python
# CRAFT: Corpus Retrieval and Augmented Fine-Tuning (ACL 2025)
# Ключевая идея: использовать большие LLM для генерации
# обучающих данных для меньших локальных LLM

class CRAFTDataPipeline:
    """
    Шаг 1: Собрать seed корпус (реальные педагогические данные)
    Шаг 2: Claude/Gemini генерируют 30K QA пар из seed данных
    Шаг 3: Фильтрация + валидация качества
    Шаг 4: QLoRA fine-tuning Qwen3.5-27B
    """

    SEED_SOURCES = {
        "MMLU-RU": {
            "описание": "57 академических предметов на русском",
            "размер": "~15K вопросов с ответами",
            "педагогическая_ценность": "фактические знания"
        },
        "MERA": {
            "описание": "Russian LLM Evaluation benchmark",
            "размер": "~9 задач, тысячи примеров",
            "педагогическая_ценность": "reasoning, знания о России"
        },
        "gsm8k-ru": {
            "описание": "Математические задачи (переведены + адаптированы)",
            "размер": "~8K задач",
            "педагогическая_ценность": "пошаговое решение задач"
        },
        "teacher_lesson_plans": {
            "описание": "Реальные поурочные планы учителей",
            "размер": "~500 планов (собраны с согласия авторов)",
            "педагогическая_ценность": "структура урока, ФГОС формат"
        }
    }

    GENERATION_PROMPT = """
Ты — эксперт по педагогике. Создай обучающий пример для AI-модели
на основе следующих учебных материалов.

Материал:
{seed_content}

Создай пример в формате JSON:
{{
  "instruction": "Задание для учителя (например: 'Создай 3 варианта контрольной...')",
  "input": "Дополнительный контекст (тема урока, уровень класса)",
  "output": "Образцовый ответ в формате ФГОС",
  "subject": "предмет",
  "grade_level": "5-11",
  "task_type": "assessment|lesson_plan|adaptation|report"
}}

Ответ должен соответствовать российским образовательным стандартам.
"""

    def generate_training_data(self, n_samples: int = 30000) -> list[dict]:
        """
        Использовать Claude + Gemini Batch API для генерации.
        Batch API: x10 дешевле vs realtime, ~$20-30 за 30K примеров.
        """
        pairs = []
        for seed in self._sample_seed_corpus(n_samples):
            # Чередовать модели для разнообразия
            if len(pairs) % 2 == 0:
                response = self.claude_batch.generate(
                    self.GENERATION_PROMPT.format(seed_content=seed)
                )
            else:
                response = self.gemini_batch.generate(
                    self.GENERATION_PROMPT.format(seed_content=seed)
                )
            pairs.append(json.loads(response))

        return self._filter_quality(pairs)

    def _filter_quality(self, pairs: list) -> list:
        """Фильтрация: убрать короткие, нерелевантные, дубликаты."""
        return [
            p for p in pairs
            if len(p["output"]) > 100
            and p["task_type"] in ["assessment", "lesson_plan", "adaptation", "report"]
            and self._is_fgos_compliant(p["output"])
        ]
```

## QLoRA + Unsloth: $400 за 6 часов

```python
# QLoRA fine-tuning через Unsloth (2-5x быстрее стандартного HuggingFace)

from unsloth import FastLanguageModel
from trl import SFTTrainer
from transformers import TrainingArguments

def finetune_edullm(training_data: list[dict]) -> str:
    """
    QLoRA (Quantized Low-Rank Adaptation):
    - Модель в 4-bit → требует ~16 GB VRAM (Qwen3.5-27B в 4-bit)
    - LoRA адаптеры → только ~0.1% параметров обучаются
    - Unsloth: оптимизированные CUDA ядра → 2x ускорение
    """

    # Загрузить Qwen3.5-27B в 4-bit
    model, tokenizer = FastLanguageModel.from_pretrained(
        model_name="Qwen/Qwen3.5-27B-Instruct",
        max_seq_length=4096,
        dtype=None,          # auto: bfloat16 на H200
        load_in_4bit=True    # QLoRA: 4-bit квантизация
    )

    # Добавить LoRA адаптеры
    model = FastLanguageModel.get_peft_model(
        model,
        r=64,                          # ранг адаптера
        target_modules=["q_proj", "k_proj", "v_proj", "o_proj",
                        "gate_proj", "up_proj", "down_proj"],
        lora_alpha=64,
        lora_dropout=0.05,
        use_gradient_checkpointing="unsloth"  # 30% экономия VRAM
    )

    # Конфигурация обучения
    trainer = SFTTrainer(
        model=model,
        tokenizer=tokenizer,
        train_dataset=training_data,
        dataset_text_field="text",
        max_seq_length=4096,
        args=TrainingArguments(
            per_device_train_batch_size=4,
            gradient_accumulation_steps=8,
            num_train_epochs=3,
            learning_rate=2e-4,
            fp16=False,
            bf16=True,         # H200 поддерживает bfloat16
            logging_steps=50,
            output_dir="./edullm-ru",
            save_steps=500
        )
    )

    trainer.train()

    # Слить LoRA адаптеры с основной моделью
    model.save_pretrained_merged(
        "edullm-ru-merged",
        tokenizer,
        save_method="merged_16bit"
    )

    return "edullm-ru-merged"

# Стоимость:
# H200 аренда: ~$5-6/час
# 6 часов обучения: ~$30-36
# Генерация 30K QA через Batch API: ~$20
# ИТОГО: ~$50-56 (или ~4500-5000 руб) — заметно меньше 30K из заголовка
# Если считать с разработкой и итерациями: до $400
```

## EduBench-RU: бенчмарк для образовательных моделей

```python
# github.com/csylabs-org/edubench-ru
# Открытый бенчмарк для оценки LLM на задачах российских учителей

EDUBENCH_RU_TASKS = {
    "assessment_generation": {
        "описание": "Генерация вариантов контрольных работ",
        "метрики": ["тематическая_релевантность", "уровень_сложности", "соответствие_ФГОС"],
        "примеров": 500
    },
    "lesson_plan_creation": {
        "описание": "Создание поурочных планов",
        "метрики": ["структура", "временной_план", "методические_приёмы"],
        "примеров": 300
    },
    "material_adaptation": {
        "описание": "Адаптация материалов под уровень класса",
        "метрики": ["доступность", "сохранение_содержания"],
        "примеров": 400
    },
    "oge_ege_prep": {
        "описание": "Подготовка к ОГЭ/ЕГЭ",
        "метрики": ["соответствие_кодификатору", "точность"],
        "примеров": 600
    }
}

# Результаты из статьи (апрель 2025):
EDUBENCH_RESULTS = {
    "GPT-4o":           {"score": 3.28, "rank": 4},
    "Claude-3.5-Sonnet":{"score": 3.25, "rank": 6},
    "EduLLM-RU (27B)":  {"score": 3.21, "rank": 9},   # наша модель
    "Qwen3.5-32B":      {"score": 3.18, "rank": 11},
    "GigaChat-Max":     {"score": 3.10, "rank": 14},
    "Llama-3.1-70B":    {"score": 3.05, "rank": 17},
    "YandexGPT-Pro":    {"score": 2.95, "rank": 20}
}

# Ключевой вывод: архитектура > размер
# Qwen3.5-27B (fine-tuned) > Qwen3.5-32B (base)
# Специализация дала +3 позиции в рейтинге
```

## 152-ФЗ Compliance: суверенный AI для образования

```python
SOVEREIGN_EDULLM_CONFIG = {
    "deployment": "on-premise или российское облако (Yandex Cloud, Cloud.ru, РУСТЭК)",
    "данные_студентов": "НЕ покидают инфраструктуру школы/вуза",
    "соответствие": ["152-ФЗ (персональные данные)", "ФГОС", "Приказ Минпросвещения"],

    "инфраструктура": {
        "GPU": "H100 / A100 (1 карта достаточно для inference)",
        "runtime": "vLLM или Ollama (модель в GGUF формате)",
        "endpoint": "OpenAI-compatible API",
        "хранение": "модель хранится локально, 27B FP16 = ~54 GB"
    },

    "минимальный_сервер": {
        "GPU": "RTX 4090 (24 GB) → Qwen3.5-27B в 4-bit (14 GB)",
        "RAM": "64 GB",
        "стоимость_сервера": "~350 000 руб"
    }
}
```

## Применение к Lorenzo

```python
# Паттерн CRAFT для Lorenzo: синтетические QA из базы знаний

class LorenzoCRAFTPipeline:
    """
    Lorenzo имеет 140+ технических документов.
    CRAFT паттерн: генерировать QA пары для fine-tuning
    специализированной модели по базе знаний.
    """

    def generate_qa_pairs(self, n: int = 5000) -> list[dict]:
        docs = self.corpus.load_all()
        pairs = []
        for doc in docs:
            response = self.claude_batch.generate(
                prompt=f"Создай 3 QA пары из:\n{doc.content[:2000]}"
            )
            pairs.extend(json.loads(response)["pairs"])
        return pairs[:n]
```

## Возможные комбинации

| Комбинация | Новое свойство |
|------------|----------------|
| **EduLLM-RU + YADRO (R33)** | EduLLM-RU на суверенном YADRO кластере в школах — compliance + производительность |
| **EduLLM-RU + MT-Bench RU (R34)** | EduBench-RU как образовательная ось ru_mt_bench |
| **EduLLM-RU + DQ LLM (R33)** | LLM-as-judge оценка качества генерируемых учебных материалов |
| **EduLLM-RU + Cognitive Memory (R31)** | Персональный AI-тьютор с памятью прогресса студента |
| **EduLLM-RU + HITL (R30)** | Учитель проверяет и корректирует сгенерированный материал перед использованием |

## Контакт

- Статья: https://habr.com/ru/articles/1026516/ (апрель 2025)
- GitHub EduBench-RU: https://github.com/csylabs-org/edubench-ru
- Unsloth: github.com/unslothai/unsloth
- CRAFT (ACL 2025): aclanthology.org
- Смежная (RAG для абитуриентов, QA в вузе): https://habr.com/ru/articles/944500/
- Qwen3.5: huggingface.co/Qwen/Qwen3.5-27B-Instruct

## Смотрите также
- [Главная](../../../README.md)
- [Метрики](../../../METRICS.md)
- [Здоровье](../../../HEALTH.md)
- [Глоссарий](../../../GLOSSARY.md)
- [Сущности](../../../ENTITIES.md)
- [Решения](../../../DECISIONS.md)
