# План MVP-прототипа

> [!TIP]
> Этот документ описывает MVP-подход. Начните с него для быстрого прототипа.

<!-- alert-added -->

<!-- summary -->
> > Источник: `deep-research-report (1).md`, раздел «План прототипа и возможные контакты».
**Проекты:** Svyazi, CardIndex, AgentFS, LiteParse, Yodoca, NGT Memory, SENTINEL, LiteLLM

---
<!-- tags: memory, rag, security, knowledge, ingestion, roadmap, collaboration -->




> Источник: `deep-research-report (1).md`, раздел «План прототипа и возможные контакты».

Наиболее рациональный прототип — **не собирать всё сразу**, а доказать одну центральную способность: *система находит и объясняет кандидатные коллаборации по свободным описаниям, документам и речевым эпизодам, не теряя доказуемость и локальность*. Для этого достаточно минимального набора из пяти слоёв: Svyazi‑style ingestion, AgentFS‑style kernel, NGT Memory *или* Yodoca для памяти, research-docs/LiteParse для evidence и LiteLLM/Auto AI Router + SENTINEL для runtime‑периметра. Всё остальное лучше подключать как phase‑2, а не в день первый. citeturn41search0turn27view0turn22view4turn21view0turn20view5turn11search2turn39view0turn20view10

## Минимальная сборка прототипа

| Контур | Что входит | Зачем | Оценка усилий |
|---|---|---|---|
| Ядро данных | CardIndex‑схема, профили, raw/inferred разделение, файловый vault в стиле AgentFS | Сделать единый source of truth и трассируемый lifecycle карточки | 2–3 дня |
| Ingest и память | LLM extraction + нормализация + NGT Memory **или** Yodoca‑lite | Доказать, что из свободного текста получаются устойчивые профили и связи | 4–6 дней |
| Evidence | LiteParse/research-docs + page‑level viewer | Не просто показать match, а показать основание | 3–4 дня |
| Исполнение | LiteLLM/Auto AI Router + Tool Search + базовые правила безопасности | Удержать стоимость и не утонуть в MCP/context overhead | 2–3 дня |
| Guardrails | PII‑фильтры, allowlists, manual review для inferred | Снизить риск ложных связей и утечек | 1–2 дня |

**Итого**: реалистичный MVP — **12–18 инженерных дней** для одного сильного разработчика или пары «backend + agent/operator». Это оценка‑инференс на основе сложности и зрелости выбранных компонентов.

<!-- see-also -->

---

**Смотрите также:**
- [05-план-прототипа-и-возможные-контакты](docs/04-ai-collaborations/05-план-прототипа-и-возможные-контакты.md)
- [07-mvp-planning](docs/01-svyazi/07-mvp-planning.md)
- [executive-summary](docs/svyazi-2-0/overview/executive-summary.md)
- [first-contacts](docs/svyazi-2-0/outreach/first-contacts.md)


<!-- similar-docs -->

---

**Похожие документы:**
- [05-план-прототипа-и-возможные-контакты](docs/04-ai-collaborations/05-план-прототипа-и-возможные-контакты.md) (сходство 0.32)
- [05-план-прототипа-и-возможные-контакты](docs/obsidian/04-ai-collaborations/05-план-прототипа-и-возможные-контакты.md) (сходство 0.31)
- [07-mvp-planning](docs/01-svyazi/07-mvp-planning.md) (сходство 0.31)

