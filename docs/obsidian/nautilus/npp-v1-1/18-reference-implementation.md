---
title: "18. Reference Implementation"
tags:
  - rag
  - anthropic
  - collaboration
  - nautilus
date: 2026-04-29
---

# 18. Reference Implementation

<!-- summary -->
> > Источник: MHTML‑снимок `Вакансии в Anthropic по кластерам - Claude` (корень репозитория). Раздел диалога — Nautilus Portal Protocol v1.1 RFC, написанный совместно с Claude.

---
<!-- tags: rag, anthropic, collaboration -->




> Источник: MHTML‑снимок `Вакансии в Anthropic по кластерам - Claude` (корень репозитория). Раздел диалога — Nautilus Portal Protocol v1.1 RFC, написанный совместно с Claude.

## 18. Reference Implementation

Reference implementation: 
[`github.com/svend4/nautilus`](https://github.com/svend4/nautilus).

Reference НЕ является нормативной. Альтернативные implementations 
NPP-compatible, если они:

- Корректно парсят `nautilus.json` per раздел 3
- Реализуют BaseAdapter interface per раздел 6
- Производят PortalEntry структуры per раздел 7
- Обеспечивают Q6 для Level 2+ per раздел 8
- Вычисляют consensus per раздел 9
- Предоставляют required REST endpoints per раздел 13

### 18.1. Current Reference Implementation Metrics

(Informative snapshot, v1.1.0-draft, 2026-04-19)

| Метрика | Значение |
|---------|----------|
| Python LOC | 6 782 |
| Адаптеров | 13 (7 реестровых + 6 расширенных) |
| Тестов | 60 / 60 passing |
| mypy errors | 0 |
| Внешних зависимостей | 0 (stdlib only) |
| Health Score | 82 / 100 |
| Q6 coverage (real) | 21.9% (14 / 64 vertices) |

---

<!-- see-also -->

---

**Смотрите также:**
- [[93-18-reference-implementation]]
- [[13-reference-implementation]]
- [[25-13-reference-implementation]]
- [[14-sdk]]


<!-- similar-docs -->

---

**Похожие документы:**
- [[93-18-reference-implementation]] (сходство 0.67)
- [[93-18-reference-implementation]] (сходство 0.59)
- [[13-reference-implementation]] (сходство 0.45)

