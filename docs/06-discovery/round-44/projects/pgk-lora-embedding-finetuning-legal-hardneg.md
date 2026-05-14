# LoRA fine-tuning эмбеддингов на юридических документах с hard-negative mining

**Автор:** huraligne (Саприн Семён, PGK)  
**Хабр:** https://habr.com/ru/companies/pgk/articles/913912/  
**GitHub:** нет (автор: Telegram @huraligne)  
**Слой:** analytics  
**Дата:** июнь 2025  
**Уникальность:** Полный воспроизводимый pipeline доменного fine-tuning эмбеддинговой модели для production RAG: LoRA адаптеры (r=16, alpha=32, 1.94% параметров) на deepvk/USER-bge-m3 с hard-negative mining по алгоритму NVIDIA NV-Retriever (порог 0.97, n=3 hard negatives) на юридических документах. Обучение на ~2400 триплетах, A100, 2 часа, 40 эпох. Recall@5 67.5%→79.4% (+11.9 pp), NDCG@5 0.525→0.612. Единственная на Хабре статья с полным quantitative бенчмарком доменного LoRA fine-tuning эмбеддингов для русскоязычного юридического RAG.

## Проблема: общая эмбеддинговая модель плохо работает на домене

```
Проблема in-domain retrieval:
  → Общие модели (text-embedding-ada-002, multilingual-e5)
    обучены на общем корпусе
  → Юридические документы: специфическая терминология
  → "Договор оказания услуг" ≠ "договор подряда" в общем пространстве
  → Семантически близкие юридические понятия далеко в эмбеддинг-пространстве

Baseline recall для юридического RAG:
  → multilingual-e5-base: Recall@5 ≈ 67.5%
  → Значит: 32.5% вопросов → RAG не найдёт правильный документ
  → Ошибка на 1 из 3 юридических вопросов

Подход: LoRA доменная адаптация
  → Не переобучать всю модель (дорого, опасность catastrophic forgetting)
  → LoRA: только 1.94% параметров → дёшево + сохраняет общие знания
  → Hard negative mining: самые сложные негативные примеры для обучения
```

## Hard Negative Mining по алгоритму NVIDIA NV-Retriever

```python
# PGK: LoRA fine-tuning эмбеддингов
# habr.com/ru/companies/pgk/articles/913912

from sentence_transformers import SentenceTransformer, losses
from sentence_transformers.readers import InputExample
import torch
import numpy as np

class HardNegativeMiner:
    """
    NVIDIA NV-Retriever алгоритм hard negative mining.

    Hard negatives: документы семантически похожие на запрос,
    но НЕ являющиеся ответом.
    Модель должна научиться их различать.

    threshold=0.97: брать только документы с similarity > 0.97 * max_similarity
    n=3: 3 hard negative на каждый positive пример
    """

    def __init__(self, model_name: str = "deepvk/USER-bge-m3"):
        self.model = SentenceTransformer(model_name)
        self.threshold = 0.97
        self.n_hard_negatives = 3

    def mine_hard_negatives(self, queries: list[str],
                              positives: list[str],
                              corpus: list[str]) -> list[InputExample]:
        """
        Для каждой пары (query, positive) найти hard negatives из corpus.
        Hard negative: corpus[i] с высокой similarity к query,
        но НЕ являющийся positive.
        """
        triplets = []

        # Эмбеддинги всего корпуса
        corpus_embeddings = self.model.encode(corpus,
                                               normalize_embeddings=True,
                                               batch_size=32)

        for query, positive in zip(queries, positives):
            # Эмбеддинг запроса
            query_emb = self.model.encode([query],
                                           normalize_embeddings=True)[0]

            # Сходство со всем корпусом
            similarities = corpus_embeddings @ query_emb

            # Максимальное сходство (не считая positive)
            positive_idx = corpus.index(positive) if positive in corpus else -1
            if positive_idx >= 0:
                similarities[positive_idx] = -1  # исключить positive

            max_sim = similarities.max()

            # Hard negatives: similarity > threshold * max_sim
            hard_neg_mask = similarities > self.threshold * max_sim
            hard_neg_indices = np.where(hard_neg_mask)[0]

            # Взять топ-n самых сложных
            if len(hard_neg_indices) > 0:
                top_n = hard_neg_indices[
                    np.argsort(similarities[hard_neg_indices])[-self.n_hard_negatives:]
                ]
                for neg_idx in top_n:
                    triplets.append(InputExample(
                        texts=[query, positive, corpus[neg_idx]]
                    ))

        return triplets
```

## LoRA Fine-Tuning

```python
from peft import LoraConfig, get_peft_model, TaskType
from transformers import AutoModel

class LoRAEmbeddingTrainer:
    """
    LoRA адаптеры для эмбеддинговой модели.
    Только 1.94% параметров обучаемы → быстро + дёшево.
    """

    LORA_CONFIG = LoraConfig(
        r=16,                          # rank: баланс качество/параметры
        lora_alpha=32,                 # scaling factor
        target_modules=[               # какие слои адаптировать
            "query", "key", "value",   # self-attention
            "dense"                    # выходной проекционный слой
        ],
        lora_dropout=0.1,
        bias="none",
        task_type=TaskType.FEATURE_EXTRACTION
    )

    def train(self,
               base_model_name: str = "deepvk/USER-bge-m3",
               triplets: list,
               output_dir: str = "./lora-legal-embeddings") -> None:
        """
        Обучение с Triplet Margin Loss.
        Задача: anchor и positive близко, anchor и negative далеко.
        """
        from sentence_transformers import SentenceTransformer, losses, evaluation
        from torch.utils.data import DataLoader

        # Базовая модель
        model = SentenceTransformer(base_model_name)

        # Применить LoRA к трансформеру внутри модели
        # (sentence-transformers использует HuggingFace под капотом)
        model[0].auto_model = get_peft_model(
            model[0].auto_model,
            self.LORA_CONFIG
        )

        # Проверить: сколько % параметров обучаемо
        trainable = sum(p.numel() for p in model.parameters()
                        if p.requires_grad)
        total = sum(p.numel() for p in model.parameters())
        print(f"Обучаемые параметры: {trainable/total:.2%}")  # → 1.94%

        # Triplet Margin Loss
        train_dataloader = DataLoader(triplets, shuffle=True, batch_size=32)
        train_loss = losses.TripletLoss(
            model=model,
            distance_metric=losses.TripletDistanceMetric.COSINE,
            triplet_margin=0.5  # margin между positive и negative
        )

        # Обучение
        model.fit(
            train_objectives=[(train_dataloader, train_loss)],
            epochs=40,
            warmup_steps=100,
            output_path=output_dir,
            show_progress_bar=True
        )

        print(f"Модель сохранена в {output_dir}")


TRAINING_SETUP = {
    "base_model": "deepvk/USER-bge-m3",
    "domain": "Юридические документы (договоры, регламенты)",
    "corpus_size": "~1000 юридических чанков",
    "triplets": "~2400 (query, positive, hard_negative)",
    "hardware": "NVIDIA A100 (40GB)",
    "training_time": "~2 часа",
    "epochs": 40,
    "batch_size": 32,
    "lora_r": 16,
    "lora_alpha": 32,
    "trainable_params": "7.1M из 366M (1.94%)"
}
```

## Результаты бенчмарка

```python
BENCHMARK_RESULTS = {
    "задача": "Retrieval в юридическом RAG",
    "тест_сет": "~200 вопросов с золотыми ответами (юридические документы PGK)",

    "до_fine_tuning": {
        "model": "deepvk/USER-bge-m3 (baseline)",
        "recall_at_5": 0.675,
        "ndcg_at_5": 0.525
    },

    "после_fine_tuning": {
        "model": "deepvk/USER-bge-m3 + LoRA (legal)",
        "recall_at_5": 0.794,
        "ndcg_at_5": 0.612,
        "recall_improvement": "+11.9 pp (+17.6%)",
        "ndcg_improvement": "+0.087 (+16.6%)"
    },

    "вывод": "Hard-negative LoRA адаптация даёт значимый прирост на 2 часа обучения",

    "сравнение_с_альтернативами": {
        "full_fine_tuning": "Дорого, catastrophic forgetting, не нужно",
        "prompt_engineering": "Нет доступа к эмбеддинговой модели из промпта",
        "более_крупная_модель": "text-embedding-3-large дороже и медленнее",
        "lora_выигрывает": "Дёшево + быстро + сохраняет общие знания"
    }
}
```

## Применение к Lorenzo

```python
# Lorenzo: LoRA fine-tuning эмбеддингов для improve_embedding_index.py

class LorenzoEmbeddingFineTune:
    """
    PGK паттерн для Lorenzo:
    Fine-tune эмбеддинговую модель на корпусе docs/
    для лучшего семантического поиска по базе знаний Svyazi.
    """

    def prepare_triplets(self, docs_path: str) -> list:
        """
        Из docs/ сгенерировать триплеты для обучения.
        Query: вопросы о проектах (LLM генерирует)
        Positive: правильный раздел документа
        Hard negative: семантически похожий, но другой документ
        """
        corpus = self.load_chunks(docs_path)
        miner = HardNegativeMiner()

        queries, positives = self.generate_qa_pairs(corpus)
        return miner.mine_hard_negatives(queries, positives, corpus)

    def fine_tune_for_svyazi(self) -> None:
        """
        2 часа обучения → лучший поиск по 176 проектам Svyazi.
        Базовая модель: multilingual-e5-base или deepvk/USER-bge-m3.
        """
        triplets = self.prepare_triplets("/home/user/lorenzo/docs")
        trainer = LoRAEmbeddingTrainer()
        trainer.train(
            base_model_name="deepvk/USER-bge-m3",
            triplets=triplets,
            output_dir="./models/svyazi-embeddings"
        )
```

## Возможные комбинации

| Комбинация | Новое свойство |
|------------|----------------|
| **LoRA Embeddings + Graph RAG (R38)** | LoRA-дообученные эмбеддинги для VectorCypher → лучший domain retrieval |
| **LoRA Embeddings + Академия РАНХиГС (R40)** | Дообучить multilingual-e5 на образовательных документах → лучший RAG для абитуриентов |
| **LoRA Embeddings + RAG чанкинг (R43)** | Гибридный чанкинг + доменные эмбеддинги = максимальный RAGAS |
| **LoRA Embeddings + FRIDA (SberDevices)** | FRIDA как base → LoRA юридический fine-tune для русских правовых систем |
| **LoRA Embeddings + Lorenzo Gateway** | /api/ask с доменными эмбеддингами = лучший поиск по Lorenzo docs/ |

## Контакт

- Статья: https://habr.com/ru/companies/pgk/articles/913912/ (июнь 2025)
- Автор: Telegram @huraligne (Саприн Семён, PGK)
- Base model: deepvk/USER-bge-m3 (HuggingFace)
- Смежная (FRIDA русская эмбеддинг-модель, SberDevices): https://habr.com/ru/companies/sberdevices/articles/909924/
- Смежная (ruMTEB бенчмарк): https://habr.com/ru/companies/sberdevices/articles/831150/
- NVIDIA NV-Retriever: arxiv.org/abs/2407.15831
