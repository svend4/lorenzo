---
date: 2026-06-05
tags: [memory, rag, orchestration, ingestion, architecture]
state: normalized
---

# feeds.fun: LLM-автотегирование новостей с прозрачным ранжированием

<!-- toc-auto -->
<!-- tags: feedsfun-llm-news-autotag-ranking, docs -->


<!-- summary -->
> Хабр: https://habr.com/ru/articles/891308/ GitHub: https://github.com/Tiendil/feeds.fun
Хабр: https://habr.com/ru/articles/891308/  
GitHub: https://github.com/Tiendil/feeds.fun  
Слой: analytics / orchestration  
Дата: март 2025  
Уникальность: Open-source новостной агрегатор (Python/FastAPI/PostgreSQL + Vue.js) с LLM-


> [!NOTE]
> Документ создан на основе исследования. Ссылки ведут на связанные материалы.

<!-- alert-added -->

**Автор:** Tiendil  
**Хабр:** https://habr.com/ru/articles/891308/  
**GitHub:** https://github.com/Tiendil/feeds.fun  
**Слой:** analytics / orchestration  
**Дата:** март 2025  
**Уникальность:** Open-source новостной агрегатор (Python/FastAPI/PostgreSQL + Vue.js) с LLM-автотегированием входящих RSS-статей по пользовательским сценариям интересов и прозрачным (не black-box) ранжированием. LLM генерирует теги → пользователь определяет правила → числовой скор объясним. Поддержка OpenAI, Gemini. Self-reported: 1000 статей/день → 50-100 релевантных (90% экономия времени). Двухуровневая дедупликация URL, прокси для bot-blocking сайтов, test-корпус с обязательными/желательными тег-утверждениями.

## Проблема: новостной шум убивает производительность

```
Типичный информационный поток:
  → 1000+ статей в день из RSS-лент
  → 90%+ нерелевантны конкретным интересам
  → Ручной просмотр: 2-3 часа/день
  → Рекомендательные алгоритмы: черный ящик, не объясняют

Проблемы существующих решений:
  → Feedly/Inoreader: фильтрация по ключевым словам (неточно)
  → ML-рекомендации: "похожие статьи" без объяснения
  → Нет поддержки сложных семантических сценариев
    ("статьи о Rust но не о системном программировании")

feeds.fun подход:
  → LLM читает каждую статью → генерирует теги
  → Пользователь описывает интересы через сценарии (теги + правила)
  → Прозрачный скор: "эта статья набрала 0.87 потому что
    совпали теги: AI, RAG, production (из сценария 'AI engineering')"
  → Пользователь понимает и может корректировать
```

## Архитектура системы

```python
# feeds.fun: LLM-тегирование + прозрачное ранжирование
# github.com/Tiendil/feeds.fun

from dataclasses import dataclass, field
from typing import Optional
import asyncio

@dataclass
class Article:
    """Входящая статья из RSS."""
    url: str
    title: str
    content: str
    source_feed: str
    published_at: str
    tags: list[str] = field(default_factory=list)        # LLM-теги
    score: float = 0.0                                    # финальный скор


@dataclass
class InterestScenario:
    """
    Пользовательский сценарий интересов.
    Пример: "AI Engineering" = required[AI] + desired[RAG, production] - blocked[hype]
    """
    name: str
    required_tags: list[str]     # обязательные теги (AND логика)
    desired_tags: list[str]      # желательные (повышают скор)
    blocked_tags: list[str]      # блокирующие (исключают статью)
    weight: float = 1.0          # вес сценария в итоговом скоре


class FeedsFunPipeline:
    """
    Основной pipeline: RSS → LLM-теги → скоринг → UI.
    """

    # Шаг 1: Сбор статей из RSS
    async def fetch_feeds(self, feed_urls: list[str]) -> list[Article]:
        """
        Async RSS парсинг с двухуровневой дедупликацией:
        Уровень 1: exact URL match
        Уровень 2: canonical URL (без utm_, после редиректов)
        """
        articles = []
        async with aiohttp.ClientSession() as session:
            for url in feed_urls:
                feed_content = await self.fetch_with_proxy(session, url)
                parsed = feedparser.parse(feed_content)
                for entry in parsed.entries:
                    canonical = self.canonicalize_url(entry.link)
                    if canonical not in self.seen_urls:
                        self.seen_urls.add(canonical)
                        articles.append(Article(
                            url=canonical,
                            title=entry.title,
                            content=entry.summary,
                            source_feed=url,
                            published_at=entry.published
                        ))
        return articles

    # Шаг 2: LLM-автотегирование
    async def tag_articles(self, articles: list[Article],
                            model: str = "gpt-4o-mini") -> list[Article]:
        """
        LLM читает статью → генерирует семантические теги.
        Теги: конкретные ("RAG", "Python", "production") не абстрактные ("technology").

        Batch processing: до 20 статей параллельно.
        """
        async def tag_one(article: Article) -> Article:
            prompt = f"""Прочитай статью и сгенерируй 5-15 конкретных тегов.
Теги должны быть: технические термины, концепции, инструменты, домены.
НЕ использовать: общие слова (статья, технология, разработка).

Заголовок: {article.title}
Содержание: {article.content[:2000]}

Верни теги через запятую."""

            response = await self.llm.acomplete(prompt, model=model)
            article.tags = [t.strip().lower()
                             for t in response.split(",")
                             if t.strip()]
            return article

        # Batch: 20 параллельных запросов к LLM
        semaphore = asyncio.Semaphore(20)
        async def bounded_tag(article):
            async with semaphore:
                return await tag_one(article)

        return await asyncio.gather(*[bounded_tag(a) for a in articles])

    # Шаг 3: Прозрачное ранжирование
    def score_article(self, article: Article,
                       scenarios: list[InterestScenario]) -> tuple[float, dict]:
        """
        Детерминированный, объяснимый скор.
        Пользователь видит: какие теги совпали с каким сценарием.
        """
        total_score = 0.0
        explanation = {}

        for scenario in scenarios:
            # Блокирующие теги: статья исключается полностью
            if any(t in article.tags for t in scenario.blocked_tags):
                return 0.0, {"blocked_by": scenario.name}

            # Обязательные: все должны быть
            if not all(t in article.tags for t in scenario.required_tags):
                continue

            # Подсчёт скора через желательные теги
            matched_desired = [t for t in scenario.desired_tags
                                if t in article.tags]
            scenario_score = (
                len(matched_desired) / max(len(scenario.desired_tags), 1)
            ) * scenario.weight

            total_score += scenario_score
            explanation[scenario.name] = {
                "matched": matched_desired,
                "score": scenario_score
            }

        return total_score, explanation
```

## Тест-корпус для валидации тегирования

```python
class TaggingQualityTests:
    """
    Test corpus: набор статей с ожидаемыми тегами.
    CI/CD интеграция: тесты падают если LLM начинает хуже тегировать.
    """

    TEST_CASES = [
        {
            "article_url": "https://habr.com/...",
            "mandatory_tags": ["RAG", "python"],    # ДОЛЖНЫ быть
            "desired_tags": ["production", "LLM"],  # ЖЕЛАТЕЛЬНЫ
            "forbidden_tags": ["javascript"]        # НЕ ДОЛЖНЫ быть
        },
        # ... другие кейсы
    ]

    def run_quality_check(self, tagged_articles: list[Article]) -> dict:
        """
        Проверка качества тегирования на корпусе.
        Если точность падает → нужно обновить промпт или сменить модель.
        """
        results = {"passed": 0, "failed": 0, "cases": []}

        for test_case in self.TEST_CASES:
            article = self._find_article(tagged_articles, test_case["article_url"])
            if not article:
                continue

            # Проверка обязательных тегов
            missing_mandatory = [t for t in test_case["mandatory_tags"]
                                  if t not in article.tags]
            # Проверка запрещённых тегов
            present_forbidden = [t for t in test_case["forbidden_tags"]
                                  if t in article.tags]

            passed = not missing_mandatory and not present_forbidden
            results["passed" if passed else "failed"] += 1
            results["cases"].append({
                "url": test_case["article_url"],
                "passed": passed,
                "missing": missing_mandatory,
                "forbidden_present": present_forbidden
            })

        return results
```

## Технический стек

```python
SYSTEM_PROFILE = {
    "github": "https://github.com/Tiendil/feeds.fun",
    "license": "открытый код",

    "стек": {
        "backend": "Python + FastAPI",
        "frontend": "Vue.js",
        "database": "PostgreSQL",
        "llm_providers": ["OpenAI (gpt-4o-mini)", "Google Gemini"],
        "rss_parsing": "feedparser",
        "async": "aiohttp + asyncio"
    },

    "возможности": {
        "дедупликация": "двухуровневая (exact URL + canonical)",
        "прокси": "поддержка для bot-blocking сайтов",
        "тегирование": "LLM на каждую статью",
        "ранжирование": "прозрачный числовой скор",
        "тест_корпус": "mandatory/desired assertions для CI",
        "сценарии": "пользовательские комбинации тегов"
    },

    "результаты": {
        "обработка": "1000 статей/день",
        "релевантных": "50-100 (5-10%)",
        "экономия_времени": "~90% по самооценке автора"
    },

    "модели_стоимость": {
        "gpt-4o-mini": "~$0.00015/статья при 1000 токенов",
        "1000_статей_день": "~$0.15/день = ~$4.5/месяц",
        "gemini_flash": "ещё дешевле"
    }
}
```

## Применение к Lorenzo

```python
# Lorenzo: feeds.fun паттерн для мониторинга Хабра

class LorenzoFeedMonitor:
    """
    feeds.fun паттерн для Lorenzo:
    Автоматический мониторинг новых статей Хабра по темам discovery.
    LLM тегирует → сценарии фильтруют → только релевантные в очередь.
    """

    INTEREST_SCENARIOS = [
        InterestScenario(
            name="LLM Engineering",
            required_tags=["LLM", "python"],
            desired_tags=["RAG", "agents", "production", "MCP"],
            blocked_tags=["hype", "overview-only"]
        ),
        InterestScenario(
            name="Russian AI Projects",
            required_tags=["russia", "open-source"],
            desired_tags=["github", "benchmark", "evaluation"],
            blocked_tags=[]
        )
    ]

    async def monitor_habr(self) -> list[Article]:
        """Каждые 6 часов: новые статьи → LLM-теги → фильтрация → review_queue."""
        articles = await self.fetch_feeds(["https://habr.com/ru/rss/all/"])
        tagged = await self.tag_articles(articles)
        return [a for a in tagged
                if self.score_article(a, self.INTEREST_SCENARIOS)[0] > 0.5]
```

## Возможные комбинации

| Комбинация | Новое свойство |
|------------|----------------|
| **feeds.fun + Lorenzo Gateway** | /api/feed → LLM-тегированные статьи Хабра как источник для discovery |
| **feeds.fun + Collab Finder** | Новые статьи → автоматический поиск коллабораций через BM25 |
| **feeds.fun + LangFuse (R38)** | Трейсинг качества тегирования: какие статьи LLM тегирует плохо |
| **feeds.fun + Structured Output (R40)** | Instructor + Pydantic: гарантированный список тегов (не free-form строка) |
| **feeds.fun + 5-Layer Memory (R39)** | Запоминать профиль интересов пользователя между сессиями |

## Контакт

- Статья: https://habr.com/ru/articles/891308/ (март 2025)
- GitHub: https://github.com/Tiendil/feeds.fun
- Смежная (Rewrite Factory для медиа, vaganovelena): https://habr.com/ru/articles/1002228/
- Смежная (LLM для новостной суммаризации): https://habr.com/ru/articles/848898/

## Смотрите также
- [Главная](../../../README.md)
- [Метрики](../../../METRICS.md)
- [Здоровье](../../../HEALTH.md)
- [Глоссарий](../../../GLOSSARY.md)
- [Сущности](../../../ENTITIES.md)
- [Решения](../../../DECISIONS.md)
