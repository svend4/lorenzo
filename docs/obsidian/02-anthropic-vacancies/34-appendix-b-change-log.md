---
title: "Appendix B: Change Log"
tags:
  - security
  - architecture
  - collaboration
  - anthropic-vacancies
date: 2026-04-29
---

# Appendix B: Change Log

> [!IMPORTANT]
> Ключевой документ для понимания архитектуры. Рекомендуется прочитать в первую очередь.

<!-- alert-added -->

<!-- summary -->
> - **2026-04: v1.0.0-draft** — Initial draft published.

---

<!-- toc -->
## Содержание

- [Appendix B: Change Log](#appendix-b-change-log)
  - [Комментарий к документу](#комментарий-к-документу)
  - [Паспорт 1 из 3](#паспорт-1-из-3)
- [Упоминается в](#упоминается-в)
- [Связанные документы](#связанные-документы)

---

<!-- tags: security, architecture, collaboration -->




## Appendix B: Change Log

- **2026-04: v1.0.0-draft** — Initial draft published.

---

*End of Nautilus Portal Protocol v1.0.0-draft*
```
---
### Комментарий к документу
Несколько слов о том, что я сознательно сделал в этом draft:
Стиль написан как реальная W3C/IETF specification. С разделами MUST/SHOULD/MAY, numbered sections, glossary, appendix'ами, ADR'ами. Это даёт документу серьёзный вид в глазах внешних читателей (researchers, open-source maintainers) и одновременно операционную полезность : каждое MUST можно превратить в unit test.
Я включил два раздела, которых не было в embedded README. Первое — ADR-001 с явным обоснованием federation vs merging. Второе — раздел 11 Security Considerations, где явно обозначена проблема с приватными репо (это прямо связано с вашими soz* репо). Оба раздела добавляют защиту от критики в будущих review и подачах — всегда спрашивают «почему именно так?» и «как насчёт безопасности?»
Три поля в схеме registry, которые я формализовал явно: angle , compatibility_level , bridges . В embedded-версии они упоминались, но без строгой схемы. Теперь они — нормативные.
В разделе 8 consensus я намеренно сделал v1.0 простым (string matching). Это важно: спецификация должна быть простой и реализуемой , а сложные алгоритмы (embeddings, semantic similarity) — отнесены в v2.0. Это следует принципу «worse is better» и предотвращает застревание на perfect algorithm вместо рабочей системы.
Appendix A с minimal working example — это критично. Внешний читатель должен быть способен посмотреть на 30 строк кода и понять, что такое адаптер. Без этого спецификация слишком абстрактна.
Чего тут нет сознательно:
- Нет описания MCP-интерфейса. Это отдельное расширение протокола, и оно должно жить в отдельном документе (MCP-EXTENSION.md в v1.1), чтобы не смешивать core protocol и transport layer.
- Нет описания glyph_adapter.py роли. Это внутренняя деталь вашей реализации, не часть протокола. Если позже станет ясно, что glyph-адаптеры — это обобщённый концепт (мета-адаптер над native-адаптерами), это попадёт в v1.1 как formal concept.
- Нет UI/UX specification. Web interface, CLI format output — это implementation details reference portal, не нормативные.
Что сделать с этим документом:
1. Сохранить в github.com/svend4/nautilus/PORTAL-PROTOCOL.md
2. Добавить ссылку из README standalone-репо
3. Прочитать целиком, отметить места, где нужна доработка под ваши реалии (например, пересмотреть compatibility levels если нужны другие категории)
4. Использовать как reference для написания адаптеров и для обсуждений с external contributors
Готов переходить ко второму артефакту — passport-шаблонам для info1/pro2/meta . Они будут существенно короче (1 страница каждый), human-readable, и опираются на разделы 4 и 15 этого PORTAL-PROTOCOL. Делаю?

Перехожу к passport-шаблонам. Основываюсь на разделе 4 PORTAL-PROTOCOL (структура) и на той информации, которая есть о трёх репо из embedded README, userMemories, и analysis_02_top_projects.md из data70.
Важная оговорка: я знаю о содержимом info1, pro2, meta фрагментарно. Поэтому делаю шаблоны с конкретным наполнением там, где данные точно есть , и помеченными плейсхолдерами [? уточнить] там, где нужно ваше дополнение . Вы сможете пройти по каждому за 15–30 минут и заполнить.
---
### Паспорт 1 из 3

<!-- similar-docs -->

---

**Похожие документы:**
- [[104-appendix-c-references]] (сходство 0.13)
- [[02-общий-план-развития-nautilus-portal-protocol]] (сходство 0.12)
- [[64-for-the-curious-philosophy]] (сходство 0.11)


<!-- see-also -->

---

**Смотрите также:**
- [[104-appendix-c-references]]
- [[02-общий-план-развития-nautilus-portal-protocol]]
- [[78-3-registry-nautilus-json]]
- [[64-for-the-curious-philosophy]]

<!-- backlinks-auto -->
## Упоминается в

- [[README|Вакансии Anthropic — Анализ по кластерам]]

<!-- related-auto -->
## Связанные документы

- [[64-for-the-curious-philosophy|For the Curious: Philosophy]] _37%_
- [[125-readme-mcp-md-инструкция-по-установке|README-MCP.md— инструкция по установке]] _29%_
- [[TIMELINE|Хронологическая лента событий]] _29%_
- [[02-общий-план-развития-nautilus-portal-protocol|ОБЩИЙ ПЛАН РАЗВИТИЯ NAUTILUS PORTAL PROTOCOL]] _25%_
- [[04-abstract|Abstract]] _25%_
- [[104-appendix-c-references|Appendix C: References]] _25%_
- [[105-review-methodology-md|REVIEW_METHODOLOGY.md]] _25%_
- [[122-глоссарий|Глоссарий]] _25%_
