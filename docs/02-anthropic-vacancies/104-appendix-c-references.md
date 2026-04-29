# Appendix C: References

<!-- abstract-auto -->
> **Абстракт** (авто)
>
> 🎯 **Проблема:** Informative — описывает, что нужно SDK на других языках, чтобы считаться NPP-compatible.
> 🔧 **Подход:** Нормализация isfallback в протокол — честный подход, который позволяет consensus-модели различать real и fallback coverage.
> ✅ **Результат:** Нормализация isfallback в протокол — честный подход, который позволяет consensus-модели различать real и fallback coverage.
> 🏷️ **Ключевые слова:** `protocol`, `portal`, `anthropic`, `nautilus`, `appendix`, `vacancies`, `normative`, `informative`
>


<!-- summary -->
> - RFC 2119 — Key words for use in RFCs to Indicate Requirement Levels

---

<!-- toc -->
## Содержание

- [Appendix C: References](#appendix-c-references)
  - [Normative](#normative)
  - [Informative](#informative)
  - [Комментарий к документу](#комментарий-к-документу)

---

<!-- tags: memory, rag, ingestion, architecture, roadmap, anthropic, collaboration -->




## Appendix C: References

### Normative
- RFC 2119 — Key words for use in RFCs to Indicate Requirement Levels
- OpenAPI Specification v3.1.0 (for REST API schemas)
- JSON Schema (for passport validation)

### Informative
- Wolfram, S. — "A New Kind of Science" (CA classification)
- Peirce, C.S. — "Elements of Logic" (semiotic triad as ecosystem angle metaphor)
- Fielding, R. — "Architectural Styles..." (REST constraints)
- W3C ActivityPub — Federation protocol reference
- Solid Project — Personal data pods reference
- Anthropic MCP — LLM tool integration protocol

---

*End of Nautilus Portal Protocol v1.1.0-draft*

*Feedback, issues, proposals: 
[github.com/svend4/nautilus/issues](https://github.com/svend4/nautilus/issues)*
```
---
### Комментарий к документу
Несколько принципиальных решений, которые стоит проговорить отдельно.
#### Что я сохранил из v1.0
Базовая структура, нумерация разделов (1–15 из v1.0 остались с теми же номерами для обратной совместимости чтения), стиль MUST/SHOULD/MAY, ADR-формат, ядро federation-over-merging. Если у кого-то есть v1.0, они могут читать v1.1 параллельно — те же разделы говорят о том же, плюс новые.
#### Что я добавил новое
Раздел 8 — Q6 Space Normative. Это главное нововведение. В v1.0 Q6 упоминался как implementation detail. Теперь это first-class protocol concept со строгим mapping rules, normative requirement для Level 2+, и алгоритмом Q6-neighbors через Hamming.
Раздел 12 — Five Onboarding Paths. Пять стратегий (A–E) из INTEGRATION.md формализованы как equal-rank выборы. Это отражает то, что на практике все пять работают, и ни одна не "главная".
Раздел 13 — REST API Contract. Mandatory для compatible porталов. Три required endpoints ( /api/query , /api/describe , /api/health ) плюс четыре recommended. Формальные JSON schemas для responses.
Раздел 14 — SDK Contract. Informative — описывает, что нужно SDK на других языках, чтобы считаться NPP-compatible.
Раздел 16 — MCP Extension. Informative, но указывает, какие 5 tools минимум должна экспонировать MCP-обёртка. Это закладывает фундамент для будущего portal-mcp.py , о котором мы говорили.
ADR-002 и ADR-003 — два новых architecture decisions, обосновывающих Q6 upgrade и five-paths decision.
is_fallback как normative field. Это критично: STATUS.md явно признаёт 88% fallback. Нормализация is_fallback в протокол — честный подход, который позволяет consensus-модели различать real и fallback coverage.
Double coverage в Consensus ( coverage vs coverage_with_fallback ) — прямое следствие этого.
#### Что я сознательно оставил для v1.2 или v2.0
Formal bridge algebra. Part 3 implementation docs указывает это как главный концептуальный пробел. В v1.1 bridges остаются текстовыми описаниями. В v2.0 — возможная типизация (композиция, инверсия, транзитивность).
Temporal model. timeline.py и diff_report.py дают partial temporal view. Полная time-series модель — для v2.0.
Write operations. v1.x — read-only. Write-extension — возможно в v2.0 как optional extension.
Formal MCP spec. Сейчас informative. После того как portal-mcp.py будет написан и испытан — можно делать formal mandatory spec в v1.2.
#### Что ссылается на реальные артефакты в вашем репо
Документ ссылается на:
- github.com/svend4/nautilus — reference implementation
- passport_schema.json — JSON Schema для passports (предположительно существует)
- openapi.yaml — OpenAPI 3.1.0 spec (упомянут в STATUS)
- .github/workflows/ — 4 CI/CD файла (упомянуты в STATUS)
Все эти ссылки — на реальные файлы, которые я видел в документации. Если какой-то из них ещё не создан (например, passport_schema.json ) — это open item, который легко заметить.
#### Почему это важный артефакт для вас
Три причины, по которым v1.1 специфично ценно:
Первое — arxiv-ready. На этом документе можно построить arxiv preprint "Nautilus Portal Protocol: A Git-Based Federation Framework for Knowledge Ecosystems". Draft paper — это, по сути, reorganized abstract + sections 1–19 + метрики из 18.1 + цитирования.
Первое/второе — defensible claim. ADR-001, ADR-002, ADR-003 — это formal записи ваших архитектурных решений с обоснованиями. Любой reviewer, спрашивающий "почему federation, а не centralization?" — получает ссылку на ADR-001. Это научная строгость.
Третье — grant-ready. EIC Pathfinder или Horizon Europe application могут ссылаться на PORTAL-PROTOCOL.md как formal specification, которая "already has reference implementation meeting its requirements" — это сильный сигнал технической зрелости для reviewers.
#### Что делать с этим файлом
Рекомендую следующий workflow:
1. Создать docs/PORTAL-PROTOCOL.md в репо с этим содержимым (или PORTAL-PROTOCOL.md в корне, если хотите более заметно)
2. Добавить ссылку из README.md: в footer заменить Nautilus Portal Protocol v1.1 на [Nautilus Portal Protocol v1.1](./docs/PORTAL-PROTOCOL.md) с рабочим линком
3. Коммит с сообщением docs: add formal PORTAL-PROTOCOL.md v1.1 specification
4. Пройтись по документу и проверить цифры в 18.1 против актуальных (6782 LOC, 13 адаптеров, 60 тестов, 82/100 health)
5. Если есть расхождения — обновить в разделе 18.1
После этого документ можно использовать как canonical reference.
---
Готов перейти ко второму артефакту — REVIEW_METHODOLOGY.md как meta-документ о вашем трёхфазном подходе. Он существенно короче (5-7 страниц вместо 20+), и он делает ваш "параллельные версии → консолидация" workflow explicit и defensible. Делать?

Перехожу ко второму артефакту. REVIEW_METHODOLOGY.md — это meta-документ о вашем рабочем процессе. Пишу его с расчётом на две аудитории: вас самого (как напоминание правил на будущее) и внешнего читателя (researcher, collaborator, grant reviewer), который встретит артефакты с параллельными версиями и должен сразу понять, почему они так устроены.
---

<!-- similar-docs -->

---

**Похожие документы:**
- [122-глоссарий](122-глоссарий.md) (сходство 0.16)
- [34-appendix-b-change-log](34-appendix-b-change-log.md) (сходство 0.13)
- [69-section](69-section.md) (сходство 0.11)


<!-- see-also -->

---

**Смотрите также:**
- [122-глоссарий](122-глоссарий.md)
- [34-appendix-b-change-log](34-appendix-b-change-log.md)
- [69-section](69-section.md)
- [02-общий-план-развития-nautilus-portal-protocol](02-общий-план-развития-nautilus-portal-protocol.md)

<!-- backlinks-auto -->
## Упоминается в

- [13. Reference Implementation](25-13-reference-implementation.md)
- [14. SDK Contract (Informative)](89-14-sdk-contract-informative.md)
- [16. MCP Extension (Informative)](91-16-mcp-extension-informative.md)
- [18. Reference Implementation](93-18-reference-implementation.md)
- [20. ADR-002: Q6 as First-Class Protocol Concept](95-20-adr-002-q6-as-first-class-protocol-concept.md)
- [21. ADR-003: Five Onboarding Paths as Equal-Rank](96-21-adr-003-five-onboarding-paths-as-equal-rank.md)
- [3. Registry (`nautilus.json`)](78-3-registry-nautilus-json.md)
- [3. Принципы консолидации (Фаза C)](109-3-принципы-консолидации-фаза-c.md)
- [4. Nautilus Portal as Reference Substrate](141-4-nautilus-portal-as-reference-substrate.md)
- [Appendix B: Change Log](103-appendix-b-change-log.md)
- [Appendix B: Change Log](34-appendix-b-change-log.md)
- [For the Curious: Philosophy](64-for-the-curious-philosophy.md)
- [References](147-references.md)
- [Вакансии Anthropic — Анализ по кластерам](README.md)
- [Глоссарий](122-глоссарий.md)
- [Доступные инструменты](128-доступные-инструменты.md)
- [Зачем две версии параллельно](70-зачем-две-версии-параллельно.md)
- [ОБЩИЙ ПЛАН РАЗВИТИЯ NAUTILUS PORTAL PROTOCOL](02-общий-план-развития-nautilus-portal-protocol.md)
- [⬡](69-section.md)
- [🇬🇧 About](68-about.md)
- [🇷🇺 О проекте](67-о-проекте.md)
## Упоминается в

- [Вакансии Anthropic — Анализ по кластерам](../README.md)

<!-- related-auto -->
## Связанные документы

- [18. Reference Implementation](93-18-reference-implementation.md) _29%_
- [13. Reference Implementation](25-13-reference-implementation.md) _25%_
- [Appendix B: Change Log](34-appendix-b-change-log.md) _21%_
- [⬡](69-section.md) _21%_
- [Appendix B: Change Log](103-appendix-b-change-log.md) _17%_
- [Глоссарий](122-глоссарий.md) _17%_
- [References](147-references.md) _17%_
- [For the Curious: Philosophy](64-for-the-curious-philosophy.md) _17%_
## Связанные документы

- [18. Reference Implementation](93-18-reference-implementation.md) _33%_
- [13. Reference Implementation](25-13-reference-implementation.md) _29%_
- [For the Curious: Philosophy](64-for-the-curious-philosophy.md) _29%_
- [🇬🇧 About](68-about.md) _29%_
- [Appendix B: Change Log](103-appendix-b-change-log.md) _25%_
- [Глоссарий](122-глоссарий.md) _25%_
- [4. Nautilus Portal as Reference Substrate](141-4-nautilus-portal-as-reference-substrate.md) _25%_
- [Appendix A: Minimal Working Example](28-appendix-a-minimal-working-example.md) _25%_
