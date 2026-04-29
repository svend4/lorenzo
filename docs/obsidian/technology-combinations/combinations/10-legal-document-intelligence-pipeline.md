---
title: "Комбинация 10: Legal Document Intelligence Pipeline"
tags:
  - rag
  - knowledge
  - ingestion
  - architecture
  - collaboration
  - technology-combinations
date: 2026-04-29
---

# Комбинация 10: Legal Document Intelligence Pipeline

<!-- summary -->
> > Источник: MHTML‑снимок `Комбинирование технологий для новых свойств - Claude` (корень репозитория).
**Проекты:** Svyazi, CardIndex

---
<!-- tags: rag, knowledge, ingestion, architecture, collaboration -->




> Источник: MHTML‑снимок `Комбинирование технологий для новых свойств - Claude` (корень репозитория).

Родители:

LLM Parsing (habr.com/ru/articles/892954/) - Structured Outputs, Pydantic validation, HTML→JSON

Svyazi 6-layer extraction architecture

Docling (IBM Research) - structured DoclingDocument from PDF/DOCX

Дети:

German Sozialrecht corpus auto-builder

Docling extracts structure from Sozialgericht PDFs (headings, paragraphs, citations)

LLM+Pydantic parses legal entities: class Bescheid(BaseModel): aktenzeichen: str; paragraphs: List[SGB_Reference]; deadline: date

Svyazi CardIndex deduplicates decisions by SHA256

Итог: self-updating knowledge base of 50k+ decisions, structured queries

Precedent search with semantic + structural filters

Docling knows document structure (§, headings, footnotes)

Pydantic enforces schema: type="Widerspruch" AND sgb="IX" AND paragraph="78 Abs. 6"

Graph-RAG links precedents through citations

ROI: 10 sec queries vs 2 hour manual search

Уникальность: Docling maintains structure, Pydantic validates legal schema, Svyazi deduplicates. Ни один SaaS не делает это для немецкого социального права.

<!-- see-also -->

---

**Смотрите также:**
- [[04-sozialrecht-domain]]
- [[18-llm-powered-legal-corpus-builder]]
- [[13-legal-document-transpiler]]
- [[28-pydantic-enforced-legal-workflows]]


<!-- similar-docs -->

---

**Похожие документы:**
- [[04-sozialrecht-domain]] (сходство 0.58)
- [[04-sozialrecht-domain]] (сходство 0.54)
- [[18-llm-powered-legal-corpus-builder]] (сходство 0.39)

