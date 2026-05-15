# Rewrite Factory: LLM в стиле конкретного СМИ через стилевую декомпозицию

> [!NOTE]
> Документ создан на основе исследования. Ссылки ведут на связанные материалы.

<!-- alert-added -->

**Автор:** vaganovelena (Лена Богданова), Rewrite Factory / Рерайт-Завод  
**Хабр:** https://habr.com/ru/articles/1002228/  
**GitHub:** нет (production-система)  
**Слой:** orchestration / analytics  
**Дата:** февраль 2025  
**Уникальность:** Декомпозиция редакционного голоса на независимые компоненты (структура/тон/лексика/заголовки/эмоциональный регистр) вместо монолитного промпта. Осознанный отказ от RAG: семантическое сходство не захватывает стилистику, chunking уничтожает целостность editorial voice. Тег-based пример selection + Handlebars templating. Производственная автоматизация рерайтинга для региональных российских СМИ.

## Проблема: монолитный промпт не захватывает стиль СМИ

```
Наивный подход: "Перепиши эту новость в стиле РБК"
  → LLM выдаёт "деловой текст" — общее представление о РБК
  → Не захватывает: конкретную длину абзацев РБК, их паттерны заголовков,
    специфическую лексику, эмоциональный регистр, структуру лида

Проблема RAG для стиля:
  → Векторный поиск: "найди похожие новости РБК"
  → Семантическое сходство ищет по ТЕМЕ, не по СТИЛЮ
  → Чанкинг разрушает паттерны: заголовок+лид+тело = целостный образец

Что работает:
  → Стилевая декомпозиция: каждый аспект стиля анализируется отдельно
  → Тег-based selection: примеры подбираются по рубрике/теме, не по семантике
  → Handlebars templating: стиль-профиль инжектируется структурированно
```

## Архитектура: стилевая декомпозиция на 5 компонентов

```python
# Rewrite Factory: стилевая декомпозиция editorial voice

from dataclasses import dataclass
from typing import Optional

@dataclass
class StyleProfile:
    """
    Редакционный стиль СМИ = 5 независимых компонентов.
    Каждый анализируется отдельно → reusable профиль.
    """

    # Компонент 1: Структурные паттерны
    structure: dict = None
    # → средняя длина абзаца (слов), количество абзацев
    # → позиция цитат (первый/второй/последний абзац)
    # → наличие буллет-листов, структура лида

    # Компонент 2: Тональность
    tone: dict = None
    # → нейтральный / аналитический / эмоциональный / экспертный
    # → дистанция: официальная / неформальная
    # → позиция к предмету: нейтральная / оценочная

    # Компонент 3: Лексические предпочтения
    lexical: dict = None
    # → предпочтительные глаголы действия (заявил vs сказал vs отметил)
    # → канцелярит: высокий / низкий
    # → иностранные слова: много / мало
    # → специфические клише издания

    # Компонент 4: Паттерны заголовков
    headline: dict = None
    # → длина (слов), наличие двоеточия
    # → активный vs пассивный залог
    # → вопросительные заголовки: да/нет
    # → использование цифр в заголовке

    # Компонент 5: Эмоциональный регистр
    emotional_register: dict = None
    # → инклюзивность: "мы"/"нас" vs безличное
    # → экспрессия: восклицания, усилители
    # → оценочные слова: позитивные / негативные / нейтральные


class StyleAnalyzer:
    """
    Анализ образцов → Style Profile.
    Каждый компонент — отдельный LLM вызов с узким промптом.
    """

    STRUCTURE_PROMPT = """
Проанализируй структурные паттерны следующих {n} статей издания {publication}.

Статьи:
{articles}

Верни JSON:
{{
  "avg_paragraph_length_words": X,
  "avg_paragraphs_per_article": X,
  "lead_style": "one-sentence|two-sentence|anecdote|data-first",
  "quote_position": "early|middle|late|distributed",
  "uses_bullets": true|false,
  "typical_article_length_words": X
}}
"""

    HEADLINE_PROMPT = """
Проанализируй паттерны заголовков {publication}:

Заголовки:
{headlines}

Верни JSON:
{{
  "avg_word_count": X,
  "uses_colon": "often|rarely|never",
  "voice": "active|passive|mixed",
  "question_headlines_pct": X,
  "uses_numbers": "often|rarely|never",
  "typical_pattern": "Описание типичного паттерна в 1 предложении"
}}
"""

    def analyze_publication(self, publication_name: str,
                             sample_articles: list[str]) -> StyleProfile:
        """Параллельный анализ всех 5 компонентов."""
        import asyncio

        async def analyze_all():
            tasks = [
                self._analyze_structure(publication_name, sample_articles),
                self._analyze_tone(publication_name, sample_articles),
                self._analyze_lexical(publication_name, sample_articles),
                self._analyze_headlines(publication_name, sample_articles),
                self._analyze_emotional(publication_name, sample_articles)
            ]
            results = await asyncio.gather(*tasks)
            return StyleProfile(*results)

        return asyncio.run(analyze_all())
```

## Почему RAG не работает для стиля

```python
class StyleVsRAGComparison:
    """
    Из статьи: почему авторы отказались от RAG для стилевой адаптации.
    """

    RAG_PROBLEM_1 = """
    Семантический поиск ищет по СМЫСЛУ, не по СТИЛЮ:

    Запрос: "новость об акциях ЦБ"
    RAG найдёт: статьи об акциях ЦБ (по теме)
    Не найдёт: образцы из нужного стилевого регистра

    Нужен: поиск по СТИЛЮ — "покажи статьи того же регистра/тональности"
    → Этого стандартный RAG не делает
    """

    RAG_PROBLEM_2 = """
    Chunking уничтожает целостность образца:

    Статья РБК = целостный стилистический образец
    Chunk статьи РБК = фрагмент без контекста заголовка, лида, концовки

    LLM должна видеть ЦЕЛУЮ статью, чтобы понять паттерн
    → Chunking это делает невозможным
    """

    SOLUTION = """
    Тег-based selection (вместо semantic search):
    → Каждый образец помечается тегами: рубрика, тема, тип материала
    → Для рерайтинга: подобрать образцы той же рубрики/типа
    → Семантика не нужна — нужна типологическая близость
    """
```

## Handlebars templating для инжекции стиля

```python
# Handlebars шаблоны для структурированного промпта

REWRITE_TEMPLATE = """
{{! Шаблон рерайтинга с инжектированным стилем }}

Ты — редактор издания {{publication_name}}.

СТИЛЬ ИЗДАНИЯ:
Структура: {{style.structure.lead_style}} лид, {{style.structure.avg_paragraph_length_words}} слов в абзаце
Тональность: {{style.tone.register}}, дистанция {{style.tone.distance}}
Заголовки: {{style.headline.typical_pattern}}
Лексика: {{style.lexical.preferred_verbs}} (не: {{style.lexical.avoided_words}})

ОБРАЗЦЫ СТИЛЯ ({{n_examples}} статей):
{{#each examples}}
  ---
  Заголовок: {{this.headline}}
  Текст: {{this.body}}
{{/each}}

ИСХОДНЫЙ МАТЕРИАЛ:
{{source_text}}

Перепиши материал в стиле {{publication_name}}. Длина: ~{{target_length}} слов.
"""

class RewriteEngine:
    """
    Production пайплайн для региональных СМИ.
    """

    def rewrite_for_publication(self, source_text: str,
                                 publication: str) -> str:
        # 1. Загрузить стиль-профиль (предвычислен)
        style = self.style_db.get(publication)

        # 2. Тег-based selection: подобрать образцы
        examples = self.select_examples(
            publication=publication,
            source_tags=self.extract_tags(source_text),
            n=3
        )

        # 3. Рендер шаблона
        prompt = self.render_template(
            REWRITE_TEMPLATE,
            publication_name=publication,
            style=style,
            examples=examples,
            source_text=source_text,
            target_length=style.structure.typical_article_length_words
        )

        # 4. LLM рерайтинг
        return self.llm.complete(prompt)

    def select_examples(self, publication: str,
                         source_tags: list[str], n: int = 3) -> list[dict]:
        """
        Тег-based selection: статьи той же рубрики, не по семантике.
        """
        candidates = self.article_db.filter(
            publication=publication,
            tags_overlap=source_tags  # пересечение тегов
        )
        # Выбрать n самых свежих (актуальный стиль)
        return sorted(candidates, key=lambda x: x.date, reverse=True)[:n]
```

## Production пайплайн для региональных СМИ

```python
PRODUCTION_PIPELINE = {
    "клиенты": "региональные городские порталы, Telegram-каналы",
    "задача": "автоматический рерайтинг федеральных новостей в локальный стиль",

    "шаги": [
        "1. Мониторинг RSS/Telegram: новые материалы федеральных изданий",
        "2. Fact-checking: проверка основных фактов (кто/что/когда/где)",
        "3. Тег-извлечение: рубрика, тема, тип материала",
        "4. Стиль-selection: 3 образца той же рубрики из архива",
        "5. LLM рерайтинг по стиль-профилю",
        "6. Пост-обработка: проверка длины, заголовка, лида",
        "7. CMS публикация или очередь на ревью редактора"
    ],

    "метрики_производительности": {
        "время_на_статью": "~45 секунд (vs 2-3 часа вручную)",
        "экономия": ">90% времени редактора",
        "качество_оценка": "редакторы принимают без правок в 60-70% случаев"
    }
}
```

## Применение к Lorenzo

```python
# Lorenzo пишет технические документы.
# Rewrite Factory паттерн: стилевая адаптация документов

class LorenzoStyleAdapter:
    """
    Lorenzo создаёт документы разных типов (project files, session logs).
    Стиль-декомпозиция: обеспечить консистентный стиль всех файлов.
    """

    LORENZO_STYLE_PROFILE = StyleProfile(
        structure={"lead_style": "metadata-first",
                   "avg_paragraph_length_words": 25},
        tone={"register": "technical", "distance": "neutral"},
        headline={"pattern": "Title: описание через двоеточие"},
        lexical={"preferred_verbs": ["реализует", "использует", "поддерживает"]}
    )
```

## Возможные комбинации

| Комбинация | Новое свойство |
|------------|----------------|
| **Rewrite Factory + Enterprise RAG (R32)** | RAG для поиска образцов по тегам (не семантике) — гибридный тег+BM25 |
| **Rewrite Factory + LLM Data Quality (R33)** | DQ правила для стиль-профилей: проверка консистентности стиля |
| **Rewrite Factory + HITL (R30)** | Редактор одобряет/отклоняет рерайтинг → обновление стиль-профиля |
| **Rewrite Factory + Cognitive Memory (R31)** | Стиль-профиль как SEMANTIC memory node: эволюция редакционного стиля |
| **Rewrite Factory + MT-Bench RU (R34)** | Бенчмарк стилевой точности: оценка LLM на задаче style transfer |

## Контакт

- Статья: https://habr.com/ru/articles/1002228/ (февраль 2025)
- Rewrite Factory: рерайт-завод.рф
- Смежная (n8n + GigaChat + Telegram дайджест): https://habr.com/ru/articles/966928/
- Смежная (детекция AI-текста гибридный подход): https://habr.com/ru/amp/publications/1029046/
- Смежная (мониторинг СМИ vs ChatGPT): https://habr.com/ru/companies/scan_interfax/articles/1026422/
