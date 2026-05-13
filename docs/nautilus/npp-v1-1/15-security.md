---
state: normalized
---

# 15. Security Considerations

<!-- toc-auto -->
## Contents

- [15. Security Considerations](#15-security-considerations)
  - [15.1. Untrusted Adapters](#151-untrusted-adapters)
  - [15.2. Private Repositories](#152-private-repositories)
  - [15.3. MCP Exposure](#153-mcp-exposure)
  - [15.4. Rate Limiting](#154-rate-limiting)
  - [15.5. Supply Chain](#155-supply-chain)
- [Использование](#использование)
- [Смотрите также](#смотрите-также)


> [!WARNING]
> Документ содержит описание рисков и ограничений. Изучите их перед принятием архитектурных решений.

<!-- alert-added -->

<!-- summary -->

> [!WARNING]
> Документ описывает ограничения, риски или требования безопасности. Читайте внимательно.

> > Источник: MHTML‑снимок `Вакансии в Anthropic по кластерам - Claude` (корень репозитория). Раздел диалога — Nautilus Portal Protocol v1.1 RFC, написанный совместно с Claude.

---
<!-- tags: anthropic -->




> Источник: MHTML‑снимок `Вакансии в Anthropic по кластерам - Claude` (корень репозитория). Раздел диалога — Nautilus Portal Protocol v1.1 RFC, написанный совместно с Claude.

## 15. Security Considerations

### 15.1. Untrusted Adapters

Adapters выполняются внутри Portal-процесса. Portal MUST 
обрабатывать adapters как untrusted code:

- Timeout на каждый adapter call (RECOMMENDED 5 секунд)
- Exception handling вокруг каждого call
- XSS protection (`_html.escape`) во всех user-facing rendered полях

Portal SHOULD НЕ выполнять adapters из untrusted sources без review.

### 15.2. Private Repositories

Repos, содержащие чувствительные данные (legal, medical, personal), 
SHOULD НЕ включаться в публичную registry.

Для приватных Repos RECOMMENDED:

- Отдельный `private-nautilus.json` с explicit opt-in
- Отдельный portal instance, не доступный публично
- Authentication на REST API (JWT / API keys)
- Нет MCP exposure без whitelist

Implementation MUST различать public и private registries и не 
смешивать результаты без явного запроса.

### 15.3. MCP Exposure

При экспонировании Portal через MCP (см. раздел 16), implementation 
SHOULD:

- Требовать явный whitelist Repos, доступных через MCP
- Логировать queries отдельно, с возможностью очистки
- Не включать private Repos в MCP responses по умолчанию

### 15.4. Rate Limiting

Public-facing portals SHOULD реализовать rate limiting:

- RECOMMENDED: 60 requests per minute per IP для `/api/query`
- RECOMMENDED: 120 requests per minute per IP для `/api/describe` и 
`/api/health`

### 15.5. Supply Chain

Reference implementation использует только Python stdlib (zero 
external dependencies). Это RECOMMENDED для альтернативных 
implementations. Каждая external dependency — потенциальный 
supply-chain риск.

---

<!-- see-also -->

---

## Использование
```bash
# Поиск по теме документа
python scripts/improve_semantic_search.py --query "15 Security Considerations"
```

## Смотрите также
- [90-15-security-considerations](../../02-anthropic-vacancies/90-15-security-considerations.md)
- [11-security-considerations](../npp-v1-0/11-security-considerations.md)
- [23-11-security-considerations](../../02-anthropic-vacancies/23-11-security-considerations.md)
- [06-adapter-interface](06-adapter-interface.md)


<!-- backlinks -->

---

**Кто ссылается на этот документ (6):**
- [OUTLINE](../../OUTLINE.md)
- [READABILITY](../../READABILITY.md)
- [READING_TIME](../../READING_TIME.md)
- [SEARCH](../../SEARCH.md)
- [11-security-considerations](../npp-v1-0/11-security-considerations.md)
- [README](README.md)


<!-- similar-docs -->

---

**Похожие документы:**
- [15-security](../../obsidian/nautilus/npp-v1-1/15-security.md) (сходство 0.98)
- [90-15-security-considerations](../../obsidian/02-anthropic-vacancies/90-15-security-considerations.md) (сходство 0.64)
- [90-15-security-considerations](../../02-anthropic-vacancies/90-15-security-considerations.md) (сходство 0.64)

