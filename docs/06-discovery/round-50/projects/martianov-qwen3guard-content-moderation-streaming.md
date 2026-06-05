# Qwen3Guard: модерация контента с on-the-fly логитами против LlamaGuard и ShieldGemma

> [!WARNING]
> Документ содержит описание рисков и ограничений. Изучите их перед принятием архитектурных решений.

<!-- alert-added -->

**Автор:** Martianov (Миша Мартьянов, red_mad_robot)  
**Хабр:** https://habr.com/ru/companies/redmadrobot/articles/971388/  
**GitHub:** нет (production кейс)  
**Слой:** orchestration  
**Дата:** ноябрь 2025  
**Уникальность:** Единственная русскоязычная статья 2025 года с детальным сравнением специализированных моделей content moderation: BERT-классификатор (20мс) vs Qwen3Guard-Stream (60мс, on-the-fly классификация по логитам каждого токена) vs Qwen3Guard-Gen (LLM 8B, лучший F1 против LlamaGuard и ShieldGemma). Не защита LLM от атак (SENTINEL, R47) — а фильтрация нежелательного UGC-контента пользователей AI-сервиса (генератор видео/изображений Daisy). Streaming-детекция токсичности без ожидания полного ответа.

## Проблема: модерировать UGC для AI-генератора

```
Сервис Daisy (red_mad_robot): AI-генератор изображений и видео
  → Пользователи отправляют промпты на генерацию
  → Некоторые промпты нарушают правила: насилие, незаконный контент,
    экстремизм, наркотики
  → Нужно: блокировать до генерации (не после!)

Эволюция системы модерации:

  Версия 1: эвристики (keyword blacklist)
  → Обходится вариациями написания

  Версия 2: LLaMA 7B fine-tuned
  → Долго, много false positives на метафорах

  Версия 3: Qwen 30B (дорого, медленно)

  Версия 4 (итоговая): BERT-преклассификатор + GPT-4o mini судья
  → 8% уровень ошибок → хотим 2-3%

  Версия 5 (Qwen3Guard): streaming-детекция по токенам
  → Перехватывает вредный контент в середине генерации
```

## Три уровня архитектуры модерации

```python
# Martianov (red_mad_robot): Qwen3Guard content moderation
# habr.com/ru/companies/redmadrobot/articles/971388/

from dataclasses import dataclass
from typing import Literal, AsyncIterator
import asyncio

HarmCategory = Literal[
    "VIOLENCE",
    "ILLEGAL_ACTIVITIES",
    "DRUGS",
    "EXTREMISM",
    "SEXUAL_CONTENT",
    "SAFE"
]

HarmSeverity = Literal["LOW", "MEDIUM", "HIGH", "CRITICAL"]

@dataclass
class ModerationResult:
    """Результат модерации контента."""
    is_safe: bool
    category: HarmCategory
    severity: HarmSeverity
    confidence: float
    latency_ms: float
    method: str  # "bert_fast" | "qwen3guard_stream" | "qwen3guard_gen"
    explanation: Optional[str] = None


class BERTFastModerator:
    """
    Уровень 1: BERT-классификатор для быстрой предварительной фильтрации.

    Latency: ~20ms (vs 60-500ms у LLM-подходов)
    Точность: средняя (много false positives на edge cases)
    Роль: отсеять очевидные случаи до вызова дорогого LLM

    Архитектура:
    - Базовая модель: ruBERT или multilingual BERT
    - Fine-tuned на корпусе токсичных промптов
    - Бинарная классификация: safe/potentially_harmful
    - Threshold: 0.3 (low) → дальше Qwen3Guard
    """

    def classify(self, text: str) -> ModerationResult:
        """Быстрая классификация за 20ms."""
        # BERT inference
        score = self._bert_score(text)

        if score < 0.3:
            return ModerationResult(
                is_safe=True, category="SAFE",
                severity="LOW", confidence=1 - score,
                latency_ms=20, method="bert_fast"
            )
        # score >= 0.3 → отправить в Qwen3Guard
        return None  # сигнал для следующего уровня


class Qwen3GuardStream:
    """
    Уровень 2: Qwen3Guard-Stream — on-the-fly классификация.

    Latency: ~60ms
    Метод: классификация по логитам первого safety-токена.

    Принцип:
    Промпт: "Is the following content safe? [TEXT]\nAnswer:"
    → Первый генерируемый токен: "Yes" или "No"
    → НЕ ждать полного ответа — смотреть логиты на первом токене
    → P("Yes") vs P("No") → confidence score мгновенно

    Преимущество: не нужно ждать полного completion.
    Быстрее Qwen3Guard-Gen в 2-3 раза.
    """

    async def classify_stream(self, text: str) -> ModerationResult:
        """
        Классификация по логитам первого токена.
        Не ждёт полного ответа модели.
        """
        prompt = f"""Classify if this content violates safety guidelines.
Content: {text}
Is this content safe? Answer with Yes or No."""

        # Запрос с max_new_tokens=1 — только первый токен
        response = await self.llm.generate(
            prompt,
            max_new_tokens=1,
            return_logits=True
        )

        # Извлечь вероятности "Yes" и "No"
        yes_token_id = self.tokenizer.encode("Yes")[0]
        no_token_id = self.tokenizer.encode("No")[0]

        logits = response.logits[0]
        import torch
        probs = torch.softmax(logits[[yes_token_id, no_token_id]], dim=0)

        p_safe = probs[0].item()
        p_harmful = probs[1].item()

        return ModerationResult(
            is_safe=p_safe > 0.7,
            category="VIOLENCE" if p_harmful > 0.7 else "SAFE",
            severity="HIGH" if p_harmful > 0.9 else "MEDIUM",
            confidence=max(p_safe, p_harmful),
            latency_ms=60,
            method="qwen3guard_stream"
        )


class Qwen3GuardGen:
    """
    Уровень 3: Qwen3Guard-Gen — полная LLM-классификация (8B модель).

    Latency: 200-500ms
    Точность: наивысшая, лучше LlamaGuard и ShieldGemma
    Роль: финальный судья для сложных edge cases

    Метод: полная генерация structured output с объяснением.
    Возвращает: категорию + серьёзность + объяснение нарушения.
    """

    async def classify_detailed(self, text: str) -> ModerationResult:
        """
        Детальная классификация с объяснением (200-500ms).
        Используется только если Qwen3Guard-Stream не уверен.
        """
        prompt = f"""Analyze the following content for safety violations.

Content: {text}

Classify and explain any violations.
Respond in JSON:
{{"is_safe": bool, "category": "VIOLENCE|ILLEGAL_ACTIVITIES|DRUGS|EXTREMISM|SAFE",
  "severity": "LOW|MEDIUM|HIGH|CRITICAL", "explanation": "..."}}"""

        response = await self.llm.generate(
            prompt,
            response_format={"type": "json_object"},
            temperature=0.0
        )

        result = json.loads(response)
        return ModerationResult(
            is_safe=result["is_safe"],
            category=result["category"],
            severity=result["severity"],
            confidence=0.95,  # LLM с объяснением — высокая уверенность
            latency_ms=350,
            method="qwen3guard_gen",
            explanation=result["explanation"]
        )


class ThreeLevelModerationPipeline:
    """
    Каскадная модерация: BERT → Qwen3Guard-Stream → Qwen3Guard-Gen.
    Каждый уровень вызывается только если предыдущий не уверен.
    Оптимизация: большинство запросов проходит через Level 1 (20ms).
    """

    THRESHOLDS = {
        "bert_safe": 0.3,        # <0.3 → безопасно без LLM
        "stream_confident": 0.85, # >0.85 → уверенный ответ без Gen
        "escalate_to_human": 0.5  # stream confidence < 0.5 → human review
    }

    async def moderate(self, text: str) -> ModerationResult:
        """
        Каскадная классификация: начинаем с быстрого, эскалируем при неуверенности.
        """
        # Level 1: BERT (20ms)
        bert_result = self.bert.classify(text)
        if bert_result and bert_result.is_safe:
            return bert_result

        # Level 2: Qwen3Guard-Stream (60ms)
        stream_result = await self.stream.classify_stream(text)
        if stream_result.confidence >= self.THRESHOLDS["stream_confident"]:
            return stream_result

        # Level 3: Qwen3Guard-Gen (350ms) — только для edge cases
        return await self.gen.classify_detailed(text)
```

## Сравнение с LlamaGuard и ShieldGemma

```python
BENCHMARK_COMPARISON = {
    "датасет": "Собственный корпус Daisy (промпты пользователей AI-сервиса)",
    "категории": ["VIOLENCE", "ILLEGAL_ACTIVITIES", "DRUGS", "EXTREMISM"],

    "модели": {
        "LlamaGuard_3_8B": {
            "F1": 0.78,
            "latency_ms": 400,
            "проблема": "Много false positives на метафорах и художественных описаниях"
        },
        "ShieldGemma_9B": {
            "F1": 0.81,
            "latency_ms": 450,
            "проблема": "Чрезмерно пуританская этика: блокирует исторические тексты"
        },
        "Qwen3Guard_Stream": {
            "F1": 0.84,
            "latency_ms": 60,
            "преимущество": "Быстро + хорошее качество для очевидных случаев"
        },
        "Qwen3Guard_Gen_8B": {
            "F1": 0.91,
            "latency_ms": 350,
            "преимущество": "Лучший F1, понимает контекст (метафора vs буквально)"
        }
    },

    "каскад_BERT_Stream_Gen": {
        "avg_latency_ms": 45,  # большинство через BERT или Stream
        "F1": 0.89,
        "стоимость_vs_только_Gen": "-70% API calls к дорогому Gen"
    },

    "ключевой_вывод": (
        "Qwen3Guard-Stream's on-the-fly logit approach даёт 7× speedup vs Gen "
        "при незначительной потере качества. "
        "Для production: каскад из трёх уровней оптимален."
    )
}
```

## Применение к Lorenzo

```python
# Lorenzo: каскадная модерация для /api/cards и /api/ask

class LorenzoContentGuard:
    """
    Martianov паттерн для Lorenzo:
    Трёхуровневая модерация для карточек проектов и запросов.

    Не защита от prompt injection (это SENTINEL, R47) —
    а проверка качества контента карточек:
    нет плагиата, нет маркетинговой воды, нет фейковых метрик.

    Адаптация:
    Level 1 (BERT-fast): нет ли в карточке явного спама
    Level 2 (Stream): является ли контент техническим/содержательным
    Level 3 (Gen): полная оценка качества (CLEV из R47)
    """

    async def guard_new_card(self, card_content: str) -> dict:
        """Проверить новую карточку перед добавлением в базу знаний."""
        result = await self.pipeline.moderate(card_content)
        return {
            "approved": result.is_safe,
            "reason": result.explanation,
            "latency_ms": result.latency_ms
        }
```

## Возможные комбинации

| Комбинация | Новое свойство |
|------------|----------------|
| **Qwen3Guard + SENTINEL (R47)** | SENTINEL (защита от prompt injection) + Qwen3Guard (UGC модерация) = полный safety stack |
| **Qwen3Guard + LLM Observability (R45)** | Трейсинг: какие категории контента чаще блокируются, где streaming vs gen расходятся |
| **Qwen3Guard + CLEV (R47)** | CLEV консенсус для спорных случаев: три модели голосуют когда Qwen3Guard не уверен |
| **Qwen3Guard + LangGraph (R44)** | LangGraph с BERT→Stream→Gen как условные узлы: interrupt_before human review |
| **Qwen3Guard + Review Queue (Lorenzo)** | Спорные случаи (confidence 0.5-0.7) → Review Queue Streamlit для ручной проверки |

## Контакт

- Статья: https://habr.com/ru/companies/redmadrobot/articles/971388/ (ноябрь 2025)
- Автор: Martianov (Миша Мартьянов, red_mad_robot)
- LlamaGuard: meta-llama/LlamaGuard-3-8B (HuggingFace)
- ShieldGemma: google/shieldgemma-9b (HuggingFace)
- Qwen3Guard: Qwen3 fine-tuned на safety tasks
- Смежная (SENTINEL LLM защита, R47): docs/06-discovery/round-47/projects/dmitriila-sentinel-llm-immune-system-3ms.md
- Смежная (LLM AppSec, R22): docs/06-discovery/round-22/
- Смежная (red-teaming, R33): docs/06-discovery/round-33/
