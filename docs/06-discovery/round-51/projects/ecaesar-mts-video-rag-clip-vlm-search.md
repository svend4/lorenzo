---
date: 2026-05-15
tags: [memory, rag, security, knowledge, ingestion]
state: normalized
---

# Video Search Assistant: CLIP-Only RAG для видеонаблюдения без LLM-декодера

<!-- toc-auto -->
<!-- tags: ecaesar-mts-video-rag-clip-vlm-search, docs -->


<!-- summary -->
> Автор: eCaesar (Георгий Гайков, MTS AI) Хабр: https://habr.com/ru/companies/mts_ai/articles/804555/
Хабр: https://habr.com/ru/companies/mts_ai/articles/804555/  
GitHub: нет (production кейс)  
Слой: knowledge / ingestion  
Дата: апрель 2024  
Уникальность: Оригинальное архитектурное решение: отбросить язык


> [!WARNING]
> Документ содержит описание рисков и ограничений. Изучите их перед принятием архитектурных решений.

<!-- alert-added -->

**Автор:** eCaesar (Георгий Гайков, MTS AI)  
**Хабр:** https://habr.com/ru/companies/mts_ai/articles/804555/  
**GitHub:** нет (production кейс)  
**Слой:** knowledge / ingestion  
**Дата:** апрель 2024  
**Уникальность:** Оригинальное архитектурное решение: отбросить языковую голову мультимодальной модели при индексации, оставив только vision encoder CLIP — 10–100× ускорение vs полная VLM. RAG-пайплайн для видеопоиска: ffmpeg→CLIP(ViT-B/32)→FAISS→косинусное сходство. Recall@k=80% vs 35–70% у text-only baseline. Тестирование на запросах стиля видеонаблюдения ("конфликт", "ДТП", "возгорание").

## Проблема: поиск по видео — не поиск по тексту

```
Традиционный видеопоиск:
  → Транскрибировать речь → text search
  Проблема: 80% событий в кадре не содержат речи
  "Драка у входа" → нет слова "драка" в аудиодорожке

  → Object detection (YOLO) → метаданные объектов
  Проблема: нет семантического понимания сцен,
            нет ответа на вопрос "что происходит?"

MTS AI: видеоаналитика для систем безопасности
  Запрос: "найди момент, где кто-то падает"
  → нужно семантическое сходство запроса и видеофрагмента
  → нужна скорость: длинное видео (часы) не ждёт

Ключевая инсайт:
  VLM = vision encoder + language decoder
  Для индексации нужен только vision encoder!
  Language decoder нужен только для генерации ответа.
  → Отбросить декодер → 10-100× быстрее индексация
```

## Архитектура Video RAG Pipeline

```python
# eCaesar (MTS AI): Video Search Assistant
# habr.com/ru/companies/mts_ai/articles/804555/

from dataclasses import dataclass
from typing import Optional
import numpy as np

@dataclass
class VideoChunk:
    """
    Единица индексации видео: один ключевой кадр.

    Каждые N секунд видео → один кадр → один CLIP-вектор.
    Не транскрипция, не детекция объектов — семантический embedding всей сцены.
    """
    video_path: str
    timestamp_sec: float        # позиция в видео
    frame_embedding: np.ndarray # CLIP visual embedding (512-dim)
    scene_description: Optional[str] = None  # опц. GPT-4V для переранжирования


class CLIPVideoIndexer:
    """
    Ключевое архитектурное решение: используем ТОЛЬКО vision encoder CLIP.

    Полная VLM (LLaVA, GPT-4V) при индексации:
      → Генерирует описание каждого кадра
      → 2-10 сек/кадр → часовое видео = дни индексации

    CLIP vision encoder без декодера:
      → Прямой embedding изображения в пространство запросов
      → 100мс/кадр (CPU!) → часовое видео = минуты
      → Модель: laion/CLIP-ViT-B-32 (600MB, работает на CPU)

    Работает потому что CLIP обучен на пары (текст, изображение):
    text_embed("пожар") ≈ image_embed(фото пожара)
    """

    MODEL_NAME = "laion/CLIP-ViT-B-32"  # 600MB, CPU-runnable

    def __init__(self):
        from transformers import CLIPModel, CLIPProcessor
        self.model = CLIPModel.from_pretrained(self.MODEL_NAME)
        self.processor = CLIPProcessor.from_pretrained(self.MODEL_NAME)

        # Только vision часть — language decoder не загружаем
        self.vision_encoder = self.model.vision_model

    def extract_frame_embedding(self, frame_rgb: np.ndarray) -> np.ndarray:
        """
        Извлечь семантический вектор из одного кадра.
        Без text decoder → 10-100× быстрее чем полная VLM.
        """
        inputs = self.processor(images=frame_rgb, return_tensors="pt")
        with torch.no_grad():
            # Только vision forward pass — не generate()
            vision_outputs = self.vision_encoder(**inputs)
            # Используем CLS-токен как embedding сцены
            embedding = vision_outputs.pooler_output[0]
            # Нормализовать для косинусного сходства
            embedding = embedding / embedding.norm()
        return embedding.numpy()

    def index_video(self,
                     video_path: str,
                     frame_interval_sec: float = 1.0) -> list[VideoChunk]:
        """
        Индексировать видео: извлечь кадры каждые N секунд → CLIP embedding.

        Для часового видео (3600 кадров) на CPU:
        - 100ms/кадр × 3600 = ~6 минут (vs дни для VLM-описаний)
        """
        import cv2

        cap = cv2.VideoCapture(video_path)
        fps = cap.get(cv2.CAP_PROP_FPS)
        frame_step = int(fps * frame_interval_sec)

        chunks = []
        frame_idx = 0

        while cap.isOpened():
            ret, frame = cap.read()
            if not ret:
                break

            if frame_idx % frame_step == 0:
                timestamp = frame_idx / fps
                frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                embedding = self.extract_frame_embedding(frame_rgb)

                chunks.append(VideoChunk(
                    video_path=video_path,
                    timestamp_sec=timestamp,
                    frame_embedding=embedding
                ))

            frame_idx += 1

        cap.release()
        return chunks


class VideoRAGSearch:
    """
    Поиск по индексированному видео через косинусное сходство CLIP-векторов.

    Запрос → CLIP text encoder → text embedding
    FAISS index → топ-K ближайших кадров
    Опционально: GPT-4V переранжирует результаты (только топ-K, не всё видео)
    """

    def __init__(self, indexer: CLIPVideoIndexer):
        import faiss
        self.indexer = indexer
        self.index = faiss.IndexFlatIP(512)  # Inner Product = косинусное сходство
        self.chunks: list[VideoChunk] = []

    def add_video(self, video_path: str):
        """Добавить видео в поисковый индекс."""
        chunks = self.indexer.index_video(video_path)
        embeddings = np.stack([c.frame_embedding for c in chunks])
        self.index.add(embeddings)
        self.chunks.extend(chunks)

    def search(self,
               query_ru: str,
               top_k: int = 5,
               use_gpt4v_rerank: bool = False) -> list[VideoChunk]:
        """
        Найти релевантные моменты в видео по текстовому запросу.

        query_ru: "человек упал у входа" (русский запрос)
        → автоматически переводится в EN для CLIP (обучен на EN)
        → косинусное сходство с CLIP image vectors
        → топ-K моментов видео
        """
        # CLIP лучше понимает EN запросы → перевести
        query_en = self._translate_ru_to_en(query_ru)

        # Embed query через CLIP text encoder
        text_inputs = self.indexer.processor(text=query_en, return_tensors="pt")
        with torch.no_grad():
            text_embedding = self.indexer.model.get_text_features(**text_inputs)
            text_embedding = text_embedding / text_embedding.norm()

        # Поиск в FAISS
        query_vec = text_embedding.numpy()
        scores, indices = self.index.search(query_vec, top_k)

        results = [self.chunks[i] for i in indices[0]]

        # Опциональное переранжирование через GPT-4V
        if use_gpt4v_rerank:
            results = self._rerank_with_gpt4v(query_ru, results)

        return results

    def _rerank_with_gpt4v(self,
                            query: str,
                            candidates: list[VideoChunk]) -> list[VideoChunk]:
        """
        Переранжирование топ-K через GPT-4V как reranker.

        НЕ обрабатываем всё видео — только топ-K кандидатов от CLIP.
        Это сохраняет скорость: GPT-4V вызывается K раз, не тысячи раз.
        """
        scored_candidates = []
        for chunk in candidates:
            frame = self._extract_frame(chunk.video_path, chunk.timestamp_sec)
            score = self._ask_gpt4v_relevance(query, frame)
            scored_candidates.append((score, chunk))

        scored_candidates.sort(key=lambda x: x[0], reverse=True)
        return [chunk for _, chunk in scored_candidates]


ARCHITECTURE_SUMMARY = {
    "pipeline": [
        "1. ffmpeg/OpenCV: извлечь кадры каждые 1с",
        "2. CLIP ViT-B/32 (только vision encoder): image → 512-dim vector",
        "3. FAISS IndexFlatIP: хранить все векторы",
        "4. Query: RU→EN перевод → CLIP text encoder → text vector",
        "5. Косинусное сходство → топ-K кадров",
        "6. (Optional) GPT-4V reranker: только топ-K, не всё видео"
    ],
    "ключевое_решение": (
        "Отбросить language decoder VLM при индексации: "
        "10-100× speedup. LLM нужен только для финального answer generation."
    ),
    "результаты": {
        "Recall@K": {"CLIP+FAISS": "80%", "text-only baseline": "35-70%"},
        "скорость_индексации": "10× быстрее real-time на GPU",
        "модель": "laion/CLIP-ViT-B-32 (600MB, CPU-runnable)",
        "тест_сценарии": ["конфликт у входа", "ДТП", "возгорание", "падение человека"]
    },
    "стек": {
        "vision_encoder": "CLIP ViT-B/32 (laion)",
        "vector_index": "FAISS IndexFlatIP",
        "frame_extraction": "OpenCV + ffmpeg",
        "optional_reranker": "GPT-4 Vision"
    }
}
```

## Применение к Lorenzo

```python
# Lorenzo: видео-индексация для docs/

class LorenzoVideoKnowledge:
    """
    eCaesar паттерн для Lorenzo:
    Индексировать видео-лекции, записи конференций, туториалы
    для поиска по содержимому кадров (не только субтитрам).

    Пример: "найди момент где показывают LangGraph граф" →
    CLIP video search найдёт скриншот с графом из видео-доклада

    Отдельный retriever для video_chunks в CardStore:
    card_type="video_chunk" с timestamp + frame_embedding
    """
    pass
```

## Возможные комбинации

| Комбинация | Новое свойство |
|------------|----------------|
| **Video RAG + Multimodal RAG v2 (R48)** | Gemini Embedding для video + CLIP для surveillance: два подхода видео-RAG, разные компромиссы |
| **Video RAG + Finance RAG 4-head (R49)** | Видеопоиск как пятый retriever в 4-головый ансамбль: видео-документы как источник знаний |
| **Video RAG + LLM Observability (R45)** | Трейсинг: где CLIP уверен, где нужен GPT-4V reranker — визуализация точек эскалации |
| **Video RAG + SENTINEL (R47)** | Видеонаблюдение + SENTINEL: детекция угроз в видеопотоке через семантический поиск |
| **Video RAG + Lorenzo Search** | Video chunks как отдельный тип карточек в CardStore: поиск по содержимому видеолекций |

## Контакт

- Статья: https://habr.com/ru/companies/mts_ai/articles/804555/ (апрель 2024)
- Автор: eCaesar (Георгий Гайков, MTS AI Smart Video Analytics)
- CLIP: openai/clip-vit-base-patch32 / laion/CLIP-ViT-B-32
- FAISS: github.com/facebookresearch/faiss
- Смежная (Gemini Embedding video-RAG, R48): docs/06-discovery/round-48/projects/ab429-gemini-embedding2-multimodal-video-rag.md
- Смежная (Avito VLM, R45): docs/06-discovery/round-45/
- Смежная (MTS code review, R47): docs/06-discovery/round-47/projects/mts-evgzor-llm-code-review-gitlab-n8n-ollama.md

## Смотрите также
- [Главная](../../../README.md)
- [Метрики](../../../METRICS.md)
- [Здоровье](../../../HEALTH.md)
- [Глоссарий](../../../GLOSSARY.md)
- [Сущности](../../../ENTITIES.md)
- [Решения](../../../DECISIONS.md)
