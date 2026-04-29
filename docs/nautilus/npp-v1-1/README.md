# Nautilus Portal Protocol v1.1 — RFC

Полный RFC из 23 разделов, написанный в диалоге как формальная спецификация протокола федерации репозиториев знаний.

| # | Раздел | Файл |
|---|---|---|
| — | Abstract + Status | [`00-abstract-status.md`](00-abstract-status.md) |
| 1 | Introduction (Motivation, Design Goals, Non-Goals, Terminology, Changes from v1.0) | [`01-introduction.md`](01-introduction.md) |
| 2 | Terminology | [`02-terminology.md`](02-terminology.md) |
| 3 | Registry (`nautilus.json`) | [`03-registry.md`](03-registry.md) |
| 4 | Passport (`passport.md`) | [`04-passport.md`](04-passport.md) |
| 5 | Compatibility Levels | [`05-compatibility-levels.md`](05-compatibility-levels.md) |
| 6 | Adapter Interface | [`06-adapter-interface.md`](06-adapter-interface.md) |
| 7 | PortalEntry Structure | [`07-portal-entry.md`](07-portal-entry.md) |
| 8 | Q6 Space (Normative) | [`08-q6-space.md`](08-q6-space.md) |
| 9 | Consensus Algorithm | [`09-consensus-algorithm.md`](09-consensus-algorithm.md) |
| 10 | Query Flow | [`10-query-flow.md`](10-query-flow.md) |
| 11 | Relevance Ranking | [`11-relevance-ranking.md`](11-relevance-ranking.md) |
| 12 | Onboarding Paths (Normative) | [`12-onboarding-paths.md`](12-onboarding-paths.md) |
| 13 | REST API Contract | [`13-rest-api.md`](13-rest-api.md) |
| 14 | SDK Contract (Informative) | [`14-sdk.md`](14-sdk.md) |
| 15 | Security Considerations | [`15-security.md`](15-security.md) |
| 16 | MCP Extension (Informative) | [`16-mcp-extension.md`](16-mcp-extension.md) |
| 17 | Versioning Policy | [`17-versioning-policy.md`](17-versioning-policy.md) |
| 18 | Reference Implementation | [`18-reference-implementation.md`](18-reference-implementation.md) |
| 19 | ADR-001: Federation over Merging | [`19-adr-001-federation-over-merging.md`](19-adr-001-federation-over-merging.md) |
| 20 | ADR-002: Q6 as First-Class Protocol Concept | [`20-adr-002-q6-first-class.md`](20-adr-002-q6-first-class.md) |
| 21 | ADR-003: Five Onboarding Paths as Equal-Rank | [`21-adr-003-five-onboarding-paths.md`](21-adr-003-five-onboarding-paths.md) |
| 22 | Glossary of Reference Examples | [`22-glossary.md`](22-glossary.md) |

## Ключевой принцип

**Федерация, а не слияние.** Native-форматы репозиториев сохраняются; унификация происходит только в момент обращения, через адаптер.

## См. также

- [`../README.md`](../README.md) — обзор всех Nautilus-связанных материалов.
- [`../../glossary/concepts.md`](../../glossary/concepts.md) — связанные понятия (Q6, MoME).
