# 11. Security Considerations

<!-- summary -->
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

**Смотрите также:**
- [23-11-security-considerations](docs/02-anthropic-vacancies/23-11-security-considerations.md)
- [15-security](docs/nautilus/npp-v1-1/15-security.md)
- [90-15-security-considerations](docs/02-anthropic-vacancies/90-15-security-considerations.md)
- [10-query-result](docs/nautilus/npp-v1-0/10-query-result.md)


<!-- similar-docs -->

---

**Похожие документы:**
- [23-11-security-considerations](docs/obsidian/02-anthropic-vacancies/23-11-security-considerations.md) (сходство 0.60)
- [15-security](docs/nautilus/npp-v1-1/15-security.md) (сходство 0.59)
- [23-11-security-considerations](docs/02-anthropic-vacancies/23-11-security-considerations.md) (сходство 0.55)

