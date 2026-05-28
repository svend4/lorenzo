---
date: 2026-05-28
tags: [rag, orchestration, local-first, architecture, self-improve]
state: normalized
---

# Finam Arena: 6 LLM торгуют на бирже 39 дней — автономный эксперимент

<!-- toc-auto -->
<!-- tags: finam-arena-llm-trading, docs -->


<!-- summary -->
> Finam Arena: 6 LLM торгуют на бирже 39 дней — автономный эксперимент — раздел документации проекта Lorenzo.
 
 
 
>   — раздел документации проекта Lorenzo.


> [!WARNING]
> Документ содержит описание рисков и ограничений. Изучите их перед принятием архитектурных решений.

<!-- alert-added -->

**Автор:** команда Finam AI Lab (Хабр, март 2026)  
**Хабр:** https://habr.com/ru/companies/finam_broker/articles/1005638/  
**GitHub:** не опубликован (брокерская инфраструктура, результаты открыты)  
**Слой:** orchestration / analytics  
**Дата:** март 2026 (эксперимент: февраль–март 2026)  
**Уникальность:** Первый публичный российский эксперимент: 6 ведущих LLM (GPT-5.2, Claude Sonnet 4.5, Gemini 3 Flash, DeepSeek v3.2, Qwen3 Max, Grok 4.1) торговали реальными деньгами на MOEX и NYSE полностью автономно 39 торговых дней. Ensemble AI показал лучший результат (+1.67%). Результаты: LLM разумно ограничивают риск, но не превосходят рынок.

## Параметры эксперимента

```
Период: 2 февраля — 31 марта 2026 (39 торговых дней)
Рынки: MOEX (Московская биржа) + NYSE (США)

Начальный капитал:
  MOEX: 100,000 ₽ на каждого агента
  NYSE: $10,000 на каждого агента

Инструменты у каждого агента:
  → Текущие котировки (Finam Trade API)
  → Новостной фид (Finam + Reuters)
  → Веб-поиск (актуальные события)
  → Размещение ордеров (market, limit)
  → История сделок своего портфеля

Автономность: ПОЛНАЯ — без человеческого участия
```

## Участники и результаты (MOEX)

```
Индекс MOEX за 39 дней: -0.33% (рынок был flat)

GPT-5.2 (OpenAI):          -0.24%  ← почти вровень с рынком
Claude Sonnet 4.5 (Anthr): -0.18%  ← немного лучше рынка
Gemini 3 Flash (Google):   -0.41%  ← хуже рынка
DeepSeek v3.2:             -0.73%  ← значительно хуже
Qwen3 Max (Alibaba):       +0.30%  ← лучший из одиночных
Grok 4.1 Fast (xAI):       -0.24%  ← вровень с рынком
──────────────────────────────────
AI Ensemble (все 6):       +1.67%  ← лучший результат ★

Итог Ensemble: 101,670 ₽ (старт: 100,000 ₽)
```

## Как работал Ensemble

```python
# Ensemble не простое голосование — взвешенное на уверенность

class TradingEnsemble:
    def __init__(self, agents: list[TradingAgent]):
        self.agents = agents

    def make_decision(self, market_state: MarketState) -> Order | None:
        # Каждый агент предлагает действие + уверенность
        votes = []
        for agent in self.agents:
            action, confidence = agent.analyze(market_state)
            votes.append((action, confidence))

        # Агрегация: взвешенное голосование
        consensus = self.weighted_vote(votes)

        # Только если консенсус > порога → торговать
        if consensus.confidence > 0.65:
            return consensus.action
        else:
            return None  # воздержаться (важно!)

    def weighted_vote(self, votes):
        # buy: +confidence, sell: -confidence, hold: 0
        net_signal = sum(
            v.confidence if v.action == "buy"
            else -v.confidence if v.action == "sell"
            else 0
            for v in votes
        )
        return ConsensusSignal(
            action="buy" if net_signal > 0.3 else "sell" if net_signal < -0.3 else "hold",
            confidence=abs(net_signal) / len(votes)
        )
```

## Торговая стратегия агентов

```python
# Промпт торгового агента (упрощённо)

TRADING_AGENT_PROMPT = """
Ты — автономный трейдер на {market}.
Твоя цель: максимизировать прибыль при ограниченном риске.

Текущий портфель:
{portfolio_state}

Рыночные данные (последние 5 торговых дней):
{market_data}

Последние новости:
{news_feed}

Правила:
1. Максимум 20% капитала в одну позицию
2. Stop-loss 5% от позиции
3. Объяснить каждое решение (reasoning)
4. Можно держать cash — бездействие = стратегия

Формат ответа:
{{
  "action": "buy|sell|hold",
  "ticker": "SBER|GAZP|...",
  "amount": 1000,  // в рублях или долларах
  "reasoning": "...",
  "confidence": 0.7,
  "stop_loss": 95.5
}}
"""
```

## Выводы эксперимента

```
Что LLM делали хорошо:
  ✅ Ограничение риска: агенты редко превышали 20% в одной позиции
  ✅ News-driven decisions: реагировали на новости разумно
  ✅ Transparency: каждая сделка с объяснением (аудируемость)
  ✅ No panic: не продавали в убыток при краткосрочных коррекциях

Что плохо:
  ❌ Не превзошли рынок ни один агент-одиночка
  ❌ DeepSeek и Gemini показали негативный альфа
  ❌ Консервативность: многие держали >60% cash (недоиспользование)
  ❌ Нет адаптации стратегии: агенты не учатся из своих ошибок

Главный вывод:
  LLM = разумный консервативный инвестор,
  но не чемпион рынка.
  Ensemble > одиночный агент (+8× vs лучшего одиночки).
```

## Финансовые бенчмарки LLM (смежная статья 989842)

```
Finam AI Lab создал 6 финансовых бенчмарков:

Benchmark         | Задача                           | Вопросов
──────────────────────────────────────────────────────────────
CFA-like L3       | Портфельные стратегии + этика    | 318
CMT-like L2       | Технический анализ + риски       | 251
VLigaBench-ru     | Олимпиадные задачи (RU)          | 324
Trading_TA        | Паттерны, индикаторы, системы    | 413
Trading_Derivatives| Опционы, арбитраж, синтетика    | 544
FinDER            | Многошаговый анализ документов   | 2,837

Топ-3 по финансовым задачам (май 2026):
  1. GPT-5.2:        83.4% общий балл
  2. Claude Opus 4.7: 81.9%
  3. Gemini 3 Pro:    79.2%
  
Открытый репозиторий с метриками: github.com/finam-ai-lab/llm-finance-bench
```

## Применение к Lorenzo

Finam Arena паттерн → **Autonomous Benchmark Agent**:

```python
# improve_benchmark_agent.py (паттерн):
# Вместо ручного замера → агент автономно тестирует и сравнивает

class LorenzoBenchmarkAgent:
    """Автономно запускает и сравнивает скрипты Lorenzo"""

    def run_benchmark(self, scripts: list[str]) -> BenchmarkReport:
        results = {}
        for script in scripts:
            # Запустить → измерить время, качество выхода, ошибки
            result = self.run_timed(script)
            results[script] = {
                "time_ms": result.duration,
                "output_quality": self.evaluate_output(result.output),
                "error_rate": result.error_count / result.total_runs
            }

        # Сравнить с прошлым запуском (как агент vs рынок)
        return self.compare_with_baseline(results)
```

## Возможные комбинации

| Комбинация | Новое свойство |
|------------|----------------|
| **Finam Arena + LLM Router (R20)** | Маршрутизация торговых решений: новости → Sonnet, технический анализ → Haiku |
| **Finam Arena + Reasoning LLM (R20)** | Reasoning-модель для анализа сложных ситуаций (опционы, арбитраж) |
| **Finam Arena + Langfuse (R13)** | Трейсинг каждого торгового решения: reasoning → action → outcome |
| **Finam Arena + CAVM (R26)** | CAVM анализирует финансовые данные → Ensemble принимает решение |
| **Finam Arena + Graph RAG (R22)** | Knowledge Graph: компании → зависимости → новости → торговый сигнал |

## Контакт

- Статья (Finam Arena): https://habr.com/ru/companies/finam_broker/articles/1005638/ (март 2026)
- Смежная (финансовые бенчмарки LLM): https://habr.com/ru/companies/finam_broker/articles/989842/
- Смежная (Finam MCP для выбора акций): https://habr.com/ru/companies/finam_broker/articles/977740/
- Finam Trade API: api.finam.ru
- FinGPT (open-source): github.com/AI4Finance-Foundation/FinGPT (MIT)

## Смотрите также
- [Главная](../../../README.md)
- [Метрики](../../../METRICS.md)
- [Здоровье](../../../HEALTH.md)
- [Глоссарий](../../../GLOSSARY.md)
- [Сущности](../../../ENTITIES.md)
