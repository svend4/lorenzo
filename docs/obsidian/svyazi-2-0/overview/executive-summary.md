---
title: "Executive summary"
tags:
  - svyazi-2-0
date: 2026-04-29
---

# Executive summary

> [!TIP]
> Этот документ описывает MVP-подход. Начните с него для быстрого прототипа.

<!-- alert-added -->

<!-- summary -->
> > Источник: `deep-research-report (1).md`, раздел «Executive summary».
**Проекты:** Svyazi, CardIndex, AgentFS, mclaude, AI Factory, Rufler, LiteParse, Legal RAG

---
<!-- tags: memory, rag, orchestration, security, knowledge, ingestion, local-first, architecture, roadmap, collaboration -->




> Источник: `deep-research-report (1).md`, раздел «Executive summary».

Если смотреть не на отдельные статьи, а на то, как их можно состыковать, то на Хабре за первые месяцы 2026 года уже сложился почти полный конструктор для **Svyazi‑2.0**: ingestion и нормализация профилей из свободного текста, agent‑first knowledge base, файлосистемная память для агентов, ассоциативная и консолидируемая долговременная память, визуально проверяемый RAG, многоагентная оркестрация, безопасный MCP‑слой, локальный voice→vault вход и бюджетно‑осознанный роутинг моделей. Самостоятельно каждый блок выглядит либо как аккуратный pet‑project, либо как «узкая» инженерная находка. Но вместе они уже дают не «ещё один AI‑ассистент», а операционную систему для обнаружения коллабораций, накопления доказуемого знания и полуавтономной работы агентов в локальном контуре. citeturn41search0turn33view3turn33view4turn21view0turn22view4turn20view5turn20view6turn20view11

Самая сильная линия синергии выглядит так. Основа — Svyazi‑подобный гибридный пайплайн: LLM извлекает смысл, детерминированный код нормализует, а **CardIndex** фиксирует состояние карточки и версионирование. Поверх этого нужен agent‑readable слой знаний и единый source of truth для разных рантаймов — здесь хорошо ложатся knowledge‑space и AgentFS. Дальше память должна не просто хранить факты, а уметь усиливать слабые сигналы, консолидировать эпизоды и забывать шум — это зона Yodoca, NGT Memory, MemNet и более инженерных систем вроде agent-memory-mcp/Memory OS. Для многоагентной работы уже есть mclaude, AI Factory, AIF Handoff, Rufler и протокол Sequential; для forensic‑режима — research-docs/LiteParse, Legal RAG, Hybrid RAG и Graph RAG; для безопасного и дешёвого исполнения — Tool Search, LiteLLM, Auto AI Router, RLM-Toolkit и SENTINEL. citeturn33view2turn27view0turn21view1turn22view3turn21view4turn20view16turn39view3turn20view2turn20view3turn20view4turn20view11turn20view5turn34view2turn34view3turn39view1turn39view0turn20view18turn20view10

Главный аналитический вывод: **на Хабре пока не видно одного готового проекта, который уже собрал все слои в единое целое, но видно много авторов, каждый из которых почти идеально закрывает один слой будущей системы.** Поэтому реальная ценность исследования — не в списке ссылок, а в правильной сборке ансамблей. Наиболее прагматичный путь — не строить большой новый монолит, а начать с минимального прототипа из пяти компонентов: Svyazi‑подобный import/normalize/CardIndex, AgentFS‑подобное файловое ядро, NGT կամ Yodoca‑подобная память, research-docs/LiteParse‑подобный evidence‑слой и LiteLLM/Auto AI Router+SENTINEL как исполнительный периметр. citeturn41search0turn27view0turn22view4turn21view0turn20view5turn11search2turn39view0turn20view10

<!-- see-also -->

---

**Смотрите также:**
- [[01-executive-summary]]
- [[mvp-plan]]
- [[license-tree]]
- [[first-contacts]]


<!-- similar-docs -->

---

**Похожие документы:**
- [[01-executive-summary]] (сходство 0.72)
- [[01-executive-summary]] (сходство 0.67)
- [[01-executive-summary]] (сходство 0.57)

