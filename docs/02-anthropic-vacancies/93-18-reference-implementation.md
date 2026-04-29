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
- [25-13-reference-implementation](docs/02-anthropic-vacancies/25-13-reference-implementation.md) (сходство 0.36)
- [73-portal-protocol-md-v1-1](docs/02-anthropic-vacancies/73-portal-protocol-md-v1-1.md) (сходство 0.13)
- [89-14-sdk-contract-informative](docs/02-anthropic-vacancies/89-14-sdk-contract-informative.md) (сходство 0.12)


<!-- see-also -->

---

**Смотрите также:**
- [25-13-reference-implementation](docs/02-anthropic-vacancies/25-13-reference-implementation.md)
- [42-author-contact](docs/02-anthropic-vacancies/42-author-contact.md)
- [73-portal-protocol-md-v1-1](docs/02-anthropic-vacancies/73-portal-protocol-md-v1-1.md)
- [03-portal-protocol-md](docs/02-anthropic-vacancies/03-portal-protocol-md.md)

<!-- backlinks-auto -->
## Упоминается в

- [Вакансии Anthropic — Анализ по кластерам](docs/02-anthropic-vacancies/README.md)

<!-- related-auto -->
## Связанные документы

- [13. Reference Implementation](docs/02-anthropic-vacancies/25-13-reference-implementation.md) _81%_
- [Author & Contact](docs/02-anthropic-vacancies/42-author-contact.md) _60%_
- [Author & Contact](docs/02-anthropic-vacancies/62-author-contact.md) _48%_
- [0. Status of This Document](docs/02-anthropic-vacancies/05-0-status-of-this-document.md) _37%_
- [0. Status of This Document](docs/02-anthropic-vacancies/75-0-status-of-this-document.md) _37%_
- [Appendix C: References](docs/02-anthropic-vacancies/104-appendix-c-references.md) _33%_
- [passports/info1.md](docs/02-anthropic-vacancies/35-passports-info1-md.md) _33%_
- [Author & Contact](docs/02-anthropic-vacancies/52-author-contact.md) _33%_
