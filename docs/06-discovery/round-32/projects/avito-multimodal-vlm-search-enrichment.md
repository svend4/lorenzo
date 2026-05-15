---
date: 2026-05-15
tags: [memory, rag, ingestion, architecture, roadmap]
state: normalized
---

# Авито: мультимодальные модели для обогащения поиска — vLLM, LoRA, GPU-кластеры

<!-- toc-auto -->
<!-- tags: avito-multimodal-vlm-search-enrichment, docs -->


<!-- summary -->
> Авито: мультимодальные модели для обогащения поиска — vLLM, LoRA, GPU-кластеры — раздел документации проекта Lorenzo.
 
 
 
>   — раздел документации проекта Lorenzo.


> [!TIP]
> Документ содержит практические рекомендации и лучшие практики.

<!-- alert-added -->

**Автор:** Кирилл Нетреба (@Kirill0720), Backend ML Engineer, Авито  
**Хабр:** https://habr.com/ru/companies/avito/articles/1024136/  
**GitHub:** не опубликован (production-система Авито)  
**Слой:** ingestion / orchestration / analytics  
**Дата:** апрель 2026  
**Уникальность:** Production VLM pipeline Авито (50M+ пользователей): Qwen2.5-VL-7B ("A-Vision") генерирует русскоязычные описания объявлений по фото → обогащает поисковый индекс. 1500 объявлений/минуту, 21 нода, 3 ДЦ. Категорийные LoRA (0.1-1% параметров). Rebuilding Cyrillic tokenizer: -50% времени генерации. vLLM continuous batching + PagedAttention для мультимодального инференса.

## Задача: изображения без текста = невидимые для поиска

```
Авито — крупнейшая доска объявлений РФ (50M+ пользователей):
  → Продавцы загружают фото товара БЕЗ описания
  → "Синяя куртка Columbia 48 размер" видна на фото
  → Текстовый поиск: ничего не находит (нет текста)
  → Покупатель уходит к конкурентам

Решение:
  VLM смотрит на фото → генерирует описание на русском
  → Добавить в поисковый индекс → объявление стало находимым

Масштаб:
  → 1500 новых объявлений/минуту (пиковая нагрузка)
  → Несколько фото на объявление
  → 21 нода, 3 дата-центра
  → Требование: latency < 2 сек на объявление
```

## A-Vision: fine-tuned Qwen2.5-VL для русского рынка

```python
# Базовая модель → кастомная A-Vision

class AVisionModel:
    """
    Qwen2.5-VL-7B-Instruct + категорийные LoRA адаптеры
    Fine-tuned на данных Авито (изображения + описания объявлений).
    """

    BASE_MODEL = "Qwen/Qwen2.5-VL-7B-Instruct"

    # Категорийные LoRA: каждая категория = свой адаптер
    LORA_ADAPTERS = {
        "electronics":  "lora/electronics-v3",   # телефоны, ноутбуки
        "clothing":     "lora/clothing-v2",       # одежда, обувь
        "auto":         "lora/auto-v4",           # авто, запчасти
        "real_estate":  "lora/real-estate-v1",    # квартиры, комнаты
        "furniture":    "lora/furniture-v2",      # мебель, интерьер
    }

    GENERATION_PROMPT = """Опиши товар на изображении для объявления о продаже.
Укажи: тип товара, цвет, размер/габариты, бренд (если виден),
состояние, характерные особенности.
Ответ: одно-два предложения, без приветствий и "на фотографии".
Язык: русский."""

    def generate_description(self, image: Image,
                              category: str) -> str:
        adapter = self.LORA_ADAPTERS.get(category, None)
        with self.load_adapter(adapter):
            output = self.model.generate(
                images=[image],
                text=self.GENERATION_PROMPT,
                max_new_tokens=150,
                temperature=0.3   # детерминированный вывод
            )
        return output
```

## LoRA для мультимодальных моделей: 0.1-1% параметров

```python
# Почему категорийные LoRA вместо одной общей модели?

LORA_DESIGN_RATIONALE = {
    "проблема_одной_модели": [
        "Электроника: нужно распознать модель телефона по камере",
        "Одежда: нужен цвет, бренд, размер",
        "Авто: VIN, пробег по спидометру, состояние кузова",
        "→ Один prompt и один checkpoint не оптимален для всех"
    ],

    "решение_lora": {
        "параметры": "0.1-1% от базовой модели (7B → +7-70M параметров на категорию)",
        "обучение": "каждый адаптер обучается на своём датасете",
        "применение": "hot-swap адаптеров без перезагрузки модели",
        "стоимость": "хранение нескольких LoRA << хранение нескольких 7B моделей"
    }
}

# vLLM поддерживает LoRA multiplexing:
# разные запросы → разные адаптеры → один base model в VRAM

from vllm import LLM, SamplingParams
from vllm.lora.request import LoRARequest

llm = LLM(
    model="Qwen/Qwen2.5-VL-7B-Instruct",
    enable_lora=True,
    max_loras=5,         # одновременно до 5 адаптеров в памяти
    max_lora_rank=64,
)

# Запросы с разными LoRA в одном батче
outputs = llm.generate(
    prompts=[...],
    lora_request=[
        LoRARequest("electronics", 1, "lora/electronics-v3"),
        LoRARequest("clothing",    2, "lora/clothing-v2"),
        LoRARequest("electronics", 1, "lora/electronics-v3"),  # reuse
    ]
)
```

## Cyrillic Tokenizer: -50% времени генерации

```python
# Критическая оптимизация для русскоязычных VLM

TOKENIZER_PROBLEM = {
    "базовый_tokenizer": {
        "coverage": "обучен на английском (90%+ обучающих данных)",
        "русский_текст": "2-4 токена на слово ('компьютер' → 4 токена)",
        "следствие": "150 слов описания = ~500 токенов = медленная генерация"
    },
    "rebuilt_tokenizer": {
        "coverage": "расширен русским корпусом",
        "русский_текст": "1-1.5 токена на слово ('компьютер' → 1-2 токена)",
        "следствие": "150 слов = ~200 токенов → -60% токенов",
        "speedup": "-50% времени генерации (decode фаза линейна по токенам)"
    }
}

# Сравнение (из статьи Авито):
# Стандартный Qwen tokenizer:
#   "Синяя куртка Columbia мужская 48 размер зимняя" → 18 токенов
# Rebuilt Cyrillic tokenizer:
#   "Синяя куртка Columbia мужская 48 размер зимняя" → 10 токенов
# → ~44% меньше токенов → пропорциональный speedup decode

class CyrillicTokenizerBuilder:
    """
    Перестройка tokenizer для эффективной работы с русским языком.
    """

    def extend_vocabulary(self, base_tokenizer,
                           russian_corpus: list[str]) -> Tokenizer:
        """
        Добавить русские токены в словарь через BPE-слияния.
        """
        # Обучить BPE на русском корпусе
        bpe_trainer = BpeTrainer(
            vocab_size=10_000,          # дополнительные токены
            special_tokens=["<image>"], # для мультимодальности
            min_frequency=5             # минимум вхождений
        )

        new_tokens = bpe_trainer.train(russian_corpus)

        # Добавить в base tokenizer (не заменить, а расширить)
        base_tokenizer.add_tokens(new_tokens)
        return base_tokenizer
```

## Production Pipeline: Queue-based Architecture

```python
# Архитектура: Worker → QaaS → LLM Worker → Search Index

class AvitoMLPipeline:
    """
    Decoupled architecture: создание объявления не ждёт VLM.
    """

    def on_listing_created(self, listing_id: str, images: list[str],
                            category: str):
        """
        Обработчик события: новое объявление создано.
        НЕ вызываем VLM синхронно — публикуем в очередь.
        """
        self.queue.publish(
            topic="listing.enrich",
            message={
                "listing_id": listing_id,
                "image_urls": images,
                "category": category,
                "priority": "normal"
            }
        )
        # Возврат немедленный — пользователь не ждёт VLM

    async def llm_worker(self):
        """
        LLM Worker: консьюмер очереди → батч → VLM → индекс.
        """
        async for batch in self.queue.consume_batch(
            topic="listing.enrich",
            max_batch_size=32,      # эффективный батч для GPU
            max_wait_ms=100         # не ждать долго неполный батч
        ):
            # Скачать изображения параллельно
            images = await asyncio.gather(*[
                self.download_image(item["image_urls"][0])
                for item in batch
            ])

            # VLM inference через vLLM (continuous batching)
            descriptions = await self.vlm.generate_batch(
                images=images,
                categories=[item["category"] for item in batch],
                use_prefix_cache=True  # system prompt кэшируется
            )

            # Обновить поисковый индекс
            await self.search_index.bulk_update([
                {"listing_id": item["listing_id"],
                 "description": desc}
                for item, desc in zip(batch, descriptions)
            ])
```

## vLLM: почему выбрали для мультимодального инференса

```python
VLLM_MULTIMODAL_ADVANTAGES = {
    "PagedAttention": {
        "описание": "Управление KV-cache страницами (как виртуальная память ОС)",
        "выгода": "Изображения = длинные токены (до 1344 для Qwen2.5-VL)",
        "следствие": "Без фрагментации KV-памяти → больше concurrent запросов"
    },

    "continuous_batching": {
        "описание": "Новые запросы вставляются в текущий батч на лету",
        "выгода": "GPU не простаивает между запросами",
        "следствие": "1500 listing/min → GPU утилизация > 85%"
    },

    "prefix_caching_для_изображений": {
        "описание": "Повторяющиеся system prompt + prefix → один раз вычислен",
        "выгода": "GENERATION_PROMPT одинаков для всей категории",
        "следствие": "Только image tokens + new text = prefill"
    },

    "lora_multiplexing": {
        "описание": "Несколько LoRA адаптеров в одном serving process",
        "выгода": "Не нужно 5 отдельных серверов для 5 категорий",
        "следствие": "Экономия GPU памяти и ops overhead"
    }
}
```

## Инфраструктура: 21 нода, 3 ДЦ

```python
AVITO_INFRASTRUCTURE = {
    "scale": {
        "nodes": 21,
        "datacenters": 3,
        "throughput": "1500 listings/min peak",
        "images_per_listing": "avg 4-6 images"
    },

    "deployment_pattern": {
        "serving": "vLLM + Kubernetes",
        "model_weights": "shared NFS между нодами",
        "lora_adapters": "lazy-loaded per category",
        "monitoring": "Prometheus + Grafana (GPU utilization, queue lag)"
    },

    "resilience": {
        "queue_as_service": "Kafka (Авито внутренний QaaS)",
        "retry": "exponential backoff при GPU OOM",
        "fallback": "объявление публикуется без описания (не блокирует)"
    }
}
```

## Применение к Lorenzo

```python
# improve_image_enrichment.py (паттерн):

class LorenzoImageEnricher:
    """
    Lorenzo работает с текстовыми документами.
    Если появятся изображения (скриншоты, диаграммы) —
    A-Vision паттерн: VLM генерирует alt-text → обогащает поиск.
    """

    async def enrich_document_images(self, doc_path: str):
        doc = self.parser.parse(doc_path)
        images = doc.extract_images()

        for image in images:
            # VLM описывает изображение
            description = await self.vlm.describe(
                image=image.data,
                context=f"Изображение из документа '{doc.title}'"
            )
            # Добавить alt-text → search_index.json
            self.index.add_alt_text(
                doc_id=doc.id,
                image_id=image.id,
                alt_text=description
            )
```

## Возможные комбинации

| Комбинация | Новое свойство |
|------------|----------------|
| **Avito VLM + vLLM inference (R32)** | Оба используют vLLM — Авито = production case study для vLLM |
| **Avito VLM + IDP+VLM (R30)** | IDP для структурных полей документов + A-Vision для контекста |
| **Avito VLM + LLM Judge (R28)** | Judge оценивает качество VLM-описаний (без галлюцинаций?) |
| **Avito VLM + Synthetic Data (R30)** | Синтетические объявления с изображениями → обучение категорийных LoRA |
| **Avito VLM + Enterprise RAG (R32)** | RAG по мультимодальному корпусу: поиск по тексту + изображениям |

## Контакт

- Статья: https://habr.com/ru/companies/avito/articles/1024136/ (апрель 2026)
- Авито Tech: habr.com/ru/companies/avito/
- Смежная (ASR+LLM, SKB Kontur): https://habr.com/ru/companies/skbkontur/articles/1024206/
- Смежная (vLLM+видео inference): https://habr.com/ru/articles/936110/
- Qwen2.5-VL: github.com/QwenLM/Qwen2.5-VL (Apache 2.0)
- vLLM: github.com/vllm-project/vllm (Apache 2.0)

## Смотрите также
- [Главная](../../../README.md)
- [Метрики](../../../METRICS.md)
- [Здоровье](../../../HEALTH.md)
- [Глоссарий](../../../GLOSSARY.md)
- [Сущности](../../../ENTITIES.md)
- [Решения](../../../DECISIONS.md)
