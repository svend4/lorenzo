---
state: normalized
---

# План MVP-прототипа

<!-- toc-auto -->
## Contents

- [Минимальная сборка прототипа](#минимальная-сборка-прототипа)
- [Использование](#использование)
- [Смотрите также](#смотрите-также)


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

## Использование
```bash
# Поиск по теме документа
python scripts/improve_semantic_search.py --query "План MVP прототипа"
```

## Смотрите также
- [05-план-прототипа-и-возможные-контакты](../../04-ai-collaborations/05-план-прототипа-и-возможные-контакты.md)
- [07-mvp-planning](../../01-svyazi/07-mvp-planning.md)
- [executive-summary](../overview/executive-summary.md)
- [first-contacts](../outreach/first-contacts.md)


<!-- backlinks -->

---

**Кто ссылается на этот документ (10):**
- [OUTLINE](../../OUTLINE.md)
- [READABILITY](../../READABILITY.md)
- [READING_TIME](../../READING_TIME.md)
- [SEARCH](../../SEARCH.md)
- [TABLES](../../TABLES.md)
- [reading-paths](../../reading-paths.md)
- [message-template](../outreach/message-template.md)
- [executive-summary](../overview/executive-summary.md)
- _...ещё 2_


<!-- similar-docs -->

---

**Похожие документы:**
- [mvp-plan](../../obsidian/svyazi-2-0/prototype/mvp-plan.md) (сходство 0.97)
- [05-план-прототипа-и-возможные-контакты](../../obsidian/04-ai-collaborations/05-план-прототипа-и-возможные-контакты.md) (сходство 0.32)
- [05-план-прототипа-и-возможные-контакты](../../04-ai-collaborations/05-план-прототипа-и-возможные-контакты.md) (сходство 0.32)

