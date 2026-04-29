# Nautilus Portal Protocol v1.0.0-draft — RFC

Более **ранняя версия** Nautilus Portal Protocol (v1.0.0-draft), предшествовавшая [`../npp-v1-1/`](../npp-v1-1/). 18 разделов + комментарий о дизайн-решениях.

| # | Раздел | Файл |
|---|---|---|
| — | Abstract + Status | [`00-abstract-status.md`](00-abstract-status.md) |
| 1 | Introduction | [`01-introduction.md`](01-introduction.md) |
| 2 | Terminology | [`02-terminology.md`](02-terminology.md) |
| 3 | Registry (`nautilus.json`) | [`03-registry.md`](03-registry.md) |
| 4 | Passport (`passport.md`) | [`04-passport.md`](04-passport.md) |
| 5 | Compatibility Levels | [`05-compatibility-levels.md`](05-compatibility-levels.md) |
| 6 | Adapter Interface | [`06-adapter-interface.md`](06-adapter-interface.md) |
| 7 | PortalEntry Structure | [`07-portal-entry.md`](07-portal-entry.md) |
| 8 | Consensus Algorithm (v1.0: string normalization) | [`08-consensus-algorithm.md`](08-consensus-algorithm.md) |
| 9 | Query Flow | [`09-query-flow.md`](09-query-flow.md) |
| 10 | QueryResult Structure | [`10-query-result.md`](10-query-result.md) |
| 11 | Security Considerations | [`11-security-considerations.md`](11-security-considerations.md) |
| 12 | Versioning Policy | [`12-versioning-policy.md`](12-versioning-policy.md) |
| 13 | Reference Implementation | [`13-reference-implementation.md`](13-reference-implementation.md) |
| 14 | ADR-001: Federation over Merging | [`14-adr-001-federation-over-merging.md`](14-adr-001-federation-over-merging.md) |
| 15 | Glossary of Examples | [`15-glossary.md`](15-glossary.md) |
| — | Appendix A: Minimal Working Example | [`16-appendix-a-minimal-working-example.md`](16-appendix-a-minimal-working-example.md) |
| — | Appendix B: Change Log | [`17-appendix-b-change-log.md`](17-appendix-b-change-log.md) |
| — | Комментарий: дизайн-решения NPP v1.0 | [`18-comment-on-document.md`](18-comment-on-document.md) |

## Что сознательно сделано в этом draft

> Стиль написан как реальная W3C/IETF specification. С разделами MUST/SHOULD/MAY, numbered sections, glossary, appendix'ами, ADR'ами. Это даёт документу серьёзный вид в глазах внешних читателей и одновременно операционную полезность: каждое MUST можно превратить в unit test.

Подробнее — в [`18-comment-on-document.md`](18-comment-on-document.md).

## Отличия от v1.1

См. [`../npp-v1-1/01-introduction.md`](../npp-v1-1/01-introduction.md) (раздел 1.5 «Changes from v1.0»). Главные изменения в v1.1:

- Q6 Space выделено в нормативный раздел (раздел 8 в v1.1).
- Consensus structure изменена: введены real vs fallback consensus.
- AutoAdapter добавлен как special case.
- Onboarding paths формализованы как 5 нормативных путей.
- Timeout per adapter снижен с 10 до 5 секунд.

## См. также

- [`../npp-v1-1/README.md`](../npp-v1-1/README.md) — следующая версия (v1.1.0-draft) с расширенными разделами.
