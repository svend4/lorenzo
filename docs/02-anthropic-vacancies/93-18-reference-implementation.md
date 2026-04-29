# 18. Reference Implementation

<!-- summary -->
> [`github.com/svend4/nautilus`](https://github.com/svend4/nautilus).

---
<!-- tags: rag, collaboration -->




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

<!-- similar-docs -->

---

**Похожие документы:**
- [25-13-reference-implementation](25-13-reference-implementation.md) (сходство 0.36)
- [73-portal-protocol-md-v1-1](73-portal-protocol-md-v1-1.md) (сходство 0.13)
- [89-14-sdk-contract-informative](89-14-sdk-contract-informative.md) (сходство 0.12)


<!-- see-also -->

---

**Смотрите также:**
- [25-13-reference-implementation](25-13-reference-implementation.md)
- [42-author-contact](42-author-contact.md)
- [73-portal-protocol-md-v1-1](73-portal-protocol-md-v1-1.md)
- [03-portal-protocol-md](03-portal-protocol-md.md)

<!-- backlinks-auto -->
## Упоминается в

- [0. Status of This Document](05-0-status-of-this-document.md)
- [0. Status of This Document](75-0-status-of-this-document.md)
- [13. Reference Implementation](25-13-reference-implementation.md)
- [14. SDK Contract (Informative)](89-14-sdk-contract-informative.md)
- [Appendix B: Change Log](103-appendix-b-change-log.md)
- [Appendix C: References](104-appendix-c-references.md)
- [Author & Contact](42-author-contact.md)
- [Author & Contact](52-author-contact.md)
- [Author & Contact](62-author-contact.md)
- [Content Overview](48-content-overview.md)
- [History](53-history.md)
- [passports/info1.md](35-passports-info1-md.md)
- [Вакансии Anthropic — Анализ по кластерам](README.md)
- [Доступные инструменты](128-доступные-инструменты.md)
- [🇬🇧 About](68-about.md)
- [🇷🇺 О проекте](67-о-проекте.md)
## Упоминается в

- [Вакансии Anthropic — Анализ по кластерам](../README.md)

<!-- related-auto -->
## Связанные документы

- [13. Reference Implementation](25-13-reference-implementation.md) _81%_
- [Author & Contact](42-author-contact.md) _60%_
- [Author & Contact](62-author-contact.md) _53%_
- [0. Status of This Document](05-0-status-of-this-document.md) _48%_
- [0. Status of This Document](75-0-status-of-this-document.md) _48%_
- [Content Overview](48-content-overview.md) _33%_
- [Appendix C: References](104-appendix-c-references.md) _29%_
- [12. Versioning Policy](24-12-versioning-policy.md) _29%_
## Связанные документы

- [13. Reference Implementation](25-13-reference-implementation.md) _81%_
- [Author & Contact](42-author-contact.md) _60%_
- [Author & Contact](62-author-contact.md) _48%_
- [0. Status of This Document](05-0-status-of-this-document.md) _37%_
- [0. Status of This Document](75-0-status-of-this-document.md) _37%_
- [Appendix C: References](104-appendix-c-references.md) _33%_
- [passports/info1.md](35-passports-info1-md.md) _33%_
- [Author & Contact](52-author-contact.md) _33%_
