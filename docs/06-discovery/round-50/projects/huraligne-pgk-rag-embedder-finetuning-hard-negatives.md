---
date: 2026-05-29
tags: [memory, rag, orchestration, knowledge, ingestion]
state: normalized
---

# RAG Embedder Fine-Tuning: LoRA + Triplet Loss + Hard Negative Mining для юридических документов

<!-- toc-auto -->
<!-- tags: huraligne-pgk-rag-embedder-finetuning-hard-negatives, docs -->


<!-- summary -->
> `huraligne-pgk-rag-embedder-finetuning-hard-negatives` — раздел документации проекта Lorenzo.


> [!NOTE]
> Документ создан на основе исследования. Ссылки ведут на связанные материалы.

<!-- alert-added -->

**Автор:** huraligne (Саприн Семён, ПГК Диджитал)  
**Хабр:** https://habr.com/ru/companies/pgk/articles/913912/  
**GitHub:** нет (production кейс)  
**Слой:** knowledge / ingestion  
**Дата:** июнь 2025  
**Уникальность:** Domain-specific fine-tuning retrieval-компонента RAG для юридических документов: deepvk/USER-bge-m3 + LoRA (r=16, 1.94% обучаемых параметров) через Triplet Margin Loss с hard negative mining из ансамбля 3 учительских моделей. Синтетические данные через Qwen2.5-14B (10 вопросов/чанк). Recall@5: 67.5%→79.4%, NDCG@5: 0.525→0.612. Не RAFT (обучение генератора) — обучение embedder специально для работы со специализированным доменом.

## Проблема: general-purpose embeddings плохо работают в юридическом домене

```
ПГК Диджитал: RAG-система для юридических документов компании

Стандартный подход:
  → Взять multilingual-e5-large или bge-m3
  → Индексировать юридические документы
  → Поиск по запросу

Проблема domain mismatch:
  "расторжение договора перевозки" → общая модель находит
  документы про "разрыв соглашений" и "прекращение контрактов"
  → юридически это РАЗНЫЕ документы с разными последствиями

  "статья 785 ГК РФ" → общая модель не знает что это
  "договор перевозки груза" → нет связи в embedding space

Без fine-tuning:
  Recall@5 = 67.5% → треть релевантных документов не находится

С fine-tuning (LoRA + hard negatives):
  Recall@5 = 79.4% → +11.9 pp
  NDCG@5 = 0.612 (+0.087)
```

## Архитектура fine-tuning pipeline

```python
# huraligne (ПГК Диджитал): fine-tuning embedder для RAG
# habr.com/ru/companies/pgk/articles/913912/

from dataclasses import dataclass
from typing import Optional
import numpy as np

@dataclass
class Triplet:
    """
    Обучающий пример: anchor + positive + hard_negative.

    anchor: вопрос пользователя (синтетически сгенерированный)
    positive: релевантный чанк документа
    hard_negative: нерелевантный чанк, который похож по поверхностным признакам
                   (выбран учительскими моделями — не случайный!)
    """
    anchor: str              # вопрос: "Каков порядок расторжения договора перевозки?"
    positive: str            # правильный чанк из документа
    hard_negative: str       # похожий, но неправильный чанк
    source_document: str
    difficulty_score: float  # насколько сложный negative (0.5-0.99)


class SyntheticDataGenerator:
    """
    Генерация синтетических обучающих данных через Qwen2.5-14B.

    10 вопросов на каждый чанк → ~3000 пар → ~2400 триплетов.

    Разнообразие типов вопросов:
    - Фактический: "Каков срок исковой давности по договору перевозки?"
    - Процедурный: "Как правильно оформить претензию перевозчику?"
    - Нормативный: "Какие статьи ГК РФ регулируют договор перевозки?"
    - Сравнительный: "Чем отличается фрахт от перевозки?"
    """

    def __init__(self, llm_url: str = "http://localhost:11434"):
        self.llm_url = llm_url

    async def generate_questions(self, chunk: str, n: int = 10) -> list[str]:
        """
        Сгенерировать N вопросов к чанку документа.
        Вопросы должны быть разнообразными и отвечаться из чанка.
        """
        prompt = f"""Сгенерируй {n} разнообразных вопросов, ответы на которые
можно найти в следующем фрагменте юридического документа.

Типы вопросов: фактические, процедурные, нормативные, сравнительные.
Формат: JSON массив строк.

Фрагмент документа:
{chunk}

Вопросы (JSON):"""

        response = await self._call_qwen(prompt, model="qwen2.5:14b")
        return json.loads(response)


class HardNegativeMiner:
    """
    Hard Negative Mining: отбор сложных отрицательных примеров.

    Случайный negative: "договор перевозки" vs "рецепт пирога" → слишком легко
    Hard negative: "договор перевозки" vs "договор экспедиции" → модель путается

    Метод ансамбля учительских моделей:
    Три модели находят топ-K чанков для запроса.
    Пересечение топ-K (но не positive) = hard negatives.
    Ансамбль = более надёжный отбор чем одна модель.
    """

    TEACHER_MODELS = [
        "intfloat/multilingual-e5-large-instruct",  # multilingual
        "sergeyzh/rubert-tiny-turbo",                # быстрая русская
        "cointegrated/LaBSE-en-ru"                   # cross-lingual
    ]

    def mine_hard_negatives(self,
                              query: str,
                              positive_chunk: str,
                              all_chunks: list[str],
                              top_k: int = 50) -> list[str]:
        """
        Найти hard negatives через ансамбль учительских моделей.

        1. Каждая учительская модель ранжирует все чанки по query
        2. Берём top-K каждой модели
        3. Берём пересечение (что ВСЕ три модели считают похожим)
        4. Убираем positive → остаются hard negatives
        """
        # Ранжирование каждой учительской моделью
        teacher_rankings = {}
        for model_name in self.TEACHER_MODELS:
            model = self._load_teacher(model_name)
            scores = model.similarity(query,
                                       [c for c in all_chunks if c != positive_chunk])
            top_k_indices = np.argsort(scores)[-top_k:]
            teacher_rankings[model_name] = set(top_k_indices)

        # Пересечение: чанки которые все 3 модели считают похожими
        intersection = teacher_rankings[self.TEACHER_MODELS[0]]
        for model_name in self.TEACHER_MODELS[1:]:
            intersection &= teacher_rankings[model_name]

        # Сложность: насколько близко к positive (чем ближе → сложнее)
        hard_negatives = []
        for idx in intersection:
            chunk = all_chunks[idx]
            difficulty = self._compute_difficulty(query, positive_chunk, chunk)
            if 0.5 <= difficulty < 0.99:  # не слишком лёгкий, не идентичный
                hard_negatives.append(chunk)

        return hard_negatives[:5]  # топ-5 hard negatives на пример
```

## LoRA Fine-Tuning с Triplet Margin Loss

```python
from peft import LoraConfig, get_peft_model
import torch
import torch.nn as nn

class TripletEmbedderTrainer:
    """
    Fine-tuning embedder через LoRA + Triplet Margin Loss.

    Базовая модель: deepvk/USER-bge-m3
    LoRA конфигурация: r=16, alpha=32 → 1.94% обучаемых параметров
    Обучение: 40 эпох на A100 (40GB)
    """

    LORA_CONFIG = LoraConfig(
        r=16,
        lora_alpha=32,
        target_modules=["query", "key", "value"],  # attention layers
        lora_dropout=0.1,
        bias="none",
        task_type="FEATURE_EXTRACTION"
    )

    def setup_model(self, base_model_name: str = "deepvk/USER-bge-m3"):
        """Загрузить базовую модель и применить LoRA."""
        from transformers import AutoModel
        base_model = AutoModel.from_pretrained(base_model_name)
        self.model = get_peft_model(base_model, self.LORA_CONFIG)
        self.model.print_trainable_parameters()
        # Вывод: trainable params: 1.94% of total parameters

    def triplet_loss(self,
                      anchor_emb: torch.Tensor,
                      positive_emb: torch.Tensor,
                      negative_emb: torch.Tensor,
                      margin: float = 0.3) -> torch.Tensor:
        """
        Triplet Margin Loss:
        L = max(d(anchor, positive) - d(anchor, negative) + margin, 0)

        Обучает: anchor должен быть БЛИЖЕ к positive,
                 чем к negative (на margin).

        Результат: в embedding space похожие документы собраны вместе,
                   непохожие — разнесены.
        """
        pos_dist = 1 - nn.functional.cosine_similarity(anchor_emb, positive_emb)
        neg_dist = 1 - nn.functional.cosine_similarity(anchor_emb, negative_emb)
        loss = torch.clamp(pos_dist - neg_dist + margin, min=0)
        return loss.mean()

    def train_epoch(self, triplets: list[Triplet]) -> float:
        """Одна эпоха обучения."""
        total_loss = 0
        for batch in self._batch(triplets, size=32):
            anchor_embs = self._encode([t.anchor for t in batch])
            positive_embs = self._encode([t.positive for t in batch])
            negative_embs = self._encode([t.hard_negative for t in batch])

            loss = self.triplet_loss(anchor_embs, positive_embs, negative_embs)
            loss.backward()
            self.optimizer.step()
            total_loss += loss.item()

        return total_loss / len(triplets)


TRAINING_DETAILS = {
    "базовая_модель": "deepvk/USER-bge-m3",
    "lora_r": 16,
    "lora_alpha": 32,
    "обучаемых_параметров_%": 1.94,
    "обучение": {
        "эпох": 40,
        "железо": "A100 40GB",
        "размер_батча": 32,
        "optimizer": "AdamW, lr=2e-4"
    },
    "данные": {
        "синтетика": "Qwen2.5-14B: 10 вопросов × каждый чанк",
        "всего_пар": 3000,
        "всего_триплетов": 2400,
        "hard_negatives": "ансамбль 3 учительских моделей"
    },
    "результаты": {
        "Recall@5": {"до": 0.675, "после": 0.794, "delta": "+11.9pp"},
        "NDCG@5": {"до": 0.525, "после": 0.612, "delta": "+0.087"}
    }
}
```

## Применение к Lorenzo

```python
# Lorenzo: fine-tuning embedder для поиска по docs/

class LorenzoEmbedderFineTuner:
    """
    huraligne паттерн для Lorenzo:
    Fine-tuning embedder специально для базы знаний Svyazi.

    Домен: технические карточки проектов (Python, LLM, RAG, агенты)
    Базовая модель: deepvk/USER-bge-m3 или paraphrase-multilingual

    Синтетика через Claude API:
    10 вопросов на каждую карточку (1632 карточки × 10 = 16K вопросов)
    Hard negatives: карточки из похожих раундов

    Ожидаемый эффект:
    "BM25 + fine-tuned embedder" > "BM25 + general embedder"
    особенно для запросов вроде "агент с памятью для координации"
    (технически специфичный запрос → нужно доменное embedding space)
    """

    def prepare_training_data(self, cards_path: str) -> list[Triplet]:
        """
        Подготовить триплеты из карточек Lorenzo.
        positive = карточка из того же раунда/темы
        hard_negative = карточка из похожего раунда (разные имплементации)
        """
        pass
```

## Возможные комбинации

| Комбинация | Новое свойство |
|------------|----------------|
| **Fine-tuned Embedder + Finance RAG (R49)** | 4-головый ретривер + domain fine-tuned вектор = ещё лучший финансовый поиск |
| **Fine-tuned Embedder + Temporal KG (R47)** | Доменные эмбеддинги + темпоральный граф: семантически точный поиск по историческим нормам |
| **Fine-tuned Embedder + Agent Eval (R48)** | Golden Set для тестирования качества fine-tuned embedder: Recall@K как метрика |
| **Fine-tuned Embedder + Lorenzo Search** | Заменить general-purpose TF-IDF в Lorenzo на domain fine-tuned deepvk/USER-bge-m3 |
| **Fine-tuned Embedder + LoRA Embeddings (R44)** | R44: LoRA для задачи классификации; R50: LoRA для улучшения retrieval — сравнить подходы |

## Контакт

- Статья: https://habr.com/ru/companies/pgk/articles/913912/ (июнь 2025)
- Автор: huraligne (Саприн Семён, ПГК Диджитал)
- deepvk/USER-bge-m3: huggingface.co/deepvk/USER-bge-m3
- PEFT/LoRA: github.com/huggingface/peft
- Triplet Margin Loss: pytorch.org/docs/stable/generated/torch.nn.TripletMarginLoss.html
- Смежная (LoRA embeddings, R44): docs/06-discovery/round-44/
- Смежная (synthetic data RAG, R39): docs/06-discovery/round-39/
- Смежная (RAG чанкинг, R43): docs/06-discovery/round-43/

## Смотрите также
- [Главная](../../../README.md)
- [Метрики](../../../METRICS.md)
- [Здоровье](../../../HEALTH.md)
- [Глоссарий](../../../GLOSSARY.md)
- [Сущности](../../../ENTITIES.md)
- [Решения](../../../DECISIONS.md)
