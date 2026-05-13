---
state: normalized
---

# 12. Versioning Policy

<!-- toc-auto -->
## Contents

- [12. Versioning Policy](#12-versioning-policy)
  - [12.1. Semver](#121-semver)
  - [12.2. Version in Registry](#122-version-in-registry)
  - [12.3. Breaking Changes Process](#123-breaking-changes-process)
- [Похожие документы](#похожие-документы)
- [Использование](#использование)
- [Смотрите также](#смотрите-также)
- [Упоминается в](#упоминается-в)
- [Упоминается в](#упоминается-в-1)
- [Связанные документы](#связанные-документы)
- [Связанные документы](#связанные-документы-1)
- [Кто ссылается на этот документ (9)](#кто-ссылается-на-этот-документ-9)


> [!NOTE]
> Документ создан на основе исследования. Ссылки ведут на связанные материалы.

<!-- alert-added -->

<!-- summary -->

> [!NOTE]
> Документ создан на основе исследования. Ссылки ведут на связанные материалы.

> - **Major** (v1 → v2): breaking changes в interfaces или schemas

---
<!-- tags: architecture -->




## 12. Versioning Policy

### 12.1. Semver

NPP следует semver:

- **Major** (v1 → v2): breaking changes в interfaces или schemas
- **Minor** (v1.0 → v1.1): новая функциональность, backward-compatible
- **Patch** (v1.0.0 → v1.0.1): clarifications, typo fixes

### 12.2. Version in Registry

Каждый registry MUST объявлять `protocol_version`. Portal 
implementation MUST поддерживать **минимум текущую major version**.

### 12.3. Breaking Changes Process

Для major version bump требуется:

1. RFC в Issues репо Portal с обоснованием
2. Минимум 30 дней обсуждения
3. Migration guide для существующих адаптеров
4. Опубликованная compatibility shim в Portal для переходного 
   периода (минимум 6 месяцев)

---

<!-- similar-docs -->

---

## Похожие документы
- [92-17-versioning-policy](92-17-versioning-policy.md) (сходство 0.63)
- [05-0-status-of-this-document](05-0-status-of-this-document.md) (сходство 0.14)
- [75-0-status-of-this-document](75-0-status-of-this-document.md) (сходство 0.13)


<!-- see-also -->

---

## Использование
```bash
# Поиск по теме документа
python scripts/improve_semantic_search.py --query "12 Versioning Policy"
```

## Смотрите также
- [92-17-versioning-policy](92-17-versioning-policy.md)
- [05-0-status-of-this-document](05-0-status-of-this-document.md)
- [75-0-status-of-this-document](75-0-status-of-this-document.md)
- [03-portal-protocol-md](03-portal-protocol-md.md)

<!-- backlinks-auto -->
## Упоминается в

- [0. Status of This Document](05-0-status-of-this-document.md)
- [0. Status of This Document](75-0-status-of-this-document.md)
- [17. Versioning Policy](92-17-versioning-policy.md)
- [7. Реализация в проекте Nautilus](114-7-реализация-в-проекте-nautilus.md)
- [Author & Contact](42-author-contact.md)
- [Author & Contact](62-author-contact.md)
- [PORTAL-PROTOCOL.md](03-portal-protocol-md.md)
- [Вакансии Anthropic — Анализ по кластерам](README.md)
- [Примеры запросов (в Claude)](129-примеры-запросов-в-claude.md)
## Упоминается в

- [Вакансии Anthropic — Анализ по кластерам](../README.md)

<!-- related-auto -->
## Связанные документы

- [17. Versioning Policy](92-17-versioning-policy.md) _81%_
- [Author & Contact](62-author-contact.md) _37%_
- [Author & Contact](42-author-contact.md) _33%_
- [0. Status of This Document](75-0-status-of-this-document.md) _33%_
- [0. Status of This Document](05-0-status-of-this-document.md) _29%_
- [13. Reference Implementation](25-13-reference-implementation.md) _29%_
- [18. Reference Implementation](93-18-reference-implementation.md) _29%_
- [PORTAL-PROTOCOL.md](03-portal-protocol-md.md) _21%_
## Связанные документы

- [17. Versioning Policy](92-17-versioning-policy.md) _81%_
- [0. Status of This Document](05-0-status-of-this-document.md) _29%_
- [Author & Contact](42-author-contact.md) _29%_
- [Author & Contact](62-author-contact.md) _29%_
- [0. Status of This Document](75-0-status-of-this-document.md) _29%_
- [PORTAL-PROTOCOL.md](03-portal-protocol-md.md) _25%_
- [Хронологическая лента событий](../TIMELINE.md) _25%_
- [Примеры запросов (в Claude)](129-примеры-запросов-в-claude.md) _21%_

<!-- backlinks -->

---

## Кто ссылается на этот документ (9)
- [03-portal-protocol-md](03-portal-protocol-md.md)
- [05-0-status-of-this-document](05-0-status-of-this-document.md)
- [129-примеры-запросов-в-claude](129-примеры-запросов-в-claude.md)
- [25-13-reference-implementation](25-13-reference-implementation.md)
- [42-author-contact](42-author-contact.md)
- [62-author-contact](62-author-contact.md)
- [75-0-status-of-this-document](75-0-status-of-this-document.md)
- [93-18-reference-implementation](93-18-reference-implementation.md)
- _...ещё 1_

