---
date: 2026-06-05
tags: [memory, rag, security, knowledge, ingestion]
state: normalized
---

# Privacy-первый LLM: PII-прокси, on-device RAG, WebGPU inference

<!-- toc-auto -->
<!-- tags: privacy-llm-pii-gateway-ondevice-rag, docs -->


<!-- summary -->
> Каждый паттерн решает конкретный threat model: утечка промптов в облако, меморизация персональных данных LLM, ненадёжный провайдер.


> [!WARNING]
> Документ содержит описание рисков и ограничений. Изучите их перед принятием архитектурных решений.

<!-- alert-added -->

**Автор:** MaximML (ML Team Lead)  
**Хабр:** https://habr.com/ru/articles/988774/  
**GitHub:** нет (pet-проекты, blueprint-уровень)  
**Слой:** orchestration / analytics  
**Дата:** январь 2026  
**Уникальность:** Практический каталог 7 privacy-архитектур для LLM от ML-практика: Privacy-Gateway (PII-прокси с NER-заменой и аудит-логом), On-Device RAG (локальный FAISS + LLM без передачи данных), In-Browser inference (WebGPU/WebLLM с квантизированными 1-3B моделями). Каждый паттерн решает конкретный threat model: утечка промптов в облако, меморизация персональных данных LLM, ненадёжный провайдер. Написано с признанием реальных ограничений (false-positive NER, context leakage).

## Проблема: персональные данные уходят в облачный LLM

```
Сценарий 1: Юрист использует ChatGPT для анализа договора
  → Договор содержит: имена, суммы, ИНН, условия
  → OpenAI получает конфиденциальные данные клиента
  → GDPR/152-ФЗ нарушены

Сценарий 2: Медицинская организация → RAG по историям болезней
  → История болезни → в облачный эмбеддинг-сервис → в облачный LLM
  → Персональные медицинские данные покидают контур

Сценарий 3: Банк → LLM-ассистент для операционистов
  → Запрос: "Какой лимит у клиента Иванова 4242-4242-4242-4242?"
  → Карточные данные в промпте → в логах провайдера

Три архитектурных ответа (MaximML, 2026):
  1. Privacy-Gateway: замени PII перед отправкой, восстанови в ответе
  2. On-Device RAG: весь стек локально, данные не покидают машину
  3. In-Browser: inference в браузере клиента, сервер данных не видит
```

## Паттерн 1: Privacy-Gateway — PII-прокси

```python
# MaximML: Privacy-Gateway
# Reverse-proxy: стрипает PII → облачный LLM → восстанавливает

import re
import uuid
import hashlib
from dataclasses import dataclass, field

@dataclass
class PIISubstitution:
    """Маппинг: реальное значение → токен-заменитель."""
    original: str
    placeholder: str           # "[PERSON_1]", "[CARD_1]", "[INN_1]"
    pii_type: str              # "person", "card_number", "inn", "phone"
    session_id: str


class PrivacyGateway:
    """
    PII-прокси между клиентом и облачным LLM.
    Принцип: LLM видит только анонимизированный текст.

    Реальные ограничения (MaximML):
    - NER false positives: "Иванов" в "ул. Иванова" → ложная замена
    - Context leakage: уникальные детали проекта → LLM может идентифицировать
    - Не защищает от inference атак на паттерны данных
    """

    def __init__(self):
        self.substitutions: dict[str, list[PIISubstitution]] = {}

        # Русскоязычные NER правила (regex + heuristics)
        self.pii_patterns = {
            "card_number": r"\b\d{4}[\s-]\d{4}[\s-]\d{4}[\s-]\d{4}\b",
            "phone_ru":    r"\b(?:\+7|8)[\s-]?\(?\d{3}\)?[\s-]?\d{3}[\s-]?\d{2}[\s-]?\d{2}\b",
            "inn":         r"\b\d{10,12}\b",  # ИНН 10 или 12 цифр
            "passport":    r"\b\d{4}\s\d{6}\b",
            "email":       r"\b[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}\b"
        }

    def anonymize(self, text: str, session_id: str) -> tuple[str, list[PIISubstitution]]:
        """
        Замена PII на токены перед отправкой в облако.
        Возвращает анонимизированный текст + маппинг для восстановления.
        """
        anonymized = text
        subs = []
        counters = {}

        # Regex-based замена структурированных данных
        for pii_type, pattern in self.pii_patterns.items():
            for match in re.finditer(pattern, anonymized):
                original = match.group()
                counters[pii_type] = counters.get(pii_type, 0) + 1
                placeholder = f"[{pii_type.upper()}_{counters[pii_type]}]"

                sub = PIISubstitution(original, placeholder, pii_type, session_id)
                subs.append(sub)
                anonymized = anonymized.replace(original, placeholder, 1)

        # NER-based замена персональных имён (pymorphy2 + словарь)
        anonymized, name_subs = self._anonymize_names(anonymized, session_id)
        subs.extend(name_subs)

        return anonymized, subs

    def restore(self, response: str, subs: list[PIISubstitution]) -> str:
        """
        Обратная замена: токены → реальные значения в ответе LLM.
        """
        restored = response
        for sub in subs:
            restored = restored.replace(sub.placeholder, sub.original)
        return restored

    def _anonymize_names(self, text: str,
                          session_id: str) -> tuple[str, list[PIISubstitution]]:
        """
        NER для русских имён: pymorphy2 + эвристики.
        Осторожно: высокий false-positive rate (MaximML предупреждает).
        """
        # Реализация: морфологический анализатор + список имён
        # False positive: "Иванов" в "метод Иванова" → ложно
        return text, []  # упрощённо


class AuditLog:
    """
    Аудит-лог: кто, когда, какие PII-типы были в запросе.
    Не хранит реальные значения — только типы и хеши.
    """

    def log_request(self, session_id: str,
                     pii_types: list[str],
                     text_hash: str) -> None:
        entry = {
            "session_id": session_id,
            "timestamp": __import__("datetime").datetime.utcnow().isoformat(),
            "pii_types_found": pii_types,
            "text_hash": text_hash  # SHA-256 анонимизированного текста
        }
        # Сохранить в защищённый лог
```

## Паттерн 2: On-Device RAG — локальный стек без передачи данных

```python
# MaximML: On-Device RAG
# Полный стек локально: FAISS + local embeddings + local LLM

import faiss
import numpy as np
from pathlib import Path

class OnDeviceRAG:
    """
    RAG полностью на локальной машине:
    - Документы: PDF/MD/TXT в локальной папке
    - Эмбеддинги: локальная модель (sentence-transformers, GGUF)
    - Индекс: FAISS (in-memory или файловый)
    - LLM: Ollama / llama.cpp локально

    Zero data egress: ни один байт документов не покидает машину.
    """

    def __init__(self, docs_path: str, model_name: str = "all-MiniLM-L6-v2"):
        from sentence_transformers import SentenceTransformer
        self.embedder = SentenceTransformer(model_name)
        self.docs_path = Path(docs_path)
        self.index = None
        self.chunks = []

    def build_index(self) -> None:
        """
        Индексирование всех документов из локальной папки.
        Чанкинг: 512 символов с перекрытием 128.
        """
        all_chunks = []
        for doc_path in self.docs_path.rglob("*.md"):
            text = doc_path.read_text(encoding="utf-8")
            chunks = self._chunk(text, size=512, overlap=128)
            all_chunks.extend([(c, str(doc_path)) for c in chunks])

        self.chunks = all_chunks
        texts = [c for c, _ in all_chunks]

        # Локальное эмбеддирование
        embeddings = self.embedder.encode(texts, normalize_embeddings=True)

        # FAISS: Inner Product (= cosine для нормализованных)
        dim = embeddings.shape[1]
        self.index = faiss.IndexFlatIP(dim)
        self.index.add(embeddings.astype(np.float32))

    def query(self, question: str, top_k: int = 5) -> list[dict]:
        """
        Локальный поиск: эмбеддинг запроса → FAISS → топ-K чанков.
        """
        q_embedding = self.embedder.encode([question], normalize_embeddings=True)
        scores, indices = self.index.search(q_embedding.astype(np.float32), top_k)

        results = []
        for score, idx in zip(scores[0], indices[0]):
            if idx >= 0:
                chunk, source = self.chunks[idx]
                results.append({"text": chunk, "source": source, "score": float(score)})
        return results

    def answer(self, question: str) -> str:
        """
        RAG ответ через локальный Ollama LLM.
        Данные не покидают машину.
        """
        import subprocess, json
        context_docs = self.query(question)
        context = "\n\n".join([d["text"] for d in context_docs])

        prompt = f"""Используй только следующий контекст для ответа.
Контекст:
{context}

Вопрос: {question}
Ответ:"""

        # Ollama local API
        result = subprocess.run(
            ["ollama", "run", "mistral", prompt],
            capture_output=True, text=True, timeout=60
        )
        return result.stdout.strip()
```

## Паттерн 3: In-Browser Inference с WebGPU

```python
# MaximML: In-Browser LLM через WebGPU/WebLLM
# Клиентская сторона: модель загружается в браузер
# Сервер НЕ видит промпты пользователя

WEBLLM_CONFIG = {
    "библиотека": "WebLLM (MLC LLM)",
    "url": "https://webllm.mlc.ai",
    "принцип": "WASM + WebGPU: квантизированная модель в браузере",

    "поддерживаемые_модели": [
        "Llama-3.2-1B-Instruct-q4f32_1-MLC",   # 1B, ~600MB
        "Llama-3.2-3B-Instruct-q4f32_1-MLC",   # 3B, ~1.5GB
        "Phi-3.5-mini-instruct-q4f16_1-MLC",   # 3.8B, ~2GB
        "Gemma-2-2b-it-q4f16_1-MLC"            # 2B, ~1.3GB
    ],

    "требования": {
        "браузер": "Chrome 113+ / Edge 113+ (WebGPU required)",
        "RAM": "4-8 GB доступной памяти",
        "первый_запуск": "Загрузка модели ~600MB-2GB (кэшируется)"
    },

    "threat_model": "Провайдер не видит промпты; данные остаются в браузере"
}

WEBLLM_JS = """
// JavaScript: WebLLM в браузере
import * as webllm from "https://esm.run/@mlc-ai/web-llm";

const engine = await webllm.CreateMLCEngine(
  "Llama-3.2-1B-Instruct-q4f32_1-MLC",
  { initProgressCallback: (progress) => console.log(progress) }
);

// Inference полностью в браузере
const response = await engine.chat.completions.create({
  messages: [{ role: "user", content: "Анализируй этот контракт: ..." }]
});
// Сервер ничего не видит
"""
```

## Матрица выбора privacy-архитектуры

```python
PRIVACY_DECISION_MATRIX = {
    "Privacy-Gateway": {
        "когда_использовать": "Структурированные PII (номера карт, ИНН, телефоны) + нужен облачный LLM",
        "не_подходит":        "Уникальные контекстуальные данные (context leakage)",
        "сложность":          "Средняя (NER + маппинг + аудит)",
        "защита_от":          "Прямой передачи идентификаторов в облако"
    },
    "On-Device RAG": {
        "когда_использовать": "Конфиденциальные документы + сервер доступен + 152-ФЗ/GDPR",
        "не_подходит":        "Слабое железо, нужна мощь GPT-4o",
        "сложность":          "Высокая (инфраструктура: Ollama + FAISS + embedder)",
        "защита_от":          "Любой передачи данных за периметр"
    },
    "In-Browser": {
        "когда_использовать": "B2C: пользователь не доверяет серверу; конфиденциальный чат",
        "не_подходит":        "Сложные задачи требующие больших моделей",
        "сложность":          "Низкая (WebLLM + JS), но ограниченные модели",
        "защита_от":          "Утечки через сервер; подходит для личных ассистентов"
    }
}
```

## Применение к Lorenzo

```python
# Lorenzo: privacy-first режим для конфиденциальных документов

class LorenzoPrivacyMode:
    """
    MaximML паттерны для Lorenzo:
    При работе с конфиденциальными корпусами (договоры, медданные)
    переключить в privacy-режим.
    """

    def ask_private(self, question: str, docs_path: str) -> str:
        """On-Device RAG: весь стек локально, данные не покидают сервер."""
        rag = OnDeviceRAG(docs_path, model_name="all-MiniLM-L6-v2")
        rag.build_index()
        return rag.answer(question)

    def ask_with_pii_strip(self, question: str) -> str:
        """
        Privacy-Gateway для /api/ask:
        PII → токены → Claude API → восстановление.
        Аудит-лог всех запросов с PII-типами.
        """
        gateway = PrivacyGateway()
        anonymized, subs = gateway.anonymize(question, session_id="session_1")
        raw_answer = self._call_claude(anonymized)
        return gateway.restore(raw_answer, subs)
```

## Возможные комбинации

| Комбинация | Новое свойство |
|------------|----------------|
| **Privacy RAG + Enterprise RAG МТС (R32)** | Privacy-Gateway перед МТС enterprise pipeline для конфиденциальных запросов |
| **Privacy RAG + 5-Layer Memory (R39)** | Локальная pgvector-память без передачи персональных данных в облако |
| **Privacy Gateway + AISecurity (R37)** | FLAME guard + PII-strip: двойная защита для финансовых/медицинских чатботов |
| **On-Device RAG + Kaspersky MCP (R40)** | Локальный codegen анализ логов безопасности без передачи логов в облако |
| **Privacy + Lorenzo Gateway** | /api/ask в privacy-режиме: PII-strip перед Claude, on-device FAISS резерв |

## Контакт

- Статья: https://habr.com/ru/articles/988774/ (январь 2026)
- WebLLM: webllm.mlc.ai (github.com/mlc-ai/web-llm)
- FAISS: github.com/facebookresearch/faiss
- OpenFHE (FHE для LLM): github.com/openfheorg/openfhe-development
- Смежная (FHE + LLM, GlobalSign): https://habr.com/ru/companies/globalsign/articles/979114/
- Смежная (приватный LLM, Sberbank обзор): https://habr.com/ru/companies/sberbank/articles/845388/

## Смотрите также
- [Главная](../../../README.md)
- [Метрики](../../../METRICS.md)
- [Здоровье](../../../HEALTH.md)
- [Глоссарий](../../../GLOSSARY.md)
- [Сущности](../../../ENTITIES.md)
- [Решения](../../../DECISIONS.md)
