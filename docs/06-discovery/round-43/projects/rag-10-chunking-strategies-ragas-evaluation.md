# RAG высоконагруженных систем: 10 стратегий чанкинга + RAGAS оценка

**Автор:** Tianno (Андрей Носов)  
**Хабр:** https://habr.com/ru/companies/oleg-bunin/articles/967102/  
**GitHub:** нет (образовательная статья)  
**Слой:** orchestration / analytics  
**Дата:** декабрь 2025  
**Уникальность:** Системная классификация 10 стратегий чанкинга для production RAG с оценкой через RAGAS на 100-примерном golden benchmark (три уровня сложности). Покрыты: fixed-size, sentence, semantic clustering, recursive/hierarchical, topic-based (LDA), modality-aware (текст/таблицы/изображения), agentic auto-selection, гибридный. Интеграция с Weaviate, Qwen/Llama/Gemma. CI/CD-интегрированные RAGAS-метрики (Recall, Precision, Faithfulness) как gates качества.

## Проблема: один размер чанка не работает для всех документов

```
Типичная ошибка в RAG:
  → Зафиксировать chunk_size=512 токенов на всё
  → Применить ко всем документам одинаково
  → Результат: разрыв таблиц, потеря контекста, шум

Реальные документы разные:
  → Научная статья: абзацы = логические единицы
  → Финансовый отчёт: таблицы = атомарные единицы
  → Руководство пользователя: разделы = иерархия
  → Код + документация: mixed modality

Стоимость неправильного чанкинга:
  → RAGAS Recall падает: чанк содержит только часть ответа
  → RAGAS Faithfulness падает: LLM галлюцинирует из-за шума
  → False negatives: нужный факт разбит между чанками
  → False positives: нерелевантный контекст попадает в промпт
```

## 10 стратегий чанкинга

```python
# Tianno: 10 chunking strategies для production RAG
# habr.com/ru/companies/oleg-bunin/articles/967102

from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Optional
import re

@dataclass
class Chunk:
    text: str
    metadata: dict
    strategy_used: str
    chunk_index: int
    doc_id: str


class BaseChunker(ABC):
    @abstractmethod
    def chunk(self, text: str, metadata: dict) -> list[Chunk]:
        pass


# Стратегия 1: Fixed-Size (базовая)
class FixedSizeChunker(BaseChunker):
    """
    Простейший: разбивка по N токенов с перекрытием.
    Плюсы: предсказуемо, быстро.
    Минусы: разрывает предложения, таблицы, списки.
    Применение: однородный текст без структуры.
    """
    def __init__(self, chunk_size: int = 512, overlap: int = 64):
        self.chunk_size = chunk_size
        self.overlap = overlap

    def chunk(self, text: str, metadata: dict) -> list[Chunk]:
        tokens = text.split()
        chunks = []
        for i in range(0, len(tokens), self.chunk_size - self.overlap):
            chunk_tokens = tokens[i:i + self.chunk_size]
            chunks.append(Chunk(
                text=" ".join(chunk_tokens),
                metadata=metadata,
                strategy_used="fixed_size",
                chunk_index=len(chunks),
                doc_id=metadata.get("doc_id", "")
            ))
        return chunks


# Стратегия 2: Sentence-Based
class SentenceChunker(BaseChunker):
    """
    Разбивка по предложениям, объединение до max_tokens.
    Плюсы: сохраняет семантическую целостность предложений.
    Минусы: плохо работает с маркированными списками.
    """
    def chunk(self, text: str, metadata: dict) -> list[Chunk]:
        import nltk
        sentences = nltk.sent_tokenize(text, language="russian")
        # Объединять предложения до max_tokens
        return self._merge_sentences(sentences, max_tokens=512, metadata=metadata)


# Стратегия 3: Semantic Clustering
class SemanticChunker(BaseChunker):
    """
    Embedding-based: группировать семантически близкие предложения.
    Сравнивать cosine similarity между соседними предложениями.
    При падении similarity ниже threshold → новый чанк.

    Плюсы: семантически связные чанки.
    Минусы: медленно (эмбеддинг каждого предложения), дорого.
    Применение: разнородный контент, mix тем.
    """
    def __init__(self, embedder, threshold: float = 0.75):
        self.embedder = embedder
        self.threshold = threshold

    def chunk(self, text: str, metadata: dict) -> list[Chunk]:
        sentences = text.split(". ")
        embeddings = self.embedder.encode(sentences)

        chunks, current = [], [sentences[0]]
        for i in range(1, len(sentences)):
            sim = self._cosine(embeddings[i-1], embeddings[i])
            if sim < self.threshold:
                chunks.append(self._make_chunk(current, metadata, len(chunks)))
                current = []
            current.append(sentences[i])

        if current:
            chunks.append(self._make_chunk(current, metadata, len(chunks)))
        return chunks


# Стратегия 4: Recursive/Hierarchical
class RecursiveChunker(BaseChunker):
    """
    LangChain RecursiveTextSplitter логика:
    Пробовать разделители по приоритету: \n\n → \n → . → пробел
    Плюсы: сохраняет структуру (параграфы → предложения → слова).
    Применение: структурированные тексты с заголовками.
    """
    SEPARATORS = ["\n\n", "\n", ". ", " ", ""]

    def chunk(self, text: str, metadata: dict) -> list[Chunk]:
        return self._recursive_split(text, self.SEPARATORS, metadata)


# Стратегия 5: Topic-Based (LDA)
class TopicBasedChunker(BaseChunker):
    """
    Latent Dirichlet Allocation: определить темы → разбивать по границам тем.
    Плюсы: топически связные чанки.
    Минусы: требует обучения LDA-модели, медленно.
    Применение: большие корпуса смешанных документов.
    """
    def chunk(self, text: str, metadata: dict) -> list[Chunk]:
        from sklearn.decomposition import LatentDirichletAllocation
        from sklearn.feature_extraction.text import CountVectorizer
        # LDA на параграфах → определить границы смены темы
        paragraphs = text.split("\n\n")
        topics = self._assign_topics(paragraphs)
        return self._split_by_topic_boundaries(paragraphs, topics, metadata)


# Стратегия 6: Modality-Aware
class ModalityAwareChunker(BaseChunker):
    """
    Детектировать тип контента → применять стратегию:
    Таблицы → сохранять целиком (не разбивать)
    Код → сохранять функцию/класс целиком
    Изображения → caption + alt text
    Текст → sentence-based
    """
    def chunk(self, text: str, metadata: dict) -> list[Chunk]:
        segments = self._detect_modalities(text)
        chunks = []
        for segment in segments:
            if segment["type"] == "table":
                chunks.append(self._chunk_table(segment, metadata))
            elif segment["type"] == "code":
                chunks.append(self._chunk_code(segment, metadata))
            else:
                chunks.extend(SentenceChunker().chunk(segment["text"], metadata))
        return chunks


# Стратегия 7: Agentic Auto-Selection
class AgenticChunker(BaseChunker):
    """
    LLM выбирает стратегию чанкинга для каждого документа.
    Анализирует структуру → выбирает лучший чанкер.

    Дорого, но оптимально для разнородных корпусов.
    """
    CHUNKER_MAP = {
        "tabular": ModalityAwareChunker(),
        "narrative": SemanticChunker(embedder=None),
        "structured": RecursiveChunker(),
        "mixed": ModalityAwareChunker()
    }

    def chunk(self, text: str, metadata: dict) -> list[Chunk]:
        doc_type = self._llm_classify(text[:500])  # первые 500 символов
        chunker = self.CHUNKER_MAP.get(doc_type, FixedSizeChunker())
        return chunker.chunk(text, metadata)


# Стратегия 8: Hybrid (Production Winner)
class HybridChunker(BaseChunker):
    """
    Production-рекомендация: 3-стадийный гибрид.
    1. Regex: детект структурных границ (заголовки, таблицы, код)
    2. Topic modeling: тематические границы внутри секций
    3. Semantic: финальная проверка связности чанков

    Наилучший RAGAS на 3-уровневом benchmark (Tianno).
    """
    def chunk(self, text: str, metadata: dict) -> list[Chunk]:
        # Стадия 1: Структурные границы
        structural = self._split_by_structure(text)

        # Стадия 2: Тематические границы
        topic_split = []
        for section in structural:
            topic_split.extend(TopicBasedChunker().chunk(section, metadata))

        # Стадия 3: Семантическая проверка
        return self._merge_incoherent(topic_split)
```

## RAGAS Evaluation Framework

```python
from ragas import evaluate
from ragas.metrics import (
    faithfulness,
    answer_recall,
    context_precision,
    answer_relevancy
)

class RAGASEvaluator:
    """
    Оценка RAG-системы на golden benchmark.
    100 примеров, 3 уровня сложности: простые/средние/сложные вопросы.
    """

    GOLDEN_BENCHMARK = {
        "easy": 40,    # факты из одного чанка
        "medium": 40,  # факты из 2-3 чанков
        "hard": 20     # multi-hop reasoning, таблицы
    }

    def evaluate_chunker(self, chunker: BaseChunker,
                          docs: list[str],
                          questions_answers: list[dict]) -> dict:
        """
        Pipeline: чанкинг → индексирование → retrieval → LLM → RAGAS.
        """
        # Построить индекс с данным чанкером
        chunks = []
        for doc in docs:
            chunks.extend(chunker.chunk(doc, {}))

        self.vector_db.index(chunks)

        # Ответить на вопросы
        results = []
        for qa in questions_answers:
            retrieved = self.vector_db.search(qa["question"], top_k=5)
            answer = self.llm.generate(qa["question"], retrieved)
            results.append({
                "question": qa["question"],
                "answer": answer,
                "contexts": [c.text for c in retrieved],
                "ground_truth": qa["answer"]
            })

        # RAGAS метрики
        return evaluate(
            dataset=results,
            metrics=[faithfulness, answer_recall,
                     context_precision, answer_relevancy]
        )

# Результаты сравнения (из статьи)
CHUNKING_BENCHMARK = {
    "winner": "Hybrid (regex + topic + semantic)",
    "метрики_winner": {
        "faithfulness": 0.91,
        "answer_recall": 0.88,
        "context_precision": 0.84,
        "answer_relevancy": 0.87
    },
    "loser": "Fixed-Size 512 tokens",
    "метрики_loser": {
        "faithfulness": 0.74,
        "answer_recall": 0.71,
        "context_precision": 0.68,
        "answer_relevancy": 0.73
    },
    "стек": ["Weaviate", "Qwen2.5/Llama3/Gemma2"],
    "benchmark_size": "100 QA пар (40 easy + 40 medium + 20 hard)"
}
```

## Применение к Lorenzo

```python
# Lorenzo: адаптивный чанкинг для improve_chunk_semantic.py

class LorenzoAdaptiveChunker:
    """
    Tianno паттерн для Lorenzo:
    Разные стратегии для разных типов docs/:
    - session-log.md: sentence-based (нарративный)
    - project/*.md: modality-aware (код + текст)
    - README.md: recursive (структурированный)
    - CONTACTS.md: fixed-size (однородный)
    """

    def chunk_doc(self, path: str, content: str) -> list[Chunk]:
        if "session-log" in path:
            return SentenceChunker().chunk(content, {"path": path})
        elif "projects/" in path:
            return ModalityAwareChunker().chunk(content, {"path": path})
        elif content.count("#") > 10:
            return RecursiveChunker().chunk(content, {"path": path})
        else:
            return FixedSizeChunker(chunk_size=400).chunk(content, {"path": path})
```

## Возможные комбинации

| Комбинация | Новое свойство |
|------------|----------------|
| **Chunking + Graph RAG (R38)** | Модальный чанкинг → Skeleton Indexing: правильные чанки для извлечения сущностей |
| **Chunking + Академия РАНХиГС (R40)** | Гибридный чанкинг нормативных документов РАНХиГС → лучший RAG-поиск |
| **Chunking + LangFuse (R38)** | RAGAS в CI через LangFuse: отслеживать деградацию качества при смене чанкера |
| **Chunking + Lorenzo Gateway** | /api/ask с adaptive chunker: разные стратегии для разных типов документов |
| **Chunking + Structured Output (R40)** | Outlines для gарантированного RAGAS JSON output (без retry) |

## Контакт

- Статья: https://habr.com/ru/companies/oleg-bunin/articles/967102/ (декабрь 2025)
- Oleg Bunin Conf: highload.ru
- RAGAS: github.com/explodinggradients/ragas
- Weaviate: weaviate.io
- Смежная (Graph RAG + Skeleton Indexing, VladSpace): https://habr.com/ru/articles/1003064/
- Смежная (Agentic RAG eval, Stryker Testing аналог): https://habr.com/ru/articles/918548/
