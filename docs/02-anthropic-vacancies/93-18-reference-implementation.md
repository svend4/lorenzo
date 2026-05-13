---
state: normalized
---

# 18. Reference Implementation

<!-- toc-auto -->
## Contents

- [18. Reference Implementation](#18-reference-implementation)
  - [18.1. Current Reference Implementation Metrics](#181-current-reference-implementation-metrics)
- [Похожие документы](#похожие-документы)
- [Использование](#использование)
- [Смотрите также](#смотрите-также)
- [Упоминается в](#упоминается-в)
- [Упоминается в](#упоминается-в-1)
- [Связанные документы](#связанные-документы)
- [Связанные документы](#связанные-документы-1)
- [Кто ссылается на этот документ (19)](#кто-ссылается-на-этот-документ-19)


> [!NOTE]
> Документ создан на основе исследования. Ссылки ведут на связанные материалы.

<!-- alert-added -->

<!-- summary -->

> [!NOTE]
> Документ создан на основе исследования. Ссылки ведут на связанные материалы.

> [`github.com/svend4/nautilus`](https://github.com/svend4/nautilus).

---
<!-- tags: rag, collaboration -->




## 18. Reference Implementation

Reference implementation: 
[`github.com/svend4/nautilus`](https://github.com/svend4/nautilus).

Reference НЕ является нормативной. Альтернативные implementations 
NPP-compatible, если они:

- Корректно парсят `[nautilus](../05-habr-projects/memory/memnet.md).json` per раздел 3
- Реализуют [BaseAdapter](01-интегральный-анализ-профиля-svend4.md) interface per раздел 6
- Производят [PortalEntry](01-интегральный-анализ-профиля-svend4.md) структуры per раздел 7
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

## Похожие документы
- [25-13-reference-implementation](25-13-reference-implementation.md) (сходство 0.36)
- [73-portal-protocol-md-v1-1](73-portal-protocol-md-v1-1.md) (сходство 0.13)
- [89-14-sdk-contract-informative](89-14-sdk-contract-informative.md) (сходство 0.12)


<!-- see-also -->

---

## Использование
```bash
# Поиск по теме документа
python scripts/improve_semantic_search.py --query "18 Reference Implementation"
```

## Смотрите также
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

<!-- backlinks -->

---

## Кто ссылается на этот документ (19)
- [03-portal-protocol-md](03-portal-protocol-md.md)
- [05-0-status-of-this-document](05-0-status-of-this-document.md)
- [103-appendix-b-change-log](103-appendix-b-change-log.md)
- [104-appendix-c-references](104-appendix-c-references.md)
- [128-доступные-инструменты](128-доступные-инструменты.md)
- [129-примеры-запросов-в-claude](129-примеры-запросов-в-claude.md)
- [164-10-appendices](164-10-appendices.md)
- [24-12-versioning-policy](24-12-versioning-policy.md)
- _...ещё 11_

