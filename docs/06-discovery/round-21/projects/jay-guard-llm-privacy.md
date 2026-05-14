# Jay Guard — динамическая анонимизация данных для LLM API

**Автор:** команда Just AI (российская AI-компания)  
**Хабр:** https://habr.com/ru/companies/just_ai/articles/946392/  
**GitHub:** не опубликован (production-инструмент, архитектура описана + benchmark на HuggingFace)  
**Слой:** orchestration / knowledge / ingestion  
**Дата:** 2025  
**Уникальность:** Первый открыто-описанный российский middleware для защиты персональных данных при работе с LLM API. Jay Guard = intelligent proxy между пользователем и LLM: перехватывает запросы, анонимизирует ПД, передаёт в модель, деанонимизирует ответ. Benchmark на HuggingFace с анонимизированными данными.

## Контекст: почему важно в РФ

```
Российское законодательство (ФЗ-152):
  - Персональные данные нельзя передавать за рубеж без согласия
  - ChatGPT, Claude, GPT-4 = американские серверы
  - Нарушение = административная ответственность (2025: штрафы выросли)

Риски без анонимизации:
  → сотрудник вставляет договор с ФИО в ChatGPT
  → данные могут попасть в обучение модели
  → «shadow AI»: неконтролируемое использование корпоративных данных
```

## Архитектура Jay Guard

```
Пользователь → запрос с ПД
  "Проверь договор с Ивановым Иваном Ивановичем, ИНН 7710123456"
        ↓
Jay Guard (proxy):
  Stage 1: Scan
    → NER: найти ПД (ФИО, ИНН, email, телефон, паспорт)
    → результат: [(Иванов Иван Иванович, PERSON), (7710123456, INN)]

  Stage 2: Anonymize
    → замена: Иванов Иван Иванович → [PERSON_1]
    → замена: 7710123456 → [INN_1]
    → хранить маппинг: {[PERSON_1]: "Иванов Иван Иванович"}
    → анонимизированный текст → LLM API (ChatGPT/Claude/YandexGPT)

  Stage 3: Deanonymize
    → ответ LLM: "Договор с [PERSON_1] содержит ошибку в п.3..."
    → подставить обратно: [PERSON_1] → Иванов Иван Иванович
    → итоговый ответ пользователю с оригинальными именами
```

## NER-компонент: что анонимизирует

```python
ENTITY_TYPES = {
    "PERSON":     "ФИО (русский + английский)",
    "ORG":        "Названия организаций",
    "INN":        "ИНН (10 или 12 цифр)",
    "OGRN":       "ОГРН",
    "PHONE":      "Телефонные номера (все форматы)",
    "EMAIL":      "Адреса email",
    "PASSPORT":   "Серия и номер паспорта",
    "BANK_CARD":  "Номера банковских карт",
    "ADDRESS":    "Адреса (город, улица, дом)",
    "DATE":       "Даты рождения (контекстуально)",
}
```

## Benchmark на HuggingFace

```
Задача: найти и анонимизировать ПД в русскоязычных текстах
  - Деловые письма с договорами
  - Клиентские запросы
  - HR-документы
  - Медицинские записи

Метрики:
  Precision:  95%  (если пометил → это действительно ПД)
  Recall:     92%  (из всех ПД найдено 92%)
  F1:         93.5%

Benchmark публично на HuggingFace: анонимизированная версия данных
```

## Режимы работы

```
Режим 1: Proxy (прозрачный)
  → встаёт между корпоративным чатом и LLM API
  → сотрудники ничего не меняют в работе
  → Jay Guard работает «под капотом»

Режим 2: SDK (интеграция)
  → jay_guard.scan(text) → entities
  → jay_guard.anonymize(text) → anonymized_text, mapping
  → jay_guard.deanonymize(llm_response, mapping) → final_text

Режим 3: Audit
  → только логирование: какие ПД были в запросах
  → без блокировки → анализ рисков
```

## Сравнение с аналогами

| Решение | Тип | Точность RU | Open source |
|---------|-----|------------|-------------|
| **Jay Guard** | proxy/SDK | 93% F1 | нет (just_ai) |
| Microsoft Presidio | SDK | ~80% RU | да (MIT) |
| OpenAI Privacy Filter | модель | ~85% EN | да (новый 2026) |
| spaCy + правила | библиотека | ~70% RU | да |

Jay Guard специализирован на русском языке и российских форматах ПД (ИНН, ОГРН, паспорт).

## ChamelOn (смежный open-source проект)

```
ChamelOn: production-ready анонимизация с защитой от ReDoS
  → 95% точность
  → защита от regex DoS атак
  → Habr: /ru/articles/969766/
  → open source, Apache 2.0
```

Альтернатива Jay Guard если нужен open source.

## Применение к Lorenzo

Lorenzo передаёт тексты в Claude API (`improve_llm_*.py`).  
Если документы содержат ПД пользователей Svyazi:

```python
# В improve_llm_enrich.py — добавить Jay Guard:
from jay_guard import JayGuard  # или ChamelOn

guard = JayGuard()

def safe_llm_call(text: str) -> str:
    anonymized, mapping = guard.anonymize(text)
    response = claude_client.messages.create(
        messages=[{"role": "user", "content": anonymized}]
    )
    return guard.deanonymize(response.content[0].text, mapping)
```

## Возможные комбинации

| Комбинация | Новое свойство |
|------------|----------------|
| **Jay Guard + improve_llm_enrich** | ПД в документах → анонимизация перед Claude API |
| **Jay Guard + Gateway (Lorenzo)** | gateway.py как Jay Guard proxy для внешних клиентов |
| **Jay Guard + LLM Immune System (R15)** | Двойной фильтр: PD анонимизация + токен-by-токен проверка |
| **Jay Guard + GigaAM (R16)** | Голос → текст → Jay Guard → LLM: приватный voice assistant |
| **Jay Guard + RAG Eval (R16)** | RAGAS тестирует: не утекают ли ПД через RAG retrieval |

## Контакт

- Статья: https://habr.com/ru/companies/just_ai/articles/946392/ (2025)
- Just AI: just-ai.com (российская AI-компания)
- Benchmark: huggingface.co/datasets/just-ai/pd-anonymization-benchmark (анонимизированный)
- ChamelOn (open-source альтернатива): https://habr.com/ru/articles/969766/
- Microsoft Presidio: github.com/microsoft/presidio (MIT)
