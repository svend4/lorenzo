"""Cross-encoder реранкинг: улучшает precision@k после первичного retrieval."""
import re
from pathlib import Path
from typing import Protocol, runtime_checkable

from docstoolkit.rag.types import Passage


@runtime_checkable
class Reranker(Protocol):
    """Protocol для реранкеров: принимает query + passages, возвращает scores."""

    name: str

    def score(self, query: str, passages: list[Passage]) -> list[float]:
        """Возвращает scores параллельно списку passages."""
        ...


class NoOpReranker:
    """Не меняет оценки: возвращает исходные passage.score."""

    name = "noop"

    def score(self, query: str, passages: list[Passage]) -> list[float]:
        return [p.score for p in passages]


def _tokenize(text: str) -> set[str]:
    """Простая токенизация: слова ≥3 символов, строчные."""
    return set(re.findall(r'[а-яёa-z]{3,}', text.lower()))


class TFIDFReranker:
    """Лёгкий реранкер на основе unigram overlap (cosine similarity).

    Без внешних зависимостей: stdlib-only.
    """

    name = "tfidf"

    def score(self, query: str, passages: list[Passage]) -> list[float]:
        query_tokens = _tokenize(query)
        if not query_tokens:
            return [0.0] * len(passages)

        scores: list[float] = []
        for p in passages:
            passage_tokens = _tokenize(p.text)
            if not passage_tokens:
                scores.append(0.0)
                continue
            intersection = query_tokens & passage_tokens
            # Cosine similarity = |A ∩ B| / sqrt(|A| * |B|)
            import math
            sim = len(intersection) / math.sqrt(len(query_tokens) * len(passage_tokens))
            scores.append(sim)
        return scores


class LLMReranker:
    """Реранкер на основе LLM-оценок релевантности.

    Для каждого пассажа строит промпт и вызывает answerer, парсит float 0-10.
    """

    name = "llm"

    def __init__(self, answerer_name: str = "echo", batch_size: int = 5):
        self.answerer_name = answerer_name
        self.batch_size = batch_size
        self._answerer = None

    def _get_answerer(self):
        if self._answerer is None:
            from docstoolkit.rag.answerer import get_answerer
            self._answerer = get_answerer(self.answerer_name)
        return self._answerer

    def _score_single(self, query: str, passage: Passage) -> float:
        prompt = (
            f"On scale 0-10, how relevant is this passage to the query? "
            f"Query: {query}\n"
            f"Passage: {passage.text[:300]}\n"
            f"Answer with just a number."
        )
        answerer = self._get_answerer()
        try:
            answer_text, _, _ = answerer.answer(system="You are a relevance judge.", user=prompt)
            # Parse first float/int from response
            match = re.search(r'\b([0-9]+(?:\.[0-9]+)?)\b', answer_text)
            if match:
                val = float(match.group(1))
                return min(10.0, max(0.0, val))
            return 0.0
        except Exception:
            return 0.0

    def score(self, query: str, passages: list[Passage]) -> list[float]:
        scores: list[float] = []
        # Process in batches (currently sequential but grouped for future async)
        for i in range(0, len(passages), self.batch_size):
            batch = passages[i:i + self.batch_size]
            for p in batch:
                scores.append(self._score_single(query, p))
        return scores


class BGEReranker:
    """Опциональный реранкер на основе BGE cross-encoder.

    Требует sentence_transformers или transformers.
    При отсутствии зависимостей gracefully fallback на TFIDFReranker.
    """

    name = "bge"

    def __init__(
        self,
        model_name: str = "BAAI/bge-reranker-base",
        cache_dir: Path | None = None,
    ):
        self.model_name = model_name
        self.cache_dir = cache_dir
        self._available: bool = False
        self._model = None
        self._tokenizer = None
        self._use_sentence_transformers: bool = False
        self._tfidf_fallback = TFIDFReranker()

    def _load_model(self):
        """Lazy load: пробует sentence_transformers, затем transformers."""
        if self._model is not None or not self._available:
            return

        cache = str(self.cache_dir) if self.cache_dir else None

        try:
            from sentence_transformers import CrossEncoder  # type: ignore
            self._model = CrossEncoder(self.model_name, cache_folder=cache)
            self._use_sentence_transformers = True
            self._available = True
            return
        except ImportError:
            pass

        try:
            from transformers import (  # type: ignore
                AutoModelForSequenceClassification,
                AutoTokenizer,
            )
            kwargs = {}
            if cache:
                kwargs["cache_dir"] = cache
            self._tokenizer = AutoTokenizer.from_pretrained(self.model_name, **kwargs)
            self._model = AutoModelForSequenceClassification.from_pretrained(
                self.model_name, **kwargs
            )
            self._model.eval()
            self._available = True
        except ImportError:
            self._available = False

    def _try_init(self):
        """Вызывается один раз для проверки доступности зависимостей."""
        # Try importing without actually loading the model weights
        try:
            import sentence_transformers  # noqa: F401
            self._available = True
        except ImportError:
            try:
                import transformers  # noqa: F401
                self._available = True
            except ImportError:
                self._available = False

    def score(self, query: str, passages: list[Passage]) -> list[float]:
        # Check availability lazily
        if self._model is None and not self._available:
            # Try once to detect availability
            self._try_init()

        if not self._available:
            return self._tfidf_fallback.score(query, passages)

        try:
            self._load_model()
        except Exception:
            self._available = False
            return self._tfidf_fallback.score(query, passages)

        if not self._available or self._model is None:
            return self._tfidf_fallback.score(query, passages)

        try:
            if self._use_sentence_transformers:
                pairs = [[query, p.text[:512]] for p in passages]
                raw_scores = self._model.predict(pairs)
                return [float(s) for s in raw_scores]
            else:
                import torch  # type: ignore
                scores: list[float] = []
                for p in passages:
                    inputs = self._tokenizer(
                        query, p.text[:512],
                        return_tensors="pt",
                        truncation=True,
                        max_length=512,
                    )
                    with torch.no_grad():
                        logits = self._model(**inputs).logits
                    scores.append(float(logits[0][0]))
                return scores
        except Exception:
            return self._tfidf_fallback.score(query, passages)


def rerank(
    query: str,
    passages: list[Passage],
    reranker: Reranker,
    top_k: int | None = None,
) -> list[Passage]:
    """Реранкирует passages: сортирует по score, обрезает top_k.

    Возвращает новый список Passage с обновлёнными score.
    """
    from dataclasses import replace

    if not passages:
        return []

    scores = reranker.score(query, passages)

    # Build (score, passage) pairs, update score field
    scored = [
        replace(p, score=s) for p, s in zip(passages, scores)
    ]
    scored.sort(key=lambda p: p.score, reverse=True)

    if top_k is not None:
        scored = scored[:top_k]

    return scored


def get_reranker(name: str, **kwargs) -> Reranker:
    """Фабрика реранкеров по имени.

    Поддерживает: "noop", "tfidf", "llm", "bge".
    """
    if name == "noop":
        return NoOpReranker()
    if name == "tfidf":
        return TFIDFReranker()
    if name == "llm":
        return LLMReranker(**kwargs)
    if name == "bge":
        return BGEReranker(**kwargs)
    raise ValueError(f"Неизвестный реранкер: {name!r}. Доступны: noop, tfidf, llm, bge")
