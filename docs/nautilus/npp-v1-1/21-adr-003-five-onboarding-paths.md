# 21. ADR-003: Five Onboarding Paths as Equal-Rank

<!-- toc-auto -->
## Contents

- [21. ADR-003: Five Onboarding Paths as Equal-Rank](#21-adr-003-five-onboarding-paths-as-equal-rank)
- [Смотрите также](#смотрите-также)


> [!NOTE]
> Документ создан на основе исследования. Ссылки ведут на связанные материалы.

<!-- alert-added -->

<!-- summary -->
> > Источник: MHTML‑снимок `Вакансии в Anthropic по кластерам - Claude` (корень репозитория). Раздел диалога — Nautilus Portal Protocol v1.1 RFC, написанный совместно с Claude.

---
<!-- tags: anthropic -->

> [!NOTE]
> Документ создан на основе исследования. Ссылки ведут на связанные материалы.





> Источник: MHTML‑снимок `Вакансии в Anthropic по кластерам - Claude` (корень репозитория). Раздел диалога — Nautilus Portal Protocol v1.1 RFC, написанный совместно с Claude.

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

<!-- see-also -->

---

## Использование

```bash
# Поиск по теме документа
python scripts/improve_semantic_search.py --query "21 ADR 003 Five Onboarding Paths as"
```

## Смотрите также
- [96-21-adr-003-five-onboarding-paths-as-equal-rank](../../02-anthropic-vacancies/96-21-adr-003-five-onboarding-paths-as-equal-rank.md)
- [19-adr-001-federation-over-merging](19-adr-001-federation-over-merging.md)
- [20-adr-002-q6-first-class](20-adr-002-q6-first-class.md)
- [11-relevance-ranking](11-relevance-ranking.md)

Документ индексирован в базе знаний репозитория. Навигация возможна через семантический поиск и граф концептов репозитория Lorenzo. Материал доступен для семантического поиска, BM25-поиска и навигации через граф концептов. Используйте скрипты группы reports для получения актуальной статистики по разделу. Рекомендуется начинать с основных документов раздела и переходить к деталям через внутренние ссылки. Все связанные документы доступны через граф концептов и поисковый индекс репозитория Lorenzo. Документ индексирован в базе знаний репозитория.

<!-- backlinks -->

---

**Кто ссылается на этот документ (8):**
- [OUTLINE](../../OUTLINE.md)
- [READABILITY](../../READABILITY.md)
- [READING_TIME](../../READING_TIME.md)
- [SEARCH](../../SEARCH.md)
- [12-onboarding-paths](12-onboarding-paths.md)
- [19-adr-001-federation-over-merging](19-adr-001-federation-over-merging.md)
- [20-adr-002-q6-first-class](20-adr-002-q6-first-class.md)
- [README](README.md)

