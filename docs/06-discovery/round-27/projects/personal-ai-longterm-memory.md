---
date: 2026-05-28
tags: [memory, rag, orchestration, security, knowledge]
state: normalized
---

# AI-агент с долгосрочной памятью: личный аналитик на Claude Code + PostgreSQL

<!-- toc-auto -->
<!-- tags: personal-ai-longterm-memory, docs -->


<!-- summary -->
> AI-агент с долгосрочной памятью: личный аналитик на Claude Code + PostgreSQL — раздел документации проекта Lorenzo.
 
 
 
>   — раздел документации проекта Lorenzo.


> [!WARNING]
> Документ содержит описание рисков и ограничений. Изучите их перед принятием архитектурных решений.

<!-- alert-added -->

**Автор:** разработчик (системный аналитик, финтех), Хабр, март 2026  
**Хабр:** https://habr.com/ru/articles/1007940/  
**GitHub:** не опубликован (личный проект, Dockerfile в статье)  
**Слой:** memory / orchestration / knowledge  
**Дата:** март 2026  
**Уникальность:** Персональный AI-аналитик здоровья с послойной архитектурой памяти: оперативная (сессия) + эпизодическая (PostgreSQL+pgvector) + семантическая (MEMORY.md — поведенческие паттерны за месяцы). Memory Synthesizer пишет накопленные инсайты в постоянный файл между сессиями. 14 структурированных инструментов, Docker Compose, Telegram-бот — полностью локально без облака.

## Проблема: AI-ассистент забывает вас после каждой сессии

```
Обычный Claude/GPT:
  Сессия 1: "У меня проблемы со сном в рабочие дни"
  Сессия 2: Claude забыл → начинает с чистого листа
  
Проблема для личного ассистента:
  → Не строит долгосрочные паттерны
  → Не замечает корреляции (стресс → сон → работоспособность)
  → Каждый раз нужен onboarding заново
  → Нет персонализации под конкретного человека
```

## Трёхслойная архитектура памяти

```python
class PersonalAnalystMemory:
    """
    Слой 1: Оперативная память (in-session context window)
    Слой 2: Эпизодическая память (PostgreSQL + pgvector)
    Слой 3: Семантическая память (MEMORY.md — поведенческие паттерны)
    """

    # Слой 1: текущая сессия
    session_context: list[Message] = []

    # Слой 2: история событий с embeddings
    episodic_store: PostgreSQLStore  # pgvector, 1536-dim embeddings

    # Слой 3: долгосрочные паттерны (человекочитаемый файл)
    semantic_memory_path: str = "~/MEMORY.md"


class MemorySynthesizer:
    """Запускается в конце каждой сессии: извлекает паттерны → пишет в MEMORY.md"""

    def synthesize(self, session: Session, episodic: PostgreSQLStore) -> None:
        # Берём последние 30 дней событий
        recent_events = episodic.query(
            days=30,
            categories=["sleep", "nutrition", "workouts", "mood", "labs"]
        )

        # LLM извлекает поведенческие паттерны
        insights = self.llm.extract_patterns(
            events=recent_events,
            existing_memory=self.read_memory()
        )

        # Обновляет MEMORY.md (не дублирует, мержит)
        self.update_memory_file(insights)
        # → "Пользователь стабильно плохо спит в воскресенье вечером.
        #    Корреляция: когда занятий >3/нед → среднее настроение +0.8"
```

## 14 инструментов агента

```python
AGENT_TOOLS = {
    # Группа 1: Сон (4 инструмента)
    "log_sleep": "записать сон: время, качество, пробуждения",
    "analyze_sleep_patterns": "паттерны сна за N дней",
    "compare_sleep_factors": "корреляция сна с другими метриками",
    "get_sleep_recommendations": "рекомендации на основе истории",

    # Группа 2: Питание (3 инструмента)
    "log_meal": "записать приём пищи: продукты, КБЖУ",
    "analyze_nutrition_week": "питание за неделю",
    "find_nutrition_patterns": "что едите в стрессовые дни",

    # Группа 3: Тренировки (3 инструмента)
    "log_workout": "записать тренировку: тип, нагрузка, самочувствие",
    "analyze_workout_progress": "прогресс за период",
    "correlate_workout_recovery": "тренировки vs восстановление",

    # Группа 4: Лаборатория и общее (4 инструмента)
    "log_lab_results": "записать результаты анализов",
    "track_biomarkers": "отслеживание биомаркеров в динамике",
    "generate_weekly_report": "аналитический отчёт за неделю",
    "ask_my_history": "свободный вопрос по истории данных"
}

# Ключевой инструмент:
async def ask_my_history(query: str) -> str:
    """
    'В какие дни недели я хуже сплю?'
    'Есть ли связь между нагрузкой и настроением?'
    'Когда у меня лучше анализы — после кардио или силовых?'
    """
    # Шаг 1: семантический поиск по MEMORY.md (быстро)
    memory_context = semantic_search(MEMORY_PATH, query)

    # Шаг 2: точный поиск по pgvector (медленнее, но точнее)
    relevant_events = episodic_store.similarity_search(
        query_embedding=embed(query),
        top_k=20,
        date_filter="last_90_days"
    )

    # Шаг 3: LLM анализирует
    return llm.analyze(
        query=query,
        memory=memory_context,
        events=relevant_events
    )
```

## Технический стек

```yaml
# docker-compose.yml (упрощённо)

services:
  postgres:
    image: pgvector/pgvector:pg16
    environment:
      POSTGRES_DB: personal_analytics
    volumes:
      - pgdata:/var/lib/postgresql/data

  agent:
    build: .
    environment:
      - ANTHROPIC_API_KEY=${ANTHROPIC_API_KEY}
      - DATABASE_URL=postgresql://postgres:5432/personal_analytics
    volumes:
      - ~/MEMORY.md:/app/MEMORY.md  # постоянный файл паттернов

  bot:
    image: python:3.12-slim
    # Telegram бот через aiogram 3
    # FastAPI для webhooks

# Всё локально: данные не покидают машину
# Claude API = единственный облачный компонент
```

## Паттерн долгосрочной памяти

```python
# Как MEMORY.md выглядит через 3 месяца использования:

MEMORY_EXAMPLE = """
# Персональные паттерны (обновлено: 2026-03-10)

## Сон
- Стабильно плохой сон в воскр. вечером (засыпание >60 мин, 89% случаев)
- Лучший сон: вт/ср, коррелирует с рабочей нагрузкой ≤6ч
- Кофе после 14:00 → ухудшение засыпания на 23 мин (n=47)

## Тренировки vs восстановление
- После 3+ тренировок/нед → настроение +0.8 (шкала 1-10)
- Оптимум: 4 тренировки/нед, не более 2 силовых подряд

## Биомаркеры
- Ферритин опускается ниже 40 каждые ~6 мес → профилактика нужна
- Витамин D: зима = стабильно дефицит без добавок

## Стресс-паттерны
- Стрессовые недели: +340 ккал/день, -1.2ч сна, -1 тренировка
"""

# При каждой сессии MEMORY.md грузится в системный промпт
# → агент знает вас даже в первом сообщении новой сессии
```

## Применение к Lorenzo

Lorenzo тоже нуждается в памяти между сессиями:

```python
# improve_session_memory.py (паттерн):

class LorenzoSessionMemory:
    """
    Аналог: между сессиями Lorenzo помнит контекст исследования
    """
    memory_path = "docs/SESSION_MEMORY.md"

    def load_context(self) -> str:
        """Загрузить в промпт при старте сессии"""
        return read(self.memory_path)
        # → "В раунде R26 нашли CAVM. R27 ищем: кибербезопасность,
        #    персональный AI, планирование агентов, DevEx.
        #    Следующий после R27: мониторинг embedding drift, ..."

    def synthesize_after_round(self, round_data: RoundData) -> None:
        """После каждого раунда — обновить память"""
        patterns = self.extract_patterns(round_data)
        self.update_memory(patterns)
        # → Паттерн: финтех-тематика → много практических кейсов
        # → Паттерн: Solar/Sber/VK = корпоративные, богатые деталями
```

## Возможные комбинации

| Комбинация | Новое свойство |
|------------|----------------|
| **Personal AI + Durable State (R23)** | SessionContext = слой 1 памяти; агент не теряет контекст при реконнекте |
| **Personal AI + agent-memory-mcp (R01)** | MCP-протокол для чтения/записи персональной памяти |
| **Personal AI + LLM Privacy (R24)** | Privacy Gateway: личные данные локально, облако видит только анонимный запрос |
| **Personal AI + CAVM (R26)** | CAVM пайплайн: данные за неделю → анализ → отчёт → обновление MEMORY.md |
| **Personal AI + Graph RAG (R22)** | Граф личных связей: события → концепты → паттерны в Neo4j |

## Контакт

- Статья: https://habr.com/ru/articles/1007940/ (март 2026)
- Смежная (Obsidian как память агентов): https://habr.com/ru/articles/1033746/
- Смежная (LLM-Wiki личная база знаний): https://habr.com/ru/articles/1031970/
- pgvector: github.com/pgvector/pgvector (PostgreSQL extension)
- aiogram 3: github.com/aiogram/aiogram (Telegram bot framework)

## Смотрите также
- [Главная](../../../README.md)
- [Метрики](../../../METRICS.md)
- [Здоровье](../../../HEALTH.md)
- [Глоссарий](../../../GLOSSARY.md)
- [Сущности](../../../ENTITIES.md)
