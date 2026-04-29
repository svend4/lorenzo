# Домен: немецкое социальное право

<!-- summary -->
> Sozialrecht corpus auto-builder Docling extracts structure from Sozialgericht PDFs (headings, paragraphs, citations) LLM+Pydantic parses legal entities: class Bescheid(BaseModel): aktenzeichen: str; p
**Проекты:** Svyazi, CardIndex

---
<!-- tags: rag, knowledge, ingestion, architecture -->




Sozialrecht corpus auto-builder Docling extracts structure from Sozialgericht PDFs (headings, paragraphs, citations) LLM+Pydantic parses legal entities: class Bescheid(BaseModel): aktenzeichen: str; paragraphs: List[SGB_Reference]; deadline: date Svyazi CardIndex deduplicates decisions by SHA256 Итог: self-updating knowledge base of 50k+ decisions, structured queries
2. Precedent search with semantic + structural filters Docling knows document structure (§, headings, footnotes) Pydantic enforces schema: type="Widerspruch" AND sgb="IX" AND paragraph="78 Abs. 6" Graph-RAG links precedents through citations ROI: 10 sec queries vs 2 hour manual search
Уникальность: Docling maintains structure, Pydantic validates legal schema, Svyazi deduplicates. Ни один SaaS не делает это для

<!-- similar-docs -->

---

**Похожие документы:**
- [README](docs/03-technology-combinations/README.md) (сходство 0.15)


<!-- see-also -->

---

**Смотрите также:**
- [GLOSSARY](docs/GLOSSARY.md)
- [MINDMAP](docs/MINDMAP.md)
- [360-что-ты-всегда-делаешь](docs/02-anthropic-vacancies/360-что-ты-всегда-делаешь.md)
- [321-appendix-a-decision-tree-for-ingit-adopters](docs/02-anthropic-vacancies/321-appendix-a-decision-tree-for-ingit-adopters.md)

<!-- backlinks-auto -->
## Упоминается в

- [Комбинирование технологий для новых свойств](docs/03-technology-combinations/README.md)
