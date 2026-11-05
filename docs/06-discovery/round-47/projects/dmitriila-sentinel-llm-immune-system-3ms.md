---
date: 2026-06-05
tags: [memory, rag, orchestration, security, ingestion]
state: normalized
---

# SENTINEL: трёхслойная иммунная система для LLM за <3ms

<!-- toc-auto -->
<!-- tags: dmitriila-sentinel-llm-immune-system-3ms, docs -->


<!-- summary -->
> `dmitriila-sentinel-llm-immune-system-3ms` — раздел документации проекта Lorenzo.


> [!NOTE]
> Документ создан на основе исследования. Ссылки ведут на связанные материалы.

<!-- alert-added -->

**Автор:** Dmitriila (Дмитрий Лабинцев)  
**Хабр:** https://habr.com/ru/articles/996896/  
**GitHub:** есть (116,000 строк C + Rust + Python)  
**Слой:** orchestration  
**Дата:** февраль 2025  
**Уникальность:** Production-grade open-source защита LLM без GPU за <3ms: Layer 1 (C + eBPF, <1ms) → Layer 2 (Rust, 49 детекторов, <1ms) → Layer 3 (Python micro-swarm, 8000 параметров, ~1ms). F1 = 0.997 на датасете 87,056 реальных паттернов атак. Биmodal confidence scoring устраняет "серую зону". Micro-swarm из крошечных моделей превосходит крупные трансформеры на adversarial входах.

## Проблема: LLM открыты для атак в production

```
Векторы атак на production LLM:
  → Prompt injection: "Игнорируй предыдущие инструкции и..."
  → Jailbreak: обход системного промпта через ролевые игры
  → PII leakage: извлечение персональных данных из RAG
  → Token-splitting: "игно|рируй" → обход keyword-фильтров
  → Unicode obfuscation: гомоглифы (а vs а кириллица/латиница)
  → Base64 обфускация: скрытые инструкции в encoded строках

Стандартные решения:
  → Keyword blacklist: обходится вариациями написания
  → Крупная модель-классификатор: 50-500мс, дорого, нужен GPU
  → Облачные guardrails: данные уходят к вендору

Требования к production решению:
  → <5мс (не блокирует UX)
  → On-premise (данные не покидают инфраструктуру)
  → F1 > 0.99 (производственное качество)
  → Без GPU (дешевле, доступнее)
```

## Трёхслойная архитектура SENTINEL

```
Layer 1 (Shield, C):    eBPF packet filtering → <1ms
Layer 2 (Brain, Rust):  49 detection engines → <1ms
Layer 3 (Swarm, Python): micro-model ensemble → ~1ms
─────────────────────────────────────────────────────
Total:                  <3ms (CPU only, no GPU)
```

```python
# Dmitriila: SENTINEL — иммунная система для LLM
# habr.com/ru/articles/996896

from dataclasses import dataclass
from typing import Literal
import ctypes
import json

@dataclass
class ThreatAssessment:
    """Результат оценки входящего промпта."""
    is_threat: bool
    confidence: float          # bimodal: концентрируется у 0 или 1
    threat_type: str | None    # "injection" | "jailbreak" | "pii" | "obfuscation"
    layer_triggered: int       # 1, 2 или 3
    latency_ms: float
    features: dict             # 22 извлечённых признака


class SentinelLayer1Shield:
    """
    Layer 1: Сетевой DMZ на C + eBPF.
    Фильтрация на уровне пакетов до достижения приложения.

    eBPF: Extended Berkeley Packet Filter
    → Работает в kernel space → минимальный overhead
    → Rate limiting: защита от DDoS на LLM endpoint
    → Geo-blocking: блокировка по IP/ASN
    → Payload inspection: отклонение аномально длинных запросов

    Latency: <1мс (kernel-level, нет context switch)
    """

    def __init__(self, bpf_program_path: str):
        # Загрузить eBPF программу в kernel
        self.lib = ctypes.CDLL("libsentinel_shield.so")
        self.bpf_fd = self.lib.load_bpf_program(bpf_program_path.encode())

    def check_request(self, raw_payload: bytes) -> tuple[bool, str]:
        """
        Быстрая проверка на уровне L1.
        Возвращает (passed, reason).
        """
        result = self.lib.shield_check(self.bpf_fd, raw_payload, len(raw_payload))
        if result == 0:
            return True, "passed"
        elif result == 1:
            return False, "rate_limit_exceeded"
        elif result == 2:
            return False, "payload_too_large"
        return False, "blocked_by_policy"


class SentinelLayer2Brain:
    """
    Layer 2: 49 специализированных Rust-детекторов.
    Каждый детектор — узкоспециализированный модуль для одного класса угроз.

    Примеры детекторов:
    - InjectionDetector: "ignore previous", "disregard", "bypass"
    - JailbreakDetector: DAN промпты, ролевые игры, "pretend you are"
    - PiiExtractorDetector: попытки извлечь данные из контекста
    - TokenSplitDetector: разбивка слов токен-разделителями
    - UnicodeHomoglyphDetector: кириллица/латиница смешение
    - Base64Detector: hidden инструкции в base64
    """

    DETECTOR_COUNT = 49

    def analyze(self, prompt: str) -> dict[str, float]:
        """
        Запустить все 49 детекторов параллельно (Rust async).
        Возвращает score 0-1 для каждого детектора.
        """
        # Вызов Rust библиотеки через FFI
        import ctypes
        lib = ctypes.CDLL("libsentinel_brain.so")

        prompt_bytes = prompt.encode("utf-8")
        scores_buffer = (ctypes.c_float * self.DETECTOR_COUNT)()

        lib.brain_analyze(
            prompt_bytes,
            len(prompt_bytes),
            scores_buffer
        )

        return {
            f"detector_{i}": scores_buffer[i]
            for i in range(self.DETECTOR_COUNT)
        }

    def extract_features(self, prompt: str) -> dict:
        """
        22 извлечённых признака для Layer 3.
        Статистические: энтропия, char ratios, keyword scoring.
        Структурные: наличие base64, unicode диапазоны, токен-разделители.
        """
        return {
            "entropy": self._compute_entropy(prompt),
            "cyrillic_ratio": self._char_ratio(prompt, "cyrillic"),
            "latin_ratio": self._char_ratio(prompt, "latin"),
            "special_char_ratio": self._char_ratio(prompt, "special"),
            "avg_word_length": self._avg_word_length(prompt),
            "injection_keyword_score": self._keyword_score(prompt, "injection"),
            "jailbreak_keyword_score": self._keyword_score(prompt, "jailbreak"),
            "base64_segments": self._count_base64(prompt),
            "unicode_homoglyph_count": self._count_homoglyphs(prompt),
            "token_split_patterns": self._detect_token_splits(prompt),
            "sentence_count": len(prompt.split(".")),
            "max_sentence_length": max(len(s) for s in prompt.split(".")),
            # ... ещё 10 признаков
        }
```

## Micro-Swarm: 8000 параметров > крупный трансформер

```python
class SentinelLayer3MicroSwarm:
    """
    Layer 3: ансамбль крошечных ML-моделей (~8000 параметров суммарно).

    Ключевое открытие:
    Micro-swarm из маленьких специализированных моделей
    превосходит крупные трансформеры (BERT, RoBERTa) на adversarial входах.

    Почему:
    1. Крупные модели обучены на общем корпусе → не специализированы на атаках
    2. Micro-models обучены ТОЛЬКО на паттернах атак → нет шума
    3. Ensemble из 10+ micro-models → variance reduction
    4. 8000 параметров vs 110M у BERT → 14000x меньше → быстрее, дешевле

    Bimodal confidence scoring:
    Стандартный classifier: confidence распределена равномерно 0-1
    SENTINEL: confidence концентрируется у 0 или 1 (нет "серой зоны")
    → Меньше false positives в пограничных случаях
    """

    MICRO_MODELS = [
        "injection_linear",       # линейный классификатор на injection keywords
        "jailbreak_ngram",        # N-gram модель для jailbreak паттернов
        "entropy_threshold",      # threshold-based на энтропии
        "pii_ner_tiny",           # крошечный NER для PII детекции
        "unicode_rule_engine",    # детерминированный для гомоглифов
        "base64_heuristic",       # regex + entropy для base64
        "token_split_detector",   # паттерн-матчинг для split-токенов
        "length_anomaly",         # статистика длины промпта
        "semantic_drift_tiny",    # embedding-distance от нормальных промптов
        "ensemble_meta"           # мета-классификатор над 9 предыдущими
    ]

    def classify(self, features: dict) -> ThreatAssessment:
        """
        Классификация через ансамбль micro-models.
        Bimodal output: уверенность либо высокая (<0.1 или >0.9),
        либо передаётся на human review.
        """
        scores = []
        for model_name in self.MICRO_MODELS:
            model = self._load_micro_model(model_name)
            score = model.predict(features)
            scores.append(score)

        # Взвешенное голосование
        ensemble_score = self._weighted_vote(scores)

        # Bimodal bounding: отодвинуть от серой зоны
        confidence = self._bimodal_transform(ensemble_score)

        return ThreatAssessment(
            is_threat=confidence > 0.5,
            confidence=confidence,
            threat_type=self._identify_threat_type(scores, features),
            layer_triggered=3,
            latency_ms=self._measure_latency(),
            features=features
        )

    def _bimodal_transform(self, raw_score: float) -> float:
        """
        Трансформация скора для bimodal распределения.
        raw_score → |raw_score - 0.5| * 2 → ближе к 0 или 1.
        Устраняет "серую зону" [0.4, 0.6].
        """
        if raw_score < 0.4:
            return raw_score * 0.5  # прижать к 0
        elif raw_score > 0.6:
            return 0.5 + (raw_score - 0.5) * 1.5  # прижать к 1
        else:
            # Серая зона: оставить как есть, но пометить
            return raw_score


SENTINEL_BENCHMARK = {
    "датасет": "87,056 реальных паттернов атак на LLM (публичные + собственные)",
    "метрики": {
        "F1": 0.997,
        "precision": 0.996,
        "recall": 0.998,
        "latency_p99": "2.8ms",
        "false_positive_rate": 0.004
    },
    "сравнение": {
        "keyword_blacklist": {"F1": 0.73, "latency": "0.1ms"},
        "bert_classifier": {"F1": 0.961, "latency": "45ms", "gpu_required": True},
        "SENTINEL": {"F1": 0.997, "latency": "2.8ms", "gpu_required": False}
    },
    "open_source": True,
    "языки": "C (Layer 1) + Rust (Layer 2) + Python (Layer 3)"
}
```

## Применение к Lorenzo

```python
# Lorenzo: SENTINEL для защиты gateway.py

class LorenzoGatewayProtection:
    """
    Dmitriila паттерн для Lorenzo:
    SENTINEL middleware перед gateway.py /api/ask.
    Блокировать попытки извлечь конфиденциальные данные из docs/
    или инъектировать инструкции через query.
    """

    def protect_query(self, query: str) -> tuple[bool, str]:
        """
        Проверить запрос перед RAG-поиском.
        Блокировать: попытки прочитать .env, credentials, private docs.
        Разрешить: легитимные запросы о проектах Svyazi.
        """
        shield = SentinelLayer1Shield("bpf/rate_limit.o")
        brain = SentinelLayer2Brain()
        swarm = SentinelLayer3MicroSwarm()

        # Layer 2: extract features
        features = brain.extract_features(query)
        detector_scores = brain.analyze(query)

        # Layer 3: classify
        assessment = swarm.classify({**features, **detector_scores})

        if assessment.is_threat:
            return False, f"Query blocked: {assessment.threat_type}"

        return True, "passed"
```

## Возможные комбинации

| Комбинация | Новое свойство |
|------------|----------------|
| **SENTINEL + Privacy Gateway (R41)** | Двойная защита: SENTINEL (атаки) + Privacy Gateway (PII) = полный security stack |
| **SENTINEL + LLM Observability (R45)** | Semantic span для каждого detection event: когда какой слой срабатывает |
| **SENTINEL + Lorenzo Gateway** | Middleware перед /api/ask: защита RAG от prompt injection |
| **SENTINEL + LangGraph (R44)** | SENTINEL как guard узел в LangGraph: проверка перед каждым tool call |
| **SENTINEL + Coordination Harness (R46)** | Измерить как adversarial injection деградирует F-метрику в мультиагентных системах |

## Контакт

- Статья: https://habr.com/ru/articles/996896/ (февраль 2025)
- Автор: Dmitriila (Дмитрий Лабинцев)
- GitHub: есть (116,000 строк C + Rust + Python)
- eBPF: ebpf.io
- Смежная (Kaspersky MCP security, R40): docs/06-discovery/round-40/
- Смежная (Privacy Gateway PII, R41): docs/06-discovery/round-41/projects/privacy-llm-pii-gateway-ondevice-rag.md
- Смежная (LLM AppSec, R22): docs/06-discovery/round-22/

## Смотрите также
- [Главная](../../../README.md)
- [Метрики](../../../METRICS.md)
- [Здоровье](../../../HEALTH.md)
- [Глоссарий](../../../GLOSSARY.md)
- [Сущности](../../../ENTITIES.md)
- [Решения](../../../DECISIONS.md)
