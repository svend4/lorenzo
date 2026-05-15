---
date: 2026-05-15
tags: [rag, ingestion, architecture, self-improve, collaboration]
state: normalized
---

# Кириллица в LLM: почему русский язык стоит дороже и работает медленнее

<!-- toc-auto -->
<!-- tags: cyrillic-llm-tokenization-russian, docs -->


<!-- summary -->
> Автор: AGmind (Хабр, май 2025) Хабр: https://habr.com/ru/articles/1032610/ GitHub: не применимо (аналитическая статья с бенчмарками)
Хабр: https://habr.com/ru/articles/1032610/  
GitHub: не применимо (аналитическая статья с бенчмарками)  
Слой: orchestration / analytics  
Дата: май 2025  
Уникальность: Практический разбор: почему русский текст стои


> [!TIP]
> Документ содержит практические рекомендации и лучшие практики.

<!-- alert-added -->

**Автор:** AGmind (Хабр, май 2025)  
**Хабр:** https://habr.com/ru/articles/1032610/  
**GitHub:** не применимо (аналитическая статья с бенчмарками)  
**Слой:** orchestration / analytics  
**Дата:** май 2025  
**Уникальность:** Практический разбор: почему русский текст стоит ~2× дороже английского в LLM API. GPT-3.5/4 (`cl100k_base`) — только 435 кириллических токенов из 100 235. GPT-4o расширил до 4 660. Русская морфология даёт 2–3+ токенов/слово вместо ~1 для английского. Бенчмарк: Qwen 3, DeepSeek R1, GigaChat, YandexGPT. Порог: < 1.7 токенов/слово = приемлемо.

## Корень проблемы: токенизаторы обучались на английском

```
Распределение токенов в cl100k_base (GPT-3.5/4):

Всего токенов:         100,235
Латинских токенов:      ~67,000  (67%)
Кириллических токенов:      435  (0.43%!)
Прочих:                ~32,800  (32.57%)

Последствие:
Английское слово "contract" → 1 токен
Русское слово "договор"     → 3 токена (до-го-вор)
Русское слово "договора"    → 4 токена (другой падеж!)
Русское слово "договором"   → 4 токена (ещё один падеж)

Стоимость:
"Analyze this contract."                → ~4 токена
"Проанализируй этот договор."           → ~9 токенов
→ Русский обходится в 2-2.5× дороже за тот же смысл
```

## Почему русская морфология особенно дорогостоящая

```python
# Русский язык = высокоморфологичный
# Одна лексема → много словоформ

RUSSIAN_MORPHOLOGY_COST = {
    "договор": {
        "формы": [
            "договор",     # ном. ед.  → 3 токена (cl100k)
            "договора",    # ген. ед.  → 4 токена
            "договору",    # дат. ед.  → 4 токена
            "договором",   # тв. ед.   → 4 токена
            "договоре",    # пр. ед.   → 4 токена
            "договоры",    # ном. мн.  → 4 токена
            "договоров",   # ген. мн.  → 4 токена
        ],
        "средних токенов": 3.86
    },
    "работать": {
        "формы": [
            "работаю", "работаешь", "работает",
            "работают", "работал", "работала",
            "работали", "работающий", "работавший"
        ],
        "средних токенов": 4.2
    }
}

# Для сравнения:
ENGLISH_MORPHOLOGY_COST = {
    "contract": {
        "формы": ["contract", "contracts", "contracted", "contracting"],
        "средних токенов": 1.3
    }
}

# Разрыв: 3.86 vs 1.3 → 3× дороже за морфологию
```

## Эволюция: как провайдеры улучшают кириллицу

```python
CYRILLIC_SUPPORT_EVOLUTION = {
    "GPT-3.5 (cl100k_base)": {
        "кириллических_токенов": 435,
        "tokens_per_word_ru": 2.8,
        "tokens_per_word_en": 1.1,
        "ratio": 2.5,
        "context_128k_в_рус_словах": "~46K слов vs 116K на английском"
    },
    "GPT-4o (o200k_base)": {
        "кириллических_токенов": 4660,  # +10× улучшение!
        "tokens_per_word_ru": 1.8,
        "tokens_per_word_en": 1.05,
        "ratio": 1.71,
        "context_128k_в_рус_словах": "~71K слов"
    },
    "Qwen3 (CL200k)": {
        "кириллических_токенов": "~15K+",
        "tokens_per_word_ru": 1.5,
        "ratio": 1.4,
        "comment": "Специально оптимизирован для CJK + Cyrillic"
    },
    "DeepSeek R1 (deepseek_tokenizer)": {
        "tokens_per_word_ru": 1.6,
        "ratio": 1.5,
        "comment": "Хорошая поддержка кириллицы"
    },
    "YandexGPT (собственный)": {
        "tokens_per_word_ru": 1.3,  # лучший для русского!
        "ratio": 1.15,
        "comment": "Обучен на русском корпусе, токенизатор под русский"
    },
    "GigaChat (собственный)": {
        "tokens_per_word_ru": 1.4,
        "ratio": 1.25,
        "comment": "Сбер, русскоязычный корпус"
    }
}

# Практический порог AGmind:
# < 1.7 токенов/слово → приемлемо для production
# > 2.0 токенов/слово → плохая оптимизация кириллицы
```

## Измерение: как посчитать стоимость для вашего языка

```python
def measure_tokenization_efficiency(text: str,
                                     tokenizer_name: str) -> TokenReport:
    """Практический инструмент: сравнение токенизаторов"""
    import tiktoken
    from transformers import AutoTokenizer

    # Посчитать токены
    if tokenizer_name.startswith("cl100k"):
        enc = tiktoken.get_encoding("cl100k_base")
        tokens = enc.encode(text)
    else:
        enc = AutoTokenizer.from_pretrained(tokenizer_name)
        tokens = enc.encode(text)

    # Посчитать слова
    words = text.split()

    return TokenReport(
        token_count=len(tokens),
        word_count=len(words),
        tokens_per_word=len(tokens) / len(words),
        efficiency_grade=(
            "excellent" if len(tokens) / len(words) < 1.5 else
            "good"      if len(tokens) / len(words) < 1.7 else
            "acceptable"if len(tokens) / len(words) < 2.0 else
            "poor"
        )
    )

# Пример:
russian_text = "Проанализируй договор поставки и выдели ключевые риски."
english_text = "Analyze the supply contract and highlight key risks."

ru_report = measure_tokenization_efficiency(russian_text, "cl100k_base")
# → tokens_per_word=2.4, efficiency_grade="poor"

en_report = measure_tokenization_efficiency(english_text, "cl100k_base")
# → tokens_per_word=1.1, efficiency_grade="excellent"
```

## Практические последствия для систем

```python
PRACTICAL_IMPLICATIONS = {
    "context_window": {
        "проблема": "128K токенов ≠ 128K слов на русском",
        "расчёт": {
            "cl100k (GPT-4)": "128K токенов ÷ 2.8 ≈ 46K рус. слов",
            "o200k (GPT-4o)": "128K токенов ÷ 1.8 ≈ 71K рус. слов",
            "YandexGPT":      "128K токенов ÷ 1.3 ≈ 98K рус. слов"
        },
        "вывод": "YandexGPT вмещает вдвое больше русского текста в тот же контекст"
    },

    "api_cost": {
        "проблема": "Одинаковый документ стоит по-разному",
        "пример": "1000 слов договора: $0.028 (English) vs $0.068 (Russian, GPT-4)",
        "оптимизация": "Переключиться на Qwen3/YandexGPT для RU-документов"
    },

    "rag_retrieval": {
        "проблема": "Чанки по токенам ≠ чанки по смыслу для русского",
        "решение": "Чанковать по предложениям, не по токенам",
        "код": """
        # Плохо: chunk_size=512 токенов → обрезает русское предложение
        # Хорошо: 
        sentences = sent_tokenize(text, language='russian')
        chunks = merge_sentences_to_max_tokens(sentences, max_tokens=512)
        """
    },

    "fine_tuning": {
        "проблема": "Обучение на русском данных дороже",
        "решение": "Начинать с Qwen3 или YandexGPT как base model для RU задач"
    }
}
```

## Бенчмарк: выбор токенизатора для русскоязычного продукта

```python
TOKENIZER_SELECTION_GUIDE = {
    "задача: русскоязычный B2B (юридика, финансы)": {
        "рекомендация": "YandexGPT Pro или GigaChat Pro",
        "причина": "лучший tokens/word для русского, данные остаются в РФ",
        "альтернатива": "Qwen3-72B (open source, хорошая кириллица)"
    },
    "задача: смешанный RU/EN контент": {
        "рекомендация": "GPT-4o (o200k) или Qwen3",
        "причина": "o200k значительно улучшил кириллицу vs cl100k"
    },
    "задача: on-premise, self-hosted": {
        "рекомендация": "Qwen3-14B или Qwen3-32B",
        "причина": "лучший tokens/word среди open-source, Apache 2.0"
    },
    "задача: RAG на русских документах": {
        "рекомендация": "embedding: FRIDA (R18) + LLM: YandexGPT/Qwen3",
        "причина": "FRIDA = русские embeddings, Qwen3 = экономный токенизатор"
    }
}
```

## Применение к Lorenzo

Lorenzo работает с русскоязычными документами (85%+ контента):

```python
# improve_tokenizer_audit.py (паттерн):

class LorenzoTokenizerAudit:
    """
    Аудит: сколько токенов тратит Lorenzo на свои операции
    Оптимизация: выбрать модель с лучшим tokens/word для RU
    """

    def audit_llm_costs(self) -> CostReport:
        docs = list_docs("docs/")

        total_tokens = {}
        for model, enc in self.tokenizers.items():
            tokens = sum(len(enc.encode(read(doc))) for doc in docs)
            total_tokens[model] = {
                "tokens": tokens,
                "estimated_cost_usd": tokens * self.price_per_token[model]
            }

        # Найти самый экономный токенизатор для нашего контента
        best = min(total_tokens, key=lambda m: total_tokens[m]["tokens"])
        return CostReport(recommendation=best, breakdown=total_tokens)

    def recommend_chunking_strategy(self) -> str:
        """Для русских документов: чанки по предложениям"""
        return "Используй sent_tokenize(language='russian'), не chunk_size=N_tokens"
```

## Возможные комбинации

| Комбинация | Новое свойство |
|------------|----------------|
| **Cyrillic + FRIDA (R18)** | FRIDA embeddings + YandexGPT = полный RU-стек без дорогого cl100k |
| **Cyrillic + LLM Router (R20)** | Роутинг: RU-контент → YandexGPT/Qwen3, EN-контент → GPT-4o |
| **Cyrillic + Legal RAG (R25)** | Юридические документы на русском: токенизатор = критический выбор |
| **Cyrillic + Fine-tuning (R24)** | Для RU fine-tuning: Qwen3 base → меньше токенов → дешевле обучение |
| **Cyrillic + LLM Judge (R28)** | Кросс-модельная оценка RU контента: учитывать разницу tokens/word |

## Контакт

- Статья: https://habr.com/ru/articles/1032610/ (май 2025)
- Смежная (адаптация LLM для русского языка): https://habr.com/ru/articles/964510/
- Смежная (токенизация для морфологически богатых языков): https://habr.com/ru/articles/973324/
- FRIDA (RU embeddings R18): github.com/ai-forever/FRIDA
- Tiktoken (OpenAI tokenizer): github.com/openai/tiktoken
- SentencePiece: github.com/google/sentencepiece

## Смотрите также
- [Главная](../../../README.md)
- [Метрики](../../../METRICS.md)
- [Здоровье](../../../HEALTH.md)
- [Глоссарий](../../../GLOSSARY.md)
- [Сущности](../../../ENTITIES.md)
- [Решения](../../../DECISIONS.md)
