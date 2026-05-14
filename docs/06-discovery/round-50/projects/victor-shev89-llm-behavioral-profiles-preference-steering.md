# Краткосрочные поведенческие профили LLM: управление предпочтениями без fine-tuning

**Автор:** victor_shev89 (Виктор Шевченко, NLP-инженер)  
**Хабр:** https://habr.com/ru/articles/1001554/  
**GitHub:** нет (исследовательская статья с экспериментами)  
**Слой:** orchestration  
**Дата:** февраль 2026  
**Уникальность:** "Preference control" как прикладная поведенческая экономика для LLM: краткосрочные поведенческие профили управляют поведением модели на уровне инференса без fine-tuning и без внешнего хранилища. Двухфазный ANALYST/POLICY метод снижает фреймингозависимость. Эксперимент: коэффициент неприятия потерь Gemini Flash 1.12 → 3.00 с профилем "сохранение капитала" — биологически реалистичный уровень по Тверски/Канеману. Три системных ограничения профилей: стохастичность, фреймингозависимость, корреляция параметров.

## Проблема: персонализация без долгосрочного хранения

```
Три уровня персонализации LLM:

  Уровень 1 (долгосрочная память): pgvector, SQLite → хранить факты о пользователе
  Уровень 2 (рекомендации): collaborative filtering → что пользователь предпочитает
  Уровень 3 (поведенческое управление): профили → КАК вести себя per-session

Эта статья — уровень 3.

Проблема уровня 3:
  → Нельзя просто написать в промпте "будь осторожен в инвестициях"
  → LLM игнорирует или неверно интерпретирует
  → Стохастичность: одинаковый промпт → разное поведение
  → Фреймингозависимость: "сохрани капитал" vs "избегай потерь" → разные решения
  → Корреляция: включил "осторожность" → автоматически усилилась "консервативность"

Сценарий применения:
  → Финансовый ассистент с профилем инвестора
  → HR-бот с профилем корпоративной культуры
  → Персональный тренер с профилем мотивационного стиля
  → Все — без переобучения модели, только через промпт-конфигурацию
```

## ANALYST/POLICY: двухфазный метод

```python
# victor_shev89: краткосрочные поведенческие профили LLM
# habr.com/ru/articles/1001554/

from dataclasses import dataclass
from typing import Optional
import json

@dataclass
class BehavioralProfile:
    """
    Краткосрочный поведенческий профиль LLM.

    Параметры управляют поведением модели в течение одной сессии.
    Не хранятся между сессиями (краткосрочный = per-session).

    Три системных ограничения:
    1. Стохастичность: temperature > 0 → между прогонами расхождения
    2. Фреймингозависимость: "сохрани капитал" != "избегай потерь"
       хотя экономически эквивалентны → разные решения LLM
    3. Корреляция: risk_aversion ↑ → conservative_bias ↑ (автоматически)
    """
    # Финансовые параметры
    risk_tolerance: float     # 0.0 = максимально осторожен, 1.0 = агрессивен
    loss_aversion: float      # коэф. неприятия потерь (норма ~1.5-2.5 у людей)
    time_horizon: str         # "short_term" | "medium_term" | "long_term"

    # Коммуникационные параметры
    verbosity: float          # 0.0 = краткий, 1.0 = подробный
    formality: float          # 0.0 = неформальный, 1.0 = официальный
    empathy_level: float      # 0.0 = деловой, 1.0 = эмпатичный

    # Когнитивные параметры
    analytical_depth: float   # 0.0 = поверхностный, 1.0 = глубокий анализ
    contrarian_bias: float    # склонность предлагать контраргументы

    # Метаданные
    profile_name: str
    description: str


# Пример профилей
CONSERVATIVE_INVESTOR = BehavioralProfile(
    risk_tolerance=0.2,
    loss_aversion=3.0,    # высокое неприятие потерь (vs норма ~1.5-2.5)
    time_horizon="long_term",
    verbosity=0.6,
    formality=0.7,
    empathy_level=0.3,
    analytical_depth=0.9,
    contrarian_bias=0.2,
    profile_name="conservative_investor",
    description="Сохранение капитала приоритетнее роста. Избегать волатильных активов."
)

AGGRESSIVE_GROWTH = BehavioralProfile(
    risk_tolerance=0.8,
    loss_aversion=1.2,    # низкое неприятие потерь → принимает риски
    time_horizon="medium_term",
    verbosity=0.4,
    formality=0.5,
    empathy_level=0.5,
    analytical_depth=0.7,
    contrarian_bias=0.6,
    profile_name="aggressive_growth",
    description="Максимизация доходности. Волатильность приемлема для роста."
)


class TwoPhaseProfiledLLM:
    """
    Двухфазный ANALYST/POLICY метод управления профилем.

    Проблема наивного подхода:
    Промпт: "Ты консервативный инвестор. Стоит ли покупать биткоин?"
    → Фреймингозависимость: ответ зависит от формулировки "консервативный"
    → LLM смешивает анализ и оценку → профиль влияет на факты

    ANALYST/POLICY разделяет:
    Фаза 1 (ANALYST): нейтральный анализ без профиля
    Фаза 2 (POLICY): принятие решения с профилем на основе нейтрального анализа
    """

    def __init__(self, llm_client, profile: BehavioralProfile):
        self.llm = llm_client
        self.profile = profile

    async def answer(self, question: str) -> dict:
        """
        Двухфазный ответ: нейтральный анализ → профильное решение.
        """
        # Фаза 1: ANALYST — нейтральный анализ фактов
        analyst_result = await self._analyst_phase(question)

        # Фаза 2: POLICY — принятие решения с профилем
        policy_result = await self._policy_phase(question, analyst_result)

        return {
            "answer": policy_result["answer"],
            "analysis": analyst_result,
            "profile_applied": self.profile.profile_name,
            "reasoning": policy_result.get("reasoning")
        }

    async def _analyst_phase(self, question: str) -> str:
        """
        Фаза 1: нейтральный анализ без профиля.
        Собирает факты, риски, варианты — без оценочных суждений.
        """
        prompt = f"""Проанализируй следующий вопрос нейтрально и объективно.
Перечисли: ключевые факты, возможные варианты, риски каждого варианта.
НЕ давай рекомендации — только факты.

Вопрос: {question}

Нейтральный анализ:"""
        return await self.llm.generate(prompt, temperature=0.1)

    async def _policy_phase(self, question: str, analysis: str) -> dict:
        """
        Фаза 2: принятие решения через профиль.
        Профиль применяется ПОСЛЕ нейтрального анализа → меньше фреймингозависимость.
        """
        profile_prompt = self._profile_to_prompt(self.profile)

        prompt = f"""{profile_prompt}

На основе следующего нейтрального анализа дай рекомендацию:

Вопрос: {question}

Нейтральный анализ:
{analysis}

Твоя рекомендация с учётом профиля:"""

        response = await self.llm.generate(
            prompt,
            temperature=0.2,  # чуть выше для "личности"
            response_format={"type": "json_object"}
        )
        return json.loads(response)

    def _profile_to_prompt(self, profile: BehavioralProfile) -> str:
        """Конвертировать профиль в системный промпт."""
        risk_desc = "крайне осторожен с рисками" if profile.risk_tolerance < 0.3 \
                    else "умеренно рискован" if profile.risk_tolerance < 0.7 \
                    else "принимает высокие риски"

        return f"""Ты действуешь согласно профилю: {profile.description}

Поведенческие параметры:
- Отношение к риску: {risk_desc} (risk_tolerance={profile.risk_tolerance:.1f})
- Неприятие потерь: коэффициент {profile.loss_aversion:.1f}x (норма человека: 1.5-2.5x)
- Временной горизонт: {profile.time_horizon}
- Глубина анализа: {'детальная' if profile.analytical_depth > 0.7 else 'краткая'}"""
```

## Экспериментальные результаты

```python
EXPERIMENT_RESULTS = {
    "датасет": "20 прогонов на инвестиционных задачах с перспективными теориями Тверски/Канемана",
    "модель": "Gemini 3 Flash (Gemini 2.5 Flash)",

    "коэффициент_неприятия_потерь": {
        "без_профиля_нейтральный": {
            "lambda": 1.12,
            "интерпретация": "Почти рационален — близко к risk-neutral"
        },
        "с_профилем_сохранение_капитала": {
            "lambda": 3.00,
            "интерпретация": "Биологически реалистичный уровень (человек: 1.5-2.5x)"
        },
        "человек_тверски_канеман": {
            "lambda": "1.5-2.5x",
            "интерпретация": "Эталонные данные поведенческой экономики"
        }
    },

    "системные_ограничения": {
        "стохастичность": {
            "описание": "Один и тот же профиль → разное поведение между прогонами",
            "митигация": "Снизить temperature; использовать детерминированный seed"
        },
        "фреймингозависимость": {
            "описание": "'Сохрани капитал' vs 'Избегай потерь' → разные решения",
            "митигация": "ANALYST/POLICY двухфаз: анализ отделён от оценки"
        },
        "корреляция_параметров": {
            "описание": "Включил risk_aversion=high → автоматически conservative=high",
            "митигация": "Явно задавать все параметры профиля, а не один"
        }
    }
}
```

## Применение к Lorenzo

```python
# Lorenzo: поведенческие профили для gateway.py

class LorenzoGatewayProfiles:
    """
    victor_shev89 паттерн для Lorenzo:
    Разные профили поведения /api/ask для разных контекстов запроса.

    Профиль "исследователь": глубокий технический анализ, все детали
    Профиль "менеджер": краткие выводы, бизнес-импакт, без кода
    Профиль "новичок": простые объяснения, аналогии, больше примеров

    ANALYST/POLICY: сначала нейтральный BM25-поиск,
    потом ответ через профиль пользователя.
    """

    PROFILES = {
        "researcher": BehavioralProfile(
            analytical_depth=0.95, verbosity=0.8, formality=0.6,
            profile_name="researcher",
            description="Глубокий технический анализ. Показывать код и метрики."
        ),
        "manager": BehavioralProfile(
            analytical_depth=0.4, verbosity=0.3, formality=0.8,
            profile_name="manager",
            description="Краткие выводы. Бизнес-импакт. Без технических деталей."
        )
    }
```

## Возможные комбинации

| Комбинация | Новое свойство |
|------------|----------------|
| **Behavioral Profiles + NGT Memory (R01)** | Статичная долгосрочная память + динамический профиль per-session = полная персонализация |
| **Behavioral Profiles + LangGraph (R44)** | LangGraph: analyst_node → policy_node с профилем + memory checkpoint |
| **Behavioral Profiles + LLM Observability (R45)** | Трейсинг: как профиль меняет reasoning traces — где начинается "фреймингозависимость" |
| **Behavioral Profiles + Finance RAG (R49)** | Finance RAG + профиль инвестора: разные стратегии поиска для conservative vs aggressive |
| **Behavioral Profiles + CLEV (R47)** | CLEV-консенсус трёх судей оценивает соответствие ответа профилю |

## Контакт

- Статья: https://habr.com/ru/articles/1001554/ (февраль 2026)
- Автор: victor_shev89 (Виктор Шевченко, Хабр)
- Теория перспектив: Kahneman & Tversky, 1979 (loss_aversion коэффициент)
- Смежная (персонализация v2, R35): docs/06-discovery/round-35/
- Смежная (agent-memory-mcp, R01): docs/05-habr-projects/memory/agent-memory-mcp.md
- Смежная (LangGraph, R44): docs/06-discovery/round-44/projects/langgraph-checkpoint-fault-tolerant-agents.md
