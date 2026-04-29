# Ключевые риски и как их закрывать

> [!TIP]
> Этот документ описывает MVP-подход. Начните с него для быстрого прототипа.

<!-- alert-added -->

<!-- summary -->
> > Источник: `deep-research-report (1).md`, раздел «План прототипа и возможные контакты».
**Проекты:** Svyazi, mclaude, AI Factory, Rufler, Yodoca, NGT Memory, agent-memory-mcp, AutoResearch

---
<!-- tags: memory, orchestration, security, knowledge, ingestion, architecture, roadmap, self-improvement, collaboration -->




> Источник: `deep-research-report (1).md`, раздел «План прототипа и возможные контакты».

| Риск | Почему это важно | Снижение риска |
|---|---|---|
| Schema drift и самовольная «оптимизация» структуры моделью | На extraction‑этапе сильная модель может начать «улучшать» схему вместо исполнения | Держать extraction на constrained schema + низком reasoning, а смысл переносить в post‑processing; это совпадает и с логикой Svyazi, и с выводами Memory OS. citeturn41search0turn39view3 |
| Ложные ассоциации в памяти | Ассоциативная память полезна, но легко порождает шум | Вводить review queue для `inferred`, разделять raw vs normalized, не писать Proposal сразу в Truth‑граф. citeturn41search0turn36search0 |
| Утечка PII в карточки и prompts | Discovery‑система почти неизбежно работает с чувствительными профилями | Повторить Svyazi‑паттерн privacy‑by‑design, хранить контакты отдельно, использовать allowlist/path guard, локальные embeddings там, где можно. citeturn41search0turn20view16turn35search0 |
| Лицензионный тупик на memory‑слое | Не все «open» memory‑решения одинаково permissive | Если нужен строго permissive/commercial‑friendly стек, NGT Memory надо проверять отдельно, потому что в статье указана BSL 1.1 и free‑for‑personal grant; на таком пути проще начать с Yodoca или agent-memory-mcp. citeturn22view5turn18search1turn15search3 |
| Многоагентный хаос раньше пользы | Рой даёт выгоду только после появления handoff/lock и чётких спецификаций | Начинать с mclaude + AI Factory/AIF Handoff, а Rufler/Sequential/AutoResearch добавлять после того, как появилась стабильная spec и критерии качества. citeturn20view2turn20view3turn20view4turn20view11turn20view19 |

<!-- see-also -->

---

**Смотрите также:**
- [05-план-прототипа-и-возможные-контакты](docs/04-ai-collaborations/05-план-прототипа-и-возможные-контакты.md)
- [07-mvp-planning](docs/01-svyazi/07-mvp-planning.md)
- [first-contacts](docs/svyazi-2-0/outreach/first-contacts.md)
- [mvp-plan](docs/svyazi-2-0/prototype/mvp-plan.md)


<!-- similar-docs -->

---

**Похожие документы:**
- [05-план-прототипа-и-возможные-контакты](docs/04-ai-collaborations/05-план-прототипа-и-возможные-контакты.md) (сходство 0.33)
- [05-план-прототипа-и-возможные-контакты](docs/obsidian/04-ai-collaborations/05-план-прототипа-и-возможные-контакты.md) (сходство 0.32)
- [07-mvp-planning](docs/01-svyazi/07-mvp-planning.md) (сходство 0.32)

