---
date: 2026-05-15
tags: [rag, knowledge, ingestion, architecture, roadmap]
state: normalized
---

# Gemini Embedding 2 + мультимодальный RAG: видео, изображения и аудио в одном векторном пространстве

<!-- toc-auto -->
<!-- tags: ab429-gemini-embedding2-multimodal-video-rag, docs -->


<!-- summary -->
> `ab429-gemini-embedding2-multimodal-video-rag` — раздел документации проекта Lorenzo.


> [!WARNING]
> Документ содержит описание рисков и ограничений. Изучите их перед принятием архитектурных решений.

<!-- alert-added -->

**Автор:** ab429  
**Хабр:** https://habr.com/ru/articles/1010030/  
**GitHub:** нет (туториал с полным кодом в статье)  
**Слой:** knowledge / ingestion  
**Дата:** март 2025  
**Уникальность:** Первый русскоязычный практический туториал по video-RAG с нативными мультимодальными эмбеддингами: Gemini Embedding 2 кодирует текст, изображения, видео и аудио в единое 1536-мерное пространство без промежуточного конвертирования в текст. Двойной канал: embed для поиска + Flash-описание для контекста LLM. Бенчмарк: 68.8 vs Amazon Nova 60.3 vs Voyage Multimodal 55.2 на видео-задачах.

## Проблема: текстовые эмбеддинги не работают для видео и изображений

```
Стандартный document RAG:
  PDF/HTML → text extraction → text chunks → text embeddings → search
  Проблема: видео, изображения, схемы → теряется визуальная информация

Традиционное решение:
  видео → keyframe extraction → image captioning → текст → text embedding
  Проблема: 
    → Caption теряет детали ("схема архитектуры" ≠ сама схема)
    → Двойная latency (caption + embed)
    → Галлюцинации в caption → плохой поиск

Gemini Embedding 2 решение:
  видео/изображение/аудио/текст → ОДИН эмбеддинг 1536d
  → Поиск в едином пространстве: "как устроена система?" 
    → находит и текстовые документы, и видео-объяснения, и схемы
```

## Архитектура нативного мультимодального RAG

```python
# ab429: Gemini Embedding 2 multimodal RAG
# habr.com/ru/articles/1010030/

from dataclasses import dataclass
from typing import Literal
import httpx
import json

MediaType = Literal["text", "image", "video", "audio"]

@dataclass
class MultimodalChunk:
    """
    Чанк мультимодального контента с эмбеддингом.

    Двойной канал:
    - embedding: для semantic search (Gemini Embedding 2)
    - description: для LLM-контекста (Gemini Flash caption)
    """
    chunk_id: str
    media_type: MediaType
    raw_content: bytes | str  # оригинальный контент
    description: str          # текстовое описание (для LLM)
    embedding: list[float]    # 1536-мерный вектор (для поиска)
    source_path: str
    metadata: dict            # timestamp для видео, размер для изображений


class GeminiMultimodalEmbedder:
    """
    Нативные мультимодальные эмбеддинги через Gemini Embedding 2.

    Ключевой принцип: текст, изображения, видео, аудио →
    единое 1536-мерное пространство → поиск через косинусное сходство.

    Без промежуточного caption/transcription.
    """

    EMBEDDING_DIM = 1536  # из доступных 3072 — ограничение pgvector HNSW

    def embed_text(self, text: str) -> list[float]:
        """Текст → 1536-мерный вектор."""
        response = self._call_gemini_embed(
            content={"text": text},
            output_dimensionality=self.EMBEDDING_DIM
        )
        return response["embedding"]["values"]

    def embed_image(self, image_bytes: bytes, mime_type: str = "image/png") -> list[float]:
        """Изображение → 1536-мерный вектор. БЕЗ промежуточного caption."""
        import base64
        b64 = base64.b64encode(image_bytes).decode()
        response = self._call_gemini_embed(
            content={
                "inlineData": {
                    "mimeType": mime_type,
                    "data": b64
                }
            },
            output_dimensionality=self.EMBEDDING_DIM
        )
        return response["embedding"]["values"]

    def embed_video_chunk(self, video_bytes: bytes) -> list[float]:
        """
        Видео-чанк → 1536-мерный вектор.
        Ограничение API: max 120 секунд на чанк.
        Рекомендуемый чанк: ~97 секунд с нахлёстом 15 секунд.
        """
        import base64
        b64 = base64.b64encode(video_bytes).decode()
        response = self._call_gemini_embed(
            content={
                "inlineData": {
                    "mimeType": "video/mp4",
                    "data": b64
                }
            },
            output_dimensionality=self.EMBEDDING_DIM
        )
        return response["embedding"]["values"]

    def _call_gemini_embed(self, content: dict, output_dimensionality: int) -> dict:
        """Вызов Gemini Embedding 2 API."""
        return httpx.post(
            "https://generativelanguage.googleapis.com/v1beta/models/"
            "gemini-embedding-2-preview:embedContent",
            headers={"x-goog-api-key": self._api_key},
            json={
                "content": {"parts": [content]},
                "outputDimensionality": output_dimensionality
            }
        ).json()
```

## Двойной канал: embed + describe

```python
class DualChannelIngestor:
    """
    Двойной канал для каждого медиафайла:
    1. Embed (Gemini Embedding 2) → для semantic search
    2. Describe (Gemini Flash) → для LLM-контекста при генерации ответа

    Почему двойной:
    - Embedding хорошо находит релевантный контент
    - Но LLM не может "видеть" embedding → нужен текст для контекста
    - Flash Caption генерирует описание для передачи в RAG prompt
    """

    def __init__(self, api_key: str):
        self.embedder = GeminiMultimodalEmbedder(api_key)
        self.flash_url = "https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent"
        self._api_key = api_key

    def ingest_image(self, image_bytes: bytes, source_path: str) -> MultimodalChunk:
        """Изображение → embed + описание."""
        import base64, uuid
        b64 = base64.b64encode(image_bytes).decode()

        # Канал 1: embedding для поиска
        embedding = self.embedder.embed_image(image_bytes)

        # Канал 2: описание для LLM
        description = self._flash_describe(
            content={
                "inlineData": {"mimeType": "image/png", "data": b64}
            },
            prompt="Опиши подробно что изображено на этой картинке/схеме"
        )

        return MultimodalChunk(
            chunk_id=str(uuid.uuid4()),
            media_type="image",
            raw_content=image_bytes,
            description=description,
            embedding=embedding,
            source_path=source_path,
            metadata={"size_bytes": len(image_bytes)}
        )

    def ingest_video(self, video_path: str) -> list[MultimodalChunk]:
        """
        Видео → список чанков (каждый ~97 сек).
        Нахлёст 15 секунд для континуальности.
        """
        chunks = self._split_video(video_path,
                                    chunk_duration=97,
                                    overlap=15)
        result = []
        for i, (chunk_bytes, start_sec, end_sec) in enumerate(chunks):
            embedding = self.embedder.embed_video_chunk(chunk_bytes)
            description = self._flash_describe(
                content={"inlineData": {"mimeType": "video/mp4",
                                         "data": self._b64(chunk_bytes)}},
                prompt=f"Видео {start_sec}-{end_sec} сек. Опиши что происходит."
            )
            result.append(MultimodalChunk(
                chunk_id=f"video_{i}",
                media_type="video",
                raw_content=chunk_bytes,
                description=description,
                embedding=embedding,
                source_path=video_path,
                metadata={"start_sec": start_sec, "end_sec": end_sec}
            ))
        return result

    def _flash_describe(self, content: dict, prompt: str) -> str:
        """Gemini Flash → текстовое описание медиа."""
        response = httpx.post(
            self.flash_url,
            headers={"x-goog-api-key": self._api_key},
            json={
                "contents": [{
                    "parts": [{"text": prompt}, content]
                }]
            }
        ).json()
        return response["candidates"][0]["content"]["parts"][0]["text"]
```

## Vector Store: pgvector + Supabase

```python
class MultimodalVectorStore:
    """
    Хранение и поиск мультимодальных чанков.
    PostgreSQL + pgvector (через Supabase) — HNSW индекс.

    Ограничение: HNSW в pgvector поддерживает до 2000 измерений.
    Поэтому используем 1536 из доступных 3072 у Gemini Embedding 2.
    """

    CREATE_TABLE_SQL = """
        CREATE TABLE IF NOT EXISTS multimodal_chunks (
            id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
            source_path TEXT,
            media_type TEXT,
            description TEXT,
            embedding VECTOR(1536),
            metadata JSONB,
            created_at TIMESTAMPTZ DEFAULT NOW()
        );

        CREATE INDEX IF NOT EXISTS idx_embedding_hnsw
        ON multimodal_chunks USING hnsw (embedding vector_cosine_ops)
        WITH (m = 16, ef_construction = 64);
    """

    SEARCH_SQL = """
        SELECT id, source_path, media_type, description, metadata,
               1 - (embedding <=> $1::vector) AS cosine_similarity
        FROM multimodal_chunks
        ORDER BY embedding <=> $1::vector
        LIMIT $2;
    """

    def search(self, query: str, top_k: int = 5) -> list[dict]:
        """
        Мультимодальный поиск по текстовому запросу.
        Запрос эмбеддится через Gemini Embedding 2 → косинусный поиск.
        Находит релевантные тексты, изображения, видео, аудио.
        """
        query_embedding = self.embedder.embed_text(query)

        rows = self.db.execute(
            self.SEARCH_SQL,
            (json.dumps(query_embedding), top_k)
        ).fetchall()

        return [
            {
                "source_path": row[1],
                "media_type": row[2],
                "description": row[3],  # текст для LLM-контекста
                "metadata": row[4],
                "score": row[5]
            }
            for row in rows
        ]


BENCHMARK_RESULTS = {
    "задача": "Video/Image retrieval benchmark (Google)",
    "метрики": {
        "gemini_embedding_2": 68.8,
        "amazon_nova_2": 60.3,
        "voyage_multimodal_35": 55.2
    },
    "размерность": 1536,
    "поддерживаемые_форматы": [".md", ".txt", ".png", ".jpg", ".mp4"],
    "чанкинг_видео": {
        "chunk_duration_sec": 97,
        "overlap_sec": 15,
        "max_api_limit_sec": 120
    }
}
```

## Полный RAG Pipeline

```python
class MultimodalRAGPipeline:
    """
    Полный pipeline: ingest → search → generate.

    Поддерживаемые форматы:
    .md/.txt → text chunks → text embeddings
    .png/.jpg → image embeddings + Flash caption
    .mp4 → video chunks (97 сек) + Flash description каждого чанка
    """

    def query(self, question: str, top_k: int = 5) -> str:
        """
        Ответить на вопрос, используя мультимодальную базу знаний.

        Pipeline:
        1. Embed вопрос → vector
        2. Cosine search → топ-K чанков (text/image/video смешанно)
        3. Aggregate descriptions → контекст для LLM
        4. Gemini Flash генерирует ответ с цитатами
        """
        # Поиск
        results = self.store.search(question, top_k)

        # Контекст: используем описания (Channel 2) для LLM
        context_parts = []
        for r in results:
            source = f"[{r['media_type']}: {r['source_path']}]"
            if r['media_type'] == 'video':
                ts = r['metadata']
                source += f" (время: {ts['start_sec']}-{ts['end_sec']} сек)"
            context_parts.append(f"{source}\n{r['description']}")

        context = "\n\n---\n\n".join(context_parts)

        # Генерация
        prompt = f"""Ответь на вопрос используя контекст из базы знаний.
Контекст включает текстовые документы, описания изображений и видео-фрагментов.

Вопрос: {question}

Контекст:
{context}

Ответ:"""

        return self.flash_generate(prompt)
```

## Применение к Lorenzo

```python
# Lorenzo: мультимодальный RAG для docs/

class LorenzoMultimodalKnowledge:
    """
    ab429 паттерн для Lorenzo:
    Индексировать не только .md файлы, но и:
    - Схемы архитектуры (.png) из docs/
    - Скринкасты демо (если появятся)
    - Диаграммы Mermaid → рендер в изображение → embed

    "Как устроен прототип Svyazi?" →
    найдёт и текстовое описание, и схему архитектуры из README
    """

    def index_docs_with_diagrams(self, docs_path: str):
        """
        Расширенная индексация docs/ с поддержкой изображений.
        Mermaid → PNG (через mmdc) → Gemini embed.
        """
        pass
```

## Возможные комбинации

| Комбинация | Новое свойство |
|------------|----------------|
| **Multimodal RAG + Temporal KG (R47)** | SAT-Graph + мультимодальные чанки: "покажи схему архитектуры Итерации 1 до добавления Review Queue" |
| **Multimodal RAG + LLM Observability (R45)** | Трейсинг: какой медиа-тип (текст/изображение/видео) чаще попадает в топ-K |
| **Multimodal RAG + Code MCP (R46)** | Архитектурные схемы + кодовый анализ в одном пространстве: "найди код, соответствующий этой диаграмме" |
| **Multimodal RAG + MWS Vision Bench (R45)** | Оценить качество мультимодального RAG на задачах из MWS Vision Bench |
| **Multimodal RAG + ColPali** | Patch-embeddings по страницам PDF (ColPali) + видео-чанки (Gemini) = полный мультимодальный corpus |

## Контакт

- Статья: https://habr.com/ru/articles/1010030/ (март 2025)
- Автор: ab429 (Хабр)
- Gemini Embedding 2: ai.google.dev/gemini-api/docs/embeddings
- pgvector: github.com/pgvector/pgvector
- Supabase: supabase.com (PostgreSQL + pgvector as a service)
- Смежная (Multimodal RAG v1 Docling, R19): docs/06-discovery/round-19/
- Смежная (MWS Vision Bench, R45): docs/06-discovery/round-45/projects/mts-ai-mws-vision-bench-business-ocr-vlm.md
- Смежная (Code MCP, R46): docs/06-discovery/round-46/projects/evgeniyrasuk-mcp-codebase-architectural-vision.md

## Смотрите также
- [Главная](../../../README.md)
- [Метрики](../../../METRICS.md)
- [Здоровье](../../../HEALTH.md)
- [Глоссарий](../../../GLOSSARY.md)
- [Сущности](../../../ENTITIES.md)
- [Решения](../../../DECISIONS.md)
