# Практичный бюджетный роутинг моделей

<!-- summary -->
> > Источник: `deep-research-report (1).md`, раздел «Безопасность, приватность и бюджетный роутинг».
**Проекты:** LiteLLM, Auto AI Router, Tool Search, AutoResearch

---
<!-- tags: rag, security, ingestion, architecture, self-improvement -->




> Источник: `deep-research-report (1).md`, раздел «Безопасность, приватность и бюджетный роутинг».

| Этап | Дефолт | Когда эскалировать |
|---|---|---|
| Extraction из свободного текста | Локальная или дешёвая модель + строгая schema guidance | Только если extraction‑quality стабильно проваливает ваши acceptance tests |
| Нормализация | Детерминированный код | Практически никогда не переводить это на дорогую модель |
| Retrieval / rerank | Non‑LLM hybrid retrieval или локальный reranker | При multi-hop вопросах и слабой explainability |
| Объяснение матча / summary | Средний облачный tier | Если нужен высокий stylistic quality, а не только фактология |
| Финальный внешний отчёт | Сильная модель | Только для user-facing/public/legal‑style текста |
| Ночной ресёрч / оптимизация | AutoResearch‑подход с жёстким бюджетом и rollback | Когда уже есть benchmark и понятная функция качества |

## Обоснование

Эта схема опирается сразу на несколько наблюдений из найденных источников. Во‑первых, Memory OS показывает, что на extraction высокий reasoning не всегда полезен и может ломать schema discipline. Во‑вторых, Tool Search снижает context tax ещё до начала работы. В‑третьих, Auto AI Router и LiteLLM позволяют скрыть провайдерную сложность за единым API, а RLM‑Toolkit прямо формализует budget‑first / privacy‑first конфигурации. citeturn39view3turn39view1turn39view0turn11search2turn20view18

## Три режима

- **Самый дешёвый** — extraction, indexing и basic memory на локальной модели; в облако только ambiguous ranking и финальное объяснение.
- **Самый приватный** — локальные модели плюс gateway как внутренний abstraction layer.
- **Самый качественный** — локально retrieval и memory; премиум‑модель только на объяснение, конфликт‑resolution и сложные relation‑queries.

При таком подходе дорогая модель перестаёт быть «двигателем всего» и становится «дорогим, но редким specialist step». citeturn20view18turn39view0turn11search2

<!-- see-also -->

---

**Смотрите также:**
- [06-security-privacy](docs/01-svyazi/06-security-privacy.md)
- [06-безопасность-приватность-и-бюджетный-роутинг](docs/04-ai-collaborations/06-безопасность-приватность-и-бюджетный-роутинг.md)
- [privacy](docs/svyazi-2-0/security/privacy.md)
- [E-execution-plane](docs/svyazi-2-0/ensembles/E-execution-plane.md)

