---
date: 2026-06-05
tags: [rag, orchestration, security, knowledge, ingestion]
state: normalized
---

# T-Lite и T-Pro: открытые русскоязычные LLM с 4-этапным pipeline

<!-- toc-auto -->
<!-- tags: tbank-tlite-tpro-russian-llm-training, docs -->


<!-- summary -->
> Ключевое открытие: пропуск полного pretraining с заменой на replay русских текстов снижает затраты на 80-90% при конкурентных MERA-результатах.


> [!WARNING]
> Документ содержит описание рисков и ограничений. Изучите их перед принятием архитектурных решений.

<!-- alert-added -->

**Автор:** anatolii-potapov (Анатолий Потапов, MLE, T-Bank)  
**Хабр:** https://habr.com/ru/companies/tbank/articles/865582/  
**GitHub:** https://github.com/turbo-llm/turbo-alignment (Apache 2.0)  
**HuggingFace:** https://huggingface.co/t-tech  
**Слой:** analytics / orchestration  
**Дата:** декабрь 2024  
**Уникальность:** T-Bank открыл исходный код 7B и 32B русскоязычных LLM с полным 4-этапным continual pretraining pipeline на базе Qwen 2.5. Ключевое открытие: пропуск полного pretraining с заменой на replay русских текстов снижает затраты на 80-90% при конкурентных MERA-результатах. Библиотека turbo-alignment реализует весь SFT → DPO pipeline открытым кодом. Исчерпывающий бенчмарк: MERA, ruMMLU-Pro, ruGSM8K (94.1%), ruMATH, ruCodeEval, Arena Hard Ru ELO.

## Проблема: русскоязычные LLM отстают от английских

```
Состояние русских LLM (конец 2024):
  → GigaChat: закрытый, API-only
  → YandexGPT: закрытый, YandexCloud-only
  → ruGPT-3: устарел, не instruction-tuned
  → Mistral/Llama fine-tuned на RU: работают, но не оптимальны

Проблема continual pretraining:
  → Взять Llama 3.1 → дообучить на русском корпусе
  → Катастрофическое забывание английских знаний
  → Или: полный pretraining с нуля → $5M+ на GPU

Решение T-Bank: replay-based continual pretraining
  → Qwen 2.5 (сильная база с RU поддержкой)
  → Stage 1: 100B токенов RU + English replay (без забывания)
  → Stage 2-4: SFT → DPO
  → Стоимость: 80-90% дешевле full pretraining
  → Результат: MERA T-Pro 0.629, T-Lite 0.552
```

## 4-этапный Pipeline

```python
# T-Bank: continual pretraining pipeline
# github.com/turbo-llm/turbo-alignment

from dataclasses import dataclass
from typing import Optional

@dataclass
class TrainingConfig:
    """Конфигурация 4-этапного pipeline."""
    base_model: str = "Qwen/Qwen2.5-7B"  # или 32B
    stage: int = 1

    # Stage 1: Pretraining
    stage1_tokens: int = 100_000_000_000   # 100B токенов
    stage1_ru_ratio: float = 0.85          # 85% RU, 15% English replay
    stage1_sources: list = None            # Common Crawl RU, книги, код

    # Stage 2: Instruction mix
    stage2_tokens: int = 40_000_000_000    # 40B токенов
    stage2_mix: dict = None                # instructional + pretraining

    # Stage 3: SFT
    stage3_tokens: int = 1_000_000_000     # 1B токенов SFT
    stage3_data: str = "instruction_following"

    # Stage 4: Preference Alignment
    stage4_tokens: int = 1_000_000_000    # 1B токенов DPO
    stage4_method: str = "DPO"            # Direct Preference Optimization


class TurboAlignmentPipeline:
    """
    turbo-alignment: полный pipeline SFT → DPO для русского LLM.
    Apache 2.0. github.com/turbo-llm/turbo-alignment
    """

    # Stage 1: Continual Pretraining с Russian Replay
    def stage1_pretraining(self, config: TrainingConfig) -> None:
        """
        Ключевая инновация: English replay предотвращает
        катастрофическое забывание.

        Данные (100B токенов):
        - Common Crawl RU (качественная фильтрация)
        - Русские книги и литература
        - Русский GitHub код
        - Русская Википедия
        - 15% English replay из оригинального Qwen датасета
        """
        ru_data = self.load_russian_corpus(config.stage1_tokens * 0.85)
        en_replay = self.load_english_replay(config.stage1_tokens * 0.15)

        dataset = self.interleave(ru_data, en_replay)
        self.trainer.pretrain(
            model=config.base_model,
            data=dataset,
            lr=2e-5,
            batch_size=2048,
            seq_length=4096
        )

    # Stage 2: Instruction Pretraining Mix
    def stage2_instruction_mix(self, config: TrainingConfig) -> None:
        """
        Смешанный датасет: pretraining + instructional данные.
        Цель: плавный переход от pretraining к instruction following.

        40B токенов = дорого, но критично для русского instruction following.
        """
        mixed = self.create_instruction_pretrain_mix(
            pretrain_ratio=0.6,
            instruction_ratio=0.4,
            total_tokens=config.stage2_tokens
        )
        self.trainer.continue_training(data=mixed)

    # Stage 3: Supervised Fine-Tuning
    def stage3_sft(self, config: TrainingConfig) -> None:
        """
        SFT на русскоязычных instruction-following данных.
        1B токенов: чат-шаблон Qwen + русские инструкции.

        Использует turbo-alignment SFT trainer:
        - Поддержка LoRA / full fine-tuning
        - Маскирование системного промпта в loss
        - Русский чат-шаблон
        """
        from turbo_alignment import SFTTrainer, SFTConfig

        trainer = SFTTrainer(
            model=self.model,
            config=SFTConfig(
                max_seq_length=8192,
                num_epochs=3,
                learning_rate=1e-5,
                mask_prompt_loss=True,  # не обучаем на системном промпте
                chat_template="qwen"
            )
        )
        trainer.train(self.russian_instruction_dataset)

    # Stage 4: DPO Preference Alignment
    def stage4_dpo(self, config: TrainingConfig) -> None:
        """
        Direct Preference Optimization на русских preference парах.
        1B токенов: chosen vs rejected ответы.

        Улучшает: следование инструкциям, безопасность, качество ответов.
        beta: 0.1 (стандарт)
        """
        from turbo_alignment import DPOTrainer, DPOConfig

        trainer = DPOTrainer(
            model=self.model,
            config=DPOConfig(
                beta=0.1,
                max_seq_length=4096,
                loss_type="sigmoid"  # стандартный DPO loss
            )
        )
        trainer.train(self.russian_preference_dataset)
```

## MERA бенчмарк результаты

```python
BENCHMARK_RESULTS = {
    "бенчмарки": [
        "MERA (Multitask Evaluation for Russian Applications)",
        "ruMMLU-Pro (русский MMLU professional)",
        "ruGSM8K (математика на русском)",
        "ruMATH (сложная математика)",
        "ruCodeEval (код с русскими комментариями)",
        "Arena Hard Ru ELO (предпочтения людей)"
    ],

    "T-Lite_7B": {
        "MERA": 0.552,
        "ruGSM8K": "~75%",
        "Arena_Hard_Ru_ELO": "~75",
        "позиция": "Лучший open-source до 10B на русском (дек 2024)"
    },

    "T-Pro_32B": {
        "MERA": 0.629,
        "ruGSM8K": 0.941,   # 94.1% — ключевой результат
        "Arena_Hard_Ru_ELO": 90.17,
        "позиция": "Конкурирует с GPT-4o на русских задачах"
    },

    "сравнение": {
        "GPT-4o": "T-Pro сопоставим или лучше на RU задачах",
        "Athene-V2-Chat": "T-Pro обгоняет на ruGSM8K",
        "Qwen2.5-32B": "T-Pro лучше за счёт RU специализации"
    },

    "ключевое_открытие": {
        "факт": "Replay-based continual pretraining = -80-90% стоимости",
        "vs_full_pretraining": "Сопоставимое качество без $5M GPU budget",
        "вывод": "Большинство команд могут адаптировать LLM к своему языку"
    }
}

TURBO_ALIGNMENT_FEATURES = {
    "github": "https://github.com/turbo-llm/turbo-alignment",
    "license": "Apache 2.0",

    "возможности": [
        "SFT с маскированием промпта",
        "DPO / IPO / KTO preference optimization",
        "LoRA / QLoRA поддержка",
        "Многозадачное обучение (multi-task SFT)",
        "RLHF (PPO) поддержка",
        "Поддержка Flash Attention 2",
        "DeepSpeed ZeRO-3 интеграция"
    ],

    "использование": """
# Установка
pip install turbo-alignment

# SFT запуск
python -m turbo_alignment train_sft \\
    --config configs/sft_config.yaml \\
    --model_path Qwen/Qwen2.5-7B \\
    --dataset_path data/russian_instructions.jsonl
"""
}
```

## Применение к Lorenzo

```python
# Lorenzo: turbo-alignment для fine-tuning на docs/

class LorenzoRussianFineTune:
    """
    T-Bank паттерн для Lorenzo:
    Fine-tune небольшой RU модели (T-Lite 7B) на корпусе docs/
    для специализированного поиска по базе знаний Svyazi.

    Альтернатива RAG: дистиллированная модель знает корпус наизусть.
    """

    def prepare_sft_dataset(self, docs_path: str) -> list[dict]:
        """
        Конвертировать docs/ в SFT формат:
        instruction: "Что такое AgentFS?"
        response: "AgentFS — файловая система для агентов..."
        """
        qa_pairs = []
        for doc in self.scan_docs(docs_path):
            questions = self.generate_questions(doc)  # LLM
            for q in questions:
                answer = self.extract_answer(doc, q)  # BM25 + LLM
                qa_pairs.append({
                    "instruction": q,
                    "input": "",
                    "output": answer
                })
        return qa_pairs

    def fine_tune(self, base_model: str = "t-tech/T-lite-it-1.0") -> None:
        """
        SFT T-Lite 7B на Lorenzo docs/ через turbo-alignment.
        Результат: модель отвечает на вопросы о корпусе без RAG.
        """
        from turbo_alignment import SFTTrainer
        dataset = self.prepare_sft_dataset("/home/user/lorenzo/docs")
        trainer = SFTTrainer(model=base_model)
        trainer.train(dataset)
```

## Возможные комбинации

| Комбинация | Новое свойство |
|------------|----------------|
| **T-Pro + Agent Distillation (R39)** | Использовать turbo-alignment для дистилляции трасс в специализированный RU агент |
| **T-Pro + MERA + SWE-MERA (R41)** | T-Pro на SWE-MERA: первый российский LLM в coding бенчмарке |
| **T-Pro + Structured Output (R40)** | Outlines constrained decoding для T-Lite/T-Pro на self-hosted vLLM |
| **T-Pro + LangFuse (R38)** | Трейсинг качества T-Lite vs GPT-4o на реальных запросах |
| **T-Pro + Lorenzo Gateway** | Lorenzo Gateway на T-Lite как privacy-first локальная альтернатива Claude |

## Контакт

- Статья: https://habr.com/ru/companies/tbank/articles/865582/ (декабрь 2024)
- GitHub turbo-alignment: https://github.com/turbo-llm/turbo-alignment
- HuggingFace: https://huggingface.co/t-tech
- MERA бенчмарк: mera.a-ai.ru
- Смежная (GigaChat 3 Ultra 702B MoE): https://habr.com/en/companies/sberdevices/articles/968904/
- Смежная (Кириллица в LLM токенизация): https://habr.com/ru/articles/1032610/
- Смежная (A-Vibe Авито RU LLM): https://habr.com/ru/articles/899242/

## Смотрите также
- [Главная](../../../README.md)
- [Метрики](../../../METRICS.md)
- [Здоровье](../../../HEALTH.md)
- [Глоссарий](../../../GLOSSARY.md)
- [Сущности](../../../ENTITIES.md)
- [Решения](../../../DECISIONS.md)
