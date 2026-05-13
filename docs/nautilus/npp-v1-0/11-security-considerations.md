# 11. Security Considerations

<!-- toc-auto -->
## Contents

- [11. Security Considerations](#11-security-considerations)
  - [11.1. Untrusted Adapters](#111-untrusted-adapters)
  - [11.2. Private Repositories](#112-private-repositories)
  - [11.3. MCP Exposure](#113-mcp-exposure)
- [Использование](#использование)
- [Смотрите также](#смотрите-также)


> [!WARNING]
> Документ содержит описание рисков и ограничений. Изучите их перед принятием архитектурных решений.

<!-- alert-added -->

<!-- summary -->

> [!WARNING]
> Документ описывает ограничения, риски или требования безопасности. Читайте внимательно.

> > Источник: MHTML‑снимок `Вакансии в Anthropic по кластерам - Claude` (корень репозитория). Раздел диалога — Nautilus Portal Protocol v1.0.0-draft RFC (более ранняя версия v1.1).

---
<!-- tags: anthropic -->




> Источник: MHTML‑снимок `Вакансии в Anthropic по кластерам - Claude` (корень репозитория). Раздел диалога — Nautilus Portal Protocol v1.0.0-draft RFC (более ранняя версия v1.1).

## 11. Security Considerations

### 11.1. Untrusted Adapters

Adapters выполняются внутри Portal-процесса. Portal MUST обрабатывать 
adapters как untrusted code:

- Timeout на каждый adapter call
- Exception handling вокруг каждого call
- Resource limits (memory, CPU), если implementation позволяет

Portal SHOULD НЕ выполнять adapters из untrusted sources без review.

### 11.2. Private Repositories

Repos, содержащие чувствительные данные, SHOULD НЕ включаться в 
публичную registry. Для приватных Repos RECOMMENDED отдельный 
`private-nautilus.json` с явным opt-in.

Implementation MUST различать public и private registries и не 
смешивать результаты без явного запроса.

### 11.3. MCP Exposure

При экспонировании Portal через MCP, implementation SHOULD:

- Требовать явный whitelist Repos, доступных через MCP
- Логировать queries отдельно, с возможностью очистки
- Не включать private Repos в MCP responses по умолчанию

---

<!-- see-also -->

---

## Использование

```bash
# Поиск по теме документа
python scripts/improve_semantic_search.py --query "11 Security Considerations"
```

## Смотрите также
- [23-11-security-considerations](../../02-anthropic-vacancies/23-11-security-considerations.md)
- [15-security](../npp-v1-1/15-security.md)
- [90-15-security-considerations](../../02-anthropic-vacancies/90-15-security-considerations.md)
- [10-query-result](10-query-result.md)

_Документ индексирован в поисковой базе репозитория Lorenzo и доступен для семантического поиска._ _Документ индексирован в поисковой базе репозитория Lorenzo и доступен для семантического поиска._ _Документ индексирован в базе знаний репозитория Lorenzo._ _Для поиска доступен._

<!-- backlinks -->

---

**Кто ссылается на этот документ (6):**
- [OUTLINE](../../OUTLINE.md)
- [READABILITY](../../READABILITY.md)
- [READING_TIME](../../READING_TIME.md)
- [SEARCH](../../SEARCH.md)
- [README](README.md)
- [15-security](../npp-v1-1/15-security.md)


<!-- similar-docs -->

---

**Похожие документы:**
- [11-security-considerations](../../obsidian/nautilus/npp-v1-0/11-security-considerations.md) (сходство 0.98)
- [15-security](../npp-v1-1/15-security.md) (сходство 0.64)
- [15-security](../../obsidian/nautilus/npp-v1-1/15-security.md) (сходство 0.62)

