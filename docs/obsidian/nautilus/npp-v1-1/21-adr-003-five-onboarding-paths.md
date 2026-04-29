---
title: "21. ADR-003: Five Onboarding Paths as Equal-Rank"
tags:
  - anthropic
  - nautilus
date: 2026-04-29
---

# 21. ADR-003: Five Onboarding Paths as Equal-Rank

<!-- summary -->
> > Источник: MHTML‑снимок `Вакансии в Anthropic по кластерам - Claude` (корень репозитория). Раздел диалога — Nautilus Portal Protocol v1.1 RFC, написанный совместно с Claude.

---
<!-- tags: anthropic -->




> Источник: MHTML‑снимок `Вакансии в Anthropic по кластерам - Claude` (корень репозитория). Раздел диалога — Nautilus Portal Protocol v1.1 RFC, написанный совместно с Claude.

## 21. ADR-003: Five Onboarding Paths as Equal-Rank

**Status**: Accepted (new in v1.1)

**Context**: В v1.0 была одна "основная" стратегия подключения 
(manual adapter). В процессе развития reference implementation 
появились 4 дополнительных пути (B–E). Возникал вопрос: какой 
канонический?

**Decision**: Все 5 путей — равнорангованные. Выбор делается по 
контексту (раздел 12.6), не по иерархии.

**Consequences**:

**Positive**:
- Flexibility для разных use cases
- Self-declaring repos (Path C) enables federation без центральной 
координации
- Automated paths (D, E) scale для fleet-federation

**Negative**:
- Больше документации
- Users могут путаться, какой путь выбрать (mitigated via раздел 
12.6 guidance)

---

<!-- see-also -->

---

**Смотрите также:**
- [[96-21-adr-003-five-onboarding-paths-as-equal-rank]]
- [[19-adr-001-federation-over-merging]]
- [[20-adr-002-q6-first-class]]
- [[11-relevance-ranking]]


<!-- similar-docs -->

---

**Похожие документы:**
- [[96-21-adr-003-five-onboarding-paths-as-equal-rank]] (сходство 0.73)
- [[96-21-adr-003-five-onboarding-paths-as-equal-rank]] (сходство 0.68)
- [[20-adr-002-q6-first-class]] (сходство 0.27)

