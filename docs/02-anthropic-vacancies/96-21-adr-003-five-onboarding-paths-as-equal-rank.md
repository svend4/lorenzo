# 21. ADR-003: Five Onboarding Paths as Equal-Rank

## 21. ADR-003: Five Onboarding Paths as Equal-Rank

**Status**: Accepted (new in v1.1)

**Context**: В v1.0 была одна "основная" стратегия подключения 
(manual adapter). В процессе развития reference implementation 
появились 4 дополнительных пути (B–E). Возникал вопрос: какой 
канонический?

**Decision**: Все 5 путей — равнорангованные. Выбор делается по 
контексту (раздел 12.6), не по иерархии.

**Consequences**:

**Positive**:
- Flexibility для разных use cases
- Self-declaring repos (Path C) enables federation без центральной 
  координации
- Automated paths (D, E) scale для fleet-federation

**Negative**:
- Больше документации
- Users могут путаться, какой путь выбрать (mitigated via раздел 
  12.6 guidance)

---
